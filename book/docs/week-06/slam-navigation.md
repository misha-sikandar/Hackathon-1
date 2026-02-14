# Week 6: SLAM & Navigation for Physical AI Systems

This week, we'll explore Simultaneous Localization and Mapping (SLAM) and robot navigation, which are fundamental capabilities for autonomous robots in Physical AI systems. These technologies enable robots to understand their environment and navigate effectively in unknown spaces.

## Learning Objectives

By the end of this week, you will be able to:

1. Understand SLAM algorithms and their applications
2. Implement mapping and localization systems
3. Configure and use Navigation2 for robot navigation
4. Plan and execute navigation tasks in complex environments
5. Integrate perception with navigation for robust operation
6. Evaluate navigation performance and safety

## Introduction to SLAM

SLAM (Simultaneous Localization and Mapping) is a fundamental problem in robotics where a robot builds a map of an unknown environment while simultaneously keeping track of its location within that map. This is crucial for Physical AI systems that need to operate autonomously in real-world environments.

### Why SLAM Matters for Physical AI

SLAM is essential for Physical AI systems because:

- **Autonomous Operation**: Enables robots to navigate without prior knowledge of the environment
- **Spatial Awareness**: Creates representations of the environment for planning and reasoning
- **Localization**: Allows robots to determine their position in the world
- **Dynamic Adaptation**: Updates maps as the environment changes
- **Multi-Robot Coordination**: Provides shared spatial understanding for teams

### SLAM Approaches

There are several approaches to SLAM:

1. **Visual SLAM**: Uses cameras to extract features and landmarks
2. **LiDAR SLAM**: Uses LiDAR sensors for precise distance measurements
3. **Visual-Inertial SLAM**: Combines visual and IMU data for robust tracking
4. **Multi-Sensor SLAM**: Integrates multiple sensor modalities

## LiDAR SLAM with Cartographer

Google's Cartographer is a popular SLAM library that provides real-time simultaneous localization and mapping in 2D and 3D environments.

### Cartographer Concepts

Cartographer uses a probabilistic approach to SLAM:

- **Submaps**: Local maps that are stitched together to form a global map
- **Scan Matching**: Aligns incoming sensor data with existing submaps
- **Loop Closure**: Detects when the robot revisits a location to correct drift
- **Global Optimization**: Refines the map using constraint-based optimization

### Cartographer Configuration

Here's an example configuration for 2D LiDAR SLAM:

```lua
-- lua configuration for Cartographer 2D SLAM
options = {
  map_builder = MAP_BUILDER,
  trajectory_builder = TRAJECTORY_BUILDER,
  map_frame = "map",
  tracking_frame = "base_link",
  published_frame = "base_link",
  odom_frame = "odom",
  provide_odom_frame = true,
  publish_frame_projected_to_2d = true,
  use_odometry = false,
  use_nav_sat = false,
  use_landmarks = false,
  num_laser_scans = 1,
  num_multi_echo_laser_scans = 0,
  num_subdivisions_per_laser_scan = 1,
  num_point_clouds = 0,
  lookup_transform_timeout_sec = 0.2,
  submap_publish_period_sec = 0.3,
  pose_publish_period_sec = 5e-3,
  trajectory_publish_period_sec = 30e-3,
  rangefinder_sampling_ratio = 1.,
  odometry_sampling_ratio = 1.,
  fixed_frame_pose_sampling_ratio = 1.,
  imu_sampling_ratio = 1.,
  landmarks_sampling_ratio = 1.,
}

MAP_BUILDER.use_trajectory_builder_2d = true

TRAJECTORY_BUILDER_2D = {
  minimum_turning_radius = 0.1,
  max_range = 20.,
  min_range = 0.3,
  missing_data_ray_length = 5.,
  num_accumulated_range_data = 1,
  voxel_filter_size = 0.025,

  adaptive_voxel_filter = {
    max_length = 0.9,
    min_num_points = 100,
    max_range = 30.,
  },

  loop_closure_adaptive_voxel_filter = {
    max_length = 0.9,
    min_num_points = 100,
    max_range = 30.,
  },

  use_online_correlative_scan_matching = true,
  real_time_correlative_scan_matcher = {
    linear_search_window = 0.1,
    angular_search_window = math.rad(20.),
    translation_delta_cost_weight = 1e-1,
    rotation_delta_cost_weight = 1e-1,
  },

  ceres_scan_matcher = {
    occupied_space_weight = 20.,
    translation_weight = 10.,
    rotation_weight = 1.,
    ceres_solver_options = {
      use_nonmonotonic_steps = false,
      max_num_iterations = 50,
      num_threads = 1,
    },
  },

  motion_filter = {
    max_time_seconds = 5.,
    max_distance_meters = 0.2,
    max_angle_radians = math.rad(1.),
  },

  -- Different sampling parameters for dense trajectories.
  -- Faster and less strict in the beginning when the trajectory is far from
  -- closed, tighter when closing the loop.
  -- The parameters are chosen to close the loop at medium speed driving.
  -- For slow driving we expect lower coverage and vice versa.
  -- TODO(gaschler): Consider dynamically adjusting these parameters based
  -- on the current trajectory speed.
  submaps = {
    num_range_data = 90,
    grid_options_2d = {
      grid_type = "PROBABILITY_GRID",
      resolution = 0.05,
    },
    range_data_inserter = {
      probability_grid_range_data_inserter = {
        insert_free_space = true,
        hit_probability = 0.55,
        miss_probability = 0.45,
      },
    },
    -- It is valid to scale to more submaps to allow for more sparsity.
    -- However, matching in the higher resolution is more computationally
    -- intensive.
    num_restriction = 3,
  },

  max_submaps_to_keep = nil,
  -- It is valid to have no global localizations (but loops are still
  -- detected).
  global_localization_min_score = 0.6,
}

POSE_GRAPH = {
  optimize_every_n_nodes = 360,
  constraint_builder = {
    sampling_ratio = 0.3,
    max_constraint_distance = 15.,
    min_score = 0.5,
    global_localization_min_score = 0.6,
    loop_closure_translation_weight = 1.1e4,
    loop_closure_rotation_weight = 1.0e5,
    log_matches = true,
    fast_correlative_scan_matcher = {
      linear_search_window = 7.,
      angular_search_window = math.rad(30.),
      branch_and_bound_depth = 7,
    },
    ceres_scan_matcher = {
      occupied_space_weight = 50.,
      translation_weight = 10.,
      rotation_weight = 1.,
      ceres_solver_options = {
        use_nonmonotonic_steps = false,
        max_num_iterations = 10,
        num_threads = 1,
      },
    },
    fast_correlative_scan_matcher_3d = {
      branch_and_bound_depth = 8,
      full_resolution_depth = 3,
      min_rotational_score = 0.77,
      min_low_resolution_score = 0.55,
      linear_xy_search_window = 5.,
      linear_z_search_window = 1.,
      angular_search_window = math.rad(15.),
    },
    ceres_scan_matcher_3d = {
      occupied_space_weight_0 = 20.,
      occupied_space_weight_1 = 60.,
      translation_weight = 10.,
      rotation_weight = 1.,
      only_optimize_yaw = true,
      ceres_solver_options = {
        use_nonmonotonic_steps = false,
        max_num_iterations = 10,
        num_threads = 1,
      },
    },
  },
  matcher_translation_weight = 5e2,
  matcher_rotation_weight = 1.6e3,
  optimization_problem = {
    huber_scale = 1e1,
    acceleration_weight = 1.0e3,
    rotation_weight = 3.0e4,
    local_slam_pose_translation_weight = 1e5,
    local_slam_pose_rotation_weight = 1e5,
    odometry_translation_weight = 1e2,
    odometry_rotation_weight = 1e2,
    fixed_frame_pose_translation_weight = 1e1,
    fixed_frame_pose_rotation_weight = 1e2,
    log_solver_summary = false,
    ceres_solver_options = {
      use_nonmonotonic_steps = false,
      max_num_iterations = 50,
      num_threads = 7,
    },
  },
  max_num_final_iterations = 200,
  global_sampling_ratio = 0.003,
  log_residual_histograms = true,
  global_constraint_isr_for_static_penalty_ratio = 0.9,
  global_constraint_max_static_penalty = 1e5,
  global_constraint_min_static_penalty = 1e4,
}

return options
```

