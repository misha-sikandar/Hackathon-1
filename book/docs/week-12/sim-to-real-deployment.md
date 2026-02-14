---
sidebar_position: 33
---

# Week 12: Sim-to-Real Transfer and Deployment

Welcome to Week 12 of our Physical AI & Humanoid Robotics journey! This week, we'll explore the critical challenge of transferring systems from simulation to real-world deployment. This is one of the most important aspects of Physical AI, as the ultimate goal is to create robots that can operate effectively in the real world.

## Learning Objectives

By the end of this week, you will be able to:

1. Understand the sim-to-real transfer problem and its challenges
2. Implement domain randomization and system identification techniques
3. Design robust systems that handle reality gaps
4. Deploy robotic systems in real-world environments
5. Evaluate and validate deployed systems
6. Implement safety measures for real-world deployment

## Introduction to Sim-to-Real Transfer

The sim-to-real transfer problem refers to the challenge of taking robotic systems developed and tested in simulation environments and successfully deploying them on physical robots in real-world environments. This is a fundamental challenge in robotics because:

- **Reality Gap**: Simulations are imperfect models of the real world
- **Sensor Noise**: Real sensors have noise and imperfections not captured in simulation
- **Actuator Dynamics**: Real actuators have delays, friction, and other non-ideal behaviors
- **Environmental Variations**: Real environments have unmodeled aspects and variations
- **Hardware Limitations**: Physical robots have constraints not present in simulation

### Why Sim-to-Real Transfer Matters

Sim-to-real transfer is crucial for Physical AI systems because:

- **Safety**: Testing in simulation prevents damage to expensive hardware
- **Cost**: Simulation is much cheaper than real-world testing
- **Speed**: Simulation allows for faster iteration and testing
- **Reproducibility**: Simulation provides controlled, repeatable experiments
- **Scalability**: Multiple simulation instances can run in parallel

### The Reality Gap

The reality gap encompasses all differences between simulation and reality:

1. **Visual Gap**: Differences in appearance between simulated and real sensors
2. **Dynamics Gap**: Differences in physical behavior and interactions
3. **Sensor Gap**: Differences in sensor characteristics and noise
4. **Actuator Gap**: Differences in motor behavior and control
5. **Environment Gap**: Differences in environmental conditions

## Domain Randomization

Domain randomization is a technique to improve sim-to-real transfer by randomizing various aspects of the simulation:

```python
import numpy as np
import random
import gym
from gym import spaces

class DomainRandomizationWrapper(gym.Wrapper):
    def __init__(self, env, randomization_params=None):
        """
        Wrapper that applies domain randomization to a gym environment
        
        Args:
            env: Gym environment to wrap
            randomization_params: Dictionary of parameters to randomize
        """
        super().__init__(env)
        self.env = env
        
        # Default randomization parameters
        self.randomization_params = randomization_params or {
            'lighting': {'range': [0.5, 1.5], 'type': 'uniform'},
            'textures': {'options': ['wood', 'metal', 'plastic'], 'type': 'categorical'},
            'physics': {
                'friction': {'range': [0.1, 0.9], 'type': 'uniform'},
                'restitution': {'range': [0.0, 0.5], 'type': 'uniform'},
                'mass_multiplier': {'range': [0.8, 1.2], 'type': 'uniform'}
            },
            'object_appearance': {
                'color_variation': {'range': [0.0, 0.2], 'type': 'uniform'},
                'size_variation': {'range': [0.8, 1.2], 'type': 'uniform'}
            }
        }
        
        # Store original parameters for reset
        self.original_params = self.get_env_params()
        
    def get_env_params(self):
        """
        Get current environment parameters that can be randomized
        """
        params = {}
        # This would depend on the specific environment
        # For a generic implementation, we'll return a placeholder
        return params
    
    def randomize_domain(self):
        """
        Apply randomization to environment parameters
        """
        # Randomize lighting conditions
        if 'lighting' in self.randomization_params:
            lighting_range = self.randomization_params['lighting']['range']
            lighting_factor = random.uniform(*lighting_range)
            self.set_lighting(lighting_factor)
        
        # Randomize textures
        if 'textures' in self.randomization_params:
            texture_options = self.randomization_params['textures']['options']
            selected_texture = random.choice(texture_options)
            self.set_texture(selected_texture)
        
        # Randomize physics parameters
        if 'physics' in self.randomization_params:
            physics_params = self.randomization_params['physics']
            
            if 'friction' in physics_params:
                friction_range = physics_params['friction']['range']
                friction = random.uniform(*friction_range)
                self.set_friction(friction)
            
            if 'restitution' in physics_params:
                restitution_range = physics_params['restitution']['range']
                restitution = random.uniform(*restitution_range)
                self.set_restitution(restitution)
            
            if 'mass_multiplier' in physics_params:
                mass_range = physics_params['mass_multiplier']['range']
                mass_mult = random.uniform(*mass_range)
                self.multiply_masses(mass_mult)
        
        # Randomize object appearance
        if 'object_appearance' in self.randomization_params:
            appearance_params = self.randomization_params['object_appearance']
            
            if 'color_variation' in appearance_params:
                color_range = appearance_params['color_variation']['range']
                color_var = random.uniform(*color_range)
                self.set_color_variation(color_var)
            
            if 'size_variation' in appearance_params:
                size_range = appearance_params['size_variation']['range']
                size_var = random.uniform(*size_range)
                self.set_size_variation(size_var)
    
    def reset(self, **kwargs):
        """
        Reset environment with randomized parameters
        """
        # Reset to original parameters
        self.restore_original_params()
        
        # Apply randomization
        self.randomize_domain()
        
        # Reset the wrapped environment
        return self.env.reset(**kwargs)
    
    def step(self, action):
        """
        Take a step in the environment
        """
        return self.env.step(action)
    
    # Placeholder methods - these would be implemented based on the specific environment
    def set_lighting(self, factor):
        """Set lighting conditions"""
        pass
    
    def set_texture(self, texture):
        """Set texture"""
        pass
    
    def set_friction(self, friction):
        """Set friction parameters"""
        pass
    
    def set_restitution(self, restitution):
        """Set restitution parameters"""
        pass
    
    def multiply_masses(self, multiplier):
        """Multiply masses of objects"""
        pass
    
    def set_color_variation(self, variation):
        """Set color variation"""
        pass
    
    def set_size_variation(self, variation):
        """Set size variation"""
        pass
    
    def restore_original_params(self):
        """Restore original environment parameters"""
        pass

# Example usage with a custom environment
class SimpleDomainRandomizationEnv:
    def __init__(self):
        """
        Simple environment for demonstrating domain randomization
        """
        self.physics_params = {
            'friction': 0.5,
            'restitution': 0.1,
            'gravity': 9.81
        }
        self.visual_params = {
            'lighting': 1.0,
            'color_shift': [0.0, 0.0, 0.0]
        }
        self.object_properties = {
            'size': 1.0,
            'mass': 1.0
        }
    
    def set_friction(self, friction):
        """Set friction parameter"""
        self.physics_params['friction'] = friction
        print(f"Friction set to: {friction}")
    
    def set_lighting(self, lighting):
        """Set lighting parameter"""
        self.visual_params['lighting'] = lighting
        print(f"Lighting set to: {lighting}")
    
    def set_size_variation(self, size_var):
        """Apply size variation"""
        self.object_properties['size'] = 1.0 * size_var
        print(f"Object size set to: {self.object_properties['size']}")

# Example: Apply domain randomization
def example_domain_randomization():
    # Create environment
    env = SimpleDomainRandomizationEnv()
    
    # Define randomization parameters
    randomization_params = {
        'lighting': {'range': [0.7, 1.3], 'type': 'uniform'},
        'physics': {
            'friction': {'range': [0.3, 0.8], 'type': 'uniform'}
        },
        'object_appearance': {
            'size_variation': {'range': [0.9, 1.1], 'type': 'uniform'}
        }
    }
    
    # Wrap environment with domain randomization
    dr_env = DomainRandomizationWrapper(env, randomization_params)
    
    print("Applying domain randomization...")
    dr_env.randomize_domain()
    
    print(f"Environment parameters after randomization:")
    print(f"  Physics: {env.physics_params}")
    print(f"  Visual: {env.visual_params}")
    print(f"  Object: {env.object_properties}")

example_domain_randomization()
```

