---
sidebar_position: 18
---

# Path Planning Algorithms for Physical AI Systems

This lesson focuses on path planning algorithms that enable robots to navigate efficiently and safely in complex environments. Path planning is a critical component of Physical AI systems, bridging the gap between high-level goals and low-level motion control.

## Learning Objectives

By the end of this lesson, you will be able to:

1. Implement classical path planning algorithms (A*, Dijkstra, RRT)
2. Understand sampling-based and optimization-based planners
3. Apply path planning to real-world Physical AI scenarios
4. Optimize paths for robot dynamics and constraints
5. Handle dynamic environments and replanning
6. Evaluate path planning performance and quality

## Classical Path Planning Algorithms

### Grid-Based Planning: A* Algorithm

A* is a popular graph traversal algorithm that finds the shortest path from start to goal using a heuristic function:

```python
import numpy as np
import heapq
from typing import List, Tuple, Optional
import matplotlib.pyplot as plt

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
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue  # Skip current node
                
                nx, ny = x + dx, y + dy
                
                # Check bounds
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    # Check if cell is free
                    if self.grid[ny, nx] == 0:
                        neighbors_list.append((nx, ny))
        
        return neighbors_list
    
    def plan(self, start: Tuple[float, float], goal: Tuple[float, float]) -> List[Tuple[float, float]]:
        """
        Plan path from start to goal using A* algorithm
        
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
            
            for next_node in self.neighbors(current):
                new_cost = cost_so_far[current] + 1  # Assuming uniform cost
                
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

# Example usage and visualization
def visualize_a_star():
    # Create a simple occupancy grid (0 = free, 1 = occupied)
    grid = np.zeros((20, 20))
    # Add some obstacles
    grid[5, 2:8] = 1  # Horizontal wall
    grid[10, 10:18] = 1  # Another wall
    grid[15, 5:15] = 1  # Bottom wall
    
    planner = AStarPlanner(grid, resolution=0.5)
    path = planner.plan((1.0, 1.0), (18.0, 18.0))
    
    # Visualization
    plt.figure(figsize=(10, 10))
    plt.imshow(grid, cmap='Greys', origin='upper')
    
    if path:
        path_x, path_y = zip(*[(p[0]/0.5, p[1]/0.5) for p in path])  # Convert back to grid coords
        plt.plot(path_y, path_x, 'r.-', linewidth=2, markersize=8, label='A* Path')
    
    # Mark start and goal
    plt.plot(1.0/0.5, 1.0/0.5, 'go', markersize=10, label='Start')
    plt.plot(18.0/0.5, 18.0/0.5, 'ro', markersize=10, label='Goal')
    
    plt.title('A* Path Planning')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
    
    print(f"A* found path with {len(path)} waypoints")
    return path

# Run visualization
path = visualize_a_star()
```

### Dijkstra's Algorithm

Dijkstra's algorithm finds the shortest path without using heuristics:

```python
import heapq
from typing import List, Tuple

class DijkstraPlanner:
    def __init__(self, occupancy_grid: np.ndarray, resolution: float = 1.0):
        self.grid = occupancy_grid
        self.resolution = resolution
        self.height, self.width = occupancy_grid.shape
    
    def neighbors(self, node: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get valid neighbors of a node"""
        x, y = node
        neighbors_list = []
        
        # 4-connected neighborhood (can be extended to 8-connected)
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if self.grid[ny, nx] == 0:  # Free space
                    neighbors_list.append((nx, ny))
        
        return neighbors_list
    
    def plan(self, start: Tuple[float, float], goal: Tuple[float, float]) -> List[Tuple[float, float]]:
        """Plan path using Dijkstra's algorithm"""
        # Convert meters to grid coordinates
        start_grid = (int(start[0] / self.resolution), int(start[1] / self.resolution))
        goal_grid = (int(goal[0] / self.resolution), int(goal[1] / self.resolution))
        
        # Priority queue: (cost, node)
        frontier = [(0, start_grid)]
        came_from = {start_grid: None}
        cost_so_far = {start_grid: 0}
        
        while frontier:
            current_cost, current = heapq.heappop(frontier)
            
            if current == goal_grid:
                break
            
            for next_node in self.neighbors(current):
                new_cost = cost_so_far[current] + 1  # Uniform cost
                
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    heapq.heappush(frontier, (new_cost, next_node))
                    came_from[next_node] = current
        
        # Reconstruct path
        path = []
        current = goal_grid
        if current in came_from:
            while current is not None:
                x_meters = current[0] * self.resolution
                y_meters = current[1] * self.resolution
                path.append((x_meters, y_meters))
                current = came_from[current]
            
            path.reverse()
        
        return path
```