## Navigation2 (Nav2) Framework

Navigation2 is the next-generation navigation framework for ROS 2, designed to be more robust, flexible, and performant than its predecessor.

### Nav2 Architecture

Nav2 follows a behavior tree-based architecture:

- **Navigator**: High-level navigation orchestrator
- **Behavior Trees**: Define navigation behaviors and decision-making
- **Plugins**: Modular components for different functionalities
- **Lifecycle Manager**: Manages the state of navigation components

### Nav2 Core Components

1. **Map Server**: Provides static map information
2. **Local Planner**: Generates velocity commands for immediate navigation
3. **Global Planner**: Computes optimal path from start to goal
4. **Controller**: Converts planned path to velocity commands
5. **Recovery Behaviors**: Handles navigation failures
6. **Smoother**: Smooths computed paths

### Nav2 Configuration

Here's an example Nav2 configuration file:

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
    beam_skip_distance: 0.5
    beam_skip_error_threshold: 0.9
    beam_skip_threshold: 0.3
    do_beamskip: false
    global_frame_id: "map"
    lambda_short: 0.1
    laser_likelihood_max_dist: 2.0
    laser_max_range: 100.0
    laser_min_range: -1.0
    laser_model_type: "likelihood_field"
    max_beams: 60
    max_particles: 2000
    min_particles: 500
    odom_frame_id: "odom"
    pf_err: 0.05
    pf_z: 0.99
    recovery_alpha_fast: 0.0
    recovery_alpha_slow: 0.0
    resample_interval: 1
    robot_model_type: "nav2_amcl::DifferentialMotionModel"
    save_pose_rate: 0.5
    sigma_hit: 0.2
    tf_broadcast: true
    transform_tolerance: 1.0
    update_min_a: 0.2
    update_min_d: 0.2
    z_hit: 0.5
    z_max: 0.05
    z_rand: 0.5
    z_short: 0.05
    scan_topic: scan

bt_navigator:
  ros__parameters:
    use_sim_time: True
    global_frame: map
    robot_frame: base_link
    odom_topic: /odom
    bt_loop_duration: 10
    default_server_timeout: 20
    enable_groot_monitoring: True
    groot_zmq_publisher_port: 1666
    groot_zmq_server_port: 1667
    default_nav_through_poses_bt_xml: bt_navigator.xml
    default_nav_to_pose_bt_xml: bt_navigator.xml
    plugin_lib_names:
    - nav2_compute_path_to_pose_action_bt_node
    - nav2_compute_path_through_poses_action_bt_node
    - nav2_follow_path_action_bt_node
    - nav2_spin_action_bt_node
    - nav2_wait_action_bt_node
    - nav2_assisted_teleop_action_bt_node
    - nav2_back_up_action_bt_node
    - nav2_drive_on_heading_bt_node
    - nav2_clear_costmap_service_bt_node
    - nav2_is_stuck_condition_bt_node
    - nav2_goal_reached_condition_bt_node
    - nav2_goal_updated_condition_bt_node
    - nav2_initial_pose_received_condition_bt_node
    - nav2_reinitialize_global_localization_service_bt_node
    - nav2_rate_controller_bt_node
    - nav2_distance_controller_bt_node
    - nav2_speed_controller_bt_node
    - nav2_truncate_path_action_bt_node
    - nav2_truncate_path_local_action_bt_node
    - nav2_goal_updater_node_bt_node
    - nav2_recovery_node_bt_node
    - nav2_pipeline_sequence_bt_node
    - nav2_round_robin_node_bt_node
    - nav2_transform_available_condition_bt_node
    - nav2_time_expired_condition_bt_node
    - nav2_path_expiring_timer_condition
    - nav2_distance_traveled_condition_bt_node
    - nav2_single_trigger_bt_node
    - nav2_is_battery_low_condition_bt_node
    - nav2_navigate_through_poses_action_bt_node
    - nav2_navigate_to_pose_action_bt_node
    - nav2_remove_passed_goals_action_bt_node
    - nav2_planner_selector_bt_node
    - nav2_controller_selector_bt_node
    - nav2_goal_checker_selector_bt_node

