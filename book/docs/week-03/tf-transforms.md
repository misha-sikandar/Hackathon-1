---
sidebar_position: 9
---

# Coordinate Transforms (TF) in Physical AI Systems

In this lesson, we'll explore the Transform (TF) system in ROS, which is essential for understanding spatial relationships in Physical AI systems. TF allows us to track and transform data between different coordinate frames, which is crucial for perception, navigation, and manipulation tasks.

## Learning Objectives

By the end of this lesson, you will be able to:

1. Understand the concept of coordinate frames and transformations
2. Work with the TF2 system in ROS 2
3. Transform data between different coordinate frames
4. Broadcast and listen to transform data
5. Debug TF-related issues in robotic systems
6. Apply TF concepts to Physical AI perception and control

## Introduction to Coordinate Frames and TF

Coordinate frames are reference systems that define positions and orientations in space. In robotics, we often need to work with multiple coordinate frames simultaneously:

- **Base frame**: Attached to the robot's main body
- **Sensor frames**: Attached to individual sensors (cameras, LiDAR, etc.)
- **World/map frame**: Fixed reference frame for navigation
- **End-effector frame**: Attached to the robot's gripper or tool
- **Object frames**: Attached to objects in the environment

The TF (Transform) system maintains the relationships between these frames and allows for seamless transformation of data between them.

## TF2 Architecture

TF2 is the second-generation transform library in ROS, offering improved performance and features over the original TF system:

- **Tree structure**: Maintains a directed acyclic graph of transforms
- **Time-based queries**: Can interpolate transforms at specific timestamps
- **Efficient storage**: Optimized for real-time applications
- **Multi-representation**: Supports quaternions, Euler angles, and matrices

## Working with TF2 in Code

### Broadcasting Transforms

To broadcast transforms, we use the `TransformBroadcaster`:

```python
import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped
import math

class FramePublisher(Node):
    def __init__(self):
        super().__init__('frame_publisher')
        
        # Create transform broadcaster
        self.tf_broadcaster = TransformBroadcaster(self)
        
        # Create timer to periodically publish transforms
        self.timer = self.create_timer(0.1, self.broadcast_transform)
        
    def broadcast_transform(self):
        # Create transform message
        t = TransformStamped()
        
        # Fill header
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'world'
        t.child_frame_id = 'robot_base'
        
        # Define position and orientation
        t.transform.translation.x = 1.0
        t.transform.translation.y = 0.0
        t.transform.translation.z = 0.0
        
        # For rotation, we'll use a simple yaw rotation
        yaw = math.sin(self.get_clock().now().nanoseconds / 1e9)  # Oscillating rotation
        t.transform.rotation.z = math.sin(yaw / 2.0)
        t.transform.rotation.w = math.cos(yaw / 2.0)
        
        # Send the transform
        self.tf_broadcaster.sendTransform(t)

def main(args=None):
    rclpy.init(args=args)
    node = FramePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Listening to Transforms

To listen to transforms, we use the `TransformListener`:

```python
import rclpy
from rclpy.node import Node
from tf2_ros import TransformListener, Buffer
from geometry_msgs.msg import PointStamped
import math

class FrameListener(Node):
    def __init__(self):
        super().__init__('frame_listener')
        
        # Create TF buffer and listener
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        
        # Create publisher for transformed data
        self.pub = self.create_publisher(PointStamped, 'transformed_point', 10)
        
        # Create timer to periodically lookup transforms
        self.timer = self.create_timer(0.1, self.lookup_transform)
        
    def lookup_transform(self):
        try:
            # Look up transform from 'robot_base' to 'world'
            trans = self.tf_buffer.lookup_transform(
                'world',
                'robot_base',
                rclpy.time.Time())  # Use latest available transform
            
            # Create a point in robot_base frame
            point_in_robot = PointStamped()
            point_in_robot.header.frame_id = 'robot_base'
            point_in_robot.header.stamp = self.get_clock().now().to_msg()
            point_in_robot.point.x = 0.5  # 0.5m in front of robot
            point_in_robot.point.y = 0.0
            point_in_robot.point.z = 0.0
            
            # Transform the point to world frame
            point_in_world = self.tf_buffer.transform(point_in_robot, 'world')
            
            # Publish the transformed point
            self.pub.publish(point_in_world)
            
            self.get_logger().info(
                f'Robot position: ({trans.transform.translation.x:.2f}, '
                f'{trans.transform.translation.y:.2f})')
                
        except Exception as e:
            self.get_logger().info(f'Could not transform: {str(e)}')

