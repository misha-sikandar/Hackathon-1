---
sidebar_position: 24
---

# Balance Control Systems for Humanoid Robots

This lesson focuses on the critical aspect of balance control in humanoid robots. Maintaining balance is one of the most challenging problems in humanoid robotics, requiring sophisticated control algorithms to manage the robot's center of mass and react to disturbances.

## Learning Objectives

By the end of this lesson, you will be able to:

1. Implement advanced balance control algorithms
2. Design feedback control systems for balance
3. Apply control theory to humanoid balance
4. Integrate sensory feedback for balance control
5. Evaluate balance control performance
6. Design recovery strategies for balance loss

## Advanced Balance Control Algorithms

### Linear Quadratic Regulator (LQR) for Balance

LQR provides optimal control for linear systems with quadratic costs:

```python
import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt

class LQRBalanceController:
    def __init__(self, dt=0.01, com_height=0.8):
        """
        Linear Quadratic Regulator for humanoid balance control
        
        Args:
            dt: Time step
            com_height: Center of mass height
        """
        self.dt = dt
        self.com_height = com_height
        self.gravity = 9.81
        self.omega = np.sqrt(self.gravity / com_height)
        
        # State: [x, x_dot, y, y_dot] (CoM position and velocity)
        # Control: [zmp_x, zmp_y] (Zero Moment Point)
        
        # System matrices for inverted pendulum model
        # dx/dt = A*x + B*u
        self.A = np.array([
            [0, 1, 0, 0],
            [self.omega**2, 0, 0, 0],
            [0, 0, 0, 1],
            [0, 0, self.omega**2, 0]
        ])
        
        # Control input matrix
        self.B = np.array([
            [0, 0],
            [self.omega**2, 0],
            [0, 0],
            [0, self.omega**2]
        ])
        
        # Design LQR controller
        # Q: State cost matrix
        # R: Control cost matrix
        self.Q = np.diag([100, 10, 100, 10])  # Penalize position more than velocity
        self.R = np.diag([1, 1])  # Penalize control effort
        
        # Discretize system
        self.A_d = la.expm(self.A * self.dt)
        self.B_d = np.linalg.inv(self.A).dot((self.A_d - np.eye(4)).dot(self.B))
        
        # Compute LQR gain
        self.K = self.compute_lqr_gain(self.A_d, self.B_d, self.Q, self.R)
        
    def compute_lqr_gain(self, A, B, Q, R):
        """
        Compute LQR gain matrix
        """
        # Solve discrete-time Algebraic Riccati Equation
        P = la.solve_discrete_are(A, B, Q, R)
        
        # Compute gain matrix
        K = np.linalg.inv(R + B.T @ P @ B) @ (B.T @ P @ A)
        
        return K
    
    def update(self, state):
        """
        Compute control input using LQR
        
        Args:
            state: Current state [x, x_dot, y, y_dot]
            
        Returns:
            Control input [zmp_x, zmp_y]
        """
        # For balance, desired state is [0, 0, 0, 0] (equilibrium)
        error = -state  # Negative because we want to drive to zero
        
        # Compute control input
        control = self.K @ error
        
        return control

# Example: LQR balance control
lqr_ctrl = LQRBalanceController(dt=0.01, com_height=0.85)

# Simulate balance control
simulation_time = 10.0
dt = 0.01
time_steps = np.arange(0, simulation_time, dt)

# Start with disturbance
initial_state = np.array([0.05, 0.1, 0.03, 0.05])  # [x, x_dot, y, y_dot]
state = initial_state.copy()

states = []
controls = []

for t in time_steps:
    # Get control input
    control_input = lqr_ctrl.update(state)
    
    # Update system dynamics
    # x[k+1] = A_d * x[k] + B_d * u[k]
    state = lqr_ctrl.A_d @ state + lqr_ctrl.B_d @ control_input
    
    # Record states and controls
    states.append(state.copy())
    controls.append(control_input.copy())

states = np.array(states)
controls = np.array(controls)

# Visualization
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

# Plot CoM position over time
ax1.plot(time_steps, states[:, 0], label='X Position', linewidth=2)
ax1.plot(time_steps, states[:, 2], label='Y Position', linewidth=2)
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Position (m)')
ax1.set_title('CoM Position Over Time (LQR Control)')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot CoM velocity over time
ax2.plot(time_steps, states[:, 1], label='X Velocity', linewidth=2)
ax2.plot(time_steps, states[:, 3], label='Y Velocity', linewidth=2)
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Velocity (m/s)')
ax2.set_title('CoM Velocity Over Time (LQR Control)')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Plot phase portrait
ax3.plot(states[:, 0], states[:, 1], 'b-', linewidth=2)
ax3.set_xlabel('X Position (m)')
ax3.set_ylabel('X Velocity (m/s)')
ax3.set_title('Phase Portrait - X Direction')
ax3.grid(True, alpha=0.3)

ax4.plot(states[:, 2], states[:, 3], 'r-', linewidth=2)
ax4.set_xlabel('Y Position (m)')
ax4.set_ylabel('Y Velocity (m/s)')
ax4.set_title('Phase Portrait - Y Direction')
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print(f"LQR Balance Control - Final state: {states[-1]}")
print(f"Final position magnitude: {np.linalg.norm(states[-1, [0, 2]]):.4f}")
```

### Extended Kalman Filter (EKF) for State Estimation

Accurate state estimation is crucial for balance control:

