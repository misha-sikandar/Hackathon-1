---
sidebar_position: 23
---

# Week 8: Humanoid Locomotion and Balance Control

Welcome to Week 8 of our Physical AI & Humanoid Robotics journey! This week, we'll explore the complex challenges of humanoid locomotion and balance control. Humanoid robots face unique challenges in maintaining stability while performing dynamic movements, making locomotion one of the most difficult problems in robotics.

## Learning Objectives

By the end of this week, you will be able to:

1. Understand the biomechanics of human locomotion
2. Implement balance control algorithms for humanoid robots
3. Design walking patterns and gait generation
4. Apply control theory to humanoid balance systems
5. Integrate perception with locomotion for adaptive walking
6. Evaluate humanoid locomotion performance and stability

## Introduction to Humanoid Locomotion

Humanoid locomotion aims to replicate the complex movement patterns of human walking and balance. Unlike wheeled robots, humanoid robots must manage their center of mass (CoM) and maintain balance while moving, making this one of the most challenging problems in robotics.

### Why Humanoid Locomotion is Challenging

Humanoid locomotion presents several unique challenges:

- **Dynamic Balance**: Maintaining stability during movement
- **Degrees of Freedom**: Managing multiple joints for coordinated movement
- **Ground Contact**: Handling intermittent contact with the ground
- **Terrain Adaptation**: Adjusting to uneven surfaces
- **Energy Efficiency**: Minimizing energy consumption during walking

### Biomechanics of Human Walking

Human walking is a complex process involving multiple control systems:

1. **Central Pattern Generators (CPGs)**: Neural circuits that generate rhythmic patterns
2. **Reflexes**: Automatic responses to maintain balance
3. **Higher-Level Control**: Cognitive processes for navigation and obstacle avoidance
4. **Sensory Integration**: Combining visual, vestibular, and proprioceptive inputs

## Balance Control Fundamentals

### Zero Moment Point (ZMP)

The Zero Moment Point (ZMP) is a critical concept in humanoid balance control:

```python
import numpy as np
import matplotlib.pyplot as plt

class ZMPController:
    def __init__(self, robot_mass, gravity=9.81):
        """
        Zero Moment Point controller for humanoid balance
        
        Args:
            robot_mass: Mass of the robot (kg)
            gravity: Gravitational acceleration (m/s^2)
        """
        self.mass = robot_mass
        self.gravity = gravity
        self.com_height = 0.8  # Assumed CoM height (m)
        
    def calculate_zmp(self, com_pos, com_acc):
        """
        Calculate ZMP from Center of Mass position and acceleration
        
        Args:
            com_pos: Center of Mass position [x, y, z]
            com_acc: Center of Mass acceleration [x, y, z]
            
        Returns:
            ZMP position [x, y]
        """
        x_com, y_com, z_com = com_pos
        x_acc, y_acc, z_acc = com_acc
        
        # ZMP equations (simplified)
        zmp_x = x_com - (self.com_height / self.gravity) * x_acc
        zmp_y = y_com - (self.com_height / self.gravity) * y_acc
        
        return np.array([zmp_x, zmp_y])
    
    def is_balanced(self, zmp_pos, support_polygon):
        """
        Check if ZMP is within support polygon
        
        Args:
            zmp_pos: ZMP position [x, y]
            support_polygon: Vertices of support polygon [[x1,y1], [x2,y2], ...]
            
        Returns:
            Boolean indicating if balanced
        """
        # Simple implementation for rectangular support polygon
        # More complex implementation would use point-in-polygon algorithms
        x, y = zmp_pos
        
        # Get bounds of support polygon
        x_coords = [vertex[0] for vertex in support_polygon]
        y_coords = [vertex[1] for vertex in support_polygon]
        
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        
        return x_min <= x <= x_max and y_min <= y <= y_max

# Example usage
zmp_ctrl = ZMPController(robot_mass=50.0)

# Simulate CoM position and acceleration
com_pos = np.array([0.0, 0.0, 0.8])
com_acc = np.array([0.1, -0.05, 0.0])

zmp_pos = zmp_ctrl.calculate_zmp(com_pos, com_acc)
print(f"ZMP position: {zmp_pos}")

# Define support polygon (rectangle representing feet)
support_poly = [[-0.1, -0.05], [0.2, -0.05], [0.2, 0.05], [-0.1, 0.05]]
balanced = zmp_ctrl.is_balanced(zmp_pos, support_poly)
print(f"Is balanced: {balanced}")
```

### Center of Mass (CoM) Control

Controlling the Center of Mass is essential for humanoid balance:

