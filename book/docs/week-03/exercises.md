---
sidebar_position: 10
---

# Week 3 Exercises: URDF Modeling and TF Transforms

This exercise sheet accompanies the Week 3 lessons on URDF modeling and TF transforms. These exercises will help you practice and reinforce your understanding of robot modeling and coordinate transformations in the context of Physical AI systems.

## Exercise 1: Create a Simple Mobile Robot Model

Create a URDF model of a differential drive mobile robot with the following specifications:

### Requirements:
- Rectangular base (0.4m x 0.3m x 0.1m)
- Two cylindrical wheels (radius 0.05m, width 0.02m)
- One spherical caster wheel (radius 0.03m)
- Proper joint definitions with appropriate limits
- Visual and collision properties for all links
- Inertial properties for dynamic simulation

### Steps:
1. Create the URDF file with all required links and joints
2. Validate the URDF using `check_urdf`
3. Visualize the robot in RViz
4. Load the robot into Gazebo and test basic movement

### Solution Template:

```xml
<?xml version="1.0"?>
<robot name="mobile_robot">
  <!-- Base link -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.4 0.3 0.1"/>
      </geometry>
      <material name="light_gray">
        <color rgba="0.7 0.7 0.7 1.0"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.4 0.3 0.1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="5.0"/>
      <inertia ixx="0.2" ixy="0.0" ixz="0.0" iyy="0.3" iyz="0.0" izz="0.4"/>
    </inertial>
  </link>

  <!-- Add wheel links and joints here -->
  
</robot>
```

## Exercise 2: Create a Robotic Arm with Xacro

Using Xacro, create a 6-DOF robotic arm model with the following specifications:

### Requirements:
- Use Xacro macros to reduce redundancy
- Include at least 6 revolute joints
- Add a simple gripper mechanism
- Define appropriate link lengths and joint limits
- Include proper inertial properties

### Solution Template:

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="arm_robot">

  <!-- Define constants -->
  <xacro:property name="M_PI" value="3.14159265359"/>
  <xacro:property name="link_length" value="0.2"/>
  <xacro:property name="link_radius" value="0.05"/>
  
  <!-- Define a macro for arm segments -->
  <xacro:macro name="arm_segment" params="prefix joint_name parent_link xyz rpy joint_limits">
    <!-- Define link -->
    <link name="${prefix}_link">
      <visual>
        <geometry>
          <cylinder radius="${link_radius}" length="${link_length}"/>
        </geometry>
        <origin xyz="0 0 ${link_length/2}" rpy="0 0 0"/>
        <material name="gray">
          <color rgba="0.5 0.5 0.5 1"/>
        </material>
      </visual>
      <collision>
        <geometry>
          <cylinder radius="${link_radius}" length="${link_length}"/>
        </geometry>
        <origin xyz="0 0 ${link_length/2}" rpy="0 0 0"/>
      </collision>
      <inertial>
        <mass value="1.0"/>
        <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.01"/>
      </inertial>
    </link>
    
    <!-- Define joint -->
    <joint name="${joint_name}" type="revolute">
      <parent link="${parent_link}"/>
      <child link="${prefix}_link"/>
      <origin xyz="${xyz}" rpy="${rpy}"/>
      <axis xyz="0 0 1"/>
      <limit lower="${joint_limits[0]}" upper="${joint_limits[1]}" effort="100" velocity="1"/>
    </joint>
  </xacro:macro>

  <!-- Base link -->
  <link name="base_link">
    <visual>
      <geometry>
        <cylinder radius="0.1" length="0.1"/>
      </geometry>
      <material name="dark_gray">
        <color rgba="0.3 0.3 0.3 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.1" length="0.1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="2.0"/>
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.02"/>
    </inertial>
  </link>

  <!-- Use the macro to create arm segments -->
  <!-- Add your arm segments here using the macro -->

</robot>
```

## Exercise 3: TF Transform Practice

Create a ROS 2 node that demonstrates TF transforms between multiple coordinate frames:

### Requirements:
- Create a node that broadcasts transforms between at least 4 coordinate frames
- Implement a transform listener that receives transforms
- Transform a point from one frame to another
- Visualize the frames in RViz

### Solution Template:

```python
import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster, TransformListener, Buffer
from geometry_msgs.msg import TransformStamped, PointStamped
from tf2_geometry_msgs import do_transform_point
import math

