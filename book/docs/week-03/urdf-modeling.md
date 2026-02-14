---
sidebar_position: 8
---

# Week 3: Robot Modeling with URDF

Welcome to Week 3 of our Physical AI & Humanoid Robotics journey! This week, we'll explore URDF (Unified Robot Description Format), the standard for representing robot models in ROS. URDF is essential for defining the physical and visual properties of robots, which is fundamental for simulation, visualization, and control in Physical AI systems.

## Learning Objectives

By the end of this week, you will be able to:

1. Understand the structure and components of URDF files
2. Create complete robot models with links, joints, and materials
3. Define kinematic chains and degrees of freedom
4. Incorporate visual and collision properties
5. Validate and debug URDF models
6. Use Xacro to simplify complex robot descriptions

## Introduction to URDF

URDF (Unified Robot Description Format) is an XML format used in ROS to describe robot models. It defines the physical structure of a robot, including its links (rigid parts), joints (connections between links), and other properties like visual appearance, collision geometry, and inertial properties.

### Why URDF Matters for Physical AI

URDF is crucial for Physical AI systems because it:

- **Defines robot morphology**: Specifies the physical structure of the robot
- **Enables simulation**: Provides models for physics engines in simulation environments
- **Facilitates visualization**: Allows RViz to display robot models correctly
- **Supports kinematics**: Enables forward and inverse kinematics calculations
- **Integrates with controllers**: Provides joint limits and properties for control systems

## URDF Structure

A URDF file consists of several key elements:

### Links
Links represent rigid parts of the robot. Each link has:
- Visual properties (shape, color, mesh)
- Collision properties (collision geometry)
- Inertial properties (mass, center of mass, inertia tensor)

### Joints
Joints connect links and define their relative motion. Joint types include:
- **Fixed**: No motion between links
- **Revolute**: Rotational motion around an axis
- **Continuous**: Unlimited rotational motion
- **Prismatic**: Linear motion along an axis
- **Floating**: 6DOF motion (no constraints)
- **Planar**: Motion on a plane

### Materials
Materials define the visual appearance of links.

## Basic URDF Example

Let's start with a simple robot model - a differential drive robot with a caster wheel:

```xml
<?xml version="1.0"?>
<robot name="simple_robot">
  <!-- Base Link -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.5 0.3 0.1"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 1 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.5 0.3 0.1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.01"/>
    </inertial>
  </link>

  <!-- Left Wheel -->
  <link name="left_wheel">
    <visual>
      <geometry>
        <cylinder radius="0.1" length="0.05"/>
      </geometry>
      <origin rpy="1.570796 0 0"/> <!-- Rotate to align with forward direction -->
      <material name="black">
        <color rgba="0 0 0 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.1" length="0.05"/>
      </geometry>
      <origin rpy="1.570796 0 0"/>
    </collision>
    <inertial>
      <mass value="0.2"/>
      <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.001"/>
    </inertial>
  </link>

  <!-- Right Wheel -->
  <link name="right_wheel">
    <visual>
      <geometry>
        <cylinder radius="0.1" length="0.05"/>
      </geometry>
      <origin rpy="1.570796 0 0"/>
      <material name="black">
        <color rgba="0 0 0 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.1" length="0.05"/>
      </geometry>
      <origin rpy="1.570796 0 0"/>
    </collision>
    <inertial>
      <mass value="0.2"/>
      <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.001"/>
    </inertial>
  </link>

  <!-- Caster Wheel -->
  <link name="caster_wheel">
    <visual>
      <geometry>
        <sphere radius="0.05"/>
      </geometry>
      <material name="gray">
        <color rgba="0.5 0.5 0.5 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <sphere radius="0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.1"/>
      <inertia ixx="0.0001" ixy="0.0" ixz="0.0" iyy="0.0001" iyz="0.0" izz="0.0001"/>
    </inertial>
  </link>

  <!-- Joints -->
  <joint name="left_wheel_joint" type="continuous">
    <parent link="base_link"/>
    <child link="left_wheel"/>
    <origin xyz="0 0.2 -0.05" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
  </joint>

  <joint name="right_wheel_joint" type="continuous">
    <parent link="base_link"/>
    <child link="right_wheel"/>
    <origin xyz="0 -0.2 -0.05" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
  </joint>

  <joint name="caster_wheel_joint" type="fixed">
    <parent link="base_link"/>
    <child link="caster_wheel"/>
    <origin xyz="-0.2 0 -0.05" rpy="0 0 0"/>
  </joint>
</robot>
```

