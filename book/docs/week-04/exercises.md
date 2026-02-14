---
sidebar_position: 13
---

# Week 4 Exercises: Simulation with Gazebo & Unity

This exercise sheet accompanies the Week 4 lessons on simulation environments for Physical AI systems. These exercises will help you practice and reinforce your understanding of Gazebo and Unity for creating digital twins.

## Exercise 1: Gazebo World Creation

Create a complex Gazebo world with multiple elements:

### Requirements:
- Create a custom world file (.sdf) with at least 5 different objects
- Include static obstacles and dynamic objects
- Add lighting with shadows
- Include a ground plane with custom texture
- Spawn your robot model in the world
- Test the world by launching it in Gazebo

### Steps:
1. Create a new world file in `~/.gazebo/worlds/` or your package
2. Define the world with the required elements
3. Add your robot model to the world
4. Launch the world using `gz sim -r your_world.sdf`
5. Test robot navigation in the environment

### Template for World File:
```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="exercise_world">
    <!-- Add your world elements here -->
    
    <!-- Ground plane -->
    <include>
      <uri>model://ground_plane</uri>
    </include>
    
    <!-- Sun light -->
    <include>
      <uri>model://sun</uri>
    </include>
    
    <!-- Add your custom objects -->
    
  </world>
</sdf>
```

## Exercise 2: Robot Model Integration in Gazebo

Enhance your robot model from Week 3 to work in Gazebo:

### Requirements:
- Add Gazebo-specific plugins for ROS 2 control
- Include sensor models (camera, LiDAR, IMU)
- Configure physics properties (friction, damping)
- Add visual and collision properties
- Test the model in simulation

### Gazebo Plugins to Include:
- `libgazebo_ros2_control.so` for joint control
- Sensor plugins for your specific sensors
- Material definitions for visual appearance

### Implementation Steps:
1. Modify your URDF/Xacro file to include Gazebo sections
2. Add ros2_control configuration files
3. Create a launch file to spawn the robot in Gazebo
4. Test joint control and sensor data publishing

## Exercise 3: Unity Robot Model Setup

Set up your robot model in Unity:

### Requirements:
- Import your robot model into Unity
- Set up the joint hierarchy correctly
- Configure Articulation Bodies for physics simulation
- Create a simple controller to move the robot
- Export or document the Unity scene

### Implementation Steps:
1. Import your robot model (STL/OBJ/FBX) into Unity
2. Organize the model hierarchy to match your URDF
3. Add Articulation Body components to joints
4. Configure joint limits and drive parameters
5. Create a simple script to control the robot

### Unity Robot Controller Template:
```csharp
using UnityEngine;

public class RobotController : MonoBehaviour
{
    public Transform[] joints; // Assign in inspector
    public float[] jointAngles; // Current joint angles
    public float speed = 1.0f;
    
    void Start()
    {
        jointAngles = new float[joints.Length];
    }
    
    void Update()
    {
        // Update joint positions based on jointAngles
        for (int i = 0; i < joints.Length; i++)
        {
            // Apply joint angle to transform
            joints[i].localRotation = Quaternion.Euler(0, 0, jointAngles[i]);
        }
    }
    
    // Method to set joint angles from external source (e.g., ROS)
    public void SetJointAngles(float[] newAngles)
    {
        if (newAngles.Length == jointAngles.Length)
        {
            jointAngles = newAngles;
        }
    }
}
```

## Exercise 4: Unity-ROS Communication

Establish communication between Unity and ROS:

### Requirements:
- Set up rosbridge server
- Create Unity script to connect to ROS
- Subscribe to joint states topic
- Publish sensor data from Unity
- Test the communication with a ROS node

### Implementation Steps:
1. Install and run rosbridge_suite
2. Create Unity script using RosSharp
3. Subscribe to `/joint_states` topic
4. Publish simulated sensor data (e.g., `/unity_camera/image_raw`)
5. Create a ROS node to verify communication