## Sampling-Based Planning: RRT (Rapidly-exploring Random Trees)

RRT is particularly useful for high-dimensional spaces and complex kinematic constraints:

```python
import numpy as np
from typing import List, Tuple
import random

class RRTPlanner:
    def __init__(self, x_range: Tuple[float, float], y_range: Tuple[float, float], 
                 obstacles: List[Tuple[float, float, float]], resolution: float = 0.1):
        """
        RRT path planner
        
        Args:
            x_range: (min_x, max_x) in meters
            y_range: (min_y, max_y) in meters
            obstacles: List of (x, y, radius) tuples representing circular obstacles
            resolution: Step size for extending the tree
        """
        self.x_min, self.x_max = x_range
        self.y_min, self.y_max = y_range
        self.obstacles = obstacles
        self.resolution = resolution
        self.step_size = 0.5  # Distance to extend tree at each step
    
    def is_collision_free(self, point: Tuple[float, float]) -> bool:
        """Check if a point is collision-free"""
        x, y = point
        
        # Check bounds
        if not (self.x_min <= x <= self.x_max and self.y_min <= y <= self.y_max):
            return False
        
        # Check obstacles
        for obs_x, obs_y, obs_radius in self.obstacles:
            dist = np.sqrt((x - obs_x)**2 + (y - obs_y)**2)
            if dist <= obs_radius:
                return False
        
        return True
    
    def distance(self, p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
        """Euclidean distance between two points"""
        return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    
    def nearest_node(self, tree: List[Tuple[float, float]], target: Tuple[float, float]) -> Tuple[float, float]:
        """Find the nearest node in the tree to the target"""
        nearest = tree[0]
        min_dist = self.distance(nearest, target)
        
        for node in tree:
            dist = self.distance(node, target)
            if dist < min_dist:
                min_dist = dist
                nearest = node
        
        return nearest
    
    def steer(self, from_node: Tuple[float, float], to_node: Tuple[float, float]) -> Tuple[float, float]:
        """Steer from from_node toward to_node by step_size"""
        dist = self.distance(from_node, to_node)
        
        if dist <= self.step_size:
            return to_node
        
        # Calculate direction vector
        dx = to_node[0] - from_node[0]
        dy = to_node[1] - from_node[1]
        
        # Normalize and scale by step_size
        scale = self.step_size / dist
        new_x = from_node[0] + dx * scale
        new_y = from_node[1] + dy * scale
        
        return (new_x, new_y)
    
    def plan(self, start: Tuple[float, float], goal: Tuple[float, float], 
             max_iterations: int = 10000) -> List[Tuple[float, float]]:
        """
        Plan path using RRT algorithm
        
        Args:
            start: Start position (x, y)
            goal: Goal position (x, y)
            max_iterations: Maximum number of iterations
            
        Returns:
            List of waypoints [(x, y), ...] or empty list if no path found
        """
        # Initialize tree with start node
        tree = [start]
        parent_map = {start: None}
        
        for _ in range(max_iterations):
            # Random sample (bias toward goal occasionally)
            if random.random() < 0.1:  # 10% chance to sample goal
                rand_point = goal
            else:
                rand_point = (
                    random.uniform(self.x_min, self.x_max),
                    random.uniform(self.y_min, self.y_max)
                )
            
            # Find nearest node in tree
            nearest = self.nearest_node(tree, rand_point)
            
            # Steer toward random point
            new_point = self.steer(nearest, rand_point)
            
            # Check if path to new point is collision-free
            if self.is_collision_free(new_point):
                # Add new point to tree
                tree.append(new_point)
                parent_map[new_point] = nearest
                
                # Check if we're close to goal
                if self.distance(new_point, goal) <= self.step_size:
                    # Build path from goal to start
                    path = [goal]  # Add goal explicitly
                    current = new_point
                    
                    while current is not None:
                        path.append(current)
                        current = parent_map[current]
                    
                    path.reverse()
                    return path
        
        # If we reach max iterations without finding path
        return []

# Example usage and visualization
def visualize_rrt():
    # Define environment
    x_range = (0, 20)
    y_range = (0, 20)
    
    # Add circular obstacles
    obstacles = [
        (5, 5, 2),    # Circle at (5,5) with radius 2
        (15, 10, 3),  # Circle at (15,10) with radius 3
        (10, 15, 1.5) # Circle at (10,15) with radius 1.5
    ]
    
    rrt = RRTPlanner(x_range, y_range, obstacles)
    path = rrt.plan((1, 1), (18, 18))
    
    # Visualization
    plt.figure(figsize=(10, 10))
    
    # Draw obstacles
    for obs_x, obs_y, obs_radius in obstacles:
        circle = plt.Circle((obs_x, obs_y), obs_radius, color='red', alpha=0.5)
        plt.gca().add_patch(circle)
    
    # Draw path
    if path:
        path_x, path_y = zip(*path)
        plt.plot(path_x, path_y, 'b.-', linewidth=2, markersize=6, label='RRT Path')
    
    # Mark start and goal
    plt.plot(1, 1, 'go', markersize=10, label='Start')
    plt.plot(18, 18, 'ro', markersize=10, label='Goal')
    
    plt.xlim(x_range)
    plt.ylim(y_range)
    plt.title('RRT Path Planning')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()
    
    print(f"RRT found path with {len(path)} waypoints")
    return path

# Run visualization
rrt_path = visualize_rrt()
```

