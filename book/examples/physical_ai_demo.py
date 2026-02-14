#!/usr/bin/env python3
"""
Physical AI & Humanoid Robotics - Example Simulation

This file demonstrates key concepts from the Physical AI & Humanoid Robotics course.
It includes examples of perception, planning, control, and integration.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
import math
from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass
class RobotState:
    """Represents the state of the robot"""
    position: np.ndarray  # [x, y, z]
    orientation: np.ndarray  # [roll, pitch, yaw]
    joint_angles: np.ndarray
    joint_velocities: np.ndarray
    held_object: Optional[str] = None
    battery_level: float = 1.0
    gripper_status: str = 'open'  # 'open', 'closed', 'moving'
    location: str = 'unknown'


class SimplePerceptionSystem:
    """Simple perception system for demonstration"""
    
    def __init__(self):
        self.environment_map = self._create_sample_environment()
        self.detected_objects = []
    
    def _create_sample_environment(self) -> np.ndarray:
        """Create a simple 2D occupancy grid environment"""
        # Create a 20x20 grid
        grid = np.zeros((20, 20))
        
        # Add some obstacles
        grid[5:8, 5:15] = 1  # Wall
        grid[12:15, 8:12] = 1  # Table
        grid[2:4, 2:4] = 1  # Small obstacle
        
        return grid
    
    def detect_objects(self) -> List[dict]:
        """Simulate object detection"""
        objects = [
            {"name": "red_cube", "position": [2.5, 2.5, 0.1], "confidence": 0.95},
            {"name": "blue_sphere", "position": [13.0, 10.0, 0.15], "confidence": 0.89},
            {"name": "green_cylinder", "position": [15.0, 15.0, 0.12], "confidence": 0.92}
        ]
        return objects
    
    def get_environment_map(self) -> np.ndarray:
        """Return the environment map"""
        return self.environment_map.copy()


class SimplePathPlanner:
    """Simple path planning system"""
    
    def __init__(self, perception_system: SimplePerceptionSystem):
        self.perception = perception_system
    
    def plan_path(self, start: np.ndarray, goal: np.ndarray) -> List[np.ndarray]:
        """Simple path planning using a direct line with obstacle avoidance"""
        # For simplicity, we'll use a direct path with some waypoints
        # In a real system, this would use A*, RRT, or other algorithms
        
        path = [start.copy()]
        
        # Calculate direct path
        direction = goal - start
        distance = np.linalg.norm(direction)
        
        if distance > 0.1:  # If goal is not very close
            # Add intermediate waypoints
            num_waypoints = max(2, int(distance / 0.5))  # Waypoints every 0.5m
            
            for i in range(1, num_waypoints):
                t = i / num_waypoints
                waypoint = start + t * direction
                path.append(waypoint)
        
        path.append(goal.copy())
        return path


class SimpleController:
    """Simple controller for demonstration"""
    
    def __init__(self, path_planner: SimplePathPlanner):
        self.path_planner = path_planner
        self.current_trajectory = []
        self.trajectory_index = 0
    
    def move_to_position(self, goal_pos: np.ndarray, current_state: RobotState) -> bool:
        """Simulate moving to a position"""
        print(f"Moving from {current_state.position} to {goal_pos}")
        
        # Plan path
        path = self.path_planner.plan_path(current_state.position, goal_pos)
        
        # Execute path (simulate movement)
        for i, waypoint in enumerate(path):
            # Update robot position (simulated)
            current_state.position = waypoint.copy()
            
            # Simulate time delay
            time.sleep(0.1)
            
            print(f"  Reached waypoint {i+1}/{len(path)}: [{waypoint[0]:.2f}, {waypoint[1]:.2f}, {waypoint[2]:.2f}]")
        
        print(f"Successfully reached {goal_pos}")
        return True
    
    def grasp_object(self, obj_name: str, current_state: RobotState) -> bool:
        """Simulate grasping an object"""
        print(f"Attempting to grasp {obj_name}")
        
        # Simulate the grasping process
        time.sleep(0.5)
        
        # Update robot state
        current_state.held_object = obj_name
        current_state.gripper_status = 'closed'
        
        print(f"Successfully grasped {obj_name}")
        return True
    
    def place_object(self, current_state: RobotState) -> bool:
        """Simulate placing an object"""
        if not current_state.held_object:
            print("Cannot place object: robot is not holding anything")
            return False
        
        print(f"Placing {current_state.held_object}")
        
        # Update robot state
        current_state.held_object = None
        current_state.gripper_status = 'open'
        
        print(f"Successfully placed object")
        return True


class SimpleNaturalLanguageProcessor:
    """Simple NLP system for demonstration"""
    
    def process_command(self, command: str) -> dict:
        """Process a natural language command"""
        command_lower = command.lower()
        
        # Simple intent recognition
        if any(word in command_lower for word in ["go to", "navigate", "move to", "travel"]):
            intent = "navigation"
            # Extract location
            if "kitchen" in command_lower:
                location = "kitchen"
            elif "living room" in command_lower:
                location = "living_room"
            elif "bedroom" in command_lower:
                location = "bedroom"
            else:
                location = "unknown"
            
            return {
                "intent": intent,
                "parameters": {"location": location}
            }
        
        elif any(word in command_lower for word in ["pick up", "grasp", "take", "get"]):
            intent = "grasp"
            # Extract object
            if "red cube" in command_lower:
                obj = "red_cube"
            elif "blue sphere" in command_lower:
                obj = "blue_sphere"
            elif "green cylinder" in command_lower:
                obj = "green_cylinder"
            else:
                obj = "unknown"
            
            return {
                "intent": intent,
                "parameters": {"object": obj}
            }
        
        elif any(word in command_lower for word in ["place", "put", "set down", "release"]):
            intent = "place"
            return {
                "intent": intent,
                "parameters": {}
            }
        
        else:
            return {
                "intent": "unknown",
                "parameters": {}
            }


class PhysicalAIDemoSystem:
    """Complete demonstration system integrating all components"""
    
    def __init__(self):
        self.perception = SimplePerceptionSystem()
        self.path_planner = SimplePathPlanner(self.perception)
        self.controller = SimpleController(self.path_planner)
        self.nlp = SimpleNaturalLanguageProcessor()
        
        # Initialize robot state
        self.robot_state = RobotState(
            position=np.array([0.0, 0.0, 0.0]),
            orientation=np.array([0.0, 0.0, 0.0]),
            joint_angles=np.zeros(6),  # 6 DOF for simple arm
            joint_velocities=np.zeros(6),
            battery_level=1.0
        )
    
    def execute_command(self, command: str) -> bool:
        """Execute a natural language command"""
        print(f"\nProcessing command: '{command}'")
        
        # Process command with NLP
        parsed_command = self.nlp.process_command(command)
        intent = parsed_command["intent"]
        params = parsed_command["parameters"]
        
        print(f"Parsed intent: {intent}, parameters: {params}")
        
        if intent == "navigation":
            location = params.get("location", "unknown")
            if location == "kitchen":
                goal_pos = np.array([10.0, 5.0, 0.0])
            elif location == "living_room":
                goal_pos = np.array([5.0, 10.0, 0.0])
            elif location == "bedroom":
                goal_pos = np.array([15.0, 15.0, 0.0])
            else:
                print(f"Unknown location: {location}")
                return False
            
            return self.controller.move_to_position(goal_pos, self.robot_state)
        
        elif intent == "grasp":
            obj_name = params.get("object", "unknown")
            if obj_name == "unknown":
                print("Unknown object to grasp")
                return False
            
            # First, find the object in the environment
            detected_objects = self.perception.detect_objects()
            target_obj = None
            for obj in detected_objects:
                if obj["name"] == obj_name:
                    target_obj = obj
                    break
            
            if not target_obj:
                print(f"Could not find object: {obj_name}")
                return False
            
            # Move to object location
            obj_pos = np.array(target_obj["position"])
            success = self.controller.move_to_position(obj_pos, self.robot_state)
            if not success:
                return False
            
            # Grasp the object
            return self.controller.grasp_object(obj_name, self.robot_state)
        
        elif intent == "place":
            return self.controller.place_object(self.robot_state)
        
        else:
            print(f"Unknown intent: {intent}")
            return False
    
    def visualize_environment(self):
        """Visualize the environment and robot state"""
        fig = plt.figure(figsize=(12, 5))
        
        # Plot environment map
        ax1 = fig.add_subplot(121)
        im = ax1.imshow(self.perception.get_environment_map(), cmap='gray', origin='lower')
        ax1.set_title('Environment Map')
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        
        # Mark robot position
        robot_pos = self.robot_state.position
        ax1.plot(robot_pos[0], robot_pos[1], 'ro', markersize=10, label='Robot')
        
        # Mark detected objects
        objects = self.perception.detect_objects()
        for obj in objects:
            pos = obj["position"]
            ax1.plot(pos[0], pos[1], 'bo', markersize=8, label=f'{obj["name"]}')
        
        ax1.legend()
        
        # Plot 3D view
        ax2 = fig.add_subplot(122, projection='3d')
        
        # Plot environment
        x, y = np.meshgrid(np.arange(20), np.arange(20))
        z = np.zeros_like(x)
        obs_z = np.where(self.perception.get_environment_map() == 1, 0.5, 0)
        ax2.bar3d(x.ravel(), y.ravel(), z.ravel(), 1, 1, obs_z.ravel(), shade=True, alpha=0.6)
        
        # Mark robot position
        ax2.scatter([robot_pos[0]], [robot_pos[1]], [robot_pos[2]], color='red', s=100, label='Robot')
        
        # Mark objects
        for obj in objects:
            pos = obj["position"]
            ax2.scatter([pos[0]], [pos[1]], [pos[2]], color='blue', s=80, label=obj["name"])
        
        ax2.set_xlabel('X')
        ax2.set_ylabel('Y')
        ax2.set_zlabel('Z')
        ax2.set_title('3D Environment View')
        
        plt.tight_layout()
        plt.show()


def main():
    """Main function to demonstrate the Physical AI system"""
    print("Physical AI & Humanoid Robotics - Example System")
    print("=" * 50)
    
    # Create the system
    system = PhysicalAIDemoSystem()
    
    # Demonstrate the system
    print("\nInitial robot state:")
    print(f"  Position: {system.robot_state.position}")
    print(f"  Holding: {system.robot_state.held_object}")
    print(f"  Battery: {system.robot_state.battery_level:.2f}")
    
    # Show environment visualization
    print("\nVisualizing environment...")
    system.visualize_environment()
    
    # Example commands to execute
    commands = [
        "Go to the kitchen",
        "Please pick up the red cube",
        "Go to the living room",
        "Place the object"
    ]
    
    print(f"\nExecuting demonstration commands:")
    for i, command in enumerate(commands, 1):
        print(f"\n{i}. Executing: {command}")
        success = system.execute_command(command)
        print(f"   Result: {'Success' if success else 'Failed'}")
        
        # Show updated state
        print(f"   Updated position: {system.robot_state.position}")
        print(f"   Holding: {system.robot_state.held_object}")
    
    print(f"\nFinal robot state:")
    print(f"  Position: {system.robot_state.position}")
    print(f"  Holding: {system.robot_state.held_object}")
    print(f"  Battery: {system.robot_state.battery_level:.2f}")
    
    print("\nDemonstration completed!")


if __name__ == "__main__":
    main()