class TFExerciseNode(Node):
    def __init__(self):
        super().__init__('tf_exercise_node')
        
        # Create transform broadcaster
        self.tf_broadcaster = TransformBroadcaster(self)
        
        # Create TF buffer and listener
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        
        # Create publisher for transformed points
        self.point_pub = self.create_publisher(PointStamped, 'transformed_point', 10)
        
        # Timer to broadcast transforms
        self.timer = self.create_timer(0.1, self.broadcast_transforms)
        
    def broadcast_transforms(self):
        # Create and broadcast multiple transforms
        # Frame hierarchy: world -> robot_base -> sensor_frame
        t1 = TransformStamped()
        t1.header.stamp = self.get_clock().now().to_msg()
        t1.header.frame_id = 'world'
        t1.child_frame_id = 'robot_base'
        t1.transform.translation.x = 1.0
        t1.transform.translation.y = 0.0
        t1.transform.translation.z = 0.0
        t1.transform.rotation.w = 1.0
        
        # Add more transforms here...
        
        self.tf_broadcaster.sendTransform([t1])  # Add other transforms to the list

def main(args=None):
    rclpy.init(args=args)
    node = TFExerciseNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Exercise 4: Sensor Data Transformation

Create a node that transforms sensor data from a robot's sensor frame to the world frame:

### Requirements:
- Subscribe to a simulated sensor topic (e.g., LaserScan or PointCloud2)
- Use TF to transform sensor data to the world frame
- Publish the transformed data
- Visualize both original and transformed data in RViz

### Implementation Notes:
- Use the `tf2_sensor_msgs` package for transforming sensor data
- Handle potential transform exceptions gracefully
- Consider the timing of sensor data and transforms

## Exercise 5: Robot with Sensors in URDF

Extend your mobile robot model from Exercise 1 to include sensors:

### Requirements:
- Add a camera sensor to the robot (define optical frame)
- Add a LiDAR sensor to the robot
- Include appropriate Gazebo plugins for simulation
- Define proper mounting positions and orientations for sensors
- Validate that the model works in Gazebo

### Gazebo Plugin Example:
```xml
<gazebo reference="camera_link">
  <sensor type="camera" name="camera_sensor">
    <update_rate>30.0</update_rate>
    <camera name="head">
      <horizontal_fov>1.3962634</horizontal_fov>
      <image>
        <width>800</width>
        <height>800</height>
        <format>R8G8B8</format>
      </image>
      <clip>
        <near>0.02</near>
        <far>300</far>
      </clip>
    </camera>
    <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
      <frame_name>camera_optical_frame</frame_name>
    </plugin>
  </sensor>
</gazebo>
```

## Exercise 6: Physical AI Scenario - Object Detection and Manipulation

Combine URDF and TF concepts to create a scenario where a robot detects an object and plans to manipulate it:

### Requirements:
- Create a URDF model of a mobile manipulator (mobile base + robotic arm)
- Implement TF to transform detected object positions to the robot's base frame
- Plan a manipulation trajectory to reach the object
- Use MoveIt! for motion planning if available

### Implementation Steps:
1. Create the URDF model with both mobile base and manipulator
2. Implement a node that simulates object detection in camera frame
3. Transform the object position to the robot's base frame
4. Plan a trajectory to reach the object
5. Visualize the planned trajectory in RViz

## Challenge Exercise: Humanoid Robot Model

Create a simplified humanoid robot model with the following specifications:

### Requirements:
- Robot with torso, head, arms, and legs
- At least 12 joints (6 per leg, 6 per arm, 1 for head yaw)
- Proper kinematic chain for walking (consider simplified model)
- Include sensors (IMU in torso, cameras in head)
- Use Xacro to organize the complex model
- Validate the model and visualize in RViz

### Additional Requirements:
- Implement a walking gait pattern using coordinated joint movements
- Show how TF would be used to maintain balance based on IMU data
- Demonstrate how sensor data from different parts of the body would be transformed to a common frame

## Submission Requirements

For each exercise, submit:
1. URDF/Xacro files
2. Python/C++ source code for TF nodes
3. Launch files to run your examples
4. Screenshots of RViz visualization
5. Brief documentation explaining your implementation
6. Any configuration files needed

## Evaluation Criteria

- Correct URDF syntax and structure
- Proper use of Xacro macros and properties
- Accurate TF transforms between frames
- Effective use of visual, collision, and inertial properties
- Integration of sensors in robot models
- Proper error handling in TF operations
- Creativity in solving the challenge exercise

## Resources

- URDF/XML Format Documentation: http://wiki.ros.org/urdf/XML
- Xacro Tutorial: http://wiki.ros.org/xacro
- TF2 Tutorials: http://wiki.ros.org/tf2/Tutorials
- Robot Modeling with URDF: http://gazebosim.org/tutorials/?tut=ros_urdf