## Optimization-Based Planning: Trajectory Optimization

For smooth, dynamically-feasible paths:

```python
import numpy as np
from scipy.optimize import minimize
from typing import List, Tuple

class TrajectoryOptimizer:
    def __init__(self, start: Tuple[float, float], goal: Tuple[float, float], 
                 obstacles: List[Tuple[float, float, float]], 
                 max_vel: float = 1.0, max_acc: float = 0.5):
        """
        Trajectory optimizer using constrained optimization
        
        Args:
            start: Start position (x, y)
            goal: Goal position (x, y)
            obstacles: List of (x, y, radius) tuples
            max_vel: Maximum velocity constraint
            max_acc: Maximum acceleration constraint
        """
        self.start = np.array(start)
        self.goal = np.array(goal)
        self.obstacles = obstacles
        self.max_vel = max_vel
        self.max_acc = max_acc
        
        # Discretization parameters
        self.num_waypoints = 20
        self.dt = 1.0  # Time step
        
    def objective(self, x):
        """Objective function to minimize (path length + smoothness)"""
        # Reshape x to waypoints (x_coords, y_coords)
        x_coords = x[:self.num_waypoints]
        y_coords = x[self.num_waypoints:]
        
        waypoints = np.column_stack([x_coords, y_coords])
        
        # Path length term
        path_length = 0
        for i in range(1, len(waypoints)):
            path_length += np.linalg.norm(waypoints[i] - waypoints[i-1])
        
        # Smoothness term (minimize curvature)
        smoothness = 0
        for i in range(1, len(waypoints)-1):
            prev_pt = waypoints[i-1]
            curr_pt = waypoints[i]
            next_pt = waypoints[i+1]
            
            # Approximate curvature as angle between consecutive segments
            v1 = curr_pt - prev_pt
            v2 = next_pt - curr_pt
            dot_product = np.dot(v1, v2)
            norms = np.linalg.norm(v1) * np.linalg.norm(v2)
            if norms > 1e-6:  # Avoid division by zero
                cos_angle = max(-1, min(1, dot_product / norms))  # Clamp to [-1, 1]
                angle = np.arccos(cos_angle)
                smoothness += angle**2  # Square to penalize sharp turns more
        
        return path_length + 0.1 * smoothness  # Weight smoothness less than length
    
    def constraint_start(self, x):
        """Constraint: first waypoint must be start position"""
        x_coords = x[:self.num_waypoints]
        y_coords = x[self.num_waypoints:]
        return [x_coords[0] - self.start[0], y_coords[0] - self.start[1]]
    
    def constraint_goal(self, x):
        """Constraint: last waypoint must be goal position"""
        x_coords = x[:self.num_waypoints]
        y_coords = x[self.num_waypoints:]
        return [x_coords[-1] - self.goal[0], y_coords[-1] - self.goal[1]]
    
    def constraint_obstacles(self, x):
        """Constraint: path must avoid obstacles"""
        x_coords = x[:self.num_waypoints]
        y_coords = x[self.num_waypoints:]
        
        constraints = []
        waypoints = np.column_stack([x_coords, y_coords])
        
        for wp in waypoints:
            for obs_x, obs_y, obs_radius in self.obstacles:
                dist = np.sqrt((wp[0] - obs_x)**2 + (wp[1] - obs_y)**2)
                # Constraint: dist >= obs_radius + safety_margin
                safety_margin = 0.5
                constraints.append(dist - (obs_radius + safety_margin))
        
        return constraints
    
    def plan(self) -> List[Tuple[float, float]]:
        """Plan optimized trajectory"""
        # Initial guess: straight line from start to goal
        init_x = np.linspace(self.start[0], self.goal[0], self.num_waypoints)
        init_y = np.linspace(self.start[1], self.goal[1], self.num_waypoints)
        x0 = np.concatenate([init_x, init_y])
        
        # Define constraints
        constraints = [
            {'type': 'eq', 'fun': self.constraint_start},
            {'type': 'eq', 'fun': self.constraint_goal},
            {'type': 'ineq', 'fun': self.constraint_obstacles}
        ]
        
        # Bounds for each variable (could be environment limits)
        bounds = [(-10, 30)] * (2 * self.num_waypoints)  # x and y bounds
        
        # Optimize
        result = minimize(
            self.objective,
            x0,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints,
            options={'maxiter': 1000, 'ftol': 1e-6}
        )
        
        if result.success:
            x_coords = result.x[:self.num_waypoints]
            y_coords = result.x[self.num_waypoints:]
            path = [(x_coords[i], y_coords[i]) for i in range(self.num_waypoints)]
            return path
        else:
            print(f"Optimization failed: {result.message}")
            return []

# Example usage
def visualize_trajectory_optimization():
    obstacles = [
        (5, 5, 2),
        (12, 8, 1.5),
        (8, 12, 2.5)
    ]
    
    optimizer = TrajectoryOptimizer((1, 1), (18, 18), obstacles)
    path = optimizer.plan()
    
    if path:
        # Visualization
        plt.figure(figsize=(10, 10))
        
        # Draw obstacles
        for obs_x, obs_y, obs_radius in obstacles:
            circle = plt.Circle((obs_x, obs_y), obs_radius, color='red', alpha=0.5)
            plt.gca().add_patch(circle)
        
        # Draw optimized path
        path_x, path_y = zip(*path)
        plt.plot(path_x, path_y, 'g.-', linewidth=2, markersize=6, label='Optimized Path')
        
        # Mark start and goal
        plt.plot(1, 1, 'go', markersize=10, label='Start')
        plt.plot(18, 18, 'ro', markersize=10, label='Goal')
        
        plt.title('Trajectory Optimization')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.axis('equal')
        plt.show()
        
        print(f"Optimized path with {len(path)} waypoints")
        return path
    else:
        print("No path found")
        return []

# Run visualization
opt_path = visualize_trajectory_optimization()
```