controller_server:
  ros__parameters:
    use_sim_time: True
    controller_frequency: 20.0
    min_x_velocity_threshold: 0.001
    min_y_velocity_threshold: 0.5
    min_theta_velocity_threshold: 0.001
    progress_checker_plugin: "progress_checker"
    goal_checker_plugin: "goal_checker"
    controller_plugins: ["FollowPath"]
    
    FollowPath:
      plugin: "nav2_mppi_controller::MPPIController"
      time_steps: 50
      model_dt: 0.05
      batch_size: 1000
      vx_std: 0.2
      vy_std: 0.05
      wz_std: 0.3
      vx_max: 0.5
      vx_min: -0.3
      vy_max: 0.3
      wz_max: 1.0
      xy_goal_tolerance: 0.25
      yaw_goal_tolerance: 0.1
      sim_frequency: 20.0
      control_frequency: 20.0
      motion_model: "DiffDrive"
      weight: [0.2, 0.2, 0.2, 0.2, 0.2]
      reference_heading: 1.0
      temperature: 0.3
      gamma: 0.01
      lambda: 0.05
      use_fleet_analyzer: false

local_costmap:
  local_costmap:
    ros__parameters:
      update_frequency: 5.0
      publish_frequency: 2.0
      global_frame: odom
      robot_base_frame: base_link
      use_sim_time: True
      rolling_window: true
      width: 3
      height: 3
      resolution: 0.05
      robot_radius: 0.22
      plugins: ["voxel_layer", "inflation_layer"]
      inflation_layer:
        plugin: "nav2_costmap_2d::InflationLayer"
        cost_scaling_factor: 3.0
        inflation_radius: 0.55
      voxel_layer:
        plugin: "nav2_costmap_2d::VoxelLayer"
        enabled: True
        publish_voxel_map: True
        origin_z: 0.0
        z_resolution: 0.05
        z_voxels: 16
        max_obstacle_height: 2.0
        mark_threshold: 0
        observation_sources: scan
        scan:
          topic: /scan
          max_obstacle_height: 2.0
          clearing: True
          marking: True
          data_type: "LaserScan"
          raytrace_max_range: 3.0
          raytrace_min_range: 0.0
          obstacle_max_range: 2.5
          obstacle_min_range: 0.0
          
global_costmap:
  global_costmap:
    ros__parameters:
      update_frequency: 1.0
      publish_frequency: 1.0
      global_frame: map
      robot_base_frame: base_link
      use_sim_time: True
      robot_radius: 0.22
      resolution: 0.05
      track_unknown_space: true
      plugins: ["static_layer", "obstacle_layer", "inflation_layer"]
      obstacle_layer:
        plugin: "nav2_costmap_2d::ObstacleLayer"
        enabled: True
        observation_sources: scan
        scan:
          topic: /scan
          max_obstacle_height: 2.0
          clearing: True
          marking: True
          data_type: "LaserScan"
          raytrace_max_range: 3.0
          raytrace_min_range: 0.0
          obstacle_max_range: 2.5
          obstacle_min_range: 0.0
      static_layer:
        plugin: "nav2_costmap_2d::StaticLayer"
        map_subscribe_transient_local: True
      inflation_layer:
        plugin: "nav2_costmap_2d::InflationLayer"
        cost_scaling_factor: 3.0
        inflation_radius: 0.55

planner_server:
  ros__parameters:
    expected_planner_frequency: 20.0
    planner_plugins: ["GridBased"]
    GridBased:
      plugin: "nav2_navfn_planner::NavfnPlanner"
      tolerance: 0.5
      use_astar: false
      allow_unknown: true
```

### Launching Nav2

```python
# Example launch file for Nav2
# navigation_launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from nav2_common.launch import RewrittenYaml