### Unity-ROS Connection Template:
```csharp
using UnityEngine;
using RosSharp.RosBridgeClient;

public class UnityRosInterface : MonoBehaviour
{
    [Header("Connection Settings")]
    public string rosBridgeServerUrl = "ws://localhost:9090";
    
    private RosSocket rosSocket;
    
    void Start()
    {
        ConnectToRos();
    }
    
    void ConnectToRos()
    {
        WebSocketNativeClient webSocket = new WebSocketNativeClient(rosBridgeServerUrl);
        rosSocket = new RosSocket(webSocket);
        
        // Subscribe to joint states
        rosSocket.Subscribe<RosSharp.Messages.Sensor_msgs.JointState>(
            "/joint_states", 
            OnJointStatesReceived);
    }
    
    void OnJointStatesReceived(RosSharp.Messages.Sensor_msgs.JointState jointState)
    {
        // Process joint states and update Unity robot
    }
    
    void OnDestroy()
    {
        rosSocket?.Close();
    }
}
```

## Exercise 5: Sensor Simulation in Both Platforms

Implement sensor simulation in both Gazebo and Unity:

### Requirements:
- Create camera sensor in Gazebo with plugin
- Create camera sensor in Unity with custom script
- Implement LiDAR simulation in both platforms
- Compare sensor outputs between platforms
- Document similarities and differences

### Gazebo Camera Plugin Example:
```xml
<gazebo reference="camera_link">
  <sensor name="camera" type="camera">
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
    </plugin>
  </sensor>
</gazebo>
```

## Exercise 6: Domain Randomization

Implement domain randomization in your simulation:

### Requirements:
- Create a system to randomize lighting conditions
- Randomize material properties (color, texture, reflectance)
- Randomize object positions and orientations
- Implement a mechanism to trigger randomization
- Document the effect on sensor data

### Implementation Steps:
1. Create scripts/components for randomization
2. Implement randomization for different aspects
3. Test the randomization system
4. Analyze the impact on sensor data

## Exercise 7: Simulation-to-Reality Transfer

Explore sim-to-real transfer techniques:

### Requirements:
- Identify key differences between simulation and reality
- Implement system identification to calibrate simulation
- Apply domain randomization to improve transfer
- Document the challenges and solutions

### Implementation Steps:
1. Compare sensor data from simulation vs reality
2. Identify discrepancies in dynamics or sensing
3. Implement calibration techniques
4. Test control policies trained in simulation on real hardware (if available)

## Exercise 8: Unity Perception Pipeline

Set up Unity's perception pipeline for synthetic data generation:

### Requirements:
- Install Unity Perception package
- Configure RGB, depth, and segmentation capture
- Set up annotation definitions
- Generate sample dataset
- Evaluate the quality of generated data

### Implementation Steps:
1. Import Unity Perception package
2. Add DatasetCapture component to camera
3. Configure annotation definitions
4. Add SegmentationLabeler components to objects
5. Run simulation to generate dataset

## Challenge Exercise: Complete Digital Twin System

Create a complete digital twin system that includes:

### Requirements:
- Robot model working in both Gazebo and Unity
- Complete sensor suite simulation
- Real-time synchronization between platforms
- Control interface that works with both simulators
- Performance comparison between platforms

### Additional Requirements:
- Implement a scenario where the same control algorithm works in both simulators
- Document the pros and cons of each platform
- Propose when to use each platform for different Physical AI tasks

## Submission Requirements

For each exercise, submit:
1. Configuration files (URDF, SDF, Unity scenes)
2. Source code for custom plugins/scripts
3. Launch files for Gazebo integration
4. Screenshots of simulation results
5. Documentation of findings and challenges
6. Performance comparisons where applicable

## Evaluation Criteria

- Correct implementation of simulation environments
- Proper integration of robot models
- Effective sensor simulation
- Quality of Unity-ROS communication
- Understanding of domain randomization
- Analysis of sim-to-real transfer challenges
- Creativity in solving the challenge exercise

## Resources

- Gazebo Tutorials: http://gazebosim.org/tutorials
- Unity Robotics Hub: https://github.com/Unity-Technologies/Unity-Robotics-Hub
- ROS-Unity Integration: https://github.com/Unity-Technologies/Unity-Robotics-Helpers
- Unity Perception: https://docs.unity3d.com/Packages/com.unity.perception@latest