## Integration with Robot Dynamics

Planning paths that respect robot kinematics and dynamics:

```python
import numpy as np
from scipy.interpolate import interp1d
from typing import List, Tuple

class DifferentialDrivePathFollower:
    def __init__(self, max_linear_vel: float = 0.5, max_angular_vel: float = 1.0,
                 wheel_base: float = 0.3):
        """
        Path follower for differential drive robot
        
        Args:
            max_linear_vel: Maximum linear velocity (m/s)
            max_angular_vel: Maximum angular velocity (rad/s)
            wheel_base: Distance between wheels (m)
        """
        self.max_linear_vel = max_linear_vel
        self.max_angular_vel = max_angular_vel
        self.wheel_base = wheel_base
        
        # Robot state
        self.current_pos = np.array([0.0, 0.0])
        self.current_theta = 0.0  # Heading angle
        
        # Path following parameters
        self.lookahead_dist = 0.5
        self.kp_linear = 1.0  # Proportional gain for linear velocity
        self.kp_angular = 2.0  # Proportional gain for angular velocity
    
    def follow_path(self, path: List[Tuple[float, float]], dt: float = 0.1) -> List[Tuple[float, float, float]]:
        """
        Generate robot trajectory following the path
        
        Args:
            path: List of waypoints [(x, y), ...]
            dt: Time step for simulation
            
        Returns:
            List of (x, y, theta) poses over time
        """
        if not path:
            return []
        
        # Convert path to numpy array
        path_array = np.array(path)
        
        trajectory = []
        current_idx = 0
        
        # Simulate following the path
        for t in np.arange(0, 20, dt):  # Simulate for 20 seconds
            # Find closest point on path
            closest_idx = self.find_closest_point(path_array)
            
            # Look ahead to find target point
            target_idx = self.find_lookahead_point(path_array, closest_idx)
            
            if target_idx is not None:
                target_point = path_array[target_idx]
                
                # Calculate control commands
                linear_vel, angular_vel = self.calculate_control(target_point)
                
                # Update robot state (simple kinematic model)
                self.current_pos[0] += linear_vel * np.cos(self.current_theta) * dt
                self.current_pos[1] += linear_vel * np.sin(self.current_theta) * dt
                self.current_theta += angular_vel * dt
                
                # Store trajectory point
                trajectory.append((self.current_pos[0], self.current_pos[1], self.current_theta))
            else:
                # Reached end of path
                trajectory.append((self.current_pos[0], self.current_pos[1], self.current_theta))
        
        return trajectory
    
    def find_closest_point(self, path: np.ndarray) -> int:
        """Find index of closest point on path to current position"""
        diffs = path - self.current_pos
        distances = np.sum(diffs**2, axis=1)
        return np.argmin(distances)
    
    def find_lookahead_point(self, path: np.ndarray, start_idx: int) -> int:
        """Find point on path that is lookahead distance ahead"""
        if start_idx >= len(path) - 1:
            return None  # Reached end of path
        
        # Search forward from start_idx
        for i in range(start_idx, len(path)):
            dist = np.linalg.norm(path[i] - self.current_pos)
            if dist >= self.lookahead_dist:
                return i
        
        # If no point is far enough, return the last point
        return len(path) - 1
    
    def calculate_control(self, target_point: np.ndarray) -> Tuple[float, float]:
        """Calculate linear and angular velocities to reach target point"""
        # Vector from robot to target
        to_target = target_point - self.current_pos
        
        # Desired heading
        desired_theta = np.arctan2(to_target[1], to_target[0])
        
        # Heading error
        heading_error = desired_theta - self.current_theta
        # Normalize angle to [-pi, pi]
        while heading_error > np.pi:
            heading_error -= 2 * np.pi
        while heading_error < -np.pi:
            heading_error += 2 * np.pi
        
        # Calculate velocities
        linear_vel = min(self.max_linear_vel, 
                        self.kp_linear * np.linalg.norm(to_target))
        angular_vel = np.clip(self.kp_angular * heading_error, 
                             -self.max_angular_vel, self.max_angular_vel)
        
        return linear_vel, angular_vel

# Example: Plan and follow a path
def demonstrate_path_following():
    # Create an environment with obstacles
    grid = np.zeros((30, 30))
    grid[10:20, 14:16] = 1  # Vertical wall
    
    # Plan path using A*
    planner = AStarPlanner(grid, resolution=0.5)
    path = planner.plan((2.0, 2.0), (25.0, 25.0))
    
    if path:
        # Follow the path with a differential drive robot
        follower = DifferentialDrivePathFollower()
        trajectory = follower.follow_path(path)
        
        # Visualization
        plt.figure(figsize=(12, 8))
        
        # Plot environment
        plt.subplot(1, 2, 1)
        plt.imshow(grid, cmap='Greys', origin='upper')
        
        # Plot planned path
        path_x, path_y = zip(*[(p[0]/0.5, p[1]/0.5) for p in path])
        plt.plot(path_y, path_x, 'b.-', linewidth=2, markersize=4, label='Planned Path')
        
        # Plot executed trajectory
        traj_x, traj_y, traj_theta = zip(*trajectory)
        traj_grid_x = [x/0.5 for x in traj_x]
        traj_grid_y = [y/0.5 for y in traj_y]
        plt.plot(traj_grid_y, traj_grid_x, 'r-', linewidth=1, label='Executed Trajectory')
        
        plt.title('Path Planning and Following')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Plot trajectory in metric coordinates
        plt.subplot(1, 2, 2)
        plt.plot([p[0] for p in path], [p[1] for p in path], 'b.-', label='Planned Path')
        plt.plot(traj_x, traj_y, 'r-', label='Executed Trajectory')
        plt.scatter([2.0, 25.0], [2.0, 25.0], c=['green', 'red'], s=100, label='Start/Goal')
        plt.title('Metric Coordinates')
        plt.xlabel('X (m)')
        plt.ylabel('Y (m)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.axis('equal')
        
        plt.tight_layout()
        plt.show()
        
        print(f"Planned path: {len(path)} waypoints")
        print(f"Executed trajectory: {len(trajectory)} poses")
        
        return path, trajectory
    else:
        print("No path found")
        return [], []

# Run demonstration
path, trajectory = demonstrate_path_following()
```