def generate_launch_description():
    # Declare launch arguments
    use_sim_time = LaunchConfiguration('use_sim_time')
    autostart = LaunchConfiguration('autostart')
    params_file = LaunchConfiguration('params_file')
    bt_xml_file = LaunchConfiguration('bt_xml_file')
    map_topic = LaunchConfiguration('map')
    cmd_vel_topic = LaunchConfiguration('cmd_vel_topic')  
    odom_topic = LaunchConfiguration('odom_topic')

    # Create launch description
    ld = LaunchDescription()

    # Declare launch arguments
    declare_use_sim_time_argument = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation (Gazebo) clock if true')

    declare_autostart_cmd = DeclareLaunchArgument(
        'autostart', 
        default_value='true',
        description='Automatically startup the nav2 stack')

    declare_params_file_cmd = DeclareLaunchArgument(
        'params_file',
        default_value='nav2_params.yaml',
        description='Full path to the ROS2 parameters file to use for all launched nodes')

    declare_bt_xml_cmd = DeclareLaunchArgument(
        'bt_xml_file',
        default_value='navigate_w_replanning_and_recovery.xml',
        description='Full path to the behavior tree xml file to use')

    declare_map_topic_cmd = DeclareLaunchArgument(
        'map',
        default_value='/map',
        description='Topic name for the map')

    declare_cmd_vel_topic_cmd = DeclareLaunchArgument(
        'cmd_vel_topic',
        default_value='/cmd_vel',
        description='Topic name for velocity commands')

    declare_odom_topic_cmd = DeclareLaunchArgument(
        'odom_topic', 
        default_value='/odom',
        description='Topic name for odometry')

    # Add launch arguments to launch description
    ld.add_action(declare_use_sim_time_argument)
    ld.add_action(declare_autostart_cmd)
    ld.add_action(declare_params_file_cmd)
    ld.add_action(declare_bt_xml_cmd)
    ld.add_action(declare_map_topic_cmd)
    ld.add_action(declare_cmd_vel_topic_cmd)
    ld.add_action(declare_odom_topic_cmd)

    # Map server
    map_server_node = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        parameters=[{'use_sim_time': use_sim_time},
                    {'topic_name': map_topic}],
        output='screen'
    )

    # Lifecycle manager
    lifecycle_manager = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager',
        parameters=[{'use_sim_time': use_sim_time},
                    {'autostart': autostart},
                    {'node_names': ['map_server', 'amcl', 'controller_server',
                                   'planner_server', 'recoveries_server',
                                   'bt_navigator', 'waypoint_follower']}],
        output='screen'
    )

    # Add nodes to launch description
    ld.add_action(map_server_node)
    ld.add_action(lifecycle_manager)

    return ld
```

## Path Planning Algorithms

### Global Path Planning

Global planners compute optimal paths from start to goal:

```python
import numpy as np
import heapq
from typing import List, Tuple

