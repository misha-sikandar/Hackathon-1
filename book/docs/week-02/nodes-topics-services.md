---
sidebar_position: 6
---

# Core ROS 2 Concepts: Nodes, Topics, Services, and Actions

In this lesson, we'll dive deeper into the fundamental communication patterns in ROS 2. Understanding these concepts is crucial for building modular, scalable robotic systems that embody the principles of Physical AI.

## Nodes: The Building Blocks of ROS 2

Nodes are the fundamental units of computation in ROS 2. Each node typically handles a specific task or aspect of the robot's functionality. In Physical AI systems, nodes might handle perception, planning, control, or actuation.

### Node Lifecycle

Understanding the lifecycle of a ROS 2 node is essential for creating robust systems:

```python
import rclpy
from rclpy.lifecycle import LifecycleNode, TransitionCallbackReturn
from rclpy.lifecycle import LifecycleState

class PhysicalAINode(LifecycleNode):
    def __init__(self):
        super().__init__('physical_ai_node')
        
    def on_configure(self, state: LifecycleState) -> TransitionCallbackReturn:
        self.get_logger().info(f'Configuring {self.get_name()}')
        # Initialize resources
        return TransitionCallbackReturn.SUCCESS
        
    def on_activate(self, state: LifecycleState) -> TransitionCallbackReturn:
        self.get_logger().info(f'Activating {self.get_name()}')
        # Activate publishers/subscribers
        return TransitionCallbackReturn.SUCCESS
        
    def on_deactivate(self, state: LifecycleState) -> TransitionCallbackReturn:
        self.get_logger().info(f'Deactivating {self.get_name()}')
        # Deactivate publishers/subscribers
        return TransitionCallbackReturn.SUCCESS
        
    def on_cleanup(self, state: LifecycleState) -> TransitionCallbackReturn:
        self.get_logger().info(f'Cleaning up {self.get_name()}')
        # Release resources
        return TransitionCallbackReturn.SUCCESS
```

### Node Composition

For performance-critical Physical AI applications, nodes can be composed into a single process to reduce communication overhead:

```python
from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup

class ComposedNode(Node):
    def __init__(self):
        super().__init__('composed_node')
        
        # Create callback groups for concurrent execution
        cb_group = MutuallyExclusiveCallbackGroup()
        
        # Create multiple publishers/subscribers within one node
        self.pub = self.create_publisher(String, 'composed_topic', 10)
        self.sub = self.create_subscription(
            String, 'input_topic', self.callback, 10, 
            callback_group=cb_group)
```

## Topics: Publish-Subscribe Communication

Topics enable asynchronous, decoupled communication between nodes using a publish-subscribe pattern. This is ideal for continuous data streams like sensor readings or motor commands.

### Topic Architecture

Topics work on a many-to-many basis:
- Multiple publishers can publish to the same topic
- Multiple subscribers can subscribe to the same topic
- Publishers and subscribers are decoupled in time and space

### Quality of Service (QoS) for Topics

QoS settings are critical for Physical AI systems where timing and reliability matter:

```python
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy

# For sensor data (real-time, lose some messages OK)
sensor_qos = QoSProfile(
    depth=5,
    reliability=ReliabilityPolicy.BEST_EFFORT,
    history=HistoryPolicy.KEEP_LAST,
    durability=DurabilityPolicy.VOLATILE
)

# For critical commands (reliable, keep all messages)
command_qos = QoSProfile(
    depth=10,
    reliability=ReliabilityPolicy.RELIABLE,
    history=HistoryPolicy.KEEP_ALL,
    durability=DurabilityPolicy.VOLATILE
)

# Publisher with specific QoS
sensor_pub = self.create_publisher(SensorMsg, 'sensor_data', sensor_qos)
command_pub = self.create_publisher(CommandMsg, 'robot_cmd', command_qos)
```

### Practical Topic Example: Sensor Fusion

```python
from sensor_msgs.msg import LaserScan, Image, Imu
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32

class SensorFusionNode(Node):
    def __init__(self):
        super().__init__('sensor_fusion_node')
        
        # Subscribe to multiple sensor streams
        self.lidar_sub = self.create_subscription(
            LaserScan, 'scan', self.lidar_callback, 10)
        self.camera_sub = self.create_subscription(
            Image, 'camera/image_raw', self.camera_callback, 10)
        self.imu_sub = self.create_subscription(
            Imu, 'imu/data', self.imu_callback, 10)
            
        # Publish fused perception data
        self.perception_pub = self.create_publisher(
            PerceptionMsg, 'perception_output', 10)
        
    def lidar_callback(self, msg):
        # Process LiDAR data for obstacle detection
        self.process_lidar_data(msg)
        
    def camera_callback(self, msg):
        # Process camera data for object recognition
        self.process_camera_data(msg)
        
    def imu_callback(self, msg):
        # Process IMU data for orientation
        self.process_imu_data(msg)
        
    def process_lidar_data(self, msg):
        # Implementation for LiDAR processing
        pass
        
    def process_camera_data(self, msg):
        # Implementation for camera processing
        pass
        
    def process_imu_data(self, msg):
        # Implementation for IMU processing
        pass
```