```python
class CoMController:
    def __init__(self, kp=10.0, ki=1.0, kd=1.0):
        """
        PID controller for Center of Mass position
        
        Args:
            kp: Proportional gain
            ki: Integral gain
            kd: Derivative gain
        """
        self.kp = kp
        self.ki = ki
        self.kd = kd
        
        # State variables
        self.previous_error = 0.0
        self.integral = 0.0
        self.dt = 0.01  # Time step
    
    def update(self, current_pos, desired_pos):
        """
        Update PID controller
        
        Args:
            current_pos: Current CoM position
            desired_pos: Desired CoM position
            
        Returns:
            Control output
        """
        error = desired_pos - current_pos
        
        # Proportional term
        p_term = self.kp * error
        
        # Integral term
        self.integral += error * self.dt
        i_term = self.ki * self.integral
        
        # Derivative term
        derivative = (error - self.previous_error) / self.dt
        d_term = self.kd * derivative
        
        # Store error for next iteration
        self.previous_error = error
        
        # Calculate output
        output = p_term + i_term + d_term
        
        return output

# Example: Controlling CoM in single support phase
com_ctrl = CoMController(kp=15.0, ki=0.5, kd=2.0)

# Simulate CoM control during walking
time = np.arange(0, 2, 0.01)  # 2 seconds of simulation
current_com = np.zeros((len(time), 2))  # x, y position
desired_com = np.zeros((len(time), 2))

# Desired CoM trajectory (simple sway)
for i, t in enumerate(time):
    desired_com[i, 0] = 0.01 * np.sin(2 * np.pi * t)  # Small lateral sway
    desired_com[i, 1] = 0.02 * np.cos(2 * np.pi * t)  # Forward-back sway

# Simulate control
control_signals = np.zeros_like(current_com)
for i in range(1, len(time)):
    control_signals[i] = com_ctrl.update(current_com[i-1], desired_com[i])
    # Update current position based on control (simplified dynamics)
    current_com[i] = current_com[i-1] + control_signals[i] * 0.01

# Visualization
plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
plt.plot(time, desired_com[:, 0], label='Desired X', linestyle='--')
plt.plot(time, current_com[:, 0], label='Actual X')
plt.title('CoM X Position')
plt.xlabel('Time (s)')
plt.ylabel('Position (m)')
plt.legend()

plt.subplot(2, 2, 2)
plt.plot(time, desired_com[:, 1], label='Desired Y', linestyle='--')
plt.plot(time, current_com[:, 1], label='Actual Y')
plt.title('CoM Y Position')
plt.xlabel('Time (s)')
plt.ylabel('Position (m)')
plt.legend()

plt.subplot(2, 2, 3)
plt.plot(current_com[:, 0], current_com[:, 1], label='Actual Trajectory')
plt.plot(desired_com[:, 0], desired_com[:, 1], label='Desired Trajectory', linestyle='--')
plt.title('CoM Trajectory')
plt.xlabel('X Position (m)')
plt.ylabel('Y Position (m)')
plt.legend()
plt.axis('equal')

plt.subplot(2, 2, 4)
plt.plot(time, control_signals[:, 0], label='X Control')
plt.plot(time, control_signals[:, 1], label='Y Control')
plt.title('Control Signals')
plt.xlabel('Time (s)')
plt.ylabel('Control Output')
plt.legend()

plt.tight_layout()
plt.show()
```

## Walking Pattern Generation

### Inverted Pendulum Model

The inverted pendulum model is fundamental for humanoid walking:

```python
class InvertedPendulum:
    def __init__(self, height=0.8, gravity=9.81):
        """
        Inverted pendulum model for walking
        
        Args:
            height: Height of pendulum (CoM height)
            gravity: Gravitational acceleration
        """
        self.height = height
        self.gravity = gravity
        self.omega = np.sqrt(gravity / height)
    
    def calculate_capture_point(self, com_pos, com_vel):
        """
        Calculate capture point for stopping the robot
        
        Args:
            com_pos: Current CoM position
            com_vel: Current CoM velocity
            
        Returns:
            Capture point position
        """
        capture_point = com_pos + com_vel / self.omega
        return capture_point
    
    def calculate_com_trajectory(self, start_pos, end_pos, duration, t):
        """
        Calculate CoM trajectory for walking step
        
        Args:
            start_pos: Starting CoM position
            end_pos: Ending CoM position
            duration: Total step duration
            t: Current time
            
        Returns:
            CoM position and velocity at time t
        """
        # Use 5th order polynomial for smooth trajectory
        if t >= duration:
            return end_pos, np.zeros_like(end_pos)
        
        # Polynomial coefficients for smooth interpolation
        t_norm = t / duration
        
        # 5th order polynomial: a*t^5 + b*t^4 + c*t^3 + d*t^2 + e*t + f
        poly_coeff = np.array([
            6*t_norm**5 - 15*t_norm**4 + 10*t_norm**3,  # Position coefficient
            duration * (30*t_norm**4 - 60*t_norm**3 + 30*t_norm**2)  # Velocity coefficient
        ])
        
        pos_traj = start_pos + (end_pos - start_pos) * poly_coeff[0]
        vel_traj = (end_pos - start_pos) * poly_coeff[1] / duration
        
        return pos_traj, vel_traj

# Example: Generate walking pattern
pendulum = InvertedPendulum(height=0.85)

# Define step parameters
step_length = 0.3  # 30 cm step
step_duration = 1.0  # 1 second per step
step_height = 0.05  # 5 cm foot lift

# Generate walking trajectory
dt = 0.01
time_steps = np.arange(0, 2*step_duration, dt)
com_trajectory = []
foot_trajectory = []

for t in time_steps:
    # Determine which phase of walking we're in
    phase = int(t // step_duration)
    t_in_phase = t % step_duration
    
    if phase % 2 == 0:  # Left foot stance
        # CoM moves laterally toward right foot
        start_com = np.array([-0.05, -0.1]) if phase == 0 else np.array([-0.05, 0.1])
        end_com = np.array([-0.05, 0.1]) if phase == 0 else np.array([-0.05, -0.1])
        
        com_pos, com_vel = pendulum.calculate_com_trajectory(
            start_com, end_com, step_duration, t_in_phase
        )
        
        # Foot trajectory (left foot moves forward)
        foot_x = 0.0 if phase == 0 else step_length
        foot_y = -0.1 if phase == 0 else 0.1
        foot_z = 0.0
        if t_in_phase < step_duration/3:  # Lift foot
            foot_z = step_height * np.sin(np.pi * t_in_phase / (step_duration/3))
        
        foot_pos = np.array([foot_x, foot_y, foot_z])
    
    else:  # Right foot stance
        # CoM moves laterally toward left foot
        start_com = np.array([-0.05, 0.1])
        end_com = np.array([-0.05, -0.1])
        
        com_pos, com_vel = pendulum.calculate_com_trajectory(
            start_com, end_com, step_duration, t_in_phase
        )
        
        # Foot trajectory (right foot moves forward)
        foot_x = step_length if phase == 1 else 2*step_length
        foot_y = 0.1 if phase == 1 else -0.1
        foot_z = 0.0
        if t_in_phase < step_duration/3:  # Lift foot
            foot_z = step_height * np.sin(np.pi * t_in_phase / (step_duration/3))
        
        foot_pos = np.array([foot_x, foot_y, foot_z])
    
    com_trajectory.append(com_pos)
    foot_trajectory.append(foot_pos)

com_trajectory = np.array(com_trajectory)
foot_trajectory = np.array(foot_trajectory)

# Visualization
fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(com_trajectory[:, 0], com_trajectory[:, 1], 'b-', linewidth=2, label='CoM Trajectory')
ax.plot(foot_trajectory[:, 0], foot_trajectory[:, 1], 'r--', linewidth=1, label='Foot Positions')

# Mark foot positions
for i in range(0, len(foot_trajectory), 50):  # Plot every 50th point
    ax.plot(foot_trajectory[i, 0], foot_trajectory[i, 1], 'ro', markersize=4)

ax.set_xlabel('X Position (m)')
ax.set_ylabel('Y Position (m)')
ax.set_title('Walking Pattern: CoM and Foot Trajectories')
ax.legend()
ax.grid(True, alpha=0.3)
ax.axis('equal')

plt.tight_layout()
plt.show()
```

### Central Pattern Generators (CPGs)

CPGs generate rhythmic patterns for walking:

```python
class CPG:
    def __init__(self, frequency=1.0, amplitude=1.0, phase_diff=0.5*np.pi):
        """
        Central Pattern Generator for rhythmic movement
        
        Args:
            frequency: Oscillation frequency
            amplitude: Oscillation amplitude
            phase_diff: Phase difference between oscillators
        """
        self.frequency = frequency
        self.amplitude = amplitude
        self.phase_diff = phase_diff
        
        # State variables
        self.left_phase = 0.0
        self.right_phase = phase_diff
        self.dt = 0.01
    
    def step(self):
        """
        Update CPG oscillators
        
        Returns:
            Left and right oscillator outputs
        """
        # Update phases
        self.left_phase += 2 * np.pi * self.frequency * self.dt
        self.right_phase += 2 * np.pi * self.frequency * self.dt
        
        # Calculate outputs
        left_output = self.amplitude * np.sin(self.left_phase)
        right_output = self.amplitude * np.sin(self.right_phase)
        
        return left_output, right_output

class CPGWalkingController:
    def __init__(self):
        """
        Walking controller based on CPGs
        """
        self.cpg = CPG(frequency=0.8, amplitude=1.0)
        self.step_height = 0.05
        self.step_length = 0.3
        self.com_height = 0.8
        
        # Joint angle mappings
        self.hip_mapping = {'left': 0, 'right': 1}
        self.knee_mapping = {'left': 2, 'right': 3}
        self.ankle_mapping = {'left': 4, 'right': 5}
    
    def generate_step_pattern(self, time):
        """
        Generate step pattern using CPG output
        
        Args:
            time: Current time
            
        Returns:
            Joint angles for walking
        """
        # Update CPG
        left_signal, right_signal = self.cpg.step()
        
        # Map CPG signals to joint angles
        # This is a simplified mapping - real implementation would be more complex
        joint_angles = np.zeros(6)  # 6 joints: 3 per leg
        
        # Hip joints (swing/stance coordination)
        joint_angles[self.hip_mapping['left']] = 0.2 * left_signal
        joint_angles[self.hip_mapping['right']] = 0.2 * right_signal
        
        # Knee joints (flexion during swing)
        knee_left = 0.3 * max(0, left_signal)  # Only flex during swing
        knee_right = 0.3 * max(0, right_signal)
        joint_angles[self.knee_mapping['left']] = knee_left
        joint_angles[self.knee_mapping['right']] = knee_right
        
        # Ankle joints (compensation)
        joint_angles[self.ankle_mapping['left']] = -0.1 * left_signal
        joint_angles[self.ankle_mapping['right']] = -0.1 * right_signal
        
        return joint_angles

# Example: Generate walking pattern with CPG
cpg_controller = CPGWalkingController()

# Simulate walking for 5 seconds
simulation_time = 5.0
dt = 0.01
time_steps = np.arange(0, simulation_time, dt)

joint_trajectories = []
cpg_signals = []

for t in time_steps:
    joint_angles = cpg_controller.generate_step_pattern(t)
    left_signal, right_signal = cpg_controller.cpg.left_phase, cpg_controller.cpg.right_phase
    
    joint_trajectories.append(joint_angles)
    cpg_signals.append([np.sin(cpg_controller.cpg.left_phase), 
                        np.sin(cpg_controller.cpg.right_phase)])

joint_trajectories = np.array(joint_trajectories)
cpg_signals = np.array(cpg_signals)

# Visualization
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

# Plot CPG signals
ax1.plot(time_steps, cpg_signals[:, 0], label='Left Leg Signal', linewidth=2)
ax1.plot(time_steps, cpg_signals[:, 1], label='Right Leg Signal', linewidth=2)
ax1.set_ylabel('CPG Output')
ax1.set_title('CPG Signals for Walking')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot joint angles
for i in range(min(6, joint_trajectories.shape[1])):
    ax2.plot(time_steps, joint_trajectories[:, i], label=f'Joint {i}', linewidth=1.5)
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Joint Angle (rad)')
ax2.set_title('Joint Angle Trajectories Generated by CPG')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

## Advanced Balance Control

### Linear Inverted Pendulum Model (LIPM)

The Linear Inverted Pendulum Model simplifies balance control:

```python
class LIPMController:
    def __init__(self, com_height=0.8, gravity=9.81, dt=0.01):
        """
        Linear Inverted Pendulum Model controller
        
        Args:
            com_height: Constant CoM height
            gravity: Gravitational acceleration
            dt: Control time step
        """
        self.com_height = com_height
        self.gravity = gravity
        self.dt = dt
        self.omega = np.sqrt(gravity / com_height)
        
        # State: [x, x_dot] for both x and y directions
        self.state_x = np.array([0.0, 0.0])  # [position, velocity]
        self.state_y = np.array([0.0, 0.0])  # [position, velocity]
    
    def update(self, desired_zmp, current_zmp):
        """
        Update LIPM controller
        
        Args:
            desired_zmp: Desired ZMP [x, y]
            current_zmp: Current ZMP [x, y]
            
        Returns:
            Control input to track desired ZMP
        """
        # Error in ZMP
        zmp_error = desired_zmp - current_zmp
        
        # LIPM dynamics: double integrator with spring-like force
        # dx/dt = v
        # dv/dt = omega^2 * (x - zmp)
        
        # Update x-direction
        self.state_x[1] += self.omega**2 * (self.state_x[0] - desired_zmp[0]) * self.dt
        self.state_x[0] += self.state_x[1] * self.dt
        
        # Update y-direction
        self.state_y[1] += self.omega**2 * (self.state_y[0] - desired_zmp[1]) * self.dt
        self.state_y[0] += self.state_y[1] * self.dt
        
        # Calculate control to reduce ZMP error
        control_x = -1.0 * zmp_error[0]  # Simple proportional control
        control_y = -1.0 * zmp_error[1]
        
        return np.array([control_x, control_y])
    
    def get_com_state(self):
        """
        Get current CoM state [x, y, x_dot, y_dot]
        """
        return np.array([self.state_x[0], self.state_y[0], 
                         self.state_x[1], self.state_y[1]])

# Example: Stabilizing with LIPM controller
lipm_ctrl = LIPMController(com_height=0.85)

# Simulate balance control
simulation_time = 10.0
dt = 0.01
time_steps = np.arange(0, simulation_time, dt)

com_positions = []
zmp_errors = []

# Start with disturbance
lipm_ctrl.state_x = np.array([0.05, 0.1])  # Initial disturbance
lipm_ctrl.state_y = np.array([0.03, 0.05])

for t in time_steps:
    # Desired ZMP (center of support)
    desired_zmp = np.array([0.0, 0.0])
    
    # Current ZMP (affected by disturbance)
    current_zmp = np.array([
        lipm_ctrl.state_x[0] - lipm_ctrl.state_x[1] / lipm_ctrl.omega,
        lipm_ctrl.state_y[0] - lipm_ctrl.state_y[1] / lipm_ctrl.omega
    ])
    
    # Update controller
    control_input = lipm_ctrl.update(desired_zmp, current_zmp)
    
    # Record states
    com_pos = lipm_ctrl.get_com_state()
    com_positions.append(com_pos[:2])  # Only positions
    zmp_errors.append(np.linalg.norm(desired_zmp - current_zmp))

com_positions = np.array(com_positions)
zmp_errors = np.array(zmp_errors)

# Visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

# Plot CoM trajectory
ax1.plot(com_positions[:, 0], com_positions[:, 1], 'b-', linewidth=2)
ax1.plot(0, 0, 'ro', markersize=10, label='Desired Position')
ax1.set_xlabel('X Position (m)')
ax1.set_ylabel('Y Position (m)')
ax1.set_title('CoM Stabilization with LIPM Controller')
ax1.grid(True, alpha=0.3)
ax1.axis('equal')
ax1.legend()