class AStarPlanner:
    def __init__(self, occupancy_grid: np.ndarray, resolution: float = 1.0):
        """
        A* path planner for grid-based maps
        
        Args:
            occupancy_grid: 2D array where 0 = free, 1 = occupied
            resolution: Size of each grid cell in meters
        """
        self.grid = occupancy_grid
        self.resolution = resolution
        self.height, self.width = occupancy_grid.shape
    
    def heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        """Manhattan distance heuristic"""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def neighbors(self, node: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get valid neighbors of a node"""
        x, y = node
        neighbors_list = []
        
        # 8-connected neighborhood
        for dx, dy in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
            nx, ny = x + dx, y + dy
            
            if (0 <= nx < self.width and 
                0 <= ny < self.height and 
                self.grid[ny, nx] == 0):  # Free space
                # Add diagonal movement cost
                cost = 1.414 if abs(dx) + abs(dy) == 2 else 1.0  # Diagonal vs straight
                neighbors_list.append(((nx, ny), cost))
        
        return neighbors_list
    
    def plan_path(self, start: Tuple[float, float], goal: Tuple[float, float]) -> List[Tuple[float, float]]:
        """
        Plan path using A* algorithm
        
        Args:
            start: Start position in meters (x, y)
            goal: Goal position in meters (x, y)
            
        Returns:
            List of waypoints in meters [(x, y), ...]
        """
        # Convert meters to grid coordinates
        start_grid = (int(start[0] / self.resolution), int(start[1] / self.resolution))
        goal_grid = (int(goal[0] / self.resolution), int(goal[1] / self.resolution))
        
        # Check if start and goal are valid
        if (not (0 <= start_grid[0] < self.width and 0 <= start_grid[1] < self.height) or
            not (0 <= goal_grid[0] < self.width and 0 <= goal_grid[1] < self.height)):
            return []
        
        if self.grid[start_grid[1], start_grid[0]] == 1 or self.grid[goal_grid[1], goal_grid[0]] == 1:
            return []  # Start or goal is in obstacle
        
        # A* algorithm
        frontier = [(0, start_grid)]
        came_from = {start_grid: None}
        cost_so_far = {start_grid: 0}
        
        while frontier:
            _, current = heapq.heappop(frontier)
            
            if current == goal_grid:
                break
            
            for next_node, move_cost in self.neighbors(current):
                new_cost = cost_so_far[current] + move_cost
                
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + self.heuristic(goal_grid, next_node)
                    heapq.heappush(frontier, (priority, next_node))
                    came_from[next_node] = current
        
        # Reconstruct path
        path = []
        current = goal_grid
        if current in came_from:
            while current is not None:
                # Convert grid coordinates back to meters
                x_meters = current[0] * self.resolution
                y_meters = current[1] * self.resolution
                path.append((x_meters, y_meters))
                current = came_from[current]
            
            path.reverse()  # Reverse to get start->goal order
        
        return path

# Example usage
def example_path_planning():
    # Create a simple occupancy grid (0 = free, 1 = occupied)
    grid = np.zeros((20, 20))
    # Add some obstacles
    grid[5, 2:8] = 1  # Horizontal wall
    grid[10, 10:18] = 1  # Another wall
    grid[15, 5:15] = 1  # Bottom wall
    
    planner = AStarPlanner(grid, resolution=0.5)
    path = planner.plan_path((1.0, 1.0), (18.0, 18.0))
    
    print(f"Found path with {len(path)} waypoints")
    if path:
        print(f"Start: {path[0]}, End: {path[-1]}")
    
    return path

example_path_planning()
```

### Local Path Planning and Control

Local planners adjust the robot's trajectory in real-time:

```python
import numpy as np
from geometry_msgs.msg import Twist, PoseStamped
from nav_msgs.msg import Path
from sensor_msgs.msg import LaserScan
from typing import List, Tuple

class LocalPlanner:
    def __init__(self, max_vel: float = 0.5, max_ang_vel: float = 1.0):
        """
        Local path planner for real-time navigation
        """
        self.max_linear_vel = max_vel
        self.max_angular_vel = max_ang_vel
        
        # Robot parameters
        self.radius = 0.3  # Robot radius in meters
        self.safe_distance = 0.5  # Safe distance from obstacles
        
        # Current state
        self.current_pose = None
        self.current_twist = None
        self.laser_data = None
        
    def update_pose(self, pose: PoseStamped):
        """Update robot's current pose"""
        self.current_pose = pose
    
    def update_laser(self, scan: LaserScan):
        """Update laser scan data"""
        self.laser_data = scan
    
    def compute_velocity(self, global_path: Path) -> Twist:
        """
        Compute velocity command based on global path and local obstacles
        
        Args:
            global_path: Global path to follow
            
        Returns:
            Velocity command (Twist)
        """
        cmd_vel = Twist()
        
        if not global_path.poses or not self.current_pose:
            return cmd_vel
        
        # Get next waypoint from global path
        next_waypoint = self.get_next_waypoint(global_path)
        
        if next_waypoint is None:
            return cmd_vel
        
        # Calculate desired direction
        dx = next_waypoint.pose.position.x - self.current_pose.pose.position.x
        dy = next_waypoint.pose.position.y - self.current_pose.pose.position.y
        
        # Calculate desired heading
        desired_heading = np.arctan2(dy, dx)
        
        # Get current heading (assuming we have orientation)
        current_heading = self.get_current_heading()
        
        # Calculate heading error
        heading_error = self.normalize_angle(desired_heading - current_heading)
        
        # Adjust velocities based on heading error and obstacles
        linear_vel = self.max_linear_vel * np.cos(heading_error)
        angular_vel = self.max_angular_vel * heading_error
        
        # Check for obstacles in laser data
        if self.laser_data:
            min_distance = min(self.laser_data.ranges)
            if min_distance < self.safe_distance:
                # Slow down when approaching obstacles
                reduction_factor = min_distance / self.safe_distance
                linear_vel *= reduction_factor
                # Add lateral movement to avoid obstacles
                angular_vel += self.avoid_obstacles()
        
        # Apply velocity limits
        cmd_vel.linear.x = np.clip(linear_vel, 0.0, self.max_linear_vel)
        cmd_vel.angular.z = np.clip(angular_vel, -self.max_angular_vel, self.max_angular_vel)
        
        return cmd_vel
    
    def get_next_waypoint(self, global_path: Path) -> PoseStamped:
        """Find the next waypoint along the path"""
        if not global_path.poses:
            return None
        
        # Find closest point on path
        closest_idx = 0
        min_dist = float('inf')
        
        for i, pose in enumerate(global_path.poses):
            dist = self.distance_2d(
                self.current_pose.pose.position,
                pose.pose.position
            )
            if dist < min_dist:
                min_dist = dist
                closest_idx = i
        
        # Return a point ahead of the closest point
        lookahead_idx = min(closest_idx + 5, len(global_path.poses) - 1)
        return global_path.poses[lookahead_idx]
    
    def get_current_heading(self) -> float:
        """Extract current heading from robot's orientation"""
        if not self.current_pose:
            return 0.0
        
        # Convert quaternion to euler (simplified for z-axis rotation)
        q = self.current_pose.pose.orientation
        siny_cosp = 2 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z)
        return np.arctan2(siny_cosp, cosy_cosp)
    
    def normalize_angle(self, angle: float) -> float:
        """Normalize angle to [-pi, pi] range"""
        while angle > np.pi:
            angle -= 2 * np.pi
        while angle < -np.pi:
            angle += 2 * np.pi
        return angle
    
    def distance_2d(self, p1, p2) -> float:
        """Calculate 2D Euclidean distance between two points"""
        return np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
    
    def avoid_obstacles(self) -> float:
        """Generate angular velocity to avoid obstacles"""
        if not self.laser_data:
            return 0.0
        
        # Simple obstacle avoidance: turn away from closest obstacle
        min_idx = np.argmin(self.laser_data.ranges)
        angle_to_obstacle = self.laser_data.angle_min + min_idx * self.laser_data.angle_increment
        
        # Turn away from obstacle (positive for left, negative for right)
        if angle_to_obstacle < 0:
            return 0.3  # Turn left
        else:
            return -0.3  # Turn right

# Example usage
def example_local_planning():
    local_planner = LocalPlanner(max_vel=0.3, max_ang_vel=0.5)
    
    # Simulate current pose
    from geometry_msgs.msg import PoseStamped
    current_pose = PoseStamped()
    current_pose.pose.position.x = 0.0
    current_pose.pose.position.y = 0.0
    current_pose.pose.orientation.w = 1.0
    
    local_planner.current_pose = current_pose
    
    # Simulate global path
    global_path = Path()
    for i in range(10):
        pose = PoseStamped()
        pose.pose.position.x = i * 0.5
        pose.pose.position.y = 0.0
        global_path.poses.append(pose)
    
    # Compute velocity command
    cmd_vel = local_planner.compute_velocity(global_path)
    print(f"Computed velocity: linear.x={cmd_vel.linear.x:.3f}, angular.z={cmd_vel.angular.z:.3f}")
    
    return cmd_vel

example_local_planning()
```

## Integration with Perception Systems

Navigation systems benefit greatly from integration with perception:

```python
import numpy as np
from typing import Dict, List, Any
from sensor_msgs.msg import Image, PointCloud2
from geometry_msgs.msg import PoseStamped
import sensor_msgs_py.point_cloud2 as pc2