```python
class ExtendedKalmanFilter:
    def __init__(self, dt=0.01, com_height=0.8):
        """
        Extended Kalman Filter for humanoid state estimation
        
        Args:
            dt: Time step
            com_height: Center of mass height
        """
        self.dt = dt
        self.com_height = com_height
        self.gravity = 9.81
        self.omega = np.sqrt(self.gravity / com_height)
        
        # State: [x, x_dot, y, y_dot, theta, theta_dot] (position, velocity, orientation)
        self.state_dim = 6
        self.obs_dim = 6  # Measurements: [x, y, z, roll, pitch, yaw]
        
        # Initialize state and covariance
        self.x = np.zeros(self.state_dim)  # State vector
        self.P = np.eye(self.state_dim) * 0.1  # Covariance matrix
        
        # Process noise
        self.Q = np.diag([0.01, 0.1, 0.01, 0.1, 0.01, 0.1])
        
        # Measurement noise
        self.R = np.diag([0.001, 0.001, 0.001, 0.01, 0.01, 0.01])  # [pos, pos, pos, orient, orient, orient]
        
        # Measurement matrix (simplified)
        self.H = np.zeros((self.obs_dim, self.state_dim))
        self.H[0, 0] = 1  # x position
        self.H[1, 2] = 1  # y position
        self.H[2, 2] = 1  # z position (fixed height assumption)
        self.H[3, 4] = 1  # roll
        self.H[4, 5] = 1  # pitch
        self.H[5, 5] = 1  # yaw
    
    def predict(self, control_input=None):
        """
        Prediction step of EKF
        
        Args:
            control_input: Control input (if any)
        """
        # State transition function (simplified inverted pendulum dynamics)
        F = self.jacobian_f(self.x)
        
        # Predict state
        self.x = self.state_transition(self.x, control_input)
        
        # Predict covariance
        self.P = F @ self.P @ F.T + self.Q
    
    def update(self, measurement):
        """
        Update step of EKF
        
        Args:
            measurement: Measurement vector [x, y, z, roll, pitch, yaw]
        """
        # Innovation
        innovation = measurement - self.observation_model(self.x)
        
        # Jacobian of observation model
        H = self.jacobian_h(self.x)
        
        # Innovation covariance
        S = H @ self.P @ H.T + self.R
        
        # Kalman gain
        K = self.P @ H.T @ np.linalg.inv(S)
        
        # Update state
        self.x = self.x + K @ innovation
        
        # Update covariance
        I = np.eye(self.state_dim)
        self.P = (I - K @ H) @ self.P
    
    def state_transition(self, x, u=None):
        """
        Nonlinear state transition function
        """
        # Simplified inverted pendulum dynamics
        new_x = x.copy()
        
        # Position updates based on velocity
        new_x[0] += x[1] * self.dt  # x position
        new_x[2] += x[3] * self.dt  # y position
        
        # Velocity updates based on inverted pendulum model
        new_x[1] += (self.omega**2 * (x[0] - (u[0] if u is not None else 0))) * self.dt  # x velocity
        new_x[3] += (self.omega**2 * (x[2] - (u[1] if u is not None else 0))) * self.dt  # y velocity
        
        # Orientation updates (simplified)
        new_x[4] += x[5] * self.dt  # roll
        new_x[5] += 0 * self.dt   # pitch rate (simplified)
        
        return new_x
    
    def jacobian_f(self, x):
        """
        Jacobian of state transition function
        """
        F = np.eye(self.state_dim)
        
        # Partial derivatives of state transition
        F[0, 1] = self.dt  # dx/dx_dot
        F[2, 3] = self.dt  # dy/dy_dot
        
        F[1, 0] = self.omega**2 * self.dt  # dx_dot/dx
        F[3, 2] = self.omega**2 * self.dt  # dy_dot/dy
        
        F[4, 5] = self.dt  # droll/droll_dot
        
        return F
    
    def observation_model(self, x):
        """
        Observation model
        """
        # Simplified: direct observation of state
        return self.H @ x
    
    def jacobian_h(self, x):
        """
        Jacobian of observation model
        """
        return self.H
    
    def get_state(self):
        """
        Get current estimated state
        """
        return self.x.copy()

# Example: EKF for state estimation
ekf = ExtendedKalmanFilter(dt=0.01, com_height=0.85)

# Simulate with noisy measurements
simulation_time = 5.0
dt = 0.01
time_steps = np.arange(0, simulation_time, dt)

# True state (with some motion)
true_states = []
measurements = []
estimates = []

# Initial state with disturbance
true_state = np.array([0.05, 0.1, 0.03, 0.05, 0.01, 0.02])
ekf.x = true_state + np.random.normal(0, 0.01, 6)  # Initial estimate with noise

for t in time_steps:
    # Update true state (simplified dynamics)
    true_state[0] += true_state[1] * dt
    true_state[2] += true_state[3] * dt
    true_state[1] += (ekf.omega**2 * (true_state[0] - 0.0)) * dt  # Damped oscillation
    true_state[3] += (ekf.omega**2 * (true_state[2] - 0.0)) * dt
    true_state[4] += true_state[5] * dt
    
    # Generate noisy measurement
    measurement = true_state + np.random.normal(0, [0.01, 0.05, 0.01, 0.01, 0.01, 0.01])
    
    # Update EKF
    ekf.predict()
    ekf.update(measurement)
    
    # Record data
    true_states.append(true_state.copy())
    measurements.append(measurement.copy())
    estimates.append(ekf.get_state().copy())

true_states = np.array(true_states)
measurements = np.array(measurements)
estimates = np.array(estimates)

# Visualization
fig, axes = plt.subplots(3, 2, figsize=(15, 12))

for i in range(2):  # Only plot position and velocity
    state_idx = i * 2  # x and y positions
    vel_idx = state_idx + 1  # corresponding velocities
    
    # Plot position
    axes[0, i].plot(time_steps, true_states[:, state_idx], label='True', linewidth=2)
    axes[0, i].plot(time_steps, measurements[:, state_idx], label='Measurement', linestyle='--', alpha=0.7)
    axes[0, i].plot(time_steps, estimates[:, state_idx], label='EKF Estimate', linewidth=2)
    axes[0, i].set_xlabel('Time (s)')
    axes[0, i].set_ylabel('Position (m)')
    axes[0, i].set_title(f'{"X" if i==0 else "Y"} Position Estimation')
    axes[0, i].legend()
    axes[0, i].grid(True, alpha=0.3)
    
    # Plot velocity
    axes[1, i].plot(time_steps, true_states[:, vel_idx], label='True', linewidth=2)
    axes[1, i].plot(time_steps, estimates[:, vel_idx], label='EKF Estimate', linewidth=2)
    axes[1, i].set_xlabel('Time (s)')
    axes[1, i].set_ylabel('Velocity (m/s)')
    axes[1, i].set_title(f'{"X" if i==0 else "Y"} Velocity Estimation')
    axes[1, i].legend()
    axes[1, i].grid(True, alpha=0.3)

# Plot estimation error
pos_error = np.linalg.norm(estimates[:, [0, 2]] - true_states[:, [0, 2]], axis=1)
vel_error = np.linalg.norm(estimates[:, [1, 3]] - true_states[:, [1, 3]], axis=1)

axes[2, 0].plot(time_steps, pos_error, label='Position Error', linewidth=2)
axes[2, 0].plot(time_steps, vel_error, label='Velocity Error', linewidth=2)
axes[2, 0].set_xlabel('Time (s)')
axes[2, 0].set_ylabel('Error (m)')
axes[2, 0].set_title('Estimation Error Over Time')
axes[2, 0].legend()
axes[2, 0].grid(True, alpha=0.3)

# Plot covariance trace
cov_trace = np.array([np.trace(ekf.P) for _ in range(len(time_steps))])  # Simplified
axes[2, 1].plot(time_steps, cov_trace[:len(time_steps)], linewidth=2)
axes[2, 1].set_xlabel('Time (s)')
axes[2, 1].set_ylabel('Covariance Trace')
axes[2, 1].set_title('Estimation Uncertainty (Covariance Trace)')
axes[2, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print(f"EKF Final estimation error: {np.linalg.norm(estimates[-1, :4] - true_states[-1, :4]):.4f}")
```

