# Week 2: ROS 2 Fundamentals for Physical AI

This week, we'll establish the foundational knowledge of ROS 2 (Robot Operating System 2), which serves as the communication backbone for Physical AI systems. ROS 2 provides the infrastructure for distributed robotics applications, enabling seamless integration of perception, planning, and control components.

## Learning Objectives

By the end of this week, you will be able to:

1. Understand the architecture and concepts of ROS 2
2. Create and manage ROS 2 nodes, topics, services, and actions
3. Implement message passing and service communication
4. Use ROS 2 tools for debugging and visualization
5. Design distributed systems using ROS 2 patterns
6. Apply ROS 2 to Physical AI system integration

## Introduction to ROS 2

ROS 2 (Robot Operating System 2) is not an operating system but rather a middleware framework that provides libraries, tools, and conventions for building robotic applications. It evolved from ROS 1 to address critical requirements for production robotics, including real-time support, security, and improved reliability.

### Why ROS 2 for Physical AI?

ROS 2 is essential for Physical AI systems because it:

- **Enables Modularity**: Break complex Physical AI systems into manageable, reusable components
- **Facilitates Communication**: Provides standardized interfaces for inter-process communication
- **Supports Distribution**: Allows nodes to run across multiple machines seamlessly
- **Ensures Interoperability**: Standardized message types and protocols enable component reuse
- **Provides Tooling**: Rich ecosystem of debugging, visualization, and development tools

### Key Improvements in ROS 2

Compared to ROS 1, ROS 2 offers:

- **Real-time Support**: Deterministic behavior for time-critical applications
- **Security**: Built-in authentication, authorization, and encryption
- **Quality of Service (QoS)**: Configurable reliability and performance characteristics
- **Multi-platform Support**: Runs on various operating systems and architectures
- **Standard Compliance**: Based on DDS (Data Distribution Service) standard

## Core ROS 2 Concepts

### Nodes

A node is a process that performs computation in ROS 2. Nodes are the fundamental building blocks of a ROS 2 system, each responsible for a specific task. Multiple nodes work together to create complex robotic behaviors.

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello World: {self.i}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Topics and Messages

Topics enable asynchronous, decoupled communication between nodes using a publish-subscribe pattern. This is ideal for continuous data streams like sensor readings or robot states.

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Services

Services provide synchronous, request-response communication between nodes. They're ideal for discrete operations that require immediate responses.

```python
from example_interfaces.srv import AddTwoInts
import rclpy
from rclpy.node import Node

class MinimalService(Node):
    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)

    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(f'Returning {request.a} + {request.b} = {response.sum}')
        return response

def main(args=None):
    rclpy.init(args=args)
    minimal_service = MinimalService()
    rclpy.spin(minimal_service)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Actions

Actions are used for long-running tasks that require feedback and the ability to cancel. They combine the features of topics and services, providing goal, result, and feedback mechanisms.

```python
from rclpy.action import ActionServer
from rclpy.node import Node
from example_interfaces.action import Fibonacci

class FibonacciActionServer(Node):
    def __init__(self):
        super().__init__('fibonacci_action_server')
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            self.execute_callback)

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')
        
        feedback_msg = Fibonacci.Feedback()
        feedback_msg.sequence = [0, 1]
        
        for i in range(1, goal_handle.request.order):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal canceled')
                return Fibonacci.Result()
            
            feedback_msg.sequence.append(
                feedback_msg.sequence[i] + feedback_msg.sequence[i-1])
            
            goal_handle.publish_feedback(feedback_msg)
        
        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = feedback_msg.sequence
        self.get_logger().info(f'Result: {result.sequence}')
        return result

def main(args=None):
    rclpy.init(args=args)
    fibonacci_action_server = FibonacciActionServer()
    rclpy.spin(fibonacci_action_server)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Quality of Service (QoS) Profiles

QoS profiles allow fine-tuning communication behavior between nodes:

```python
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

# For sensor data (real-time, lose some messages OK)
sensor_qos = QoSProfile(
    depth=5,
    reliability=ReliabilityPolicy.BEST_EFFORT,
    history=HistoryPolicy.KEEP_LAST
)

# For critical commands (reliable, keep all messages)
command_qos = QoSProfile(
    depth=10,
    reliability=ReliabilityPolicy.RELIABLE,
    history=HistoryPolicy.KEEP_ALL
)
```

## Launch Files

Launch files allow you to start multiple nodes with a single command, configure parameters, and manage complex robotic systems:

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='demo_nodes_py',
            executable='talker',
            name='minimal_publisher',
            parameters=[
                {'param_name': 'param_value'}
            ]
        ),
        Node(
            package='demo_nodes_py',
            executable='listener',
            name='minimal_subscriber'
        )
    ])
```

## ROS 2 for Physical AI Systems

### Distributed Architecture

Physical AI systems benefit from ROS 2's distributed architecture:

```python
# perception_node.py
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, PointCloud2
from geometry_msgs.msg import PoseStamped