## Dynamic Path Planning and Replanning

Handling changing environments and replanning:

```python
import numpy as np
from typing import List, Tuple, Optional
import heapq

class DynamicAStarPlanner:
    def __init__(self, initial_grid: np.ndarray, resolution: float = 1.0):
        """
        Dynamic A* planner that can handle changing environments
        """
        self.grid = initial_grid.copy()
        self.resolution = resolution
        self.height, self.width = self.grid.shape
        
        # Store previously computed paths for incremental updates
        self.last_path = []
        self.last_start = None
        self.last_goal = None
    
    def update_environment(self, new_grid: np.ndarray):
        """Update the occupancy grid with new information"""
        self.grid = new_grid.copy()
        
        # Invalidate cached path if environment changed significantly
        if self.last_path:
            self.last_path = []  # Need to replan
    
    def plan(self, start: Tuple[float, float], goal: Tuple[float, float]) -> List[Tuple[float, float]]:
        """
        Plan path using A* algorithm
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
            
            for next_node in self.neighbors(current):
                new_cost = cost_so_far[current] + 1  # Assuming uniform cost
                
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
        
        # Cache the path
        self.last_path = path
        self.last_start = start
        self.last_goal = goal
        
        return path
    
    def heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        """Manhattan distance heuristic"""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def neighbors(self, node: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get valid neighbors of a node"""
        x, y = node
        neighbors_list = []
        
        # 8-connected neighborhood
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue  # Skip current node
                
                nx, ny = x + dx, y + dy
                
                # Check bounds
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    # Check if cell is free
                    if self.grid[ny, nx] == 0:
                        neighbors_list.append((nx, ny))
        
        return neighbors_list
    
    def replan_if_needed(self, current_pos: Tuple[float, float], 
                        goal: Tuple[float, float], 
                        replan_threshold: float = 2.0) -> Optional[List[Tuple[float, float]]]:
        """
        Check if replanning is needed and return new path if so
        
        Args:
            current_pos: Current robot position
            goal: Goal position
            replan_threshold: Distance threshold to trigger replanning
            
        Returns:
            New path if replanning was needed, None otherwise
        """
        if not self.last_path:
            # No previous path, need to plan
            return self.plan(current_pos, goal)
        
        # Check if we're still on the planned path
        closest_path_idx = self.find_closest_path_point(current_pos)
        
        if closest_path_idx is None:
            # Current position is far from path, replan
            return self.plan(current_pos, goal)
        
        # Check if there are new obstacles on the path
        for i in range(closest_path_idx, len(self.last_path)):
            path_point = self.last_path[i]
            grid_x = int(path_point[0] / self.resolution)
            grid_y = int(path_point[1] / self.resolution)
            
            if (0 <= grid_x < self.width and 0 <= grid_y < self.height and 
                self.grid[grid_y, grid_x] == 1):
                # Found obstacle on path, replan
                return self.plan(current_pos, goal)
        
        # Path is still valid
        return None
    
    def find_closest_path_point(self, pos: Tuple[float, float]) -> Optional[int]:
        """Find the closest point on the last path to the current position"""
        if not self.last_path:
            return None
        
        min_dist = float('inf')
        closest_idx = None
        
        for i, path_point in enumerate(self.last_path):
            dist = np.sqrt((pos[0] - path_point[0])**2 + (pos[1] - path_point[1])**2)
            if dist < min_dist:
                min_dist = dist
                closest_idx = i
        
        return closest_idx

# Example: Dynamic replanning demonstration
def demonstrate_dynamic_planning():
    # Create initial environment
    initial_grid = np.zeros((20, 20))
    initial_grid[5, 2:8] = 1  # Initial obstacle
    
    planner = DynamicAStarPlanner(initial_grid, resolution=0.5)
    
    # Plan initial path
    initial_path = planner.plan((1.0, 1.0), (18.0, 18.0))
    print(f"Initial path: {len(initial_path)} waypoints")
    
    # Simulate robot movement along path
    robot_pos = (1.0, 1.0)
    goal = (18.0, 18.0)
    
    # Simulate encountering a new obstacle
    new_grid = initial_grid.copy()
    new_grid[10, 8:15] = 1  # New obstacle that blocks the path
    
    # Update planner with new environment
    planner.update_environment(new_grid)
    
    # Check if replanning is needed
    new_path = planner.replan_if_needed(robot_pos, goal)
    
    if new_path:
        print(f"Replanned path: {len(new_path)} waypoints")
        
        # Visualization
        plt.figure(figsize=(12, 5))
        
        # Plot initial environment and path
        plt.subplot(1, 2, 1)
        plt.imshow(initial_grid, cmap='Greys', origin='upper')
        if initial_path:
            path_x, path_y = zip(*[(p[0]/0.5, p[1]/0.5) for p in initial_path])
            plt.plot(path_y, path_x, 'b.-', linewidth=2, label='Initial Path')
        plt.plot(1.0/0.5, 1.0/0.5, 'go', markersize=10, label='Start')
        plt.plot(18.0/0.5, 18.0/0.5, 'ro', markersize=10, label='Goal')
        plt.title('Initial Environment & Path')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Plot new environment and replanned path
        plt.subplot(1, 2, 2)
        plt.imshow(new_grid, cmap='Greys', origin='upper')
        if new_path:
            path_x, path_y = zip(*[(p[0]/0.5, p[1]/0.5) for p in new_path])
            plt.plot(path_y, path_x, 'r.-', linewidth=2, label='Replanned Path')
        plt.plot(1.0/0.5, 1.0/0.5, 'go', markersize=10, label='Start')
        plt.plot(18.0/0.5, 18.0/0.5, 'ro', markersize=10, label='Goal')
        plt.title('New Environment & Replanned Path')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        return initial_path, new_path
    else:
        print("No replanning needed")
        return initial_path, None

# Run dynamic planning demonstration
initial_path, new_path = demonstrate_dynamic_planning()
```

