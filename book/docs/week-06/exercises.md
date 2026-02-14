---
sidebar_position: 19
---

# Week 6 Exercises: SLAM and Navigation

This exercise sheet accompanies the Week 6 lessons on SLAM and navigation. These exercises will help you practice and reinforce your understanding of mapping, localization, and navigation in Physical AI systems.

## Exercise 1: Implement a Basic SLAM System

Create a simple 2D SLAM system using landmark-based mapping:

### Requirements:
- Implement an Extended Kalman Filter (EKF) for SLAM
- Create a simulation environment with known landmarks
- Implement sensor models for range and bearing measurements
- Visualize the robot trajectory and map
- Evaluate the accuracy of the estimated map

### Implementation Steps:
1. Create a 2D environment with known landmarks
2. Implement the EKF-SLAM algorithm
3. Simulate robot motion and sensor measurements
4. Visualize the robot's belief about its pose and the map
5. Compare estimated map with ground truth

### Template for EKF SLAM:
```python
import numpy as np
import matplotlib.pyplot as plt

class EKFSLAM:
    def __init__(self, initial_pose, map_size):
        # Initialize state vector [x, y, theta, lm_x1, lm_y1, ...]
        self.state = np.zeros(3 + 2*map_size)  # 3 for robot pose + 2 per landmark
        self.state[:3] = initial_pose  # Initial robot pose
        
        # Initialize covariance matrix
        self.covariance = np.eye(len(self.state)) * 0.1
        
        # Process and measurement noise
        self.Q = np.diag([0.1, 0.1, 0.05])  # Process noise
        self.R = np.diag([0.1, 0.05])       # Measurement noise (range, bearing)
    
    def predict(self, control_input, dt):
        """Prediction step of EKF"""
        # Implement motion model
        pass
    
    def update(self, measurement, landmark_id):
        """Update step of EKF"""
        # Implement measurement update
        pass
```

## Exercise 2: Configure and Run Nav2

Set up and configure the Navigation2 stack:

### Requirements:
- Install Navigation2 packages
- Configure a robot for navigation
- Set up costmap parameters
- Configure path planners and controllers
- Test navigation in simulation

### Implementation Steps:
1. Install Nav2 packages
2. Create a robot description package
3. Configure Nav2 parameters (costmaps, planners, controllers)
4. Launch navigation stack in simulation
5. Send navigation goals and observe behavior

### Nav2 Configuration Template:
```yaml
# nav2_params.yaml
amcl:
  ros__parameters:
    use_sim_time: True
    alpha1: 0.2
    alpha2: 0.2
    alpha3: 0.2
    alpha4: 0.2
    alpha5: 0.2
    base_frame_id: "base_footprint"
    # ... additional parameters

controller_server:
  ros__parameters:
    use_sim_time: True
    controller_frequency: 20.0
    min_x_velocity_threshold: 0.001
    # ... additional parameters
```

## Exercise 3: Custom Path Planner Plugin

Create a custom path planner plugin for Nav2:

### Requirements:
- Implement a new global planner plugin
- Follow Nav2 plugin architecture
- Integrate with Nav2's plugin system
- Test the planner in simulation
- Compare performance with default planners

### Implementation Steps:
1. Create a new ROS 2 package for the planner
2. Implement the Nav2 global planner interface
3. Build and register the plugin
4. Configure Nav2 to use your planner
5. Test and evaluate performance

### Plugin Interface Template:
```cpp
// custom_planner.hpp
#include <nav2_core/global_planner.h>
#include <nav2_costmap_2d/costmap_2d_ros.h>
#include <nav2_util/lifecycle_node.hpp>

namespace custom_planner {

class CustomPlanner : public nav2_core::GlobalPlanner {
public:
    void configure(
        const rclcpp_lifecycle::LifecycleNode::WeakPtr & parent,
        std::string name,
        std::shared_ptr<nav2_costmap_2d::Costmap2DROS> costmap_ros) override;
    
    void cleanup() override;
    void activate() override;
    void deactivate() override;
    
    nav_msgs::msg::Path createPlan(
        const geometry_msgs::msg::PoseStamped & start,
        const geometry_msgs::msg::PoseStamped & goal) override;
    
private:
    // Your planner implementation
};

} // namespace custom_planner
```