### Texture and Appearance Randomization

Randomizing visual properties to improve perception transfer:

```python
import cv2
import numpy as np
from PIL import Image, ImageEnhance
import random

class TextureRandomizer:
    def __init__(self, texture_library=None):
        """
        Randomize textures and appearances for sim-to-real transfer
        
        Args:
            texture_library: List of texture images or None for procedural generation
        """
        self.texture_library = texture_library or self.generate_procedural_textures()
    
    def generate_procedural_textures(self):
        """
        Generate procedural textures for randomization
        """
        textures = []
        
        # Generate different types of procedural textures
        for i in range(10):
            # Create a random procedural texture
            size = (64, 64)
            texture = np.random.rand(*size, 3) * 255
            texture = texture.astype(np.uint8)
            textures.append(texture)
        
        return textures
    
    def randomize_image(self, image):
        """
        Apply randomization to an input image
        
        Args:
            image: Input image (numpy array or PIL Image)
            
        Returns:
            Randomized image
        """
        if isinstance(image, Image.Image):
            image = np.array(image)
        
        # Apply various randomizations
        randomized = image.copy()
        
        # 1. Color adjustments
        randomized = self.randomize_color(randomized)
        
        # 2. Lighting adjustments
        randomized = self.randomize_lighting(randomized)
        
        # 3. Noise addition
        randomized = self.add_noise(randomized)
        
        # 4. Blur/sharpness
        randomized = self.adjust_blur(randomized)
        
        # 5. Compression artifacts (for camera simulation)
        randomized = self.add_compression_artifacts(randomized)
        
        return randomized
    
    def randomize_color(self, image):
        """
        Randomize color properties of image
        """
        # Randomize brightness
        brightness_factor = random.uniform(0.8, 1.2)
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] * brightness_factor, 0, 255)
        image = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
        
        # Randomize contrast
        contrast_factor = random.uniform(0.8, 1.2)
        image = np.clip((image - 128) * contrast_factor + 128, 0, 255).astype(np.uint8)
        
        # Randomize saturation
        saturation_factor = random.uniform(0.8, 1.2)
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * saturation_factor, 0, 255)
        image = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
        
        return image
    
    def randomize_lighting(self, image):
        """
        Randomize lighting conditions
        """
        # Add random shadows/highlights
        shadow_strength = random.uniform(0.0, 0.3)
        highlight_strength = random.uniform(0.0, 0.2)
        
        # Create a lighting gradient
        h, w = image.shape[:2]
        x = np.linspace(0, 1, w)
        y = np.linspace(0, 1, h)
        x_grid, y_grid = np.meshgrid(x, y)
        
        # Random lighting direction
        angle = random.uniform(0, 2 * np.pi)
        lighting = np.cos((x_grid - 0.5) * np.cos(angle) + (y_grid - 0.5) * np.sin(angle))
        lighting = (lighting + 1) / 2  # Normalize to [0, 1]
        
        # Apply lighting
        lighting = 1 - shadow_strength * (1 - lighting) + highlight_strength * lighting
        lighting = np.clip(lighting, 0.7, 1.3)  # Clamp to reasonable range
        
        # Expand lighting to 3 channels
        lighting = np.repeat(lighting[:, :, np.newaxis], 3, axis=2)
        
        image = np.clip(image.astype(np.float32) * lighting, 0, 255).astype(np.uint8)
        
        return image
    
    def add_noise(self, image):
        """
        Add various types of noise
        """
        # Add Gaussian noise
        if random.random() < 0.7:  # 70% chance of Gaussian noise
            noise = np.random.normal(0, random.uniform(1, 5), image.shape)
            image = np.clip(image.astype(np.float32) + noise, 0, 255).astype(np.uint8)
        
        # Add salt and pepper noise
        if random.random() < 0.3:  # 30% chance of salt and pepper
            prob = random.uniform(0.001, 0.01)
            noise_mask = np.random.random(image.shape[:2])
            image[noise_mask < prob] = 0  # Salt
            image[noise_mask > 1 - prob] = 255  # Pepper
        
        return image
    
    def adjust_blur(self, image):
        """
        Adjust blur/sharpness
        """
        blur_amount = random.uniform(0, 1)  # 0 = no blur, 1 = max blur
        
        if blur_amount > 0.1:
            kernel_size = int(blur_amount * 5) * 2 + 1  # Odd kernel size
            image = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
        
        return image
    
    def add_compression_artifacts(self, image):
        """
        Add JPEG compression artifacts
        """
        if random.random() < 0.5:  # 50% chance
            quality = random.randint(70, 95)  # Random quality
            
            # Convert to PIL Image for JPEG compression
            pil_image = Image.fromarray(image)
            
            # Save with compression
            import io
            buffer = io.BytesIO()
            pil_image.save(buffer, format='JPEG', quality=quality)
            buffer.seek(0)
            
            # Reload the compressed image
            compressed_image = Image.open(buffer)
            image = np.array(compressed_image)
        
        return image

# Example usage
def example_texture_randomization():
    # Create a sample image
    sample_image = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    
    # Create texture randomizer
    randomizer = TextureRandomizer()
    
    # Apply randomization
    randomized_image = randomizer.randomize_image(sample_image)
    
    print(f"Original image shape: {sample_image.shape}")
    print(f"Randomized image shape: {randomized_image.shape}")
    print("Texture randomization applied successfully!")

example_texture_randomization()
```