## Path Smoothing and Optimization

Post-processing planned paths for better execution:

```python
import numpy as np
from scipy.interpolate import splprep, splev
from typing import List, Tuple

class PathSmoother:
    def __init__(self, smoothing_factor: float = 0.1):
        """
        Path smoother using cubic splines
        
        Args:
            smoothing_factor: Controls smoothness vs path following (0-1)
        """
        self.smoothing_factor = smoothing_factor
    
    def smooth_path(self, path: List[Tuple[float, float]], 
                   num_points: int = 100) -> List[Tuple[float, float]]:
        """
        Smooth a path using cubic splines
        
        Args:
            path: Original path [(x, y), ...]
            num_points: Number of points in smoothed path
            
        Returns:
            Smoothed path [(x, y), ...]
        """
        if len(path) < 3:
            return path  # Can't smooth paths with < 3 points
        
        # Extract x and y coordinates
        x_coords = [p[0] for p in path]
        y_coords = [p[1] for p in path]
        
        # Create spline representation
        # Parameter s controls smoothing: larger s = smoother path
        smooth_param = self.smoothing_factor * len(path)
        
        # Fit parametric spline to path
        tck, u = splprep([x_coords, y_coords], s=smooth_param, k=min(3, len(path)-1))
        
        # Generate new points along the spline
        u_new = np.linspace(0, 1, num_points)
        smoothed_x, smoothed_y = splev(u_new, tck)
        
        # Convert back to list of tuples
        smoothed_path = [(smoothed_x[i], smoothed_y[i]) for i in range(num_points)]
        
        return smoothed_path
    
    def optimize_for_curvature(self, path: List[Tuple[float, float]], 
                              max_curvature: float = 1.0) -> List[Tuple[float, float]]:
        """
        Optimize path to limit curvature (important for vehicle dynamics)
        
        Args:
            path: Original path
            max_curvature: Maximum allowed curvature
            
        Returns:
            Curvature-optimized path
        """
        if len(path) < 3:
            return path
        
        optimized_path = [path[0]]  # Start with first point
        
        i = 0
        while i < len(path) - 2:
            # Check curvature at current point
            p1 = np.array(path[i])
            p2 = np.array(path[i+1])
            p3 = np.array(path[i+2])
            
            # Calculate curvature (simplified approximation)
            v1 = p2 - p1
            v2 = p3 - p2
            cross_product = np.cross(v1, v2)
            norms = np.linalg.norm(v1) * np.linalg.norm(v2)
            
            if norms > 1e-6:  # Avoid division by zero
                curvature = abs(cross_product) / norms
            else:
                curvature = 0
            
            if curvature <= max_curvature:
                # Accept the next point
                optimized_path.append(path[i+1])
                i += 1
            else:
                # Skip the point and try the next one
                i += 1
        
        # Always add the last point
        optimized_path.append(path[-1])
        
        return optimized_path

# Example: Path smoothing demonstration
def demonstrate_path_smoothing():
    # Create a path with sharp turns
    original_path = [
        (0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (3, 2), (4, 2), 
        (4, 3), (4, 4), (5, 4), (6, 4), (6, 5), (6, 6), (7, 6), (8, 6)
    ]
    
    smoother = PathSmoother(smoothing_factor=0.2)
    smoothed_path = smoother.smooth_path(original_path)
    
    # Also demonstrate curvature optimization
    optimized_path = smoother.optimize_for_curvature(original_path, max_curvature=2.0)
    
    # Visualization
    plt.figure(figsize=(15, 5))
    
    # Original path
    plt.subplot(1, 3, 1)
    orig_x, orig_y = zip(*original_path)
    plt.plot(orig_x, orig_y, 'ro-', linewidth=2, markersize=8, label='Original Path')
    plt.title('Original Path')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.axis('equal')
    
    # Smoothed path
    plt.subplot(1, 3, 2)
    smooth_x, smooth_y = zip(*smoothed_path)
    plt.plot(smooth_x, smooth_y, 'b.-', linewidth=2, markersize=4, label='Smoothed Path')
    plt.title('Smoothed Path')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.axis('equal')
    
    # Comparison
    plt.subplot(1, 3, 3)
    plt.plot(orig_x, orig_y, 'ro-', linewidth=2, markersize=8, label='Original')
    plt.plot(smooth_x, smooth_y, 'b.-', linewidth=2, markersize=4, label='Smoothed')
    plt.plot([p[0] for p in optimized_path], [p[1] for p in optimized_path], 
             'g--', linewidth=2, markersize=6, label='Curvature-Optimized')
    plt.title('Comparison')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.axis('equal')
    
    plt.tight_layout()
    plt.show()
    
    print(f"Original path: {len(original_path)} waypoints")
    print(f"Smoothed path: {len(smoothed_path)} waypoints")
    print(f"Optimized path: {len(optimized_path)} waypoints")
    
    return original_path, smoothed_path, optimized_path

# Run smoothing demonstration
orig_path, smooth_path, opt_path = demonstrate_path_smoothing()
```