## Feedback Control Systems for Balance

### PID Control for Balance

PID controllers are commonly used for balance control:

```python
class PIDBalanceController:
    def __init__(self, kp_pos=10.0, ki_pos=1.0, kd_pos=0.1, 
                 kp_vel=5.0, ki_vel=0.5, kd_vel=0.05):
        """
        PID controller for humanoid balance with cascaded control
        
        Args:
            kp_pos, ki_pos, kd_pos: Position control gains
            kp_vel, ki_vel, kd_vel: Velocity control gains
        """
        # Position controller
        self.pos_controller = {
            'kp': kp_pos,
            'ki': ki_pos,
            'kd': kd_pos,
            'prev_error': np.zeros(2),
            'integral': np.zeros(2)
        }
        
        # Velocity controller
        self.vel_controller = {
            'kp': kp_vel,
            'ki': ki_vel,
            'kd': kd_vel,
            'prev_error': np.zeros(2),
            'integral': np.zeros(2)
        }
        
        self.dt = 0.01
        self.max_control_output = 0.1  # Limit ZMP control output
    
    def update(self, current_pos, desired_pos, current_vel, desired_vel):
        """
        Update PID controllers
        
        Args:
            current_pos: Current CoM position [x, y]
            desired_pos: Desired CoM position [x, y]
            current_vel: Current CoM velocity [x_dot, y_dot]
            desired_vel: Desired CoM velocity [x_dot, y_dot]
            
        Returns:
            Control output [zmp_x, zmp_y]
        """
        # Position error
        pos_error = desired_pos - current_pos
        
        # Update position PID
        pos_p_term = self.pos_controller['kp'] * pos_error
        self.pos_controller['integral'] += pos_error * self.dt
        pos_i_term = self.pos_controller['ki'] * self.pos_controller['integral']
        pos_derivative = (pos_error - self.pos_controller['prev_error']) / self.dt
        pos_d_term = self.pos_controller['kd'] * pos_derivative
        self.pos_controller['prev_error'] = pos_error
        
        # Position controller output becomes velocity reference
        vel_ref = pos_p_term + pos_i_term + pos_d_term
        
        # Velocity error
        vel_error = vel_ref - current_vel
        
        # Update velocity PID
        vel_p_term = self.vel_controller['kp'] * vel_error
        self.vel_controller['integral'] += vel_error * self.dt
        vel_i_term = self.vel_controller['ki'] * self.vel_controller['integral']
        vel_derivative = (vel_error - self.vel_controller['prev_error']) / self.dt
        vel_d_term = self.vel_controller['kd'] * vel_derivative
        self.vel_controller['prev_error'] = vel_error
        
        # Final control output
        control_output = vel_p_term + vel_i_term + vel_d_term
        
        # Limit control output
        control_output = np.clip(control_output, -self.max_control_output, self.max_control_output)
        
        return control_output

# Example: Cascaded PID balance control
pid_ctrl = PIDBalanceController(kp_pos=15.0, ki_pos=2.0, kd_pos=0.2)

# Simulate balance control
simulation_time = 10.0
dt = 0.01
time_steps = np.arange(0, simulation_time, dt)

# Initial conditions with disturbance
current_pos = np.array([0.05, 0.03])
current_vel = np.array([0.1, 0.05])
desired_pos = np.array([0.0, 0.0])
desired_vel = np.array([0.0, 0.0])

positions = []
velocities = []
controls = []

for t in time_steps:
    # Get control input
    control_input = pid_ctrl.update(current_pos, desired_pos, current_vel, desired_vel)
    
    # Simple dynamics update (inverted pendulum model)
    # For simplicity, we'll simulate the effect of control on position/velocity
    acceleration = 15.0 * (current_pos - control_input)  # Simplified inverted pendulum
    current_vel += acceleration * dt
    current_pos += current_vel * dt
    
    # Add some damping to make it more realistic
    current_vel *= 0.99
    
    # Record data
    positions.append(current_pos.copy())
    velocities.append(current_vel.copy())
    controls.append(control_input.copy())

positions = np.array(positions)
velocities = np.array(velocities)
controls = np.array(controls)

# Visualization
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

# Plot position over time
ax1.plot(time_steps, positions[:, 0], label='X Position', linewidth=2)
ax1.plot(time_steps, positions[:, 1], label='Y Position', linewidth=2)
ax1.axhline(y=0, color='k', linestyle='--', alpha=0.5, label='Desired')
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Position (m)')
ax1.set_title('CoM Position Over Time (PID Control)')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot velocity over time
ax2.plot(time_steps, velocities[:, 0], label='X Velocity', linewidth=2)
ax2.plot(time_steps, velocities[:, 1], label='Y Velocity', linewidth=2)
ax2.axhline(y=0, color='k', linestyle='--', alpha=0.5, label='Desired')
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Velocity (m/s)')
ax2.set_title('CoM Velocity Over Time (PID Control)')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Plot control output over time
ax3.plot(time_steps, controls[:, 0], label='ZMP X Control', linewidth=2)
ax3.plot(time_steps, controls[:, 1], label='ZMP Y Control', linewidth=2)
ax3.set_xlabel('Time (s)')
ax3.set_ylabel('Control Output (m)')
ax3.set_title('ZMP Control Output Over Time')
ax3.legend()
ax3.grid(True, alpha=0.3)

# Phase portrait
ax4.plot(positions[:, 0], velocities[:, 0], 'b-', linewidth=2, label='X Phase')
ax4.plot(positions[:, 1], velocities[:, 1], 'r-', linewidth=2, label='Y Phase')
ax4.set_xlabel('Position (m)')
ax4.set_ylabel('Velocity (m/s)')
ax4.set_title('Phase Portraits')
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print(f"PID Balance Control - Final position: {positions[-1]}")
print(f"Final position magnitude: {np.linalg.norm(positions[-1]):.4f}")
```

