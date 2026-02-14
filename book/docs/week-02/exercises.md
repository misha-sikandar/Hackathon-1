---
sidebar_position: 7
---

# Week 2 Exercises: ROS 2 Fundamentals

This exercise sheet accompanies the Week 2 lessons on ROS 2 fundamentals. These exercises will help you practice and reinforce your understanding of nodes, topics, services, and actions in the context of Physical AI systems.

## Exercise 1: Temperature Monitoring System

Create a ROS 2 system that simulates a temperature monitoring system for a humanoid robot. This system should include:

### Part A: Publisher Node
- Create a node called `temperature_sensor` that publishes temperature readings to a topic called `temperature_readings`
- The message should include the temperature value and timestamp
- Publish readings every 2 seconds with realistic temperature fluctuations around 25°C

### Part B: Subscriber Node
- Create a node called `temperature_monitor` that subscribes to the `temperature_readings` topic
- Log the received temperatures and calculate running statistics (average, min, max)
- If temperature exceeds 35°C, log a warning message

### Part C: Service Integration
- Add a service to the `temperature_monitor` node called `get_temperature_stats` that returns the current average, min, and max temperatures
- Create a client node that periodically calls this service and displays the results

### Solution Template

```python
# temperature_sensor.py
import rclpy
from rclpy.node import Node
import random
from std_msgs.msg import Float32
from builtin_interfaces.msg import Time

class TemperatureSensor(Node):
    def __init__(self):
        super().__init__('temperature_sensor')
        self.publisher = self.create_publisher(Float32, 'temperature_readings', 10)
        timer_period = 2  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.base_temp = 25.0  # Base temperature in Celsius

    def timer_callback(self):
        msg = Float32()
        # Add some realistic variation to the temperature
        msg.data = self.base_temp + random.uniform(-2, 5)
        self.publisher.publish(msg)
        self.get_logger().info(f'Publishing: {msg.data:.2f}°C')

def main(args=None):
    rclpy.init(args=args)
    temp_sensor = TemperatureSensor()
    rclpy.spin(temp_sensor)
    temp_sensor.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Exercise 2: Robot Navigation Service

Create a ROS 2 service that calculates the optimal path for a robot to navigate between two points in a 2D space, considering obstacles.

### Requirements:
- Create a custom service called `GetOptimalPath` with:
  - Request: start position (x, y), end position (x, y), list of obstacles (each with position and radius)
  - Response: path as a list of waypoints, success flag, error message
- Implement a simple pathfinding algorithm (e.g., A* or Dijkstra's) to compute the path
- Create a client that sends a request and displays the resulting path

### Solution Template

```python
# In your srv directory, create GetOptimalPath.srv:
# geometry_msgs/Point start_point
# geometry_msgs/Point end_point
# geometry_msgs/Point[] obstacles
# float32[] obstacle_radii
# ---
# geometry_msgs/Point[] path
# bool success
# string error_message
```

## Exercise 3: Action-Based Robot Arm Controller

Create an action server that controls a simulated robot arm to move to specified joint angles with feedback on progress.

### Requirements:
- Create a custom action called `MoveArmJoints` with:
  - Goal: target joint angles (array of floats)
  - Feedback: current joint angles, percentage completion
  - Result: success flag, error message
- Implement the action server with realistic movement simulation
- Create a client that sends goals and monitors progress

### Solution Template

```python
# In your action directory, create MoveArmJoints.action:
# float32[] target_angles
# duration movement_duration
# ---
# bool success
# string error_message
# ---
# float32[] current_angles
# float32 progress_percentage
# string status_message
```

## Exercise 4: Multi-Node Integration

Combine the concepts from the previous exercises into a single system:

### Requirements:
- Integrate the temperature monitoring system with the navigation service
- When temperature exceeds 35°C, automatically trigger a "cooling" behavior using an action
- The cooling action should move the robot to a designated "cooling zone"
- Use launch files to start all nodes simultaneously

### Launch File Template

```python
# robot_system_launch.py
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='your_package_name',
            executable='temperature_sensor',
            name='temperature_sensor'
        ),
        Node(
            package='your_package_name',
            executable='temperature_monitor',
            name='temperature_monitor'
        ),
        Node(
            package='your_package_name',
            executable='navigation_server',
            name='navigation_server'
        ),
        # Add more nodes as needed
    ])
```

## Exercise 5: Quality of Service (QoS) Experimentation

Experiment with different QoS profiles to understand their impact on communication:

### Requirements:
- Create a publisher with reliable QoS settings
- Create a publisher with best-effort QoS settings
- Create subscribers with matching and mismatched QoS settings
- Observe how message delivery changes based on QoS configurations
- Document your findings about when to use different QoS profiles

## Challenge Exercise: Physical AI Scenario

Design and implement a complete scenario that demonstrates Physical AI principles:

### Scenario: Adaptive Robot Assistant
A robot assistant that adapts its behavior based on environmental conditions and user needs.

### Requirements:
- Temperature monitoring system (from Exercise 1)
- Navigation system (from Exercise 2)
- Manipulation system (from Exercise 3)
- Additional sensors (simulated)
- Decision-making node that coordinates all systems
- Emergency behaviors triggered by sensor thresholds

### Implementation Notes:
- Use topics for continuous sensor data and actuator commands
- Use services for discrete operations like calibration or requesting specific actions
- Use actions for complex, long-running tasks like navigation or manipulation
- Implement a central coordinator node that integrates all systems
- Add safety mechanisms that override normal behavior when needed

## Submission Requirements

For each exercise, submit:
1. Source code files
2. Launch files (if applicable)
3. Brief documentation explaining your implementation
4. Results/output from running your nodes
5. Reflection on challenges faced and how you solved them

## Evaluation Criteria

- Correct implementation of ROS 2 concepts
- Proper use of nodes, topics, services, and actions
- Code quality and documentation
- Successful integration of multiple components
- Understanding of when to use different communication patterns
- Creativity in solving the challenge exercise

## Resources

- ROS 2 Documentation: https://docs.ros.org/en/humble/
- ROS 2 Tutorials: https://docs.ros.org/en/humble/Tutorials.html
- Quality of Service Guide: https://docs.ros.org/en/humble/Concepts/About-Quality-of-Service-Settings.html