## Best Practices for Path Planning in Physical AI

### 1. Algorithm Selection
- Use grid-based planners (A*, Dijkstra) for known static environments
- Use sampling-based planners (RRT) for high-dimensional spaces
- Use optimization-based planners for smooth, dynamically-feasible paths
- Consider hybrid approaches for complex scenarios

### 2. Performance Optimization
- Precompute and cache paths when possible
- Use hierarchical planning (coarse-to-fine)
- Implement efficient data structures (priority queues, spatial indexing)
- Parallelize computations where possible

### 3. Robustness Considerations
- Handle edge cases (no path exists, invalid inputs)
- Implement proper error handling and fallback behaviors
- Consider uncertainty in perception and localization
- Plan with safety margins

### 4. Integration with Control
- Ensure planned paths are dynamically feasible
- Smooth paths to reduce control effort
- Consider robot kinematics and dynamics
- Implement proper path following algorithms

## Looking Ahead

This lesson covered various path planning algorithms essential for Physical AI systems. The next lesson will focus on Vision-Language-Action (VLA) systems, which integrate perception, language understanding, and action selection for more sophisticated robot behaviors.

## Exercises

1. Implement a hybrid A*/RRT planner that combines the benefits of both approaches
2. Create a path planner that considers robot dynamics constraints
3. Develop a multi-objective optimization approach that balances path length, smoothness, and safety
4. Implement a real-time replanning system that responds to dynamic obstacles
5. Compare the performance of different path planning algorithms in various scenarios

## Further Reading

- "Planning Algorithms" by Steven LaValle: http://lavalle.pl/planning/
- OMPL (Open Motion Planning Library): https://ompl.kavrakilab.org/
- ROS Navigation Stack: http://wiki.ros.org/navigation
- "Principles of Robot Motion" by Howie Choset et al.