## URDF Elements in Detail

### Links

Each link element contains three main sub-elements:

#### Visual Element
Defines how the link appears in visualization tools:

```xml
<visual>
  <origin xyz="0 0 0" rpy="0 0 0"/>
  <geometry>
    <box size="1 1 1"/>
    <!-- Other options: <cylinder radius="0.5" length="1"/>, <sphere radius="0.5"/>, <mesh filename="path/to/mesh.stl"/> -->
  </geometry>
  <material name="red">
    <color rgba="1 0 0 1"/>
  </material>
</visual>
```

#### Collision Element
Defines the collision geometry for physics simulation:

```xml
<collision>
  <origin xyz="0 0 0" rpy="0 0 0"/>
  <geometry>
    <box size="1 1 1"/>
  </geometry>
</collision>
```

#### Inertial Element
Defines the physical properties for dynamics simulation:

```xml
<inertial>
  <mass value="1.0"/>
  <inertia ixx="1.0" ixy="0.0" ixz="0.0" iyy="1.0" iyz="0.0" izz="1.0"/>
</inertial>
```

### Joints

Joint elements define the connection between links:

```xml
<joint name="joint_name" type="revolute">
  <parent link="parent_link_name"/>
  <child link="child_link_name"/>
  <origin xyz="1 0 0" rpy="0 0 0"/>
  <axis xyz="0 0 1"/>
  <limit lower="-1.57" upper="1.57" effort="10" velocity="1"/>
  <dynamics damping="0.1" friction="0.0"/>
</joint>
```

## Kinematic Chains and Degrees of Freedom

URDF models define the kinematic structure of robots. For Physical AI systems, understanding kinematic chains is essential for:

- Forward kinematics: Calculating end-effector position from joint angles
- Inverse kinematics: Calculating joint angles to achieve desired end-effector position
- Dynamics simulation: Understanding how forces propagate through the robot

### Example: Simple Robotic Arm

```xml
<?xml version="1.0"?>
<robot name="simple_arm">
  <!-- Base of the arm -->
  <link name="base_link">
    <visual>
      <geometry>
        <cylinder radius="0.1" length="0.2"/>
      </geometry>
      <origin rpy="0 0 0" xyz="0 0 0.1"/>
      <material name="orange">
        <color rgba="1 0.5 0 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.1" length="0.2"/>
      </geometry>
      <origin rpy="0 0 0" xyz="0 0 0.1"/>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.01"/>
    </inertial>
  </link>

  <!-- Shoulder joint -->
  <joint name="shoulder_pan_joint" type="revolute">
    <parent link="base_link"/>
    <child link="shoulder_link"/>
    <origin xyz="0 0 0.2" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1"/>
  </joint>

  <link name="shoulder_link">
    <visual>
      <geometry>
        <box size="0.05 0.05 0.1"/>
      </geometry>
      <material name="white">
        <color rgba="1 1 1 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.05 0.05 0.1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.5"/>
      <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.001"/>
    </inertial>
  </link>

  <!-- Elbow joint -->
  <joint name="elbow_joint" type="revolute">
    <parent link="shoulder_link"/>
    <child link="elbow_link"/>
    <origin xyz="0 0 0.1" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1"/>
  </joint>

  <link name="elbow_link">
    <visual>
      <geometry>
        <box size="0.05 0.05 0.2"/>
      </geometry>
      <material name="white">
        <color rgba="1 1 1 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.05 0.05 0.2"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.5"/>
      <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.001"/>
    </inertial>
  </link>

  <!-- Wrist joint -->
  <joint name="wrist_joint" type="revolute">
    <parent link="elbow_link"/>
    <child link="wrist_link"/>
    <origin xyz="0 0 0.2" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1"/>
  </joint>

  <link name="wrist_link">
    <visual>
      <geometry>
        <box size="0.05 0.05 0.05"/>
      </geometry>
      <material name="white">
        <color rgba="1 1 1 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.05 0.05 0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.2"/>
      <inertia ixx="0.0001" ixy="0.0" ixz="0.0" iyy="0.0001" iyz="0.0" izz="0.0001"/>
    </inertial>
  </link>
</robot>
```