## System Identification and Calibration

### Identifying Simulation Parameters

System identification helps bridge the sim-to-real gap by calibrating simulation parameters:

```python
import numpy as np
from scipy.optimize import minimize
from scipy import signal
import matplotlib.pyplot as plt

class SystemIdentifier:
    def __init__(self, simulation_model, real_robot_interface):
        """
        System identifier to calibrate simulation parameters
        
        Args:
            simulation_model: Function that runs simulation with given parameters
            real_robot_interface: Interface to real robot for data collection
        """
        self.sim_model = simulation_model
        self.real_robot = real_robot_interface
        self.calibrated_params = {}
    
    def collect_real_data(self, input_signal, duration=10.0, dt=0.01):
        """
        Collect data from real robot with specific input
        
        Args:
            input_signal: Input signal to apply to robot
            duration: Duration of data collection
            dt: Time step
            
        Returns:
            Dictionary with input and output data
        """
        # In practice, this would interface with real robot
        # For simulation, we'll generate realistic data
        time_steps = int(duration / dt)
        real_outputs = []
        
        # Simulate collecting data from real robot
        for i in range(time_steps):
            # Apply input to real robot
            current_input = input_signal[i] if i < len(input_signal) else input_signal[-1]
            
            # Get output from real robot (simulated)
            # This would be replaced with actual robot interface
            output = self.simulate_real_robot_response(current_input, dt)
            real_outputs.append(output)
        
        return {
            'time': np.arange(0, duration, dt)[:len(real_outputs)],
            'input': input_signal[:len(real_outputs)],
            'output': np.array(real_outputs)
        }
    
    def simulate_real_robot_response(self, input_val, dt):
        """
        Simulate real robot response (in practice, this would be real robot)
        """
        # Simulate a first-order system with noise
        # y_dot = -a*y + b*u + noise
        if not hasattr(self, 'real_state'):
            self.real_state = 0.0
        
        a = 0.5  # Time constant
        b = 1.0  # Gain
        noise = np.random.normal(0, 0.01)  # Measurement noise
        
        # Update state
        self.real_state += (-a * self.real_state + b * input_val) * dt + noise
        return self.real_state
    
    def simulation_error(self, params, input_signal, real_outputs):
        """
        Calculate error between simulation and real outputs
        
        Args:
            params: Parameters to use in simulation
            input_signal: Input signal
            real_outputs: Real robot outputs
            
        Returns:
            Error metric
        """
        # Run simulation with current parameters
        sim_outputs = self.run_simulation(params, input_signal)
        
        # Calculate error (mean squared error)
        if len(sim_outputs) != len(real_outputs):
            # Truncate to same length
            min_len = min(len(sim_outputs), len(real_outputs))
            sim_outputs = sim_outputs[:min_len]
            real_outputs = real_outputs[:min_len]
        
        mse = np.mean((sim_outputs - real_outputs) ** 2)
        return mse
    
    def run_simulation(self, params, input_signal):
        """
        Run simulation with given parameters
        
        Args:
            params: Dictionary of parameters
            input_signal: Input signal
            
        Returns:
            Simulation outputs
        """
        # Extract parameters
        a = params.get('a', 0.5)  # Time constant
        b = params.get('b', 1.0)  # Gain
        noise_std = params.get('noise_std', 0.01)  # Noise standard deviation
        
        dt = 0.01  # Time step
        sim_outputs = []
        sim_state = 0.0
        
        for input_val in input_signal:
            # Simulate system: y_dot = -a*y + b*u + noise
            noise = np.random.normal(0, noise_std)
            sim_state += (-a * sim_state + b * input_val) * dt + noise
            sim_outputs.append(sim_state)
        
        return np.array(sim_outputs)
    
    def calibrate_parameters(self, initial_params, input_signal, real_outputs, 
                           bounds=None, method='L-BFGS-B'):
        """
        Calibrate simulation parameters to match real robot
        
        Args:
            initial_params: Initial parameter guesses
            input_signal: Input signal used for calibration
            real_outputs: Real robot outputs
            bounds: Parameter bounds for optimization
            method: Optimization method
            
        Returns:
            Calibrated parameters
        """
        if bounds is None:
            # Default bounds
            bounds = {
                'a': (0.1, 2.0),
                'b': (0.5, 2.0),
                'noise_std': (0.001, 0.1)
            }
        
        def objective(params_array):
            # Convert array back to parameter dictionary
            param_names = list(initial_params.keys())
            params_dict = {name: params_array[i] for i, name in enumerate(param_names)}
            
            # Calculate error
            error = self.simulation_error(params_dict, input_signal, real_outputs)
            return error
        
        # Convert initial parameters to array
        initial_array = [initial_params[name] for name in initial_params.keys()]
        
        # Define bounds for optimizer
        opt_bounds = [bounds[name] for name in initial_params.keys()]
        
        # Optimize parameters
        result = minimize(
            objective,
            initial_array,
            method=method,
            bounds=opt_bounds,
            options={'disp': True}
        )
        
        # Convert result back to parameter dictionary
        calibrated_params = {
            name: result.x[i] for i, name in enumerate(initial_params.keys())
        }
        
        self.calibrated_params = calibrated_params
        
        return calibrated_params, result

# Example usage
def example_system_identification():
    # Create a mock robot interface
    class MockRobotInterface:
        def __init__(self):
            pass
    
    # Create system identifier
    identifier = SystemIdentifier(None, MockRobotInterface())
    
    # Generate input signal (PRBS - Pseudo Random Binary Sequence)
    duration = 20.0
    dt = 0.01
    time_steps = int(duration / dt)
    
    # Create PRBS input
    input_signal = np.random.choice([-1, 1], size=time_steps) * 0.5
    # Smooth the input to make it more realistic
    input_signal = np.convolve(input_signal, np.ones(10)/10, mode='same')
    
    # Collect "real" data from robot
    real_data = identifier.collect_real_data(input_signal, duration, dt)
    
    # Define initial parameters
    initial_params = {
        'a': 0.5,  # Time constant
        'b': 1.0,  # Gain
        'noise_std': 0.01  # Noise standard deviation
    }
    
    # Calibrate parameters
    calibrated_params, result = identifier.calibrate_parameters(
        initial_params, 
        real_data['input'], 
        real_data['output']
    )
    
    print("System Identification Results:")
    print(f"Initial parameters: {initial_params}")
    print(f"Calibrated parameters: {calibrated_params}")
    print(f"Optimization success: {result.success}")
    print(f"Final error: {result.fun:.6f}")
    
    # Compare before and after calibration
    initial_outputs = identifier.run_simulation(initial_params, real_data['input'])
    calibrated_outputs = identifier.run_simulation(calibrated_params, real_data['input'])
    
    # Calculate errors
    initial_error = np.mean((initial_outputs - real_data['output']) ** 2)
    calibrated_error = np.mean((calibrated_outputs - real_data['output']) ** 2)
    
    print(f"Initial MSE: {initial_error:.6f}")
    print(f"Calibrated MSE: {calibrated_error:.6f}")
    print(f"Improvement: {(initial_error - calibrated_error) / initial_error * 100:.2f}%")

example_system_identification()
```