### Adaptive Control for Balance

Adaptive control adjusts parameters based on system performance:

```python
class AdaptiveBalanceController:
    def __init__(self, initial_kp=10.0, initial_ki=1.0, initial_kd=0.1, 
                 adaptation_rate=0.01):
        """
        Adaptive PID controller for balance control
        
        Args:
            initial_kp, initial_ki, initial_kd: Initial PID gains
            adaptation_rate: Rate of parameter adaptation
        """
        self.kp = initial_kp
        self.ki = initial_ki
        self.kd = initial_kd
        self.adaptation_rate = adaptation_rate
        
        # State variables
        self.prev_error = 0.0
        self.integral = 0.0
        self.dt = 0.01
        
        # Adaptation parameters
        self.performance_history = []
        self.max_history = 50  # Window for performance evaluation
        
    def update(self, error):
        """
        Update adaptive controller
        
        Args:
            error: Current error (scalar for simplicity)
            
        Returns:
            Control output
        """
        # PID control
        p_term = self.kp * error
        self.integral += error * self.dt
        i_term = self.ki * self.integral
        derivative = (error - self.prev_error) / self.dt
        d_term = self.kd * derivative
        self.prev_error = error
        
        control_output = p_term + i_term + d_term
        
        # Update performance history
        self.performance_history.append(abs(error))
        if len(self.performance_history) > self.max_history:
            self.performance_history.pop(0)
        
        # Adapt parameters based on recent performance
        if len(self.performance_history) >= 10:
            recent_performance = np.mean(self.performance_history[-10:])
            historical_performance = np.mean(self.performance_history[:-10]) if len(self.performance_history) > 10 else recent_performance
            
            # If performance is degrading, adjust gains
            if recent_performance > 1.2 * historical_performance:
                # Increase gains to respond more aggressively
                self.kp *= 1.01
                self.ki *= 1.01
                self.kd *= 1.01
            elif recent_performance < 0.8 * historical_performance:
                # Decrease gains to reduce overshoot
                self.kp *= 0.99
                self.ki *= 0.99
                self.kd *= 0.99
            
            # Keep gains within reasonable bounds
            self.kp = np.clip(self.kp, 1.0, 50.0)
            self.ki = np.clip(self.ki, 0.1, 10.0)
            self.kd = np.clip(self.kd, 0.01, 5.0)
        
        return control_output
    
    def get_gains(self):
        """
        Get current PID gains
        """
        return {'kp': self.kp, 'ki': self.ki, 'kd': self.kd}

# Example: Adaptive balance control
adaptive_ctrl = AdaptiveBalanceController(initial_kp=8.0, initial_ki=0.5, initial_kd=0.05)

# Simulate with changing conditions
simulation_time = 20.0
dt = 0.01
time_steps = np.arange(0, simulation_time, dt)

# Start with disturbance, then add more disturbances periodically
errors = []
controls = []
gains_history = []

current_error = 0.05  # Initial disturbance

for i, t in enumerate(time_steps):
    # Add disturbances at certain times
    if int(t) in [5, 10, 15]:
        current_error += np.random.uniform(-0.05, 0.05)
    
    # Get control input
    control_input = adaptive_ctrl.update(current_error)
    
    # Simple system response (first-order with delay)
    current_error += (-2.0 * current_error + control_input) * dt
    current_error += np.random.normal(0, 0.001)  # Add small process noise
    
    # Record data
    errors.append(current_error)
    controls.append(control_input)
    gains_history.append(adaptive_ctrl.get_gains().copy())

errors = np.array(errors)
controls = np.array(controls)

# Extract gain histories
kp_hist = [g['kp'] for g in gains_history]
ki_hist = [g['ki'] for g in gains_history]
kd_hist = [g['kd'] for g in gains_history]

# Visualization
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

# Plot error over time
ax1.plot(time_steps, errors, 'b-', linewidth=2, label='Error')
ax1.axhline(y=0, color='k', linestyle='--', alpha=0.5, label='Desired')
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Error (m)')
ax1.set_title('Tracking Error Over Time (Adaptive Control)')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot control output over time
ax2.plot(time_steps, controls, 'r-', linewidth=2, label='Control Output')
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Control Output')
ax2.set_title('Control Output Over Time')
ax2.grid(True, alpha=0.3)

# Plot adaptive gains over time
ax3_twin = ax3.twinx()
line1, = ax3.plot(time_steps, kp_hist, 'g-', linewidth=2, label='Kp')
line2, = ax3.plot(time_steps, ki_hist, 'b-', linewidth=2, label='Ki')
line3, = ax3.plot(time_steps, kd_hist, 'm-', linewidth=2, label='Kd')
ax3.set_xlabel('Time (s)')
ax3.set_ylabel('Gain Value', color='k')
ax3.set_title('Adaptive PID Gains Over Time')
ax3.tick_params(axis='y', labelcolor='k')
ax3.grid(True, alpha=0.3)

# Create legend for both axes
lines = [line1, line2, line3]
labels = [l.get_label() for l in lines]
ax3.legend(lines, labels, loc='upper left')

# Plot phase portrait
ax4.plot(errors[:-1], errors[1:], 'b-', linewidth=2)
ax4.set_xlabel('Error(t)')
ax4.set_ylabel('Error(t+1)')
ax4.set_title('Error Phase Portrait (Adaptive Control)')
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

final_gains = adaptive_ctrl.get_gains()
print(f"Adaptive Control - Final gains: KP={final_gains['kp']:.2f}, KI={final_gains['ki']:.2f}, KD={final_gains['kd']:.2f}")
print(f"Final error magnitude: {abs(errors[-1]):.4f}")
```