# Plot ZMP error over time
ax2.plot(time_steps, zmp_errors, 'r-', linewidth=2)
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('ZMP Error (m)')
ax2.set_title('ZMP Tracking Error Over Time')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

### Model Predictive Control (MPC) for Walking

MPC provides optimal control for walking patterns:

```python
import cvxpy as cp

class MPCWalkingController:
    def __init__(self, horizon=20, dt=0.01, com_height=0.8):
        """
        Model Predictive Controller for walking
        
        Args:
            horizon: Prediction horizon
            dt: Time step
            com_height: CoM height
        """
        self.horizon = horizon
        self.dt = dt
        self.com_height = com_height
        self.gravity = 9.81
        self.omega = np.sqrt(self.gravity / self.com_height)
        
        # MPC variables
        self.com_pos_var = cp.Variable((horizon, 2))  # CoM positions
        self.com_vel_var = cp.Variable((horizon, 2))  # CoM velocities
        self.zmp_pos_var = cp.Variable((horizon, 2))  # ZMP positions
        
        # Constraints
        self.constraints = []
        
        # Cost function weights
        self.Q = np.eye(2) * 10.0  # State cost
        self.R = np.eye(2) * 1.0   # Control cost
        self.P = np.eye(2) * 20.0  # Terminal cost
    
    def setup_problem(self, current_state, desired_trajectory):
        """
        Set up MPC optimization problem
        
        Args:
            current_state: Current [com_pos, com_vel]
            desired_trajectory: Desired CoM trajectory [horizon x 2]
        """
        # Reset constraints
        self.constraints = []
        
        # Initial state constraint
        self.constraints.append(self.com_pos_var[0] == current_state[:2])
        self.constraints.append(self.com_vel_var[0] == current_state[2:])
        
        # Dynamics constraints (LIPM model)
        for k in range(self.horizon - 1):
            # x[k+1] = x[k] + v[k] * dt
            # v[k+1] = v[k] + omega^2 * (x[k] - zmp[k]) * dt
            self.constraints.append(
                self.com_pos_var[k+1] == 
                self.com_pos_var[k] + self.com_vel_var[k] * self.dt
            )
            self.constraints.append(
                self.com_vel_var[k+1] == 
                self.com_vel_var[k] + 
                self.omega**2 * (self.com_pos_var[k] - self.zmp_pos_var[k]) * self.dt
            )
        
        # Cost function
        state_cost = 0
        control_cost = 0
        
        for k in range(self.horizon):
            # State tracking cost
            state_error = self.com_pos_var[k] - desired_trajectory[k]
            state_cost += cp.quad_form(state_error, self.Q)
            
            # ZMP feasibility (stay within support polygon)
            # Simplified: constrain ZMP to reasonable bounds
            self.constraints.append(self.zmp_pos_var[k, 0] >= -0.1)  # x bounds
            self.constraints.append(self.zmp_pos_var[k, 0] <= 0.2)
            self.constraints.append(self.zmp_pos_var[k, 1] >= -0.1)  # y bounds
            self.constraints.append(self.zmp_pos_var[k, 1] <= 0.1)
        
        # Terminal cost
        terminal_error = self.com_pos_var[-1] - desired_trajectory[-1]
        terminal_cost = cp.quad_form(terminal_error, self.P)
        
        # Total cost
        total_cost = state_cost + terminal_cost
        
        # Create and solve problem
        problem = cp.Problem(cp.Minimize(total_cost), self.constraints)
        
        return problem
    
    def solve(self, current_state, desired_trajectory):
        """
        Solve MPC problem and return optimal ZMP sequence
        
        Args:
            current_state: Current [com_pos, com_vel]
            desired_trajectory: Desired CoM trajectory [horizon x 2]
            
        Returns:
            Optimal ZMP sequence
        """
        problem = self.setup_problem(current_state, desired_trajectory)
        
        try:
            problem.solve(warm_start=True)
            
            if problem.status not in ["infeasible", "unbounded"]:
                optimal_zmp = self.zmp_pos_var.value
                return optimal_zmp
            else:
                print(f"MPC problem status: {problem.status}")
                return None
                
        except Exception as e:
            print(f"MPC solver error: {e}")
            return None

# Example: MPC walking control
mpc_ctrl = MPCWalkingController(horizon=20, dt=0.01, com_height=0.85)

# Define desired trajectory (simple forward walk)
current_state = np.array([0.0, 0.0, 0.0, 0.0])  # [x, y, x_dot, y_dot]
desired_trajectory = np.zeros((20, 2))

# Create forward walking pattern
for i in range(20):
    desired_trajectory[i, 0] = 0.02 * i * 0.01  # Slow forward progression
    desired_trajectory[i, 1] = 0.05 * np.sin(i * 0.5)  # Lateral sway

# Solve MPC problem
optimal_zmp = mpc_ctrl.solve(current_state, desired_trajectory)

if optimal_zmp is not None:
    print(f"MPC solution found. Optimal ZMP shape: {optimal_zmp.shape}")
    
    # Visualization
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(desired_trajectory[:, 0], desired_trajectory[:, 1], 'b--', label='Desired Trajectory', linewidth=2)
    if optimal_zmp is not None:
        plt.plot(optimal_zmp[:, 0], optimal_zmp[:, 1], 'r-', label='Optimal ZMP', linewidth=2)
    plt.xlabel('X Position (m)')
    plt.ylabel('Y Position (m)')
    plt.title('MPC Walking Control: Desired vs Optimal ZMP')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.axis('equal')
    
    plt.subplot(1, 2, 2)
    if optimal_zmp is not None:
        time_axis = np.arange(len(optimal_zmp)) * 0.01
        plt.plot(time_axis, optimal_zmp[:, 0], label='ZMP X', linewidth=2)
        plt.plot(time_axis, optimal_zmp[:, 1], label='ZMP Y', linewidth=2)
        plt.xlabel('Time (s)')
        plt.ylabel('ZMP Position (m)')
        plt.title('Optimal ZMP Trajectory Over Time')
        plt.legend()
        plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
else:
    print("MPC solution not found")
```