class PerceptionAwareNavigator:
    def __init__(self, global_planner, local_planner):
        """
        Navigation system that integrates perception for better path planning
        """
        self.global_planner = global_planner
        self.local_planner = local_planner
        self.dynamic_obstacles = []  # Detected moving obstacles
        self.static_map = None
        self.update_frequency = 10.0  # Hz
    
    def update_perception(self, image: Image, pointcloud: PointCloud2, 
                         robot_pose: PoseStamped) -> Dict[str, Any]:
        """
        Update navigation system with perception data
        
        Args:
            image: Camera image for object detection
            pointcloud: 3D point cloud for environment mapping
            robot_pose: Current robot pose
            
        Returns:
            Dictionary with updated navigation information
        """
        # Process image for object detection
        detected_objects = self.process_image(image, robot_pose)
        
        # Process point cloud for environment mapping
        environment_map = self.process_pointcloud(pointcloud, robot_pose)
        
        # Update dynamic obstacle tracking
        self.update_dynamic_obstacles(detected_objects)
        
        # Update static map if needed
        if self.static_map is None:
            self.static_map = environment_map
        
        return {
            'detected_objects': detected_objects,
            'environment_map': environment_map,
            'dynamic_obstacles': self.dynamic_obstacles
        }
    
    def process_image(self, image: Image, robot_pose: PoseStamped) -> List[Dict[str, Any]]:
        """
        Process camera image for object detection and tracking
        """
        # In practice, this would use a deep learning model for object detection
        # For this example, we'll simulate object detection
        
        # Simulate detection of objects in the environment
        objects = [
            {
                'name': 'person',
                'position': [robot_pose.pose.position.x + 2.0, 
                           robot_pose.pose.position.y + 0.5, 
                           robot_pose.pose.position.z],
                'velocity': [0.0, 0.0, 0.0],  # Stationary
                'confidence': 0.95,
                'bbox': [0.1, 0.1, 0.8, 0.8]  # Normalized coordinates
            },
            {
                'name': 'chair',
                'position': [robot_pose.pose.position.x + 1.5, 
                           robot_pose.pose.position.y - 1.0, 
                           robot_pose.pose.position.z],
                'velocity': [0.0, 0.0, 0.0],  # Stationary
                'confidence': 0.89,
                'bbox': [0.2, 0.3, 0.6, 0.7]
            }
        ]
        
        return objects
    
    def process_pointcloud(self, pointcloud: PointCloud2, robot_pose: PoseStamped) -> np.ndarray:
        """
        Process point cloud for environment mapping
        """
        # Convert point cloud to numpy array
        points = list(pc2.read_points(pointcloud, 
                                    field_names=("x", "y", "z"), 
                                    skip_nans=True))
        
        # Create occupancy grid from point cloud
        # This is a simplified approach - in practice, use more sophisticated methods
        grid_size = 50  # 50x50 grid
        resolution = 0.2  # 20cm per cell
        origin_x, origin_y = -5.0, -5.0  # Center around robot
        
        occupancy_grid = np.zeros((grid_size, grid_size))
        
        for point in points:
            x, y, z = point
            
            # Convert world coordinates to grid coordinates
            grid_x = int((x - origin_x) / resolution)
            grid_y = int((y - origin_y) / resolution)
            
            # Mark as occupied if within grid bounds
            if 0 <= grid_x < grid_size and 0 <= grid_y < grid_size:
                occupancy_grid[grid_y, grid_x] = 1
        
        return occupancy_grid
    
    def update_dynamic_obstacles(self, detected_objects: List[Dict[str, Any]]):
        """
        Update tracking of dynamic obstacles
        """
        # Simple tracking - in practice, use more sophisticated tracking algorithms
        for obj in detected_objects:
            if obj['velocity'] != [0.0, 0.0, 0.0]:  # Moving object
                # Check if this is a new dynamic obstacle
                is_new = True
                for dyn_obj in self.dynamic_obstacles:
                    if np.linalg.norm(
                        np.array(dyn_obj['position']) - np.array(obj['position'])
                    ) < 0.5:  # Same object if close
                        # Update position and velocity
                        dyn_obj['position'] = obj['position']
                        dyn_obj['velocity'] = obj['velocity']
                        dyn_obj['last_seen'] = time.time()
                        is_new = False
                        break
                
                if is_new:
                    self.dynamic_obstacles.append({
                        'name': obj['name'],
                        'position': obj['position'],
                        'velocity': obj['velocity'],
                        'confidence': obj['confidence'],
                        'last_seen': time.time()
                    })
        
        # Remove old dynamic obstacles (not seen recently)
        current_time = time.time()
        self.dynamic_obstacles = [
            obj for obj in self.dynamic_obstacles 
            if current_time - obj['last_seen'] < 5.0  # Remove if not seen in 5 seconds
        ]
    
    def plan_safe_path(self, start: Tuple[float, float], goal: Tuple[float, float]) -> List[Tuple[float, float]]:
        """
        Plan path considering both static and dynamic obstacles
        """
        # Create temporary map with dynamic obstacles added
        temp_map = self.static_map.copy() if self.static_map is not None else np.zeros((50, 50))
        
        # Add dynamic obstacles to map
        for dyn_obj in self.dynamic_obstacles:
            # Convert world coordinates to grid coordinates
            grid_x = int((dyn_obj['position'][0] + 5.0) / 0.2)
            grid_y = int((dyn_obj['position'][1] + 5.0) / 0.2)
            
            # Mark as occupied with some radius
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    nx, ny = grid_x + dx, grid_y + dy
                    if 0 <= nx < temp_map.shape[1] and 0 <= ny < temp_map.shape[0]:
                        temp_map[ny, nx] = 1
        
        # Plan path using the temporary map
        # This would use the global planner with the updated map
        # For this example, we'll use the A* planner with the temporary map
        temp_planner = AStarPlanner(temp_map, resolution=0.2)
        path = temp_planner.plan_path(start, goal)
        
        return path