class PerceptionNode(Node):
    def __init__(self):
        super().__init__('perception_node')
        
        # Subscribe to sensor data
        self.image_sub = self.create_subscription(
            Image, 'camera/image_raw', self.image_callback, 10)
        self.pointcloud_sub = self.create_subscription(
            PointCloud2, 'lidar/points', self.pointcloud_callback, 10)
        
        # Publish processed data
        self.object_pub = self.create_publisher(
            PoseStamped, 'detected_object', 10)
        self.map_pub = self.create_publisher(
            OccupancyGrid, 'environment_map', 10)
    
    def image_callback(self, msg):
        # Process image and detect objects
        # Publish results
        pass
    
    def pointcloud_callback(self, msg):
        # Process point cloud and build map
        # Publish results
        pass

# planning_node.py
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path

class PlanningNode(Node):
    def __init__(self):
        super().__init__('planning_node')
        
        # Subscribe to perception data
        self.object_sub = self.create_subscription(
            PoseStamped, 'detected_object', self.object_callback, 10)
        
        # Subscribe to map
        self.map_sub = self.create_subscription(
            OccupancyGrid, 'environment_map', self.map_callback, 10)
        
        # Subscribe to goal
        self.goal_sub = self.create_subscription(
            PoseStamped, 'goal_pose', self.goal_callback, 10)
        
        # Publish plan
        self.path_pub = self.create_publisher(Path, 'planned_path', 10)
    
    def object_callback(self, msg):
        # Update world model with detected object
        pass
    
    def map_callback(self, msg):
        # Update world model with map
        pass
    
    def goal_callback(self, msg):
        # Plan path to goal considering world model
        pass
```

### Parameter Management

ROS 2 provides powerful parameter management for configuring Physical AI systems:

```python
# config/physical_ai_params.yaml
perception_node:
  ros__parameters:
    detection_threshold: 0.7
    max_detection_range: 5.0
    processing_frequency: 10.0

planning_node:
  ros__parameters:
    planning_frequency: 5.0
    max_planning_time: 1.0
    path_resolution: 0.1
    collision_check_resolution: 0.05
```

## Best Practices for Physical AI Systems

### 1. Modularity and Reusability
- Create focused nodes that perform specific functions
- Use standard message types when possible
- Design nodes to be configurable through parameters
- Implement proper error handling and recovery

### 2. Performance Considerations
- Use appropriate QoS settings for different data types
- Consider computational requirements for real-time performance
- Implement efficient data processing pipelines
- Monitor node performance and resource usage

### 3. Safety and Reliability
- Implement proper error handling and graceful degradation
- Use latching for important static data
- Implement health monitoring and reporting
- Design for fault tolerance and recovery

### 4. Debugging and Monitoring
- Use ROS 2 tools for debugging (ros2 topic, ros2 service, etc.)
- Implement proper logging with appropriate levels
- Use visualization tools (RViz2) for debugging
- Monitor system performance and resource usage

## Integration with Physical AI Components

### Vision-Language-Action Integration

ROS 2 facilitates integration of VLA components:

```python
# vla_integration_node.py
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped

class VLAIntegrationNode(Node):
    def __init__(self):
        super().__init__('vla_integration_node')
        
        # Subscriptions
        self.image_sub = self.create_subscription(
            Image, 'camera/image_raw', self.image_callback, 10)
        self.command_sub = self.create_subscription(
            String, 'natural_language_command', self.command_callback, 10)
        
        # Publications
        self.action_pub = self.create_publisher(
            PoseStamped, 'robot_action', 10)
        
        # Internal state
        self.current_image = None
        self.current_command = None
    
    def image_callback(self, msg):
        self.current_image = msg
        if self.current_command:
            self.process_vla_command()
    
    def command_callback(self, msg):
        self.current_command = msg
        if self.current_image:
            self.process_vla_command()
    
    def process_vla_command(self):
        # Process vision and language inputs together
        # Generate appropriate action
        action_msg = self.generate_action_from_vla(
            self.current_image, self.current_command)
        self.action_pub.publish(action_msg)
    
    def generate_action_from_vla(self, image_msg, command_msg):
        # Implementation of VLA processing
        # This would typically involve:
        # 1. Processing image with vision model
        # 2. Processing command with language model
        # 3. Fusing information and generating action
        pass
```

## Looking Ahead

This week established the foundational knowledge of ROS 2, which will be essential throughout the course. Next week, we'll explore URDF (Unified Robot Description Format) for modeling robots and their kinematic structures.

## Exercises

1. Create a ROS 2 package with nodes for a simple Physical AI system
2. Implement a publisher-subscriber pair for sensor data
3. Create a service for robot control commands
4. Design a launch file for your Physical AI system
5. Implement parameter configuration for your nodes

## Further Reading

- ROS 2 Documentation: https://docs.ros.org/
- ROS 2 Tutorials: https://docs.ros.org/en/humble/Tutorials.html
- Quality of Service in ROS 2: https://docs.ros.org/en/humble/Concepts/About-Quality-of-Service-Settings.html
- ROS 2 Design: https://design.ros2.org/