## Robust Control for Reality Gap

### Adaptive Control Systems

Implementing control systems that adapt to reality gaps:

```python
import numpy as np
import matplotlib.pyplot as plt

class AdaptiveController:
    def __init__(self, initial_params=None, learning_rate=0.01):
        """
        Adaptive controller that adjusts parameters based on performance
        
        Args:
            initial_params: Initial controller parameters
            learning_rate: Rate of parameter adaptation
        """
        self.learning_rate = learning_rate
        self.params = initial_params or {
            'kp': 1.0,  # Proportional gain
            'ki': 0.1,  # Integral gain
            'kd': 0.05  # Derivative gain
        }
        
        # State variables
        self.integral = 0.0
        self.previous_error = 0.0
        self.error_history = []
        self.param_history = {'kp': [], 'ki': [], 'kd': []}
    
    def update(self, error, dt=0.01):
        """
        Update controller and adapt parameters based on error
        
        Args:
            error: Current error (desired - actual)
            dt: Time step
            
        Returns:
            Control output
        """
        # Store error for history
        self.error_history.append(error)
        
        # Calculate PID terms
        p_term = self.params['kp'] * error
        
        self.integral += error * dt
        i_term = self.params['ki'] * self.integral
        
        derivative = (error - self.previous_error) / dt if dt > 0 else 0
        d_term = self.params['kd'] * derivative
        
        # Calculate control output
        control_output = p_term + i_term + d_term
        
        # Adapt parameters based on performance
        self.adapt_parameters(error, dt)
        
        # Update previous error
        self.previous_error = error
        
        return control_output
    
    def adapt_parameters(self, error, dt):
        """
        Adapt controller parameters based on performance
        """
        # Calculate performance metrics
        recent_errors = self.error_history[-10:] if len(self.error_history) >= 10 else self.error_history
        if len(recent_errors) == 0:
            return
        
        mean_error = np.mean(np.abs(recent_errors))
        error_variance = np.var(recent_errors)
        
        # Adapt based on error characteristics
        if mean_error > 0.1:  # High steady-state error
            self.params['kp'] += self.learning_rate * 0.1
        elif mean_error < 0.01:  # Low error, possibly oscillating
            self.params['kp'] = max(0.1, self.params['kp'] - self.learning_rate * 0.05)
        
        # Adapt integral term based on steady-state error
        if mean_error > 0.05 and abs(error) > 0.05:
            self.params['ki'] += self.learning_rate * 0.01
        elif len(recent_errors) > 5 and np.all(np.abs(recent_errors[-5:]) < 0.01):
            self.params['ki'] = max(0.01, self.params['ki'] - self.learning_rate * 0.01)
        
        # Adapt derivative term based on oscillation
        if error_variance > 0.01:  # High variance indicates oscillation
            self.params['kd'] += self.learning_rate * 0.02
        elif error_variance < 0.001:  # Low variance, might need more damping
            self.params['kd'] = max(0.01, self.params['kd'] - self.learning_rate * 0.01)
        
        # Keep parameters within reasonable bounds
        self.params['kp'] = np.clip(self.params['kp'], 0.1, 10.0)
        self.params['ki'] = np.clip(self.params['ki'], 0.01, 2.0)
        self.params['kd'] = np.clip(self.params['kd'], 0.01, 2.0)
        
        # Store parameter history
        self.param_history['kp'].append(self.params['kp'])
        self.param_history['ki'].append(self.params['ki'])
        self.param_history['kd'].append(self.params['kd'])

class RobustControlSystem:
    def __init__(self, adaptive_controller):
        """
        Robust control system with adaptive capabilities
        
        Args:
            adaptive_controller: Adaptive controller instance
        """
        self.controller = adaptive_controller
        self.safety_limits = {
            'max_control': 10.0,
            'max_rate': 5.0  # Maximum rate of change
        }
        self.previous_control = 0.0
    
    def compute_control(self, error, dt=0.01):
        """
        Compute control with safety limits
        
        Args:
            error: Current error
            dt: Time step
            
        Returns:
            Safe control output
        """
        # Get control from adaptive controller
        control = self.controller.update(error, dt)
        
        # Apply safety limits
        control = np.clip(control, -self.safety_limits['max_control'], self.safety_limits['max_control'])
        
        # Limit rate of change
        rate_limit = self.safety_limits['max_rate'] * dt
        control = np.clip(
            control,
            self.previous_control - rate_limit,
            self.previous_control + rate_limit
        )
        
        self.previous_control = control
        
        return control

# Example: Adaptive control with reality gap simulation
def example_adaptive_control():
    # Create adaptive controller
    controller = AdaptiveController(
        initial_params={'kp': 0.5, 'ki': 0.05, 'kd': 0.02},
        learning_rate=0.005
    )
    
    # Create robust control system
    robust_system = RobustControlSystem(controller)
    
    # Simulate system with reality gap
    dt = 0.01
    time_steps = 1000  # 10 seconds
    time = np.arange(0, time_steps * dt, dt)
    
    # Desired trajectory (step input)
    desired = np.ones(time_steps) * 1.0
    # Add some disturbances to simulate reality gap
    disturbances = 0.1 * np.sin(2 * np.pi * 0.5 * time)  # Low frequency disturbance
    
    # Simulate plant response (first-order system with delay)
    actual = np.zeros(time_steps)
    control_signals = np.zeros(time_steps)
    
    # Plant parameters (different from controller design model)
    plant_poles = [-1.5]  # Different from assumed model
    plant_zeros = [0.5]
    
    plant_state = 0.0
    
    for i in range(1, time_steps):
        # Calculate error with disturbances
        error = desired[i-1] - actual[i-1] + disturbances[i-1]
        
        # Compute control
        control = robust_system.compute_control(error, dt)
        control_signals[i] = control
        
        # Apply control to plant (simulated)
        # Simple first-order system: dx/dt = -a*x + b*u
        a = 1.2  # Different from assumed value
        b = 0.8  # Different from assumed value
        plant_state += (-a * plant_state + b * control) * dt
        actual[i] = plant_state
    
    # Plot results
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))
    
    # Plot 1: System response
    ax1.plot(time, desired, 'g--', label='Desired', linewidth=2)
    ax1.plot(time, actual, 'b-', label='Actual', linewidth=2)
    ax1.plot(time, disturbances, 'r:', label='Disturbances', linewidth=1)
    ax1.set_ylabel('Position')
    ax1.set_title('System Response with Adaptive Control')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Control signals
    ax2.plot(time, control_signals, 'm-', linewidth=2)
    ax2.set_ylabel('Control Signal')
    ax2.set_title('Control Signals')
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Parameter adaptation
    param_history = controller.param_history
    if len(param_history['kp']) > 0:
        t_params = np.linspace(0, time[-1], len(param_history['kp']))
        ax3.plot(t_params, param_history['kp'], label='Kp', linewidth=2)
        ax3.plot(t_params, param_history['ki'], label='Ki', linewidth=2)
        ax3.plot(t_params, param_history['kd'], label='Kd', linewidth=2)
        ax3.set_xlabel('Time (s)')
        ax3.set_ylabel('Parameter Value')
        ax3.set_title('Adaptive Parameter Evolution')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # Print final parameters
    final_params = controller.params
    print(f"\nFinal adaptive parameters:")
    for param, value in final_params.items():
        print(f"  {param}: {value:.4f}")
    
    # Calculate performance metrics
    error = desired - actual
    mse = np.mean(error**2)
    final_error = error[-100:].mean()  # Average of last 100 points
    
    print(f"\nPerformance metrics:")
    print(f"  Mean Squared Error: {mse:.6f}")
    print(f"  Final Error: {final_error:.6f}")

example_adaptive_control()
```