# Example usage
def example_perception_aware_navigation():
    # Create planners
    global_planner = AStarPlanner(np.zeros((50, 50)), resolution=0.2)
    local_planner = LocalPlanner(max_vel=0.3, max_ang_vel=0.5)
    
    # Create perception-aware navigator
    navigator = PerceptionAwareNavigator(global_planner, local_planner)
    
    # Simulate perception data
    from sensor_msgs.msg import Image, PointCloud2
    from geometry_msgs.msg import PoseStamped
    
    # Create dummy perception data
    dummy_image = Image()
    dummy_pointcloud = PointCloud2()
    dummy_pose = PoseStamped()
    dummy_pose.pose.position.x = 0.0
    dummy_pose.pose.position.y = 0.0
    dummy_pose.pose.orientation.w = 1.0
    
    # Update navigation with perception
    nav_info = navigator.update_perception(dummy_image, dummy_pointcloud, dummy_pose)
    print(f"Detected {len(nav_info['detected_objects'])} objects")
    print(f"Tracked {len(nav_info['dynamic_obstacles'])} dynamic obstacles")
    
    # Plan path considering dynamic obstacles
    safe_path = navigator.plan_safe_path((0.0, 0.0), (8.0, 8.0))
    print(f"Planned safe path with {len(safe_path)} waypoints")
    
    return nav_info, safe_path

example_perception_aware_navigation()
```

## Navigation Performance Evaluation

Evaluating navigation system performance:

```python
import numpy as np
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt

class NavigationEvaluator:
    def __init__(self):
        """
        Evaluate navigation system performance
        """
        self.metrics = {
            'success_rate': [],
            'path_efficiency': [],  # Ratio of actual path length to optimal
            'execution_time': [],
            'safety_metrics': [],   # Collision avoidance, etc.
            'computational_load': [],  # CPU/GPU usage
            'energy_consumption': []
        }
        self.trial_data = []
    
    def evaluate_trial(self, planned_path: List[Tuple[float, float]], 
                      executed_path: List[Tuple[float, float]], 
                      goal_reached: bool, execution_time: float) -> Dict[str, float]:
        """
        Evaluate a single navigation trial
        
        Args:
            planned_path: Path planned by global planner
            executed_path: Actual path executed by robot
            goal_reached: Whether goal was reached successfully
            execution_time: Time taken to execute
            
        Returns:
            Dictionary with evaluation metrics
        """
        if not planned_path or not executed_path:
            return {'success': False, 'error': 'Empty paths'}
        
        # Calculate path efficiency
        planned_length = self.calculate_path_length(planned_path)
        executed_length = self.calculate_path_length(executed_path)
        
        path_efficiency = planned_length / executed_length if executed_length > 0 else 0
        
        # Calculate success rate
        success = goal_reached
        
        # Calculate deviation from planned path
        avg_deviation = self.calculate_path_deviation(planned_path, executed_path)
        
        # Calculate smoothness
        smoothness = self.calculate_path_smoothness(executed_path)
        
        # Store metrics
        trial_metrics = {
            'success': success,
            'path_efficiency': path_efficiency,
            'execution_time': execution_time,
            'planned_length': planned_length,
            'executed_length': executed_length,
            'avg_deviation': avg_deviation,
            'smoothness': smoothness
        }
        
        self.metrics['success_rate'].append(int(success))
        self.metrics['path_efficiency'].append(path_efficiency)
        self.metrics['execution_time'].append(execution_time)
        
        self.trial_data.append(trial_metrics)
        
        return trial_metrics
    
    def calculate_path_length(self, path: List[Tuple[float, float]]) -> float:
        """Calculate total length of a path"""
        if len(path) < 2:
            return 0.0
        
        total_length = 0.0
        for i in range(1, len(path)):
            p1 = np.array(path[i-1])
            p2 = np.array(path[i])
            total_length += np.linalg.norm(p2 - p1)
        
        return total_length
    
    def calculate_path_deviation(self, planned_path: List[Tuple[float, float]], 
                                executed_path: List[Tuple[float, float]]) -> float:
        """Calculate average deviation of executed path from planned path"""
        if not planned_path or not executed_path:
            return float('inf')
        
        total_deviation = 0.0
        count = 0
        
        # For each point in executed path, find closest point on planned path
        for exec_pt in executed_path:
            exec_arr = np.array(exec_pt)
            
            min_dist = float('inf')
            for plan_pt in planned_path:
                plan_arr = np.array(plan_pt)
                dist = np.linalg.norm(exec_arr - plan_arr)
                if dist < min_dist:
                    min_dist = dist
            
            total_deviation += min_dist
            count += 1
        
        return total_deviation / count if count > 0 else float('inf')
    
    def calculate_path_smoothness(self, path: List[Tuple[float, float]]) -> float:
        """Calculate path smoothness based on curvature"""
        if len(path) < 3:
            return 1.0  # Perfectly smooth for short paths
        
        total_curvature = 0.0
        
        for i in range(1, len(path) - 1):
            p_prev = np.array(path[i-1])
            p_curr = np.array(path[i])
            p_next = np.array(path[i+1])
            
            # Calculate vectors
            v1 = p_curr - p_prev
            v2 = p_next - p_curr
            
            # Calculate angle between vectors (smooth = 180°)
            if np.linalg.norm(v1) > 0 and np.linalg.norm(v2) > 0:
                cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
                cos_angle = np.clip(cos_angle, -1.0, 1.0)  # Prevent numerical errors
                angle = np.arccos(cos_angle)
                
                # Curvature is deviation from 180° (π radians)
                curvature = np.abs(np.pi - angle)
                total_curvature += curvature
        
        # Average curvature (lower is smoother)
        avg_curvature = total_curvature / (len(path) - 2) if len(path) > 2 else 0
        
        # Convert to smoothness score (higher is smoother)
        smoothness = 1.0 / (1.0 + avg_curvature)
        
        return smoothness
    
    def generate_report(self) -> str:
        """Generate evaluation report"""
        if not self.trial_data:
            return "No trials evaluated yet."
        
        # Calculate aggregate metrics
        success_rate = np.mean(self.metrics['success_rate'])
        avg_path_efficiency = np.mean(self.metrics['path_efficiency'])
        avg_execution_time = np.mean(self.metrics['execution_time'])
        std_execution_time = np.std(self.metrics['execution_time'])
        
        report = []
        report.append("=" * 60)
        report.append("NAVIGATION SYSTEM EVALUATION REPORT")
        report.append("=" * 60)
        report.append(f"Total Trials: {len(self.trial_data)}")
        report.append(f"Success Rate: {success_rate:.2%}")
        report.append(f"Average Path Efficiency: {avg_path_efficiency:.3f}")
        report.append(f"Average Execution Time: {avg_execution_time:.3f}s (±{std_execution_time:.3f}s)")
        
        # Additional metrics
        if self.metrics['path_efficiency']:
            report.append(f"Path Efficiency Range: {min(self.metrics['path_efficiency']):.3f} - {max(self.metrics['path_efficiency']):.3f}")
        
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def plot_performance(self):
        """Plot navigation performance metrics"""
        if not self.trial_data:
            print("No data to plot")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # Success rate over time
        success_rates = [trial['success'] for trial in self.trial_data]
        axes[0, 0].plot(success_rates, marker='o', linewidth=2)
        axes[0, 0].set_title('Success Rate Over Trials')
        axes[0, 0].set_xlabel('Trial Number')
        axes[0, 0].set_ylabel('Success (1=Success, 0=Failure)')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Path efficiency
        path_efficiencies = [trial['path_efficiency'] for trial in self.trial_data]
        axes[0, 1].plot(path_efficiencies, marker='s', linewidth=2, color='orange')
        axes[0, 1].set_title('Path Efficiency Over Trials')
        axes[0, 1].set_xlabel('Trial Number')
        axes[0, 1].set_ylabel('Path Efficiency')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Execution time
        execution_times = [trial['execution_time'] for trial in self.trial_data]
        axes[1, 0].plot(execution_times, marker='^', linewidth=2, color='green')
        axes[1, 0].set_title('Execution Time Over Trials')
        axes[1, 0].set_xlabel('Trial Number')
        axes[1, 0].set_ylabel('Time (s)')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Path deviation
        avg_deviations = [trial.get('avg_deviation', 0) for trial in self.trial_data]
        axes[1, 1].plot(avg_deviations, marker='d', linewidth=2, color='red')
        axes[1, 1].set_title('Path Deviation Over Trials')
        axes[1, 1].set_xlabel('Trial Number')
        axes[1, 1].set_ylabel('Average Deviation (m)')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()