## Services: Request-Response Communication

Services provide synchronous, bidirectional communication for discrete operations. They're ideal for tasks that have a clear request-response pattern.

### Service Architecture

Services follow a client-server model:
- Service server provides a specific functionality
- Service client requests the functionality
- Communication is synchronous (client waits for response)

### Defining Custom Services

Create a service definition file (`CalculatePath.srv`):

```
# Request
geometry_msgs/PoseStamped start_pose
geometry_msgs/PoseStamped goal_pose
float32 max_time
---
# Response
nav_msgs/Path path
bool success
string error_message
```

### Service Implementation

```python
from rclpy.action import ActionServer
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path
from my_robot_msgs.srv import CalculatePath  # Custom service

class PathPlannerNode(Node):
    def __init__(self):
        super().__init__('path_planner_node')
        
        # Create service server
        self.path_service = self.create_service(
            CalculatePath, 
            'calculate_path', 
            self.calculate_path_callback)
    
    def calculate_path_callback(self, request, response):
        self.get_logger().info(f'Received path request from {request.start_pose.pose.position} to {request.goal_pose.pose.position}')
        
        try:
            # Perform path calculation
            calculated_path = self.perform_path_calculation(
                request.start_pose, 
                request.goal_pose, 
                request.max_time
            )
            
            response.path = calculated_path
            response.success = True
            response.error_message = ""
            
        except Exception as e:
            response.success = False
            response.error_message = str(e)
            
        return response
    
    def perform_path_calculation(self, start_pose, goal_pose, max_time):
        # Implementation of path planning algorithm
        # This could use A*, RRT, or other algorithms
        path = Path()
        # ... path calculation logic ...
        return path
```

### Service Client Example

```python
class NavigationNode(Node):
    def __init__(self):
        super().__init__('navigation_node')
        
        # Create service client
        self.path_client = self.create_client(
            CalculatePath, 
            'calculate_path')
        
        while not self.path_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Path service not available, waiting...')
        
    def request_path(self, start_pose, goal_pose):
        request = CalculatePath.Request()
        request.start_pose = start_pose
        request.goal_pose = goal_pose
        request.max_time = 10.0  # seconds
        
        # Send async request
        future = self.path_client.call_async(request)
        future.add_done_callback(self.path_response_callback)
        
    def path_response_callback(self, future):
        try:
            response = future.result()
            if response.success:
                self.follow_path(response.path)
            else:
                self.get_logger().error(f'Path calculation failed: {response.error_message}')
        except Exception as e:
            self.get_logger().error(f'Service call failed: {e}')
```

## Actions: Long-Running Tasks with Feedback

Actions are designed for long-running operations that require feedback and cancellation capabilities. They're perfect for tasks like navigation, manipulation, or complex behaviors.

### Action Architecture

Actions combine features of topics and services:
- Goal: Request to start an action
- Result: Final outcome of the action
- Feedback: Continuous updates during execution
- Cancel: Ability to interrupt the action

### Defining Custom Actions

Create an action definition file (`NavigateToPose.action`):

```
# Goal
geometry_msgs/PoseStamped pose
float32 yaw_tolerance
---
# Result
int32 error_code
string error_string
---
# Feedback
geometry_msgs/PoseStamped current_pose
float32 distance_remaining
string message
```

### Action Server Implementation

