---
sidebar_position: 11
---

# Week 4: Digital Twins with Gazebo & Unity

Welcome to Week 4 of our Physical AI & Humanoid Robotics journey! This week, we'll explore simulation environments that serve as digital twins for physical robots. Simulation is a cornerstone of Physical AI development, allowing us to test algorithms safely, inexpensively, and repeatably before deploying on real hardware.

## Learning Objectives

By the end of this week, you will be able to:

1. Understand the role of simulation in Physical AI development
2. Create and configure Gazebo simulation environments
3. Develop Unity-based digital twins for robotics
4. Implement realistic physics and sensor models
5. Bridge simulation and reality with sim-to-real transfer techniques
6. Evaluate simulation fidelity and its impact on real-world performance

## The Importance of Simulation in Physical AI

Simulation plays a pivotal role in Physical AI development for several reasons:

### Safety and Risk Mitigation
Physical AI systems operate in the real world, where mistakes can cause damage to expensive hardware, injury to humans, or environmental harm. Simulation provides a safe environment to test novel algorithms and behaviors.

### Cost and Time Efficiency
Physical robots require maintenance, calibration, and repair. Simulation allows rapid iteration without hardware constraints, significantly reducing development time and costs.

### Reproducibility and Control
Real-world conditions vary constantly due to lighting, temperature, wear, and other factors. Simulation provides controlled, repeatable experiments essential for scientific validation.

### Scalability
Multiple simulation instances can run in parallel, enabling large-scale training and testing that would be impossible with physical robots.

## Gazebo: Physics-Based Simulation

Gazebo is a 3D dynamic simulator with accurate physics simulation, realistic rendering, and convenient programmatic interfaces. It's widely used in the robotics community for testing algorithms before deployment on real robots.

### Gazebo Architecture

Gazebo consists of several key components:

- **Physics Engine**: Supports ODE, Bullet, Simbody, and DART for accurate physics simulation
- **Rendering Engine**: Uses OGRE for high-quality 3D rendering
- **Sensor Simulation**: Models cameras, LiDAR, IMUs, GPS, and other sensors
- **Plugin System**: Extensible architecture for custom models and controllers
- **Transport Layer**: Lightweight messaging system for inter-process communication

### Installing and Running Gazebo

Gazebo Garden is the recommended version for ROS 2 Humble:

```bash
# Install Gazebo Garden
sudo apt-get install ros-humble-gazebo-ros-pkgs ros-humble-gazebo-plugins ros-humble-gazebo-dev

# Launch Gazebo with an empty world
gz sim -r empty.sdf
```

### Creating Gazebo Worlds

Gazebo worlds are defined using SDF (Simulation Description Format) files. Here's a basic example:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="small_room">
    <!-- Include a model from Fuel (online model database) -->
    <include>
      <uri>https://fuel.gazebosim.org/1.0/openrobotics/models/ground plane</uri>
    </include>
    
    <!-- Add a simple box obstacle -->
    <model name="box_obstacle">
      <pose>2 0 0.5 0 0 0</pose>
      <link name="link">
        <pose>0 0 0 0 0 0</pose>
        <collision name="collision">
          <geometry>
            <box>
              <size>1 1 1</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>1 1 1</size>
            </box>
          </geometry>
          <material>
            <ambient>0.5 0.5 0.5 1</ambient>
            <diffuse>0.8 0.8 0.8 1</diffuse>
          </material>
        </visual>
        <inertial>
          <mass>1.0</mass>
          <inertia>
            <ixx>0.166667</ixx>
            <ixy>0</ixy>
            <ixz>0</ixz>
            <iyy>0.166667</iyy>
            <iyz>0</iyz>
            <izz>0.166667</izz>
          </inertia>
        </inertial>
      </link>
    </model>
    
    <!-- Lighting -->
    <light name="sun" type="directional">
      <cast_shadows>true</cast_shadows>
      <pose>0 0 10 0 0 0</pose>
      <diffuse>0.8 0.8 0.8 1</diffuse>
      <specular>0.2 0.2 0.2 1</specular>
      <attenuation>
        <range>1000</range>
        <constant>0.9</constant>
        <linear>0.01</linear>
        <quadratic>0.001</quadratic>
      </attenuation>
      <direction>-0.5 0.1 -0.9</direction>
    </light>
  </world>
