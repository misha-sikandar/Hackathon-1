---
sidebar_position: 8
---

# ROS 2 Fundamentals: Practical Implementation Guide

This guide provides practical examples and implementation details for working with ROS 2 in Physical AI systems. We'll cover common patterns, best practices, and troubleshooting tips.

## Creating a ROS 2 Package

Every ROS 2 project starts with a package. Here's how to create one:

```bash
# Create a new workspace
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src

# Create a new package
ros2 pkg create --build-type ament_python my_physical_ai_pkg --dependencies rclpy std_msgs sensor_msgs geometry_msgs

# Navigate to the package
cd my_physical_ai_pkg
```

## Common Node Patterns

### 1. Parameterized Node

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class ParameterizedNode(Node):
    def __init__(self):
        super().__init__('parameterized_node')
        
        # Declare parameters with defaults
        self.declare_parameter('robot_name', 'my_robot')
        self.declare_parameter('publish_rate', 1.0)
        
        # Get parameter values
        self.robot_name = self.get_parameter('robot_name').value
        self.rate = self.get_parameter('publish_rate').value
        
        # Create publisher
        self.publisher = self.create_publisher(String, 'robot_status', 10)
        
        # Create timer with parameterized rate
        self.timer = self.create_timer(1.0/self.rate, self.timer_callback)
        
    def timer_callback(self):
        msg = String()
        msg.data = f'{self.robot_name} is operational at {self.rate} Hz'
        self.publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = ParameterizedNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### 2. Node with Multiple Callback Groups

```python
import rclpy
from rclpy.node import Node
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan

class MultiCallbackNode(Node):
    def __init__(self):
        super().__init__('multi_callback_node')
        
        # Create callback groups
        self.group1 = MutuallyExclusiveCallbackGroup()
        self.group2 = MutuallyExclusiveCallbackGroup()
        self.reentrant_group = ReentrantCallbackGroup()
        
        # Create subscriptions with different callback groups
        self.sub1 = self.create_subscription(
            String, 'topic1', self.callback1, 10, callback_group=self.group1)
        self.sub2 = self.create_subscription(
            String, 'topic2', self.callback2, 10, callback_group=self.group2)
        self.lidar_sub = self.create_subscription(
            LaserScan, 'scan', self.lidar_callback, 10, callback_group=self.reentrant_group)
        
        # Create executor to handle multiple threads
        self.executor = rclpy.executors.MultiThreadedExecutor(num_threads=4)
        
    def callback1(self, msg):
        self.get_logger().info(f'Received on topic1: {msg.data}')
        
    def callback2(self, msg):
        self.get_logger().info(f'Received on topic2: {msg.data}')
        
    def lidar_callback(self, msg):
        self.get_logger().info(f'Lidar range count: {len(msg.ranges)}')

def main(args=None):
    rclpy.init(args=args)
    node = MultiCallbackNode()
    rclpy.spin(node, executor=node.executor)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Working with Custom Messages

### Creating Custom Messages

1. Create a `msg` directory in your package
2. Define your message in a `.msg` file

Example `RobotState.msg`:
```
# Robot state message
std_msgs/Header header
geometry_msgs/Pose pose
geometry_msgs/Twist velocity
float32 battery_level
bool is_charging
string[] joint_names
float32[] joint_positions
```

3. Update `package.xml`:
```xml
<depend>std_msgs</depend>
<depend>geometry_msgs</depend>
<member_of_group>rosidl_interface_packages</member_of_group>
```

4. Update `setup.py`:
```python
from setuptools import setup
from glob import glob
import os

package_name = 'my_physical_ai_pkg'

setup(
    # ... other setup parameters ...
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Include all launch files
        (os.path.join('share', package_name, 'launch'), glob('launch/*launch.[pxy][yma]*')),
        # Include all message files
        (os.path.join('share', package_name, 'msg'), glob('msg/*.msg')),
    ],
    # ... rest of setup ...
)
```

## Debugging Techniques

### 1. Using ROS 2 Command Line Tools

```bash
# List all active nodes
ros2 node list

# Get information about a specific node
ros2 node info /node_name

# List all topics
ros2 topic list

# Echo messages on a topic
ros2 topic echo /topic_name

# Get information about a topic
ros2 topic info /topic_name

# Publish a single message to a topic
ros2 topic pub /topic_name std_msgs/String "data: 'hello'"

# List all services
ros2 service list

# Call a service
ros2 service call /service_name example_interfaces/srv/AddTwoInts "{a: 1, b: 2}"
```

### 2. Using rqt for Visualization

```bash
# Launch rqt with various plugins
rqt

# Specific plugins
rqt_graph  # Shows node connections
rqt_plot   # Plots numeric values
rqt_console # Shows log messages
```

### 3. Logging Best Practices

```python
import rclpy
from rclpy.node import Node

class LoggingExample(Node):
    def __init__(self):
        super().__init__('logging_example')
        
        # Different log levels
        self.get_logger().debug('Debug information')
        self.get_logger().info('General information')
        self.get_logger().warn('Warning message')
        self.get_logger().error('Error message')
        self.get_logger().fatal('Fatal error message')
        
        # Logging with variables
        value = 42
        self.get_logger().info(f'Current value is: {value}')
        
        # Conditional logging
        if value > 40:
            self.get_logger().warn(f'Value {value} is higher than threshold')

def main(args=None):
    rclpy.init(args=args)
    node = LoggingExample()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Performance Optimization

### 1. Efficient Message Handling

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
import numpy as np