## Deployment Strategies

### Gradual Deployment and Testing

Deploying systems safely from simulation to reality:

```python
import time
import logging
from enum import Enum
from typing import Dict, Any, Callable

class DeploymentStage(Enum):
    SIMULATION = "simulation"
    SIMULATION_WITH_NOISE = "simulation_with_noise"
    SIMULATION_WITH_REAL_CONTROLLERS = "simulation_with_real_controllers"
    PHYSICAL_SIMULATOR = "physical_simulator"  # Robot on test stand
    CONTROLLED_ENVIRONMENT = "controlled_environment"
    SEMI_CONTROLLED_ENVIRONMENT = "semi_controlled_environment"
    FULL_DEPLOYMENT = "full_deployment"

class DeploymentManager:
    def __init__(self, robot_interface, safety_system):
        """
        Manage deployment from simulation to real robot
        
        Args:
            robot_interface: Interface to robot control system
            safety_system: Safety monitoring system
        """
        self.robot_interface = robot_interface
        self.safety_system = safety_system
        self.current_stage = DeploymentStage.SIMULATION
        self.stage_metrics = {}
        self.logger = logging.getLogger(__name__)
        
        # Stage-specific parameters
        self.stage_params = {
            DeploymentStage.SIMULATION: {
                'max_trials': 100,
                'success_threshold': 0.95,
                'failure_threshold': 0.1
            },
            DeploymentStage.SIMULATION_WITH_NOISE: {
                'max_trials': 50,
                'success_threshold': 0.90,
                'failure_threshold': 0.15
            },
            DeploymentStage.SIMULATION_WITH_REAL_CONTROLLERS: {
                'max_trials': 30,
                'success_threshold': 0.85,
                'failure_threshold': 0.2
            },
            DeploymentStage.PHYSICAL_SIMULATOR: {
                'max_trials': 20,
                'success_threshold': 0.80,
                'failure_threshold': 0.25,
                'safety_check_interval': 1.0  # seconds
            },
            DeploymentStage.CONTROLLED_ENVIRONMENT: {
                'max_trials': 15,
                'success_threshold': 0.75,
                'failure_threshold': 0.3,
                'safety_check_interval': 0.5
            },
            DeploymentStage.SEMI_CONTROLLED_ENVIRONMENT: {
                'max_trials': 10,
                'success_threshold': 0.70,
                'failure_threshold': 0.35,
                'safety_check_interval': 0.2
            },
            DeploymentStage.FULL_DEPLOYMENT: {
                'max_trials': float('inf'),
                'success_threshold': 0.65,
                'failure_threshold': 0.4,
                'safety_check_interval': 0.1
            }
        }
    
    def advance_stage(self, success_rate: float) -> bool:
        """
        Determine if we can advance to the next deployment stage
        
        Args:
            success_rate: Current success rate
            
        Returns:
            True if stage can be advanced, False otherwise
        """
        params = self.stage_params[self.current_stage]
        
        if success_rate >= params['success_threshold']:
            # Check if we can move to next stage
            stage_order = list(DeploymentStage)
            current_idx = stage_order.index(self.current_stage)
            
            if current_idx < len(stage_order) - 1:
                next_stage = stage_order[current_idx + 1]
                self.logger.info(f"Advancing from {self.current_stage.value} to {next_stage.value}")
                self.current_stage = next_stage
                return True
        
        elif success_rate <= params['failure_threshold']:
            # Success rate too low, don't advance
            self.logger.warning(f"Success rate {success_rate:.3f} below threshold {params['failure_threshold']:.3f}, staying at {self.current_stage.value}")
            return False
        
        # Success rate is in acceptable range, don't advance automatically
        self.logger.info(f"Success rate {success_rate:.3f} in acceptable range, staying at {self.current_stage.value}")
        return False
    
    def run_stage_test(self, test_function: Callable, num_trials: int = 10) -> Dict[str, Any]:
        """
        Run tests for current deployment stage
        
        Args:
            test_function: Function that runs a single test trial
            num_trials: Number of trials to run
            
        Returns:
            Dictionary with test results
        """
        results = {
            'trials': [],
            'successes': 0,
            'failures': 0,
            'success_rate': 0.0,
            'average_time': 0.0,
            'safety_violations': 0
        }
        
        for i in range(num_trials):
            start_time = time.time()
            
            try:
                # Run safety check if applicable
                if self.current_stage in [DeploymentStage.PHYSICAL_SIMULATOR, 
                                        DeploymentStage.CONTROLLED_ENVIRONMENT,
                                        DeploymentStage.SEMI_CONTROLLED_ENVIRONMENT,
                                        DeploymentStage.FULL_DEPLOYMENT]:
                    if not self.safety_system.check_safety():
                        self.logger.error("Safety check failed, terminating test")
                        results['safety_violations'] += 1
                        continue
                
                # Run the test
                trial_result = test_function()
                
                # Record result
                trial_success = trial_result.get('success', False)
                results['trials'].append(trial_result)
                
                if trial_success:
                    results['successes'] += 1
                else:
                    results['failures'] += 1
                
                # Check for safety violations
                if trial_result.get('safety_violation', False):
                    results['safety_violations'] += 1
                
            except Exception as e:
                self.logger.error(f"Test trial {i+1} failed with exception: {e}")
                results['failures'] += 1
                results['trials'].append({'success': False, 'error': str(e)})
            
            # Calculate metrics
            total_completed = results['successes'] + results['failures']
            if total_completed > 0:
                results['success_rate'] = results['successes'] / total_completed
                results['average_time'] = (time.time() - start_time) / total_completed
        
        return results
    
    def deploy_system(self, task_function: Callable):
        """
        Deploy system through all stages
        
        Args:
            task_function: Function that executes the main task
        """
        stage_order = list(DeploymentStage)
        
        for stage in stage_order:
            self.current_stage = stage
            self.logger.info(f"Entering deployment stage: {stage.value}")
            
            # Configure environment for current stage
            self.configure_stage_environment(stage)
            
            # Run tests for this stage
            results = self.run_stage_test(
                lambda: task_function(self.current_stage),
                num_trials=self.stage_params[stage]['max_trials']
            )
            
            # Log results
            self.logger.info(f"Stage {stage.value} results:")
            self.logger.info(f"  Success rate: {results['success_rate']:.3f}")
            self.logger.info(f"  Successes: {results['successes']}")
            self.logger.info(f"  Failures: {results['failures']}")
            self.logger.info(f"  Safety violations: {results['safety_violations']}")
            
            # Store metrics
            self.stage_metrics[stage.value] = results
            
            # Check if we can advance
            if stage != DeploymentStage.FULL_DEPLOYMENT:  # Don't advance past full deployment
                self.advance_stage(results['success_rate'])
    
    def configure_stage_environment(self, stage: DeploymentStage):
        """
        Configure environment for specific deployment stage
        """
        if stage == DeploymentStage.SIMULATION_WITH_NOISE:
            # Add noise to sensors and actuators
            self.robot_interface.add_sensor_noise(0.05)
            self.robot_interface.add_actuator_noise(0.02)
        
        elif stage == DeploymentStage.SIMULATION_WITH_REAL_CONTROLLERS:
            # Use real control algorithms instead of idealized ones
            self.robot_interface.use_real_controllers()
        
        elif stage == DeploymentStage.PHYSICAL_SIMULATOR:
            # Robot on test stand with safety equipment
            self.safety_system.enable_physical_safety()
        
        elif stage == DeploymentStage.CONTROLLED_ENVIRONMENT:
            # Controlled environment with limited obstacles
            self.robot_interface.set_controlled_environment()
        
        elif stage == DeploymentStage.SEMI_CONTROLLED_ENVIRONMENT:
            # More complex environment with some unpredictability
            self.robot_interface.set_unpredictable_environment()
        
        elif stage == DeploymentStage.FULL_DEPLOYMENT:
            # Full real-world deployment
            self.robot_interface.set_real_world_environment()

# Example safety system
class SafetySystem:
    def __init__(self):
        self.safety_enabled = False
        self.emergency_stop = False
        self.safety_limits = {
            'max_velocity': 1.0,
            'max_acceleration': 2.0,
            'max_force': 50.0,
            'workspace_boundary': [[-2, 2], [-2, 2], [0, 2]]  # x, y, z limits
        }
    
    def enable_physical_safety(self):
        """Enable physical safety measures"""
        self.safety_enabled = True
        print("Physical safety measures enabled")
    
    def check_safety(self) -> bool:
        """Check if current robot state is safe"""
        if not self.safety_enabled:
            return True
        
        # In practice, this would check real robot state
        # For simulation, we'll return True most of the time
        import random
        return random.random() > 0.01  # 99% safe, 1% unsafe for testing
    
    def emergency_stop(self):
        """Trigger emergency stop"""
        self.emergency_stop = True
        print("EMERGENCY STOP ACTIVATED")

# Example usage
def example_deployment():
    # Create mock interfaces
    class MockRobotInterface:
        def __init__(self):
            self.sensor_noise = 0.0
            self.actuator_noise = 0.0
            self.use_real_controllers_flag = False
        
        def add_sensor_noise(self, noise_level):
            self.sensor_noise = noise_level
        
        def add_actuator_noise(self, noise_level):
            self.actuator_noise = noise_level
        
        def use_real_controllers(self):
            self.use_real_controllers_flag = True
        
        def set_controlled_environment(self):
            print("Set to controlled environment")
        
        def set_unpredictable_environment(self):
            print("Set to unpredictable environment")
        
        def set_real_world_environment(self):
            print("Set to real world environment")
    
    # Create deployment system
    robot_interface = MockRobotInterface()
    safety_system = SafetySystem()
    deployment_manager = DeploymentManager(robot_interface, safety_system)
    
    # Define a simple task function
    def example_task(deployment_stage):
        """Example task that returns success/failure"""
        import random
        
        # Success rate varies by stage (more difficult in later stages)
        stage_success_rates = {
            DeploymentStage.SIMULATION: 0.99,
            DeploymentStage.SIMULATION_WITH_NOISE: 0.95,
            DeploymentStage.SIMULATION_WITH_REAL_CONTROLLERS: 0.90,
            DeploymentStage.PHYSICAL_SIMULATOR: 0.85,
            DeploymentStage.CONTROLLED_ENVIRONMENT: 0.80,
            DeploymentStage.SEMI_CONTROLLED_ENVIRONMENT: 0.75,
            DeploymentStage.FULL_DEPLOYMENT: 0.70
        }
        
        success_rate = stage_success_rates.get(deployment_stage, 0.5)
        success = random.random() < success_rate
        
        return {
            'success': success,
            'stage': deployment_stage.value,
            'sensor_noise': robot_interface.sensor_noise,
            'actuator_noise': robot_interface.actuator_noise
        }
    
    # Run deployment (commented out to avoid long execution)
    # deployment_manager.deploy_system(example_task)
    
    print("Deployment system initialized with gradual testing approach.")
    print("In practice, this would run tests at each stage before advancing.")

example_deployment()
```