</sdf>
```

### Integrating Robots with Gazebo

To use your URDF robot model in Gazebo, you need to add Gazebo-specific plugins and configurations:

```xml
<?xml version="1.0"?>
<robot name="gazebo_robot" xmlns:xacro="http://www.ros.org/wiki/xacro">
  <!-- Include your URDF model here -->
  
  <!-- Gazebo-specific configurations -->
  <gazebo>
    <plugin filename="libgazebo_ros2_control.so" name="gazebo_ros2_control">
      <parameters>$(find my_robot_description)/config/my_controllers.yaml</parameters>
    </plugin>
  </gazebo>
  
  <!-- Link-specific Gazebo configurations -->
  <gazebo reference="base_link">
    <material>Gazebo/Green</material>
    <mu1>0.2</mu1>
    <mu2>0.2</mu2>
  </gazebo>
  
  <!-- Wheel links with friction settings -->
  <gazebo reference="left_wheel">
    <mu1>1.0</mu1>
    <mu2>1.0</mu2>
    <kp>1000000.0</kp>
    <kd>100.0</kd>
    <fdir1>1 0 0</fdir1>
  </gazebo>
  
  <gazebo reference="right_wheel">
    <mu1>1.0</mu1>
    <mu2>1.0</mu2>
    <kp>1000000.0</kp>
    <kd>100.0</kd>
    <fdir1>1 0 0</fdir1>
  </gazebo>
  
  <!-- Camera sensor plugin -->
  <gazebo reference="camera_link">
    <sensor name="camera" type="camera">
      <always_on>true</always_on>
      <update_rate>30</update_rate>
      <camera name="head">
        <horizontal_fov>1.3962634</horizontal_fov>
        <image>
          <width>640</width>
          <height>480</height>
          <format>R8G8B8</format>
        </image>
        <clip>
          <near>0.1</near>
          <far>100</far>
        </clip>
      </camera>
      <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
        <frame_name>camera_optical_frame</frame_name>
        <min_depth>0.1</min_depth>
        <max_depth>100</max_depth>
      </plugin>
    </sensor>
  </gazebo>
  
  <!-- LiDAR sensor plugin -->
  <gazebo reference="lidar_link">
    <sensor name="lidar" type="gpu_lidar">
      <always_on>true</always_on>
      <visualize>true</visualize>
      <update_rate>10</update_rate>
      <ray>
        <scan>
          <horizontal>
            <samples>360</samples>
            <resolution>1</resolution>
            <min_angle>-3.14159</min_angle>
            <max_angle>3.14159</max_angle>
          </horizontal>
        </scan>
        <range>
          <min>0.1</min>
          <max>30.0</max>
          <resolution>0.01</resolution>
        </range>
      </ray>
      <plugin name="gazebo_ros_lidar" filename="libgazebo_ros_gpu_lidar.so">
        <frame_name>lidar_frame</frame_name>
      </plugin>
    </sensor>
  </gazebo>
</robot>
```

### Launching Robots in Gazebo

Create a launch file to spawn your robot in Gazebo:

```python
# launch/robot_spawn.launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # Get the package share directory
    pkg_share = get_package_share_directory('my_robot_description')
    
    # Declare launch arguments
    model_arg = DeclareLaunchArgument(
        name='model',
        default_value=os.path.join(pkg_share, 'urdf', 'my_robot.urdf.xacro'),
        description='Absolute path to robot urdf file'
    )
    
    robot_description = ParameterValue(
        Command(['xacro ', LaunchConfiguration('model')]),
        value_type=str
    )
    
    # Robot State Publisher node
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}]
    )
    
    # Spawn entity in Gazebo
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description',
                  '-entity', 'my_robot'],
        output='screen'
    )
    
    # Gazebo server and client
    gzserver = Node(
        package='gz_sim',
        executable='gz_sim',
        arguments=['-r', 'empty.sdf'],
        output='screen'
    )
    
    gzclient = Node(
        package='gz_sim',
        executable='gz_sim',
        arguments=['-g'],
        output='screen'
    )
    
    return LaunchDescription([
        model_arg,
        gzserver,
        gzclient,
        robot_state_publisher,
        spawn_entity
    ])