class EfficientProcessingNode(Node):
    def __init__(self):
        super().__init__('efficient_processing')
        
        # Use appropriate queue sizes
        qos_profile = rclpy.qos.QoSProfile(depth=5)
        self.pointcloud_sub = self.create_subscription(
            PointCloud2, 
            'pointcloud', 
            self.pointcloud_callback, 
            qos_profile)
        
    def pointcloud_callback(self, msg):
        # Process data efficiently
        # Convert to numpy array for faster processing
        # Avoid unnecessary copies
        pass
```

### 2. Threading and Concurrency

```python
import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
import threading
import time

class ConcurrentNode(Node):
    def __init__(self):
        super().__init__('concurrent_node')
        
        # Shared data with thread-safe access
        self.lock = threading.Lock()
        self.shared_data = {}
        
        # Timer for periodic tasks
        self.timer = self.create_timer(0.1, self.periodic_task)
        
    def periodic_task(self):
        # Perform non-blocking operations
        # Use threading for CPU-intensive tasks
        thread = threading.Thread(target=self.intensive_computation)
        thread.start()
        
    def intensive_computation(self):
        # Perform CPU-intensive task in separate thread
        # Use lock when accessing shared data
        with self.lock:
            # Modify shared_data safely
            pass

def main(args=None):
    rclpy.init(args=args)
    node = ConcurrentNode()
    
    # Use multi-threaded executor
    executor = MultiThreadedExecutor(num_threads=4)
    executor.add_node(node)
    
    try:
        executor.spin()
    finally:
        executor.shutdown()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Integration with Physical AI Systems

### Sensor Integration Pattern

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan, Image, Imu
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32
import cv2
from cv2 import cv2
import numpy as np

class SensorIntegrationNode(Node):
    def __init__(self):
        super().__init__('sensor_integration')
        
        # Multiple sensor subscriptions
        self.lidar_sub = self.create_subscription(
            LaserScan, 'scan', self.lidar_callback, 10)
        self.camera_sub = self.create_subscription(
            Image, 'camera/image_raw', self.camera_callback, 10)
        self.imu_sub = self.create_subscription(
            Imu, 'imu/data', self.imu_callback, 10)
        
        # Publisher for fused perception
        self.perception_pub = self.create_publisher(
            PerceptionMsg, 'perception_output', 10)
        
        # Publisher for robot commands
        self.cmd_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        
        # Timer for main control loop
        self.control_timer = self.create_timer(0.1, self.control_loop)
        
        # Internal state
        self.lidar_data = None
        self.camera_frame = None
        self.imu_data = None
        
    def lidar_callback(self, msg):
        self.lidar_data = msg
        
    def camera_callback(self, msg):
        # Convert ROS Image to OpenCV format
        self.camera_frame = self.ros_to_cv2(msg)
        
    def imu_callback(self, msg):
        self.imu_data = msg
        
    def ros_to_cv2(self, img_msg):
        # Convert ROS Image message to OpenCV image
        dtype = np.dtype("uint8")  # Hardcode to uint8
        img = np.asarray(img_msg.data, dtype=dtype).reshape(img_msg.height, img_msg.width, -1)
        return img
        
    def control_loop(self):
        # Main control loop that integrates sensor data
        if self.lidar_data and self.camera_frame is not None and self.imu_data:
            # Fuse sensor data
            perception_result = self.fuse_sensor_data(
                self.lidar_data, self.camera_frame, self.imu_data)
            
            # Publish perception result
            self.perception_pub.publish(perception_result)
            
            # Generate robot commands based on perception
            cmd = self.generate_commands(perception_result)
            self.cmd_pub.publish(cmd)
    
    def fuse_sensor_data(self, lidar, camera, imu):
        # Implementation of sensor fusion algorithm
        # This would typically involve combining data from different modalities
        # to create a unified understanding of the environment
        pass
        
    def generate_commands(self, perception_result):
        # Generate robot commands based on perception
        # This could involve navigation, manipulation, or other behaviors
        cmd = Twist()
        # ... command generation logic ...
        return cmd

def main(args=None):
    rclpy.init(args=args)
    node = SensorIntegrationNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Troubleshooting Common Issues

### 1. Topic Connection Problems

If nodes aren't communicating:
- Check that nodes are on the same ROS_DOMAIN_ID
- Verify topic names match exactly (case-sensitive)
- Ensure QoS profiles are compatible between publisher and subscriber
- Check network configuration if using multiple machines

### 2. Memory Leaks

Common causes and solutions:
- Not properly destroying nodes: Always call `destroy_node()` before shutdown
- Creating too many timers/subscribers without cleanup
- Holding references to large data structures unnecessarily

### 3. Timing Issues

- Use appropriate timer periods for your application
- Consider using wall timers for real-time guarantees
- Be aware of thread safety when using timers

## Testing Your Nodes

### Unit Testing

```python
import unittest
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from my_physical_ai_pkg.my_node import MyNode

class TestMyNode(unittest.TestCase):
    def setUp(self):
        rclpy.init()
        self.node = MyNode()
        
    def tearDown(self):
        self.node.destroy_node()
        rclpy.shutdown()
        
    def test_publish_message(self):
        # Create a mock subscription to verify publishing
        received_messages = []
        
        def callback(msg):
            received_messages.append(msg.data)
            
        sub = self.node.create_subscription(
            String, 'test_topic', callback, 10)
            
        # Trigger the publishing behavior
        self.node.trigger_publish()
        
        # Spin briefly to process messages
        rclpy.spin_once(self.node, timeout_sec=0.1)
        
        # Verify the expected message was published
        self.assertEqual(len(received_messages), 1)
        self.assertEqual(received_messages[0], 'expected_message')

if __name__ == '__main__':
    unittest.main()
```

This practical guide provides the essential knowledge and patterns needed to effectively implement ROS 2 in Physical AI systems. Apply these concepts to build robust, scalable robotic applications.