## Validation and Evaluation

### Performance Metrics for Real-World Systems

Evaluating deployed systems in real environments:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List, Any
import json
import datetime

class DeploymentEvaluator:
    def __init__(self):
        """
        Evaluate deployed robotic systems in real-world environments
        """
        self.metrics = {
            'task_success_rate': [],
            'execution_time': [],
            'energy_consumption': [],
            'safety_incidents': [],
            'human_intervention': [],
            'robustness_score': [],
            'adaptability_score': [],
            'user_satisfaction': []
        }
        self.raw_data = []
    
    def record_trial(self, trial_data: Dict[str, Any]):
        """
        Record data from a single trial
        
        Args:
            trial_data: Dictionary containing trial results
        """
        self.raw_data.append({
            'timestamp': datetime.datetime.now().isoformat(),
            **trial_data
        })
        
        # Update metrics
        if 'success' in trial_data:
            self.metrics['task_success_rate'].append(trial_data['success'])
        
        if 'execution_time' in trial_data:
            self.metrics['execution_time'].append(trial_data['execution_time'])
        
        if 'energy_used' in trial_data:
            self.metrics['energy_consumption'].append(trial_data['energy_used'])
        
        if 'safety_violation' in trial_data:
            self.metrics['safety_incidents'].append(trial_data['safety_violation'])
        
        if 'human_intervention' in trial_data:
            self.metrics['human_intervention'].append(trial_data['human_intervention'])
    
    def calculate_robustness_score(self, recent_trials: int = 20) -> float:
        """
        Calculate robustness based on recent performance
        
        Args:
            recent_trials: Number of recent trials to consider
            
        Returns:
            Robustness score (0-1)
        """
        if len(self.raw_data) < recent_trials:
            recent_data = self.raw_data
        else:
            recent_data = self.raw_data[-recent_trials:]
        
        if not recent_data:
            return 0.0
        
        # Calculate robustness based on consistency of success
        successes = [trial.get('success', 0) for trial in recent_data]
        success_rate = sum(successes) / len(successes)
        
        # Also consider execution time consistency
        exec_times = [trial.get('execution_time', float('inf')) for trial in recent_data]
        finite_times = [t for t in exec_times if t != float('inf')]
        
        if finite_times:
            time_consistency = 1.0 - (np.std(finite_times) / (np.mean(finite_times) + 1e-6))
            time_consistency = max(0.0, min(1.0, time_consistency))
        else:
            time_consistency = 1.0
        
        # Combine metrics
        robustness = 0.7 * success_rate + 0.3 * time_consistency
        return min(1.0, max(0.0, robustness))
    
    def calculate_adaptability_score(self) -> float:
        """
        Calculate adaptability based on performance changes over time
        
        Returns:
            Adaptability score (0-1)
        """
        if len(self.raw_data) < 10:  # Need sufficient data
            return 0.5  # Neutral score
        
        # Divide data into early and late periods
        mid_point = len(self.raw_data) // 2
        early_data = self.raw_data[:mid_point]
        late_data = self.raw_data[mid_point:]
        
        # Calculate success rates for each period
        early_successes = [trial.get('success', 0) for trial in early_data]
        late_successes = [trial.get('success', 0) for trial in late_data]
        
        early_rate = sum(early_successes) / len(early_successes) if early_successes else 0
        late_rate = sum(late_successes) / len(late_successes) if late_successes else 0
        
        # Adaptability is improvement over time
        if early_rate == 0:
            adaptability = 1.0 if late_rate > 0 else 0.0
        else:
            improvement = (late_rate - early_rate) / early_rate
            adaptability = max(0.0, min(1.0, 0.5 + improvement))  # Center at 0.5
        
        return adaptability
    
    def calculate_comprehensive_score(self) -> Dict[str, float]:
        """
        Calculate comprehensive performance score
        
        Returns:
            Dictionary with various performance scores
        """
        if not self.metrics['task_success_rate']:
            return {'overall_score': 0.0, 'breakdown': {}}
        
        # Calculate individual metrics
        success_rate = np.mean(self.metrics['task_success_rate'])
        
        if self.metrics['execution_time']:
            avg_time = np.mean(self.metrics['execution_time'])
            # Normalize to 0-1 scale (assuming 10 seconds is poor, 1 second is excellent)
            time_score = max(0.0, min(1.0, (10.0 - avg_time) / 9.0))
        else:
            time_score = 0.5  # Neutral if no data
        
        if self.metrics['energy_consumption']:
            avg_energy = np.mean(self.metrics['energy_consumption'])
            # Normalize to 0-1 scale (assuming 100J is poor, 10J is excellent)
            energy_score = max(0.0, min(1.0, (100.0 - avg_energy) / 90.0))
        else:
            energy_score = 0.5  # Neutral if no data
        
        safety_rate = 1.0 - np.mean(self.metrics['safety_incidents']) if self.metrics['safety_incidents'] else 1.0
        intervention_rate = 1.0 - np.mean(self.metrics['human_intervention']) if self.metrics['human_intervention'] else 1.0
        
        robustness_score = self.calculate_robustness_score()
        adaptability_score = self.calculate_adaptability_score()
        
        # Calculate overall score with weighted components
        weights = {
            'success_rate': 0.25,
            'time_efficiency': 0.15,
            'energy_efficiency': 0.15,
            'safety': 0.15,
            'autonomy': 0.10,
            'robustness': 0.10,
            'adaptability': 0.10
        }
        
        overall_score = (
            weights['success_rate'] * success_rate +
            weights['time_efficiency'] * time_score +
            weights['energy_efficiency'] * energy_score +
            weights['safety'] * safety_rate +
            weights['autonomy'] * intervention_rate +
            weights['robustness'] * robustness_score +
            weights['adaptability'] * adaptability_score
        )
        
        return {
            'overall_score': overall_score,
            'breakdown': {
                'success_rate': success_rate,
                'time_efficiency': time_score,
                'energy_efficiency': energy_score,
                'safety': safety_rate,
                'autonomy': intervention_rate,
                'robustness': robustness_score,
                'adaptability': adaptability_score
            },
            'weights': weights
        }
    
    def generate_report(self) -> str:
        """
        Generate a comprehensive evaluation report
        
        Returns:
            Formatted report string
        """
        scores = self.calculate_comprehensive_score()
        
        report = []
        report.append("=" * 60)
        report.append("ROBOTIC SYSTEM DEPLOYMENT EVALUATION REPORT")
        report.append("=" * 60)
        report.append(f"Report Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Total Trials: {len(self.raw_data)}")
        report.append("")
        
        # Overall score
        report.append(f"OVERALL PERFORMANCE SCORE: {scores['overall_score']:.3f}/1.0")
        report.append("-" * 40)
        
        # Breakdown
        report.append("SCORE BREAKDOWN:")
        for metric, score in scores['breakdown'].items():
            weight = scores['weights'][metric]
            report.append(f"  {metric.replace('_', ' ').title():<15}: {score:.3f} (weight: {weight:.2f})")
        
        report.append("")
        
        # Additional metrics
        if self.metrics['execution_time']:
            avg_time = np.mean(self.metrics['execution_time'])
            std_time = np.std(self.metrics['execution_time'])
            report.append(f"EXECUTION TIME: {avg_time:.3f}s ± {std_time:.3f}s")
        
        if self.metrics['energy_consumption']:
            avg_energy = np.mean(self.metrics['energy_consumption'])
            std_energy = np.std(self.metrics['energy_consumption'])
            report.append(f"ENERGY USAGE: {avg_energy:.3f}J ± {std_energy:.3f}J")
        
        if self.metrics['safety_incidents']:
            safety_rate = 1.0 - np.mean(self.metrics['safety_incidents'])
            report.append(f"SAFETY RATE: {safety_rate:.3f}")
        
        if self.metrics['human_intervention']:
            autonomy_rate = 1.0 - np.mean(self.metrics['human_intervention'])
            report.append(f"AUTONOMY RATE: {autonomy_rate:.3f}")
        
        report.append("")
        report.append("RECOMMENDATIONS:")
        
        if scores['overall_score'] < 0.7:
            report.append("  - Performance below acceptable threshold")
            report.append("  - Consider additional training or system modifications")
        elif scores['overall_score'] < 0.85:
            report.append("  - Performance is acceptable but could be improved")
            report.append("  - Monitor closely and consider optimizations")
        else:
            report.append("  - Excellent performance, ready for broader deployment")
        
        if scores['breakdown']['robustness'] < 0.7:
            report.append("  - Robustness needs improvement")
            report.append("  - Consider additional domain randomization or robust control")
        
        if scores['breakdown']['adaptability'] < 0.6:
            report.append("  - Limited adaptability observed")
            report.append("  - Consider implementing online learning capabilities")
        
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def plot_metrics(self):
        """
        Plot performance metrics over time
        """
        if not self.raw_data:
            print("No data available for plotting")
            return
        
        # Convert to DataFrame for easier plotting
        df = pd.DataFrame(self.raw_data)
        df['time'] = pd.to_datetime(df['timestamp'])
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Plot 1: Success rate over time
        if 'success' in df.columns:
            success_rolling = df['success'].rolling(window=10, min_periods=1).mean()
            axes[0, 0].plot(df['time'], df['success'], 'o', alpha=0.3, label='Individual trials')
            axes[0, 0].plot(df['time'], success_rolling, 'b-', linewidth=2, label='Rolling average (10)')
            axes[0, 0].set_title('Task Success Rate Over Time')
            axes[0, 0].set_ylabel('Success Rate')
            axes[0, 0].legend()
            axes[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: Execution time over time
        if 'execution_time' in df.columns:
            time_rolling = df['execution_time'].rolling(window=10, min_periods=1).mean()
            axes[0, 1].plot(df['time'], df['execution_time'], 'o', alpha=0.3, label='Individual trials')
            axes[0, 1].plot(df['time'], time_rolling, 'r-', linewidth=2, label='Rolling average (10)')
            axes[0, 1].set_title('Execution Time Over Time')
            axes[0, 1].set_ylabel('Time (s)')
            axes[0, 1].legend()
            axes[0, 1].grid(True, alpha=0.3)
        
        # Plot 3: Energy consumption over time
        if 'energy_used' in df.columns:
            energy_rolling = df['energy_used'].rolling(window=10, min_periods=1).mean()
            axes[1, 0].plot(df['time'], df['energy_used'], 'o', alpha=0.3, label='Individual trials')
            axes[1, 0].plot(df['time'], energy_rolling, 'g-', linewidth=2, label='Rolling average (10)')
            axes[1, 0].set_title('Energy Consumption Over Time')
            axes[1, 0].set_ylabel('Energy (J)')
            axes[1, 0].legend()
            axes[1, 0].grid(True, alpha=0.3)
        
        # Plot 4: Safety incidents and interventions
        if 'safety_violation' in df.columns and 'human_intervention' in df.columns:
            axes[1, 1].plot(df['time'], df['safety_violation'], 'ro-', label='Safety Violations', alpha=0.7)
            axes[1, 1].plot(df['time'], df['human_intervention'], 'bs-', label='Human Interventions', alpha=0.7)
            axes[1, 1].set_title('Safety Incidents and Human Interventions')
            axes[1, 1].set_ylabel('Count')
            axes[1, 1].legend()
            axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.xticks(rotation=45)
        plt.show()

# Example usage
def example_evaluation():
    evaluator = DeploymentEvaluator()
    
    # Simulate some trial data
    import random
    
    for i in range(50):
        # Simulate performance that improves over time (adaptability)
        base_success_rate = 0.6 + 0.3 * (i / 50)  # Improve from 0.6 to 0.9
        success = random.random() < base_success_rate
        
        trial_data = {
            'success': success,
            'execution_time': random.uniform(2.0, 5.0) if success else random.uniform(5.0, 10.0),
            'energy_used': random.uniform(10, 50) if success else random.uniform(50, 100),
            'safety_violation': random.random() < 0.05,  # 5% safety violation rate
            'human_intervention': random.random() < 0.1 if i < 25 else random.random() < 0.05  # Less intervention as system improves
        }
        
        evaluator.record_trial(trial_data)
    
    # Generate report
    report = evaluator.generate_report()
    print(report)
    
    # Show plots
    evaluator.plot_metrics()

example_evaluation()
```

## Best Practices for Deployment

### 1. Gradual Progression
- Start with pure simulation
- Progress through increasingly realistic environments
- Validate at each stage before advancing
- Maintain rollback capabilities

### 2. Safety First
- Implement multiple layers of safety checks
- Use emergency stop mechanisms
- Monitor continuously during deployment
- Have human operators ready for intervention

### 3. Monitoring and Logging
- Log all system states and decisions
- Monitor performance metrics continuously
- Track error conditions and failures
- Maintain audit trails for debugging

### 4. Robustness Engineering
- Design for worst-case scenarios
- Implement graceful degradation
- Use redundant systems where critical
- Test extensively under stress conditions

## Looking Ahead

This week we covered the critical challenge of sim-to-real transfer and deployment. Next week, we'll conclude our journey with the capstone project, where we'll integrate all the concepts learned throughout the course to create a comprehensive Physical AI system.

## Exercises

1. Implement domain randomization for your robotic system
2. Create a system identifier to calibrate simulation parameters
3. Develop an adaptive controller for handling reality gaps
4. Design a deployment pipeline for your robot
5. Implement evaluation metrics for deployed systems

## Further Reading

- "Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World" by Tobin et al.
- "Sim-to-Real Transfer of Robotic Control with Dynamics Randomization" by Peng et al.
- "Closing the Sim-to-Real Loop: Efficient Low-Level Robot Control with Machine Learning" by Sadeghi and Levine
- "Benchmarking in Unification of Robotics Systems" by Stilman et al.