```

## Unity for Robotics: High-Fidelity Digital Twins

Unity provides a powerful platform for creating high-fidelity digital twins with photorealistic rendering and advanced physics simulation. The Unity Robotics Hub offers tools specifically designed for robotics applications.

### Unity Robotics Simulation Features

Unity excels in several areas for robotics simulation:

- **Photorealistic Rendering**: High-quality visuals for training perception systems
- **Flexible Physics**: Advanced physics engine for complex interactions
- **Large Environments**: Ability to create vast, detailed worlds
- **Real-time Raycasting**: Efficient sensor simulation
- **XR Support**: Virtual and augmented reality integration

### Setting Up Unity for Robotics

Unity Robotics requires several components:

1. **Unity Editor**: Latest LTS version with required packages
2. **Unity Robotics Hub**: Collection of tools and samples
3. **ROS.NET or Unity ROS TCP Connector**: For ROS communication
4. **Robot Framework**: Like ML-Agents for reinforcement learning

### Unity-Rosbridge Integration

Unity can communicate with ROS through rosbridge:

```csharp
using UnityEngine;
using RosSharp.RosBridgeClient;

public class UnityRobotController : MonoBehaviour
{
    private RosSocket rosSocket;
    
    void Start()
    {
        // Connect to ROS bridge
        WebSocketNativeClient webSocket = new WebSocketNativeClient("ws://localhost:9090");
        rosSocket = new RosSocket(webSocket);
        
        // Subscribe to robot joint states
        rosSocket.Subscribe<sensor_msgs.JointState>(
            "/joint_states", 
            ReceiveJointStates);
    }
    
    void ReceiveJointStates(sensor_msgs.JointState jointState)
    {
        // Update Unity robot model based on joint states
        for (int i = 0; i < jointState.name.Count; i++)
        {
            string jointName = jointState.name[i];
            float jointPosition = (float)jointState.position[i];
            
            // Find and update the corresponding joint in Unity
            Transform jointTransform = transform.Find(jointName);
            if (jointTransform != null)
            {
                // Apply joint position to Unity transform
                // This depends on your robot model structure
            }
        }
    }
    
    void Update()
    {
        // Send robot state back to ROS
        SendRobotState();
    }
    
    void SendRobotState()
    {
        // Publish current robot state to ROS
        sensor_msgs.JointState jointState = new sensor_msgs.JointState();
        // Populate joint state message
        rosSocket.Publish("/unity_joint_states", jointState);
    }
}
```

### Unity Perception Package

Unity's Perception package enables synthetic data generation for training AI models:

```csharp
using UnityEngine;
using Unity.Perception.GroundTruth;
using Unity.Perception.Randomization;

public class PerceptionCamera : MonoBehaviour
{
    [SerializeField] Camera m_Camera;
    [SerializeField] GameObject m_SegmentationLabeler;
    
    void Start()
    {
        // Configure camera for data collection
        var datasetCapture = m_Camera.gameObject.AddComponent<DatasetCapture>();
        datasetCapture.capturePeriod = 1.0f; // Capture every second
        
        // Add segmentation labeler
        var labeler = m_SegmentationLabeler.AddComponent<SegmentationLabeler>();
        
        // Configure annotation settings
        var annotationManager = FindObjectOfType<AnnotationManager>();
        annotationManager.annotationDefinitions.Add(new AnnotationDefinition());
    }
}
```

## Simulation Fidelity and the Reality Gap

One of the biggest challenges in simulation is achieving sufficient fidelity to ensure that behaviors learned in simulation transfer effectively to the real world.

### Sources of the Reality Gap

1. **Visual Differences**: Lighting, textures, and rendering differences
2. **Physics Approximations**: Simplified physics models in simulation
3. **Sensor Noise**: Different noise characteristics between simulated and real sensors
4. **Actuator Dynamics**: Differences in motor response and control precision
5. **Environmental Factors**: Unmodeled aspects of the real world

### Domain Randomization

Domain randomization is a technique to improve sim-to-real transfer by randomizing various aspects of the simulation:

```python
# Example of domain randomization in simulation
import random

class DomainRandomizer:
    def __init__(self):
        self.lighting_conditions = [
            {'intensity': (0.5, 1.5), 'color': ('warm', 'cool', 'neutral')}
        ]
        self.material_properties = [
            {'friction': (0.1, 0.9), 'restitution': (0.0, 0.5)}
        ]
        self.object_appearances = [
            {'texture': 'random', 'color': 'random', 'size': (0.8, 1.2)}
        ]
    
    def randomize_lighting(self):
        # Randomize lighting conditions
        intensity = random.uniform(0.5, 1.5)
        # Apply to simulation environment
        pass
    
    def randomize_physics(self):
        # Randomize physics properties
        friction = random.uniform(0.1, 0.9)
        restitution = random.uniform(0.0, 0.5)
        # Apply to simulation objects
        pass
    
    def randomize_objects(self):
        # Randomize object appearances and properties
        for obj in self.simulation_objects:
            scale_factor = random.uniform(0.8, 1.2)
            # Apply randomization to object
            pass