## Integration with Perception Systems

### Vision-Based Terrain Adaptation

Using perception to adapt walking to terrain:

```python
import numpy as np
from scipy import ndimage
from sklearn.cluster import DBSCAN

class VisionBasedWalker:
    def __init__(self):
        """
        Walker that adapts to terrain using vision
        """
        self.walk_pattern_generator = CPGWalkingController()
        self.balance_controller = LIPMController()
        
        # Terrain analysis
        self.foot_separation = 0.2  # Distance between feet
        self.max_step_height = 0.1  # Maximum step height
        self.support_margin = 0.05  # Safety margin for support polygon
    
    def analyze_terrain(self, depth_image):
        """
        Analyze terrain from depth image to identify safe footholds
        
        Args:
            depth_image: Depth image from stereo camera or similar
            
        Returns:
            Safe foothold positions and terrain characteristics
        """
        # This is a simplified terrain analysis
        # In practice, this would involve more sophisticated computer vision
        
        # Identify flat regions in depth image
        # Calculate gradients to find level areas
        grad_x = np.gradient(depth_image, axis=1)
        grad_y = np.gradient(depth_image, axis=0)
        gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
        
        # Find regions with low gradient (flat areas)
        flat_regions = gradient_magnitude < 0.1  # Threshold for "flat"
        
        # Label connected flat regions
        labeled_regions, num_regions = ndimage.label(flat_regions)
        
        # Find centroids of flat regions (potential footholds)
        footholds = []
        for region_label in range(1, num_regions + 1):
            region_mask = (labeled_regions == region_label)
            y_coords, x_coords = np.where(region_mask)
            
            if len(x_coords) > 10:  # Only consider reasonably sized regions
                centroid_x = np.mean(x_coords)
                centroid_y = np.mean(y_coords)
                avg_depth = np.mean(depth_image[region_mask])
                
                footholds.append({
                    'x': centroid_x,
                    'y': centroid_y,
                    'depth': avg_depth,
                    'size': len(x_coords)
                })
        
        return footholds
    
    def adapt_walking_pattern(self, terrain_info, current_pos, target_pos):
        """
        Adapt walking pattern based on terrain information
        
        Args:
            terrain_info: Information about safe footholds
            current_pos: Current robot position
            target_pos: Target destination
            
        Returns:
            Adapted walking pattern
        """
        # Plan path through safe footholds
        if not terrain_info:
            # No safe footholds found, use default walking
            return self.default_walk_pattern(current_pos, target_pos)
        
        # Simple path planning through safe footholds
        # In practice, this would use more sophisticated path planning
        
        # Find footholds along the path from current to target
        path_footholds = []
        for foothold in terrain_info:
            # Calculate if foothold is roughly on the path
            # This is a simplified check
            path_vector = target_pos - current_pos
            foothold_vector = np.array([foothold['x'], foothold['y']]) - current_pos
            
            # Dot product to check if foothold is in general direction
            if np.dot(path_vector, foothold_vector) > 0:
                distance_to_path = np.abs(np.cross(path_vector, foothold_vector)) / np.linalg.norm(path_vector)
                if distance_to_path < 50:  # Within 50 pixels of path
                    path_footholds.append(foothold)
        
        # Sort footholds by distance along path
        path_footholds.sort(key=lambda f: np.linalg.norm(
            np.array([f['x'], f['y']]) - current_pos
        ))
        
        return path_footholds
    
    def default_walk_pattern(self, current_pos, target_pos):
        """
        Generate default walking pattern when terrain is unknown
        """
        # Simple straight-line walking pattern
        direction = target_pos - current_pos
        distance = np.linalg.norm(direction)
        
        if distance < 0.1:  # Very close to target
            return []
        
        # Generate steps along the path
        num_steps = int(distance / 0.3)  # 30cm per step
        step_pattern = []
        
        for i in range(num_steps):
            step_pos = current_pos + (direction / distance) * (i * 0.3)
            # Add small lateral variation to simulate natural walking
            step_pos[1] += 0.05 * ((i % 2) * 2 - 1)  # Alternate sides
            step_pattern.append(step_pos)
        
        return step_pattern

# Example: Vision-based walking adaptation
vision_walker = VisionBasedWalker()

# Simulate a depth image (simplified)
depth_image = np.ones((240, 320)) * 1.0  # Base depth
# Add some terrain variation
for i in range(0, 320, 40):
    depth_image[100:140, i:i+20] = 0.8  # Flat regions

# Analyze terrain
footholds = vision_walker.analyze_terrain(depth_image)
print(f"Found {len(footholds)} potential footholds")

# Adapt walking pattern
current_pos = np.array([0, 0])
target_pos = np.array([300, 200])  # In image coordinates
adapted_pattern = vision_walker.adapt_walking_pattern(footholds, current_pos, target_pos)

print(f"Adapted walking pattern has {len(adapted_pattern)} steps")

# Visualization
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.imshow(depth_image, cmap='viridis', origin='upper')
plt.colorbar(label='Depth (m)')
plt.title('Simulated Depth Image with Terrain Features')

# Mark detected footholds
if footholds:
    foothold_x = [f['x'] for f in footholds]
    foothold_y = [f['y'] for f in footholds]
    plt.scatter(foothold_x, foothold_y, c='red', s=50, marker='x', label='Footholds')

plt.plot([current_pos[0], target_pos[0]], [current_pos[1], target_pos[1]], 
         'w--', linewidth=2, label='Direct Path')
plt.legend()

plt.subplot(1, 2, 2)
if adapted_pattern:
    pattern_x = [p[0] for p in adapted_pattern]
    pattern_y = [p[1] for p in adapted_pattern]
    plt.scatter(pattern_x, pattern_y, c='blue', s=100, label='Adapted Path', zorder=5)
    
    # Connect the path
    if len(pattern_x) > 1:
        plt.plot(pattern_x, pattern_y, 'b-', linewidth=2, alpha=0.7)

plt.title('Adapted Walking Pattern')
plt.xlabel('X (pixels)')
plt.ylabel('Y (pixels)')
plt.legend()

plt.tight_layout()
plt.show()
```