## Using Xacro for Complex Models

Xacro (XML Macros) extends URDF with macros, constants, and expressions, making complex models more manageable:

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="xacro_robot">

  <!-- Define constants -->
  <xacro:property name="M_PI" value="3.1415926535897931" />
  <xacro:property name="wheel_radius" value="0.1" />
  <xacro:property name="wheel_width" value="0.05" />
  
  <!-- Define a macro for wheels -->
  <xacro:macro name="wheel" params="prefix parent xyz">
    <link name="${prefix}_wheel">
      <visual>
        <geometry>
          <cylinder radius="${wheel_radius}" length="${wheel_width}"/>
        </geometry>
        <origin rpy="${M_PI/2} 0 0"/>
        <material name="black">
          <color rgba="0 0 0 1"/>
        </material>
      </visual>
      <collision>
        <geometry>
          <cylinder radius="${wheel_radius}" length="${wheel_width}"/>
        </geometry>
        <origin rpy="${M_PI/2} 0 0"/>
      </collision>
      <inertial>
        <mass value="0.2"/>
        <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.001"/>
      </inertial>
    </link>

    <joint name="${prefix}_wheel_joint" type="continuous">
      <parent link="${parent}"/>
      <child link="${prefix}_wheel"/>
      <origin xyz="${xyz}" rpy="0 0 0"/>
      <axis xyz="0 1 0"/>
    </joint>
  </xacro:macro>

  <!-- Base link -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.5 0.3 0.1"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 1 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.5 0.3 0.1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.01"/>
    </inertial>
  </link>

  <!-- Use the wheel macro -->
  <xacro:wheel prefix="front_left" parent="base_link" xyz="0.2 0.15 -0.05"/>
  <xacro:wheel prefix="front_right" parent="base_link" xyz="0.2 -0.15 -0.05"/>
  <xacro:wheel prefix="rear_left" parent="base_link" xyz="-0.2 0.15 -0.05"/>
  <xacro:wheel prefix="rear_right" parent="base_link" xyz="-0.2 -0.15 -0.05"/>

</robot>
```

## Validating URDF Models

Before using a URDF model, validate it to catch errors:

```bash
# Check for XML syntax errors
check_urdf /path/to/robot.urdf

# Parse and display robot information
urdf_to_graphiz /path/to/robot.urdf
```

## URDF in Physical AI Systems

For Physical AI applications, URDF models serve several critical functions:

### Simulation Integration
URDF models are used by physics engines like Gazebo to simulate robot behavior in virtual environments, allowing for safe testing of control algorithms before deployment on physical hardware.

### Visualization
RViz uses URDF models to visualize robot state, showing joint positions and the robot's pose in the environment.

### Kinematics Solvers
URDF models provide the kinematic structure needed by solvers like KDL and MoveIt! for motion planning and control.

### Control Systems
Controllers use URDF joint limits and properties to ensure safe operation within mechanical constraints.

## Best Practices

1. **Start Simple**: Begin with basic shapes and gradually add detail
2. **Validate Early**: Regularly check your URDF with validation tools
3. **Use Xacro**: For complex robots, use Xacro to reduce redundancy
4. **Accurate Inertias**: Use proper inertial values for realistic simulation
5. **Collision vs Visual**: Use simpler geometries for collision to improve performance
6. **Consistent Units**: Use meters for distances and radians for angles
7. **Meaningful Names**: Use descriptive names for links and joints

## Looking Ahead

This week we've covered the fundamentals of robot modeling with URDF. Next week, we'll explore coordinate transforms (TF) which work closely with URDF to represent the spatial relationships between different parts of the robot and the environment.

## Exercises

1. Create a URDF model of a simple humanoid robot with at least 10 joints
2. Model a robotic manipulator with 6 degrees of freedom using Xacro
3. Create a mobile robot with differential drive and validate the URDF
4. Add sensors (cameras, LiDAR) to your robot model using Gazebo plugins

## Further Reading

- URDF/XML Format Documentation: http://wiki.ros.org/urdf/XML
- Xacro Tutorial: http://wiki.ros.org/xacro
- Robot State Publisher: http://wiki.ros.org/robot_state_publisher