```

### System Identification and Model Correction

Improving simulation fidelity through system identification:

```python
import numpy as np
from scipy.optimize import minimize

class SimulatorCalibrator:
    def __init__(self, robot_model):
        self.robot_model = robot_model
        self.sim_params = {}  # Parameters to calibrate
        self.real_data = []   # Collected real-world data
        self.sim_data = []    # Corresponding simulation data
    
    def collect_data_pairs(self):
        # Collect matched pairs of real and simulated behavior
        # This involves running the same trajectories on both
        # real robot and simulation
        pass
    
    def objective_function(self, params):
        # Calculate difference between real and simulated behavior
        # with given parameters
        self.update_simulation_params(params)
        
        sim_trajectory = self.run_simulation()
        error = np.mean((self.real_trajectory - sim_trajectory) ** 2)
        return error
    
    def calibrate(self):
        # Optimize simulation parameters to match real behavior
        initial_params = list(self.sim_params.values())
        result = minimize(self.objective_function, initial_params)
        
        # Update simulation with optimized parameters
        self.sim_params = dict(zip(self.sim_params.keys(), result.x))
        return self.sim_params
```

## Best Practices for Simulation in Physical AI

### 1. Progressive Fidelity

Start with simple simulations and gradually increase complexity:

1. **Kinematic simulation**: Focus on motion planning without physics
2. **Simple dynamics**: Add basic physics without complex contacts
3. **Complex contacts**: Include friction, collisions, and deformations
4. **High-fidelity sensors**: Accurate sensor models with noise
5. **Environment complexity**: Detailed environments with many objects

### 2. Validation Against Reality

Regularly validate simulation results against real-world data:

- Compare robot trajectories in simulation vs reality
- Validate sensor outputs (images, LiDAR scans, etc.)
- Test control algorithms in both domains
- Measure performance metrics consistently

### 3. Modularity and Reusability

Structure your simulation environments to be modular:

- Create reusable world components
- Parameterize environments for different scenarios
- Use version control for simulation assets
- Document simulation assumptions and limitations

### 4. Performance Optimization

Balance simulation fidelity with performance:

- Use simplified collision meshes where possible
- Adjust physics update rates appropriately
- Optimize rendering settings for training vs visualization
- Use parallel simulation instances for data generation

## Simulation Tools and Libraries

### Gazebo Extensions
- **Ignition Gazebo**: Modern, modular version of Gazebo
- **Gazebo ROS Packages**: ROS 2 integration
- **Gazebo Garden**: Latest version with enhanced features

### Unity Extensions
- **Unity Robotics Hub**: Tools for robotics simulation
- **ML-Agents**: Reinforcement learning framework
- **Perception Package**: Synthetic data generation
- **XR Packages**: Virtual and augmented reality support

### Specialized Simulation Platforms
- **PyBullet**: Python-based physics simulation
- **MuJoCo**: High-fidelity physics engine
- **Webots**: General-purpose robot simulator
- **AirSim**: Microsoft's simulator for drones and cars

## Looking Ahead

This week we explored simulation environments that serve as digital twins for Physical AI systems. Next week, we'll dive into NVIDIA Isaac, which provides GPU-accelerated perception and manipulation capabilities that are essential for modern Physical AI applications.

## Exercises

1. Create a Gazebo world with multiple obstacles and spawn your robot model
2. Implement a simple navigation task in simulation using ROS 2 and Nav2
3. Set up a basic Unity scene with a robot model and ROS communication
4. Experiment with domain randomization techniques to improve sim-to-real transfer
5. Compare sensor data from simulation vs real hardware and quantify differences

## Further Reading

- Gazebo Documentation: http://gazebosim.org/
- Unity Robotics Blog: https://blogs.unity3d.com/robotics/
- ROS 2 with Gazebo: https://github.com/ros-simulation/gazebo_ros_pkgs
- NVIDIA Isaac Sim: https://developer.nvidia.com/isaac-sim