## Sensory Integration for Balance

### Sensor Fusion for Balance Control

Combining multiple sensors for robust balance control:

```python
class SensorFusionBalancer:
    def __init__(self, com_height=0.8):
        """
        Balance controller with sensor fusion
        
        Args:
            com_height: Center of mass height
        """
        self.com_height = com_height
        self.gravity = 9.81
        self.omega = np.sqrt(self.gravity / com_height)
        
        # State: [x, x_dot, y, y_dot, theta_pitch, theta_roll]
        self.state_dim = 6
        self.state = np.zeros(self.state_dim)
        
        # Covariance matrix for Kalman filter
        self.P = np.eye(self.state_dim) * 0.1
        
        # Process noise
        self.Q = np.diag([0.01, 0.1, 0.01, 0.1, 0.01, 0.01])
        
        # Measurement noise for different sensors
        self.R_imu = np.diag([0.01, 0.01, 0.01])  # [acc_x, acc_y, acc_z]
        self.R_ft = np.diag([1.0, 1.0, 1.0, 0.1, 0.1, 0.1])  # [fx, fy, fz, tx, ty, tz]
        self.R_encoders = np.diag([0.001, 0.001, 0.001, 0.001])  # [leg_pos1, pos2, pos3, pos4]
        
        # Measurement matrices
        # IMU measures acceleration (related to tilt)
        self.H_imu = np.zeros((3, self.state_dim))
        self.H_imu[0, 4] = self.gravity  # Pitch affects x acceleration
        self.H_imu[1, 5] = self.gravity  # Roll affects y acceleration
        self.H_imu[2, 0] = self.omega**2  # x position affects z acceleration
        
        # Force/torque sensors measure ground reaction forces
        self.H_ft = np.zeros((6, self.state_dim))
        self.H_ft[0, 1] = 1.0  # x velocity affects x force
        self.H_ft[1, 3] = 1.0  # y velocity affects y force
        self.H_ft[2, 4] = 1.0  # pitch affects z force
        self.H_ft[3, 5] = 1.0  # roll affects x moment
        self.H_ft[4, 4] = 1.0  # pitch affects y moment
        self.H_ft[5, 2] = 1.0  # y position affects z moment
        
        # Encoders measure joint positions (indirectly related to CoM)
        self.H_encoders = np.zeros((4, self.state_dim))
        self.H_encoders[0, 0] = 0.25  # x position influence
        self.H_encoders[1, 2] = 0.25  # y position influence
        self.H_encoders[2, 4] = 0.1   # pitch influence
        self.H_encoders[3, 5] = 0.1   # roll influence
        
        # State transition matrix (simplified dynamics)
        self.F = np.eye(self.state_dim)
        self.F[0, 1] = 0.01  # x_pos += x_vel * dt
        self.F[2, 3] = 0.01  # y_pos += y_vel * dt
        self.F[4, 4] = 0.99  # pitch damping
        self.F[5, 5] = 0.99  # roll damping
    
    def predict(self):
        """
        Prediction step for all sensors
        """
        # Predict state
        self.state = self.F @ self.state
        
        # Predict covariance
        self.P = self.F @ self.P @ self.F.T + self.Q
    
    def update_imu(self, imu_measurement):
        """
        Update with IMU measurement
        
        Args:
            imu_measurement: [acc_x, acc_y, acc_z]
        """
        innovation = imu_measurement - self.H_imu @ self.state
        S = self.H_imu @ self.P @ self.H_imu.T + self.R_imu
        K = self.P @ self.H_imu.T @ np.linalg.inv(S)
        
        self.state = self.state + K @ innovation
        I = np.eye(self.state_dim)
        self.P = (I - K @ self.H_imu) @ self.P
    
    def update_force_torque(self, ft_measurement):
        """
        Update with force/torque measurement
        
        Args:
            ft_measurement: [fx, fy, fz, tx, ty, tz]
        """
        innovation = ft_measurement - self.H_ft @ self.state
        S = self.H_ft @ self.P @ self.H_ft.T + self.R_ft
        K = self.P @ self.H_ft.T @ np.linalg.inv(S)
        
        self.state = self.state + K @ innovation
        I = np.eye(self.state_dim)
        self.P = (I - K @ self.H_ft) @ self.P
    
    def update_encoders(self, encoder_measurement):
        """
        Update with encoder measurement
        
        Args:
            encoder_measurement: [joint_pos1, pos2, pos3, pos4]
        """
        innovation = encoder_measurement - self.H_encoders @ self.state
        S = self.H_encoders @ self.P @ self.H_encoders.T + self.R_encoders
        K = self.P @ self.H_encoders.T @ np.linalg.inv(S)
        
        self.state = self.state + K @ innovation
        I = np.eye(self.state_dim)
        self.P = (I - K @ self.H_encoders) @ self.P
    
    def get_balance_control(self, desired_state=None):
        """
        Get balance control output based on current state
        
        Args:
            desired_state: Desired state [x, x_dot, y, y_dot, theta_pitch, theta_roll]
            
        Returns:
            Control output for balance
        """
        if desired_state is None:
            desired_state = np.zeros(self.state_dim)
        
        # Simple PD control for balance
        error = desired_state - self.state
        control = np.array([
            10.0 * error[0] + 1.0 * error[1],  # x direction
            10.0 * error[2] + 1.0 * error[3]   # y direction
        ])
        
        return control

# Example: Sensor fusion for balance
fusion_balancer = SensorFusionBalancer(com_height=0.85)

# Simulate with multiple sensors
simulation_time = 10.0
dt = 0.01
time_steps = np.arange(0, simulation_time, dt)

# True state with disturbances
true_state = np.array([0.05, 0.1, 0.03, 0.05, 0.01, 0.02])
estimated_state = true_state + np.random.normal(0, 0.01, 6)

# Initialize balancer state
fusion_balancer.state = estimated_state

imu_measurements = []
ft_measurements = []
encoder_measurements = []
estimated_states = []
controls = []

for t in time_steps:
    # Update true state with some dynamics
    true_state[0] += true_state[1] * dt
    true_state[2] += true_state[3] * dt
    true_state[1] += (fusion_balancer.omega**2 * (true_state[0] - 0.0)) * dt
    true_state[3] += (fusion_balancer.omega**2 * (true_state[2] - 0.0)) * dt
    
    # Add disturbances periodically
    if int(t) % 3 == 0 and t > 0:
        true_state[0] += np.random.uniform(-0.02, 0.02)
        true_state[2] += np.random.uniform(-0.02, 0.02)
    
    # Generate sensor measurements with noise
    imu_meas = np.array([
        true_state[4] * fusion_balancer.gravity + np.random.normal(0, 0.01),  # Pitch affects x acc
        true_state[5] * fusion_balancer.gravity + np.random.normal(0, 0.01),  # Roll affects y acc
        fusion_balancer.omega**2 * true_state[0] + fusion_balancer.gravity + np.random.normal(0, 0.01)  # z acc
    ])
    
    ft_meas = np.array([
        true_state[1] * 50 + np.random.normal(0, 0.5),  # x force
        true_state[3] * 50 + np.random.normal(0, 0.5),  # y force
        500 + true_state[4] * 10 + np.random.normal(0, 1),  # z force
        true_state[5] * 5 + np.random.normal(0, 0.1),  # x moment
        true_state[4] * 5 + np.random.normal(0, 0.1),  # y moment
        true_state[2] * 2 + np.random.normal(0, 0.1)   # z moment
    ])
    
    enc_meas = np.array([
        true_state[0] * 0.25 + np.random.normal(0, 0.001),
        true_state[2] * 0.25 + np.random.normal(0, 0.001),
        true_state[4] * 0.1 + np.random.normal(0, 0.001),
        true_state[5] * 0.1 + np.random.normal(0, 0.001)
    ])
    
    # Perform sensor fusion updates
    fusion_balancer.predict()
    fusion_balancer.update_imu(imu_meas)
    fusion_balancer.update_force_torque(ft_meas)
    fusion_balancer.update_encoders(enc_meas)
    
    # Get balance control
    control_output = fusion_balancer.get_balance_control()
    
    # Record data
    imu_measurements.append(imu_meas.copy())
    ft_measurements.append(ft_meas.copy())
    encoder_measurements.append(enc_meas.copy())
    estimated_states.append(fusion_balancer.state.copy())
    controls.append(control_output.copy())

imu_measurements = np.array(imu_measurements)
ft_measurements = np.array(ft_measurements)
encoder_measurements = np.array(encoder_measurements)
estimated_states = np.array(estimated_states)
controls = np.array(controls)

# Visualization
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

# Plot estimated vs true position
ax1.plot(time_steps, estimated_states[:, 0], label='Estimated X', linewidth=2)
ax1.plot(time_steps, estimated_states[:, 2], label='Estimated Y', linewidth=2)
ax1.ax_hline(y=0, color='k', linestyle='--', alpha=0.5, label='Desired')
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Position (m)')
ax1.set_title('Estimated CoM Position (Sensor Fusion)')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot estimated orientation
ax2.plot(time_steps, estimated_states[:, 4], label='Pitch', linewidth=2)
ax2.plot(time_steps, estimated_states[:, 5], label='Roll', linewidth=2)
ax2.ax_hline(y=0, color='k', linestyle='--', alpha=0.5, label='Desired')
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Orientation (rad)')
ax2.set_title('Estimated Orientation (Sensor Fusion)')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Plot control output
ax3.plot(time_steps, controls[:, 0], label='X Control', linewidth=2)
ax3.plot(time_steps, controls[:, 1], label='Y Control', linewidth=2)
ax3.set_xlabel('Time (s)')
ax3.set_ylabel('Control Output')
ax3.set_title('Balance Control Output')
ax3.legend()
ax3.grid(True, alpha=0.3)

# Plot estimation error
pos_error = np.linalg.norm(estimated_states[:, [0, 2]], axis=1)
orient_error = np.linalg.norm(estimated_states[:, [4, 5]], axis=1)

ax4.plot(time_steps, pos_error, label='Position Error', linewidth=2)
ax4.plot(time_steps, orient_error, label='Orientation Error', linewidth=2)
ax4.set_xlabel('Time (s)')
ax4.set_ylabel('Error Magnitude')
ax4.set_title('Estimation Error Over Time')
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

final_error = np.linalg.norm(estimated_states[-1, [0, 2]])
print(f"Sensor Fusion Balancer - Final position error magnitude: {final_error:.4f}")
```