# Example evaluation
def example_navigation_evaluation():
    evaluator = NavigationEvaluator()
    
    # Simulate some navigation trials
    for i in range(10):
        # Simulate planned and executed paths
        planned_path = [(j*0.5, 0) for j in range(20)]  # Straight line
        executed_path = [(j*0.5 + np.random.normal(0, 0.1), np.random.normal(0, 0.2)) for j in range(20)]
        
        # Simulate success/failure
        success = np.random.random() > 0.2  # 80% success rate
        execution_time = 5.0 + np.random.normal(0, 1.0)  # ~5 seconds with variation
        
        # Evaluate trial
        metrics = evaluator.evaluate_trial(planned_path, executed_path, success, execution_time)
        print(f"Trial {i+1}: Success={success}, Efficiency={metrics['path_efficiency']:.3f}")
    
    # Generate report
    report = evaluator.generate_report()
    print(f"\n{report}")
    
    # Plot performance
    evaluator.plot_performance()

example_navigation_evaluation()
```

## Best Practices for Navigation in Physical AI

### 1. System Design
- Use layered architecture for modularity
- Implement proper error handling and recovery
- Design for real-time performance
- Include safety checks and emergency procedures

### 2. Map Management
- Keep maps updated with dynamic information
- Use appropriate resolution for task requirements
- Implement map compression for efficiency
- Handle map merging for multi-robot systems

### 3. Path Planning Considerations
- Balance optimality with computational efficiency
- Consider robot dynamics in path planning
- Implement smooth path following
- Handle dynamic obstacles appropriately

### 4. Integration Strategies
- Integrate perception and navigation tightly
- Use appropriate coordinate frames
- Implement proper timing synchronization
- Handle sensor failures gracefully

## Looking Ahead

This week we explored SLAM and navigation, which are fundamental for autonomous robot operation. Next week, we'll dive into Vision-Language-Action systems, which integrate perception, language understanding, and action execution for more sophisticated Physical AI capabilities.

## Exercises

1. Implement a complete SLAM system using Cartographer
2. Create a navigation system with dynamic obstacle avoidance
3. Integrate perception data with navigation for semantic navigation
4. Evaluate navigation performance in various environments
5. Implement a behavior tree for navigation decision-making

## Further Reading

- "Probabilistic Robotics" by Thrun, Burgard, and Fox
- "Springer Handbook of Robotics" by Siciliano and Khatib
- Navigation2 Documentation: https://navigation.ros.org/
- Cartographer Documentation: https://google-cartographer-ros.readthedocs.io/