## Stability Analysis and Evaluation

### Walking Stability Metrics

Evaluating the stability of humanoid walking:

```python
class WalkingStabilityAnalyzer:
    def __init__(self):
        """
        Analyzer for humanoid walking stability
        """
        self.margins = []
        self.energy_consumption = []
        self.step_regularity = []
    
    def calculate_stability_margins(self, com_trajectory, zmp_trajectory, support_polygons):
        """
        Calculate stability margins during walking
        
        Args:
            com_trajectory: CoM trajectory over time
            zmp_trajectory: ZMP trajectory over time
            support_polygons: Support polygons for each time step
            
        Returns:
            Stability margins over time
        """
        stability_margins = []
        
        for i in range(len(com_trajectory)):
            com_pos = com_trajectory[i][:2]  # Only x, y
            zmp_pos = zmp_trajectory[i]
            support_poly = support_polygons[i]
            
            # Calculate distance from ZMP to edge of support polygon
            # This is a simplified calculation
            x_coords = [vertex[0] for vertex in support_poly]
            y_coords = [vertex[1] for vertex in support_poly]
            
            x_min, x_max = min(x_coords), max(x_coords)
            y_min, y_max = min(y_coords), max(y_coords)
            
            # Calculate margins
            margin_x = min(abs(zmp_pos[0] - x_min), abs(zmp_pos[0] - x_max))
            margin_y = min(abs(zmp_pos[1] - y_min), abs(zmp_pos[1] - y_max))
            
            # Overall margin (minimum of x and y margins)
            overall_margin = min(margin_x, margin_y)
            stability_margins.append(overall_margin)
        
        return stability_margins
    
    def calculate_energy_efficiency(self, joint_trajectories, joint_velocities):
        """
        Calculate energy consumption during walking
        
        Args:
            joint_trajectories: Joint angle trajectories
            joint_velocities: Joint velocity trajectories
            
        Returns:
            Energy consumption estimate
        """
        # Simplified energy calculation based on joint work
        total_energy = 0.0
        
        for i in range(1, len(joint_trajectories)):
            # Approximate torque as proportional to angle change
            angle_change = np.abs(joint_trajectories[i] - joint_trajectories[i-1])
            velocity = joint_velocities[i]
            
            # Energy = sum of (torque * angular displacement)
            # Torque approximated as proportional to angle change
            step_energy = np.sum(angle_change * np.abs(velocity))
            total_energy += step_energy
        
        return total_energy
    
    def evaluate_step_regularity(self, step_times, step_lengths):
        """
        Evaluate regularity of walking steps
        
        Args:
            step_times: Time duration of each step
            step_lengths: Length of each step
            
        Returns:
            Regularity metrics
        """
        if len(step_times) < 2:
            return {'time_regularity': 1.0, 'length_regularity': 1.0}
        
        # Calculate coefficients of variation
        time_cv = np.std(step_times) / np.mean(step_times) if np.mean(step_times) > 0 else 0
        length_cv = np.std(step_lengths) / np.mean(step_lengths) if np.mean(step_lengths) > 0 else 0
        
        # Convert to regularity (inverse of variability)
        time_regularity = 1.0 / (1.0 + time_cv)
        length_regularity = 1.0 / (1.0 + length_cv)
        
        return {
            'time_regularity': time_regularity,
            'length_regularity': length_regularity,
            'mean_step_time': np.mean(step_times),
            'mean_step_length': np.mean(step_lengths)
        }

# Example: Stability analysis
analyzer = WalkingStabilityAnalyzer()

# Simulate walking data
n_steps = 100
time_steps = np.linspace(0, 5, n_steps)

# Generate simulated CoM and ZMP trajectories
com_traj = np.column_stack([
    0.1 * np.sin(0.5 * time_steps),  # Lateral sway
    0.05 * np.cos(0.5 * time_steps)  # Forward sway
])

zmp_traj = np.column_stack([
    0.08 * np.sin(0.5 * time_steps + 0.1),  # Slightly offset ZMP
    0.03 * np.cos(0.5 * time_steps + 0.1)
])

# Generate support polygons (simplified - alternating feet)
support_polys = []
for i in range(n_steps):
    if i % 20 < 10:  # Left foot support for first half of each cycle
        poly = [[-0.05, -0.1], [0.15, -0.1], [0.15, 0.0], [-0.05, 0.0]]
    else:  # Right foot support for second half
        poly = [[-0.05, 0.0], [0.15, 0.0], [0.15, 0.1], [-0.05, 0.1]]
    support_polys.append(poly)

# Calculate stability margins
stability_margins = analyzer.calculate_stability_margins(com_traj, zmp_traj, support_polys)

# Generate joint trajectory data for energy calculation
joint_traj = np.random.randn(n_steps, 6) * 0.1  # 6 joints, random motion
joint_vel = np.random.randn(n_steps, 6) * 0.5   # Joint velocities
energy = analyzer.calculate_energy_efficiency(joint_traj, joint_vel)

# Evaluate step regularity
step_times = np.random.normal(0.6, 0.05, 10)  # 10 steps
step_lengths = np.random.normal(0.3, 0.02, 10)
regularity = analyzer.evaluate_step_regularity(step_times, step_lengths)

print("Walking Stability Analysis:")
print(f"  Average stability margin: {np.mean(stability_margins):.3f} m")
print(f"  Minimum stability margin: {np.min(stability_margins):.3f} m")
print(f"  Energy consumption estimate: {energy:.3f}")
print(f"  Time regularity: {regularity['time_regularity']:.3f}")
print(f"  Length regularity: {regularity['length_regularity']:.3f}")

# Visualization
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

# Plot CoM and ZMP trajectories
ax1.plot(com_traj[:, 0], com_traj[:, 1], 'b-', linewidth=2, label='CoM Trajectory')
ax1.plot(zmp_traj[:, 0], zmp_traj[:, 1], 'r--', linewidth=2, label='ZMP Trajectory')
ax1.set_xlabel('X Position (m)')
ax1.set_ylabel('Y Position (m)')
ax1.set_title('CoM vs ZMP Trajectories')
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.axis('equal')

# Plot stability margins over time
ax2.plot(time_steps, stability_margins, 'g-', linewidth=2)
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Stability Margin (m)')
ax2.set_title('Stability Margins Over Time')
ax2.grid(True, alpha=0.3)

# Plot CoM and ZMP in time domain
ax3.plot(time_steps, com_traj[:, 0], label='CoM X', linewidth=2)
ax3.plot(time_steps, zmp_traj[:, 0], label='ZMP X', linestyle='--', linewidth=2)
ax3.set_xlabel('Time (s)')
ax3.set_ylabel('X Position (m)')
ax3.set_title('X Trajectories Over Time')
ax3.legend()
ax3.grid(True, alpha=0.3)

ax4.plot(time_steps, com_traj[:, 1], label='CoM Y', linewidth=2)
ax4.plot(time_steps, zmp_traj[:, 1], label='ZMP Y', linestyle='--', linewidth=2)
ax4.set_xlabel('Time (s)')
ax4.set_ylabel('Y Position (m)')
ax4.set_title('Y Trajectories Over Time')
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

## Best Practices for Humanoid Locomotion

### 1. Control Architecture
- Use hierarchical control (high-level planning, low-level stabilization)
- Implement multiple control modes (standing, walking, stepping)
- Design smooth transitions between modes
- Include safety mechanisms and fall prevention

### 2. Sensory Integration
- Combine multiple sensors (IMU, force/torque, vision)
- Implement sensor fusion for robust state estimation
- Use predictive models to handle sensor delays
- Account for sensor noise and uncertainty

### 3. Adaptation and Learning
- Implement online adaptation to changing conditions
- Use machine learning for gait optimization
- Learn from experience to improve stability
- Adapt to individual robot characteristics

### 4. Performance Optimization
- Optimize for energy efficiency
- Minimize computation time for real-time control
- Implement model predictive control for optimal performance
- Balance stability with mobility

## Looking Ahead

This week we explored the complex challenges of humanoid locomotion and balance control. Next week, we'll focus on manipulation, which involves the control of robot arms and hands to interact with objects in the environment.

## Exercises

1. Implement a ZMP-based balance controller for a simulated humanoid
2. Create a walking pattern generator using CPGs
3. Design a Model Predictive Controller for walking
4. Implement terrain-adaptive walking using perception
5. Evaluate the stability of your walking controller

## Further Reading

- "Humanoid Robotics: A Reference" by Veljko Duburovic
- "Introduction to Humanoid Robotics" by Shuuji Kajita
- "Robotics: Control, Sensing, Vision, and Intelligence" by Fu, Gonzalez, and Lee
- "Biologically Inspired Controllers for Quadrupedal Locomotion" by Ijspeert