## Balance Recovery Strategies

### Fall Prevention and Recovery

Implementing strategies to prevent and recover from falls:

```python
class BalanceRecoverySystem:
    def __init__(self, com_height=0.8):
        """
        System for preventing and recovering from balance losses
        
        Args:
            com_height: Center of mass height
        """
        self.com_height = com_height
        self.gravity = 9.81
        self.omega = np.sqrt(self.gravity / com_height)
        
        # Thresholds for different states
        self.stability_threshold = 0.05  # meters
        self.warning_threshold = 0.08   # meters
        self.critical_threshold = 0.12  # meters
        self.fall_threshold = 0.15      # meters
        
        # Recovery strategies
        self.strategies = {
            'ankle_strategy': {'weight': 1.0, 'active': True},
            'hip_strategy': {'weight': 0.3, 'active': False},
            'stepping_strategy': {'weight': 0.0, 'active': False},
            'crouching_strategy': {'weight': 0.0, 'active': False}
        }
        
        # State tracking
        self.state_history = []
        self.max_history = 20
        self.recovery_active = False
        self.recovery_start_time = 0
        
    def assess_stability(self, com_pos, com_vel, zmp_pos, support_polygon):
        """
        Assess current stability based on multiple factors
        
        Args:
            com_pos: Current CoM position [x, y]
            com_vel: Current CoM velocity [x_dot, y_dot]
            zmp_pos: Current ZMP position [x, y]
            support_polygon: Support polygon vertices [[x1,y1], [x2,y2], ...]
            
        Returns:
            Stability assessment and required action
        """
        # Calculate distance from CoM to edge of support polygon
        com_to_support_dist = self.distance_to_support_edge(com_pos, support_polygon)
        
        # Calculate ZMP margin
        zmp_to_support_dist = self.distance_to_support_edge(zmp_pos, support_polygon)
        
        # Calculate CoM velocity magnitude
        com_speed = np.linalg.norm(com_vel)
        
        # Combine metrics into stability score
        stability_score = min(com_to_support_dist, zmp_to_support_dist) - 0.3 * com_speed
        
        # Classify stability level
        if stability_score > self.stability_threshold:
            stability_level = 'stable'
            required_action = 'maintain'
        elif stability_score > self.warning_threshold:
            stability_level = 'caution'
            required_action = 'prepare'
        elif stability_score > self.critical_threshold:
            stability_level = 'critical'
            required_action = 'recover'
        else:
            stability_level = 'fall_imminent'
            required_action = 'emergency'
        
        # Update state history
        self.state_history.append({
            'time': len(self.state_history) * 0.01,
            'com_pos': com_pos.copy(),
            'com_vel': com_vel.copy(),
            'zmp_pos': zmp_pos.copy(),
            'stability_score': stability_score,
            'level': stability_level
        })
        
        if len(self.state_history) > self.max_history:
            self.state_history.pop(0)
        
        return stability_level, required_action, stability_score
    
    def distance_to_support_edge(self, point, polygon):
        """
        Calculate minimum distance from point to edges of polygon
        """
        min_dist = float('inf')
        
        for i in range(len(polygon)):
            p1 = np.array(polygon[i])
            p2 = np.array(polygon[(i + 1) % len(polygon)])
            
            # Calculate distance from point to line segment
            dist = self.point_to_line_distance(point, p1, p2)
            min_dist = min(min_dist, dist)
        
        return min_dist
    
    def point_to_line_distance(self, point, line_start, line_end):
        """
        Calculate distance from point to line segment
        """
        point = np.array(point)
        line_start = np.array(line_start)
        line_end = np.array(line_end)
        
        line_vec = line_end - line_start
        point_vec = point - line_start
        line_len_sq = np.dot(line_vec, line_vec)
        
        if line_len_sq == 0:
            return np.linalg.norm(point - line_start)
        
        t = max(0, min(1, np.dot(point_vec, line_vec) / line_len_sq))
        projection = line_start + t * line_vec
        return np.linalg.norm(point - projection)
    
    def select_recovery_strategy(self, stability_level, com_state, zmp_state):
        """
        Select appropriate recovery strategy based on situation
        
        Args:
            stability_level: Current stability level
            com_state: Current CoM state [pos, vel]
            zmp_state: Current ZMP state
            
        Returns:
            Selected strategy and parameters
        """
        if stability_level == 'stable':
            # Deactivate all recovery strategies
            for strategy in self.strategies.values():
                strategy['active'] = False
            return 'none', {}
        
        # Activate appropriate strategies based on severity
        if stability_level == 'caution':
            self.strategies['ankle_strategy']['active'] = True
            self.strategies['hip_strategy']['active'] = False
            self.strategies['stepping_strategy']['weight'] = 0.0
        elif stability_level == 'critical':
            self.strategies['ankle_strategy']['active'] = True
            self.strategies['hip_strategy']['active'] = True
            self.strategies['stepping_strategy']['weight'] = 0.3
        else:  # fall_imminent
            self.strategies['ankle_strategy']['active'] = False
            self.strategies['hip_strategy']['active'] = True
            self.strategies['stepping_strategy']['weight'] = 0.8
            self.strategies['crouching_strategy']['weight'] = 0.5
        
        # Determine which strategy to use based on direction of instability
        com_pos, com_vel = com_state
        
        # Calculate direction of instability
        instability_direction = np.arctan2(com_vel[1], com_vel[0])
        
        # Select strategy based on situation
        if self.strategies['stepping_strategy']['weight'] > 0.5:
            return 'stepping', {
                'direction': instability_direction,
                'step_size': min(0.3, np.linalg.norm(com_vel) * 0.5)
            }
        elif self.strategies['hip_strategy']['active']:
            return 'hip', {
                'torque': -com_pos * 50 - com_vel * 10  # PD-like control
            }
        else:
            return 'ankle', {
                'angle_adjustment': -com_pos * 2 - com_vel * 0.5
            }
    
    def generate_recovery_control(self, strategy, params, current_joints):
        """
        Generate control signals for recovery strategy
        
        Args:
            strategy: Selected strategy ('ankle', 'hip', 'stepping', 'crouching')
            params: Strategy-specific parameters
            current_joints: Current joint angles
            
        Returns:
            Control signals for actuators
        """
        control_signals = np.zeros(len(current_joints))
        
        if strategy == 'ankle':
            # Ankle strategy: adjust ankle angles to move ZMP
            control_signals[0] = params['angle_adjustment'][0]  # Ankle pitch
            control_signals[1] = params['angle_adjustment'][1]  # Ankle roll
        elif strategy == 'hip':
            # Hip strategy: use hip torques to counteract imbalance
            control_signals[2:4] = params['torque'] * 0.3  # Hip joints
        elif strategy == 'stepping':
            # Stepping strategy: prepare for step in appropriate direction
            step_direction = params['direction']
            step_size = params['step_size']
            
            # Generate control to shift weight and prepare step
            control_signals[4] = np.cos(step_direction) * step_size * 0.5  # Hip yaw
            control_signals[5] = np.sin(step_direction) * step_size * 0.5  # Hip roll
        elif strategy == 'crouching':
            # Crouching strategy: lower CoM to increase stability
            control_signals[6:] = -0.1  # Knee and other joints to crouch
        
        return control_signals

# Example: Balance recovery system
recovery_system = BalanceRecoverySystem(com_height=0.85)

# Simulate a destabilizing event
simulation_time = 15.0
dt = 0.01
time_steps = np.arange(0, simulation_time, dt)

# Start stable, then introduce disturbance
com_positions = []
com_velocities = []
zmp_positions = []
stability_levels = []
recovery_strategies = []

# Initial stable state
com_pos = np.array([0.0, 0.0])
com_vel = np.array([0.0, 0.0])
zmp_pos = np.array([0.0, 0.0])

# Define support polygon (rectangle representing feet)
support_poly = [[-0.1, -0.05], [0.2, -0.05], [0.2, 0.05], [-0.1, 0.05]]

for i, t in enumerate(time_steps):
    # Introduce disturbance at specific times
    if 5.0 < t < 5.1:
        # Strong disturbance
        com_vel += np.array([0.3, 0.2])
    elif 10.0 < t < 10.1:
        # Another disturbance
        com_vel += np.array([-0.2, 0.4])
    
    # Simple dynamics
    com_pos += com_vel * dt
    # Gravity and damping effect
    com_vel += (-2.0 * com_pos - 0.5 * com_vel) * dt
    
    # Add ZMP dynamics (simplified)
    zmp_pos += (com_pos - zmp_pos) * dt * 5.0
    
    # Assess stability
    stability_level, required_action, stability_score = recovery_system.assess_stability(
        com_pos, com_vel, zmp_pos, support_poly
    )
    
    # Select recovery strategy
    strategy, params = recovery_system.select_recovery_strategy(
        stability_level, (com_pos, com_vel), zmp_pos
    )
    
    # Generate recovery control (simulated)
    current_joints = np.zeros(12)  # 12 joints for example
    recovery_control = recovery_system.generate_recovery_control(
        strategy, params, current_joints
    )
    
    # Record data
    com_positions.append(com_pos.copy())
    com_velocities.append(com_vel.copy())
    zmp_positions.append(zmp_pos.copy())
    stability_levels.append(stability_level)
    recovery_strategies.append(strategy)

com_positions = np.array(com_positions)
com_velocities = np.array(com_velocities)
zmp_positions = np.array(zmp_positions)

# Convert stability levels to numerical values for plotting
stability_numeric = []
level_map = {'stable': 0, 'caution': 1, 'critical': 2, 'fall_imminent': 3}
for level in stability_levels:
    stability_numeric.append(level_map[level])

# Visualization
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

# Plot CoM and ZMP positions
ax1.plot(com_positions[:, 0], com_positions[:, 1], 'b-', linewidth=2, label='CoM Trajectory')
ax1.plot(zmp_positions[:, 0], zmp_positions[:, 1], 'r--', linewidth=2, label='ZMP Trajectory')
ax1.plot([v[0] for v in support_poly] + [support_poly[0][0]], 
         [v[1] for v in support_poly] + [support_poly[0][1]], 
         'k-', linewidth=3, label='Support Polygon')
ax1.set_xlabel('X Position (m)')
ax1.set_ylabel('Y Position (m)')
ax1.set_title('CoM and ZMP Trajectories with Support Polygon')
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.axis('equal')

# Plot stability level over time
colors = ['green', 'yellow', 'orange', 'red']
color_map = {'stable': colors[0], 'caution': colors[1], 'critical': colors[2], 'fall_imminent': colors[3]}
stability_colors = [color_map[level] for level in stability_levels]

ax2.scatter(time_steps, [0.1] * len(time_steps), c=stability_colors, s=20, alpha=0.7)
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Stability Level')
ax2.set_title('Stability Level Over Time')
ax2.set_yticks([])
ax2.grid(True, alpha=0.3)

# Plot CoM position over time
ax3.plot(time_steps, com_positions[:, 0], label='CoM X', linewidth=2)
ax3.plot(time_steps, com_positions[:, 1], label='CoM Y', linewidth=2)
ax3.ax_hline(y=0, color='k', linestyle='--', alpha=0.5, label='Desired')
ax3.set_xlabel('Time (s)')
ax3.set_ylabel('Position (m)')
ax3.set_title('CoM Position Over Time')
ax3.legend()
ax3.grid(True, alpha=0.3)

# Plot CoM velocity over time
ax4.plot(time_steps, com_velocities[:, 0], label='CoM X Vel', linewidth=2)
ax4.plot(time_steps, com_velocities[:, 1], label='CoM Y Vel', linewidth=2)
ax4.ax_hline(y=0, color='k', linestyle='--', alpha=0.5, label='Desired')
ax4.set_xlabel('Time (s)')
ax4.set_ylabel('Velocity (m/s)')
ax4.set_title('CoM Velocity Over Time')
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

final_stability = stability_levels[-1]
print(f"Balance Recovery System - Final stability: {final_stability}")
print(f"Final CoM position: [{com_positions[-1, 0]:.3f}, {com_positions[-1, 1]:.3f}]")
print(f"Final CoM velocity: [{com_velocities[-1, 0]:.3f}, {com_velocities[-1, 1]:.3f}]")
```

