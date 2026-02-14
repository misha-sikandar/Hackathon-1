# Week 4: Simulation with Gazebo & Unity

This week, we'll explore simulation environments that are essential for developing and testing Physical AI systems. Simulation allows us to safely test algorithms, validate designs, and train AI systems before deploying on real hardware.

## Learning Objectives

By the end of this week, you will be able to:

1. Set up and configure Gazebo simulation environments
2. Create custom simulation worlds and models
3. Integrate Unity with robotics workflows
4. Implement sensor simulation and physics modeling
5. Bridge simulation and reality for transfer learning
6. Evaluate simulation fidelity and effectiveness

## Introduction to Simulation in Physical AI

Simulation is a cornerstone of Physical AI development for several reasons:

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
          <far>300</far>
        </clip>
      </camera>
      <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
        <frame_name>camera_optical_frame</frame_name>
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

## Unity for Robotics Simulation

Unity provides a powerful platform for creating high-fidelity simulation environments with photorealistic rendering and advanced physics simulation.

### Unity Robotics Hub

The Unity Robotics Hub provides tools specifically designed for robotics applications:

- **Unity ML-Agents**: Framework for reinforcement learning
- **Unity Perception**: Tools for synthetic data generation
- **ROS#**: ROS communication for Unity
- **Robot Framework**: Templates and examples for robotics simulation

### Setting Up Unity for Robotics

Unity Robotics requires several components:

1. **Unity Editor**: Latest LTS version with required packages
2. **Unity Robotics Hub**: Collection of tools and samples
3. **ROS.NET or Unity ROS TCP Connector**: For ROS communication
4. **Robot Framework**: Like ML-Agents for reinforcement learning

### Unity-ROS Integration

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
import random
import numpy as np

class DomainRandomizer:
    def __init__(self):
        """
        Randomize simulation parameters to improve sim-to-real transfer
        """
        self.randomization_params = {
            'lighting': {
                'intensity_range': (0.5, 1.5),
                'color_range': (0.8, 1.2)
            },
            'physics': {
                'friction_range': (0.1, 0.9),
                'restitution_range': (0.0, 0.5),
                'mass_multiplier_range': (0.8, 1.2)
            },
            'materials': {
                'color_variation': (0.0, 0.2),
                'texture_options': ['wood', 'metal', 'plastic', 'fabric']
            }
        }
    
    def randomize_lighting(self):
        """Randomize lighting conditions"""
        intensity = random.uniform(*self.randomization_params['lighting']['intensity_range'])
        color_variation = random.uniform(*self.randomization_params['lighting']['color_range'])
        return {
            'intensity': intensity,
            'color_variation': color_variation
        }
    
    def randomize_physics(self):
        """Randomize physics properties"""
        friction = random.uniform(*self.randomization_params['physics']['friction_range'])
        restitution = random.uniform(*self.randomization_params['physics']['restitution_range'])
        mass_mult = random.uniform(*self.randomization_params['physics']['mass_multiplier_range'])
        return {
            'friction': friction,
            'restitution': restitution,
            'mass_multiplier': mass_mult
        }
    
    def randomize_materials(self):
        """Randomize material properties"""
        color_var = random.uniform(*self.randomization_params['materials']['color_variation'])
        texture = random.choice(self.randomization_params['materials']['texture_options'])
        return {
            'color_variation': color_var,
            'texture': texture
        }
    
    def apply_randomization(self, simulation_environment):
        """Apply randomization to simulation environment"""
        lighting_params = self.randomize_lighting()
        physics_params = self.randomize_physics()
        material_params = self.randomize_materials()
        
        # Apply to simulation (implementation depends on specific simulator)
        simulation_environment.set_lighting(lighting_params)
        simulation_environment.set_physics(physics_params)
        simulation_environment.set_materials(material_params)
        
        return {
            'lighting': lighting_params,
            'physics': physics_params,
            'materials': material_params
        }
```

## Unity Perception Package

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

## Best Practices for Simulation

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

## Looking Ahead

This week we explored simulation environments that serve as digital twins for Physical AI systems. Next week, we'll dive into NVIDIA Isaac, which provides GPU-accelerated perception and manipulation capabilities.

## Exercises

1. Create a Gazebo world with multiple obstacles and spawn your robot model
2. Implement a simple navigation task in simulation using ROS 2 and Nav2
3. Set up a basic Unity scene with a robot model and ROS communication
4. Experiment with domain randomization techniques to improve sim-to-real transfer
5. Compare sensor data from simulation vs real hardware and quantify differences

## Further Reading

- Gazebo Documentation: http://gazebosim.org/
- Unity Robotics Hub: https://github.com/Unity-Technologies/Unity-Robotics-Hub
- ROS 2 with Gazebo: https://github.com/ros-simulation/gazebo_ros_pkgs
- NVIDIA Isaac Sim: https://developer.nvidia.com/isaac-sim