```python
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math

class NavigateToPoseActionServer(Node):
    def __init__(self):
        super().__init__('navigate_to_pose_action_server')
        
        # Callback group for reentrant callbacks
        callback_group = ReentrantCallbackGroup()
        
        # Action server
        self._action_server = ActionServer(
            self,
            NavigateToPose,
            'navigate_to_pose',
            execute_callback=self.execute_callback,
            callback_group=callback_group,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback)
        
        # Subscriptions and publishers for navigation
        self.odom_sub = self.create_subscription(
            Odometry, 'odom', self.odom_callback, 10)
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        
        self.current_pose = None
        
    def goal_callback(self, goal_request):
        """Accept or reject a goal."""
        self.get_logger().info('Received goal request')
        return GoalResponse.ACCEPT
        
    def cancel_callback(self, goal_handle):
        """Accept or reject a cancel request."""
        self.get_logger().info('Received cancel request')
        return CancelResponse.ACCEPT
        
    def odom_callback(self, msg):
        """Update current pose from odometry."""
        self.current_pose = msg.pose.pose
        
    def execute_callback(self, goal_handle):
        """Execute the goal."""
        self.get_logger().info('Executing goal...')
        
        # Get goal information
        target_pose = goal_handle.request.pose.pose
        yaw_tolerance = goal_handle.request.yaw_tolerance
        
        # Feedback and result messages
        feedback_msg = NavigateToPose.Feedback()
        result_msg = NavigateToPose.Result()
        
        # Navigation loop
        while not self.is_at_goal(target_pose, yaw_tolerance):
            # Check if goal was cancelled
            if goal_handle.is_cancel_requested:
                result_msg.error_code = -1
                result_msg.error_string = "Goal was canceled"
                goal_handle.canceled()
                self.get_logger().info('Goal canceled')
                return result_msg
                
            # Calculate control commands
            cmd_vel = self.calculate_navigation_control(target_pose)
            
            # Publish command
            self.cmd_vel_pub.publish(cmd_vel)
            
            # Publish feedback
            if self.current_pose:
                feedback_msg.current_pose.pose = self.current_pose
                feedback_msg.distance_remaining = self.calculate_distance(
                    self.current_pose.position, 
                    target_pose.position
                )
                feedback_msg.message = f"Navigating, {feedback_msg.distance_remaining:.2f}m remaining"
                
                goal_handle.publish_feedback(feedback_msg)
                
            # Sleep to control loop rate
            time.sleep(0.1)
            
        # Goal reached
        result_msg.error_code = 0
        result_msg.error_string = "Goal reached successfully"
        goal_handle.succeed()
        
        # Stop the robot
        stop_cmd = Twist()
        self.cmd_vel_pub.publish(stop_cmd)
        
        self.get_logger().info('Goal succeeded')
        return result_msg
        
    def is_at_goal(self, target_pose, tolerance):
        """Check if robot is at the target pose."""
        if not self.current_pose:
            return False
            
        distance = self.calculate_distance(
            self.current_pose.position, 
            target_pose.position
        )
        
        # Check position and orientation
        return distance < tolerance and abs(self.get_yaw_error(target_pose)) < 0.1
        
    def calculate_navigation_control(self, target_pose):
        """Calculate velocity commands to reach target."""
        # Simple proportional controller
        cmd_vel = Twist()
        # ... implementation ...
        return cmd_vel
        
    def calculate_distance(self, pos1, pos2):
        """Calculate Euclidean distance between two positions."""
        dx = pos2.x - pos1.x
        dy = pos2.y - pos1.y
        return math.sqrt(dx*dx + dy*dy)
        
    def get_yaw_error(self, target_pose):
        """Calculate yaw error between current and target orientations."""
        # ... implementation ...
        return 0.0
```

### Action Client Example

```python
from rclpy.action import ActionClient
from rclpy.duration import Duration

class NavigationClient(Node):
    def __init__(self):
        super().__init__('navigation_client')
        
        self._action_client = ActionClient(
            self,
            NavigateToPose,
            'navigate_to_pose')
    
    def send_goal(self, target_pose):
        # Wait for action server
        self._action_client.wait_for_server()
        
        # Create goal message
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = target_pose
        goal_msg.yaw_tolerance = 0.1
        
        # Send goal and register callbacks
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback)
        
        self._send_goal_future.add_done_callback(self.goal_response_callback)
    
    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return
            
        self.get_logger().info('Goal accepted')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)
    
    def feedback_callback(self, feedback_msg):
        self.get_logger().info(
            f'Feedback: {feedback_msg.message}')
    
    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: {result.error_string}')
```

## Integration in Physical AI Systems

In Physical AI systems, these communication patterns work together to create sophisticated behaviors:

- **Topics** for continuous sensor data and actuator commands
- **Services** for discrete operations like calibration or configuration
- **Actions** for complex, long-running tasks like navigation or manipulation

### Example: Integrated Perception-Action Loop

```python
class PhysicalAIRobot(Node):
    def __init__(self):
        super().__init__('physical_ai_robot')
        
        # Publishers for commands
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.joint_cmd_pub = self.create_publisher(JointCommand, 'joint_commands', 10)
        
        # Subscribers for sensors
        self.lidar_sub = self.create_subscription(LaserScan, 'scan', self.lidar_callback, 10)
        self.camera_sub = self.create_subscription(Image, 'camera/image_raw', self.camera_callback, 10)
        
        # Services for discrete operations
        self.calibrate_srv = self.create_service(Calibrate, 'calibrate_sensors', self.calibrate_callback)
        
        # Actions for complex tasks
        self.nav_action_server = ActionServer(
            self, NavigateToPose, 'navigate_to_pose', self.navigate_execute)
        self.manip_action_server = ActionServer(
            self, ManipulateObject, 'manipulate_object', self.manipulate_execute)
        
        # Timer for main control loop
        self.control_timer = self.create_timer(0.1, self.control_loop)
        
    def control_loop(self):
        # Main control loop that integrates perception and action
        # Uses data from sensors to make decisions and send commands
        pass
```

## Best Practices for Communication Patterns

1. **Choose the right pattern**: Use topics for streaming data, services for request-response, and actions for long-running tasks
2. **Design efficient messages**: Keep message sizes reasonable for real-time performance
3. **Handle failures gracefully**: Implement error handling and recovery mechanisms
4. **Use appropriate QoS**: Match QoS settings to your application's requirements
5. **Monitor performance**: Track message rates, latencies, and resource usage

## Summary

This lesson covered the core communication patterns in ROS 2 that form the backbone of Physical AI systems. Understanding how to effectively use nodes, topics, services, and actions is essential for building robust, modular robotic applications.

## Exercises

1. Create a node that subscribes to sensor data and publishes processed information
2. Implement a service that performs a computation based on input parameters
3. Design an action that controls a simulated robot to perform a complex task
4. Integrate multiple communication patterns in a single node to demonstrate their combined use