def main(args=None):
    rclpy.init(args=args)
    node = FrameListener()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## TF in Physical AI Perception Systems

In Physical AI systems, TF is crucial for sensor fusion and perception:

### Camera to Robot Base Transformation

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from tf2_ros import Buffer, TransformListener
from cv_bridge import CvBridge
import cv2
import numpy as np

class CameraPerceptionNode(Node):
    def __init__(self):
        super().__init__('camera_perception')
        
        # Create TF buffer and listener
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        
        # Create camera subscriber
        self.image_sub = self.create_subscription(
            Image, 'camera/image_raw', self.image_callback, 10)
        
        # Create bridge for converting ROS images to OpenCV
        self.cv_bridge = CvBridge()
        
    def image_callback(self, msg):
        # Convert ROS image to OpenCV
        cv_image = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
        
        try:
            # Get transform from camera to robot base
            transform = self.tf_buffer.lookup_transform(
                'robot_base',  # Target frame
                'camera_frame',  # Source frame
                rclpy.time.Time(),
                timeout=rclpy.duration.Duration(seconds=1.0))
                
            # Process image with knowledge of camera position
            self.process_image_with_transform(cv_image, transform)
            
        except Exception as e:
            self.get_logger().error(f'Transform lookup failed: {str(e)}')
    
    def process_image_with_transform(self, image, transform):
        # Example: Draw robot's position on image
        # Extract translation from transform
        x = transform.transform.translation.x
        y = transform.transform.translation.y
        
        # Draw text showing robot position
        cv2.putText(image, f'Robot Pos: ({x:.2f}, {y:.2f})', 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Display the image
        cv2.imshow('Camera with Robot Position', image)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    node = CameraPerceptionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### LiDAR to Map Transformation

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from tf2_ros import Buffer, TransformListener
from geometry_msgs.msg import PointStamped
import math

class LidarMappingNode(Node):
    def __init__(self):
        super().__init__('lidar_mapping')
        
        # Create TF buffer and listener
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        
        # Create LiDAR subscriber
        self.scan_sub = self.create_subscription(
            LaserScan, 'scan', self.scan_callback, 10)
        
    def scan_callback(self, msg):
        try:
            # Get transform from laser frame to map frame
            transform = self.tf_buffer.lookup_transform(
                'map',  # Target frame
                msg.header.frame_id,  # Source frame (LiDAR frame)
                rclpy.time.Time())
                
            # Process scan data in map coordinates
            self.process_scan_in_map_coordinates(msg, transform)
            
        except Exception as e:
            self.get_logger().error(f'Transform lookup failed: {str(e)}')
    
    def process_scan_in_map_coordinates(self, scan_msg, transform):
        # Convert each laser beam to map coordinates
        for i, range_val in enumerate(scan_msg.ranges):
            if not math.isnan(range_val) and range_val <= scan_msg.range_max:
                # Calculate angle of this beam
                angle = scan_msg.angle_min + i * scan_msg.angle_increment
                
                # Calculate point in laser frame
                x_laser = range_val * math.cos(angle)
                y_laser = range_val * math.sin(angle)
                
                # Create point in laser frame
                point_laser = PointStamped()
                point_laser.header = scan_msg.header
                point_laser.point.x = x_laser
                point_laser.point.y = y_laser
                point_laser.point.z = 0.0
                
                # Transform to map frame
                try:
                    point_map = self.tf_buffer.transform(point_laser, 'map')
                    
                    # Now point_map contains the coordinates in map frame
                    # This could be used for mapping, obstacle detection, etc.
                    
                except Exception as e:
                    self.get_logger().error(f'Point transform failed: {str(e)}')

def main(args=None):
    rclpy.init(args=args)
    node = LidarMappingNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## TF for Manipulation Tasks

In manipulation tasks, TF is essential for transforming between different reference frames:

```python
import rclpy
from rclpy.node import Node
from tf2_ros import Buffer, TransformListener
from geometry_msgs.msg import PoseStamped
from moveit_msgs.action import MoveGroup
from rclpy.action import ActionClient

class ManipulationController(Node):
    def __init__(self):
        super().__init__('manipulation_controller')
        
        # Create TF buffer and listener
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        
        # Create MoveIt! action client
        self.move_group = ActionClient(self, MoveGroup, 'move_group')
        
        # Timer to periodically check for objects
        self.timer = self.create_timer(1.0, self.look_for_objects)
        
    def look_for_objects(self):
        try:
            # Assume we detected an object in camera frame
            object_in_camera = PoseStamped()
            object_in_camera.header.frame_id = 'camera_rgb_optical_frame'
            object_in_camera.header.stamp = self.get_clock().now().to_msg()
            object_in_camera.pose.position.x = 0.5  # 0.5m in front of camera
            object_in_camera.pose.position.y = 0.1  # 0.1m to the right
            object_in_camera.pose.position.z = 0.2  # 0.2m above camera
            object_in_camera.pose.orientation.w = 1.0
            
            # Transform object position to base frame for manipulation
            object_in_base = self.tf_buffer.transform(object_in_camera, 'base_link')
            
            # Plan manipulation to reach the object
            self.plan_manipulation(object_in_base)
            
        except Exception as e:
            self.get_logger().error(f'Object transform failed: {str(e)}')
    
    def plan_manipulation(self, target_pose):
        # Send target pose to MoveIt! for motion planning
        # Implementation would go here
        self.get_logger().info(
            f'Planning manipulation to: ({target_pose.pose.position.x:.2f}, '
            f'{target_pose.pose.position.y:.2f}, {target_pose.pose.position.z:.2f})')

def main(args=None):
    rclpy.init(args=args)
    node = ManipulationController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## TF Best Practices for Physical AI

### 1. Frame Naming Conventions

Use consistent and descriptive names for frames:
- `base_link`: Robot's main body frame
- `camera_frame`, `lidar_frame`: Sensor-specific frames
- `map`, `odom`: Global reference frames
- `tool0`, `ee_link`: End-effector frames

### 2. Static vs Dynamic Transforms

For fixed relationships, use `static_transform_publisher`:

```bash
# Publish a static transform from 'base_link' to 'laser_frame'
ros2 run tf2_ros static_transform_publisher 0.1 0.0 0.2 0.0 0.0 0.0 base_link laser_frame
```

For dynamic relationships, broadcast transforms from a node as shown in the examples above.

### 3. Handling Time in TF

TF2 stores transforms over time, allowing you to query past states:

```python
# Get transform at a specific time in the past
past_time = rclpy.time.Time(seconds=msg.header.stamp.sec, 
                           nanoseconds=msg.header.stamp.nanosec) - \
           rclpy.duration.Duration(seconds=0.1)  # 100ms ago

transform = self.tf_buffer.lookup_transform(
    'map', 'robot_base', past_time)
```

### 4. TF Tree Visualization

Use `tf2_tools` to visualize your transform tree:

```bash
# Visualize the TF tree
ros2 run tf2_tools view_frames
```

## Common TF Issues and Debugging

### 1. Transform Not Available

This usually means the transform hasn't been published yet or there's a gap in the TF chain:

```python
# Add timeout to prevent hanging
try:
    transform = self.tf_buffer.lookup_transform(
        'target_frame', 'source_frame', 
        rclpy.time.Time(),
        timeout=rclpy.duration.Duration(seconds=1.0))
except TransformException as ex:
    self.get_logger().error(f'Could not transform: {ex}')
    return
```

### 2. TF Chain Gaps

Use `ros2 run tf2_tools view_frames` to visualize the TF tree and identify gaps.

### 3. Timestamp Issues

Ensure your nodes are publishing transforms with appropriate timestamps:

```python
# Always set the timestamp when broadcasting transforms
t.header.stamp = self.get_clock().now().to_msg()
```

## TF in Simulation vs Real Robots

In simulation, TF transforms often come from Gazebo plugins that automatically publish joint states and robot state. In real robots, you'll need to:

1. Use encoders to measure joint positions
2. Publish joint states via `joint_state_publisher`
3. Use `robot_state_publisher` to compute and publish the forward kinematics

## Integration with URDF

TF works closely with URDF models. The `robot_state_publisher` node takes joint positions and the URDF model to publish the complete TF tree:

```xml
<!-- In your launch file -->
<node pkg="robot_state_publisher" exec="robot_state_publisher" name="robot_state_publisher">
  <param name="robot_description" value="$(var robot_description)"/>
</node>
```

## Summary

TF is a fundamental component of ROS that enables Physical AI systems to understand spatial relationships. Mastering TF is essential for tasks involving perception, navigation, and manipulation. The ability to transform data between coordinate frames allows robots to operate effectively in their environment.

## Exercises

1. Create a TF tree for a simple mobile manipulator with at least 5 frames
2. Implement a node that broadcasts a moving frame relative to the robot base
3. Transform sensor data from multiple sources to a common frame
4. Debug a provided TF tree with intentional errors