## Exercise 4: Dynamic Obstacle Integration

Enhance navigation to handle dynamic obstacles:

### Requirements:
- Detect dynamic obstacles using perception system
- Update costmaps with dynamic obstacle information
- Implement dynamic path replanning
- Test navigation in presence of moving obstacles
- Evaluate navigation performance with dynamic obstacles

### Implementation Steps:
1. Create a node to detect and track dynamic obstacles
2. Integrate dynamic obstacle information with costmaps
3. Implement replanning when obstacles are detected
4. Test in simulation with moving obstacles
5. Analyze performance metrics

## Exercise 5: Multi-Robot Navigation

Implement coordination for multiple robots navigating in the same space:

### Requirements:
- Set up multiple robots in simulation
- Implement communication between robots
- Coordinate navigation to avoid conflicts
- Implement reservation-based path planning
- Test multi-robot navigation scenarios

### Implementation Steps:
1. Create simulation with multiple robots
2. Implement communication protocol for coordination
3. Develop reservation system for path planning
4. Test various multi-robot scenarios
5. Evaluate coordination effectiveness

## Exercise 6: Navigation Performance Evaluation

Develop a framework to evaluate navigation performance:

### Requirements:
- Create metrics for navigation success (success rate, time, path efficiency)
- Implement automated testing framework
- Generate reports on navigation performance
- Visualize navigation trajectories and metrics
- Test navigation under various conditions

### Metrics to Implement:
- Success rate (percentage of successful navigations)
- Average time to goal
- Path efficiency (optimal path length / actual path length)
- Average execution velocity
- Number of recovery behaviors triggered

## Exercise 7: Perception-Integrated Navigation

Create a navigation system that incorporates perception data:

### Requirements:
- Integrate object detection with navigation
- Modify costmaps based on detected objects
- Implement semantic navigation (navigate to objects)
- Handle uncertain perception data
- Test in environments with various objects

### Implementation Steps:
1. Set up object detection pipeline
2. Integrate detections with navigation system
3. Modify costmaps based on object semantics
4. Implement goal selection based on detected objects
5. Test in diverse environments

## Exercise 8: Hierarchical Navigation

Implement hierarchical path planning (coarse-to-fine):

### Requirements:
- Create multiple resolution maps
- Implement coarse global planning
- Implement fine local planning
- Coordinate between different planning levels
- Evaluate improvement over single-resolution planning

### Implementation Steps:
1. Generate multi-resolution maps
2. Implement coarse-level planner
3. Implement fine-level planner
4. Coordinate between levels
5. Compare performance with single-resolution approach

## Challenge Exercise: Complete Navigation System

Create a complete navigation system that includes:

### Requirements:
- SLAM for map building and localization
- Path planning with multiple algorithms
- Dynamic obstacle handling
- Multi-robot coordination
- Performance evaluation framework
- Integration with perception system
- Robust error handling and recovery

### Additional Requirements:
- Document the complete system architecture
- Provide configuration for different robot types
- Include simulation and real-robot testing
- Demonstrate all key navigation capabilities

## Submission Requirements

For each exercise, submit:
1. Source code for all nodes and packages
2. Configuration files and parameters
3. Launch files for testing
4. Performance benchmarks and metrics
5. Screenshots or videos of execution
6. Documentation of challenges and solutions
7. Comparative analysis where applicable

## Evaluation Criteria

- Correct implementation of SLAM algorithms
- Proper configuration and use of Nav2
- Quality of custom path planner implementation
- Effectiveness of dynamic obstacle handling
- Performance evaluation methodology
- Understanding of navigation challenges in Physical AI
- Creativity in solving the challenge exercise

## Resources

- Navigation2 Tutorials: https://navigation.ros.org/tutorials/
- ROS 2 Navigation: http://docs.ros.org/en/humble/p/robot_navigation/
- Cartographer: https://google-cartographer-ros.readthedocs.io/
- OMPL: https://ompl.kavrakilab.org/