## Best Practices for Balance Control

### 1. Control System Design
- Use multiple control strategies (ankle, hip, stepping)
- Implement hierarchical control architecture
- Design smooth transitions between strategies
- Include anti-windup mechanisms in integrators

### 2. Sensor Integration
- Fuse data from multiple sensors (IMU, FT sensors, encoders)
- Implement outlier rejection for sensor data
- Account for sensor delays in control design
- Use redundant sensors for critical measurements

### 3. Adaptation and Learning
- Implement online parameter tuning
- Use machine learning for gait adaptation
- Learn from successful balance recovery attempts
- Adapt to different terrains and conditions

### 4. Safety and Robustness
- Implement multiple levels of protection
- Design graceful degradation when sensors fail
- Include emergency stop mechanisms
- Test extensively in simulation before real-world deployment

## Looking Ahead

This lesson covered advanced balance control systems for humanoid robots. The next lesson will focus on evaluation and tuning of balance control systems, including methods for assessing performance and optimizing parameters.

## Exercises

1. Implement an LQR controller for balance and compare with PID
2. Design a sensor fusion system for your humanoid robot
3. Create a balance recovery system that handles multiple disturbance types
4. Implement adaptive control for changing payloads
5. Evaluate the robustness of your balance controller to sensor noise

## Further Reading

- "Feedback Control of Dynamic Bipedal Robot Locomotion" by Gregg and Spong
- "Humanoid Robotics: A Reference" by Veljko Duburovic
- "Robotics: Control, Sensing, Vision, and Intelligence" by Fu, Gonzalez, and Lee
- "Linear Quadratic Regulators for Continuous Dynamical Systems" by Anderson and Moore