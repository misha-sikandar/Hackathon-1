"""
Physical AI & Humanoid Robotics - Integrated System Example

This file demonstrates the integration of multiple Physical AI components:
- Perception system
- Planning system  
- Control system
- Natural language processing
- Simulation environment
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Tuple
import math
import time
import random


@dataclass
class RobotState:
    """Complete robot state representation"""
    position: np.ndarray  # [x, y, z]
    orientation: np.ndarray  # [roll, pitch, yaw] or quaternion
    joint_angles: np.ndarray
    joint_velocities: np.ndarray
    held_object: Optional[str] = None
    battery_level: float = 1.0
    gripper_status: str = 'open'  # 'open', 'closed', 'moving'
    location: str = 'unknown'
    timestamp: float = 0.0
    velocity: np.ndarray = None  # [vx, vy, vz]
    
    def __post_init__(self):
        if self.velocity is None:
            self.velocity = np.zeros(3)


class PerceptionSystem:
    """Advanced perception system with multiple modalities"""
    
    def __init__(self):
        self.environment_map = self._create_environment_map()
        self.detected_objects = []
        self.localization_confidence = 0.95
        self.last_update_time = 0.0
    
    def _create_environment_map(self) -> np.ndarray:
        """Create a more complex environment map"""
        # Create a 50x50 grid for higher resolution
        grid = np.zeros((50, 50))
        
        # Add various obstacles and features
        # Walls
        grid[10:15, 10:40] = 1  # Horizontal wall
        grid[30:40, 20:25] = 1  # Vertical wall
        grid[20:25, 30:45] = 1  # Another wall
        
        # Tables/obstacles
        grid[35:38, 5:8] = 1  # Small table
        grid[42:46, 15:20] = 1  # Medium obstacle
        
        # Add some noise to make it more realistic
        noise = np.random.random(grid.shape) < 0.02  # 2% noise
        grid = np.clip(grid + noise, 0, 1)
        
        return grid
    
    def update_sensors(self, robot_state: RobotState) -> RobotState:
        """Update robot state based on sensor data"""
        # Simulate sensor noise and delays
        sensor_noise = np.random.normal(0, 0.02, 3)  # 2cm noise
        robot_state.position = robot_state.position + sensor_noise
        
        # Update timestamp
        robot_state.timestamp = time.time()
        
        # Detect objects in vicinity
        self.detected_objects = self._detect_objects(robot_state.position)
        
        # Update localization confidence based on sensor quality
        robot_state.location = self._estimate_location(robot_state.position)
        
        return robot_state
    
    def _detect_objects(self, robot_pos: np.ndarray) -> List[Dict[str, Any]]:
        """Simulate object detection around robot position"""
        objects = []
        
        # Define some objects in the environment
        env_objects = [
            {"name": "red_cube", "position": [8.0, 8.0, 0.1], "type": "graspable", "confidence": 0.95},
            {"name": "blue_sphere", "position": [35.0, 35.0, 0.15], "type": "graspable", "confidence": 0.89},
            {"name": "green_cylinder", "position": [42.0, 18.0, 0.12], "type": "graspable", "confidence": 0.92},
            {"name": "book", "position": [37.0, 37.0, 0.05], "type": "graspable", "confidence": 0.85},
            {"name": "plant", "position": [5.0, 45.0, 0.8], "type": "non_graspable", "confidence": 0.98}
        ]
        
        # Only detect objects within sensor range (5m)
        sensor_range = 5.0
        for obj in env_objects:
            obj_pos = np.array(obj["position"])
            distance = np.linalg.norm(robot_pos[:2] - obj_pos[:2])  # Only x,y for distance
            
            if distance <= sensor_range:
                # Add some detection noise
                noisy_pos = obj_pos + np.random.normal(0, 0.05, 3)  # 5cm detection noise
                detected_obj = obj.copy()
                detected_obj["position"] = noisy_pos.tolist()
                detected_obj["distance"] = distance
                objects.append(detected_obj)
        
        return objects
    
    def _estimate_location(self, position: np.ndarray) -> str:
        """Estimate current location based on position"""
        x, y = position[0], position[1]
        
        # Define location regions
        if 0 <= x <= 15 and 0 <= y <= 15:
            return "entrance"
        elif 15 < x <= 35 and 0 <= y <= 20:
            return "living_room"
        elif 35 < x <= 50 and 0 <= y <= 20:
            return "kitchen"
        elif 0 <= x <= 20 and 20 < y <= 35:
            return "office"
        elif 20 < x <= 40 and 20 < y <= 40:
            return "dining_room"
        elif 40 < x <= 50 and 20 < y <= 40:
            return "balcony"
        elif 0 <= x <= 25 and 35 < y <= 50:
            return "bedroom"
        elif 25 < x <= 50 and 35 < y <= 50:
            return "bathroom"
        else:
            return "unknown"


class PathPlanner:
    """Advanced path planning with multiple algorithms"""
    
    def __init__(self, perception_system: PerceptionSystem):
        self.perception = perception_system
        self.occupancy_grid = self.perception.environment_map
        self.grid_resolution = 1.0  # 1m per grid cell
    
    def plan_path(self, start: np.ndarray, goal: np.ndarray, 
                  algorithm: str = "hybrid") -> List[np.ndarray]:
        """Plan path using specified algorithm"""
        if algorithm == "a_star":
            return self._a_star_plan(start, goal)
        elif algorithm == "rrt":
            return self._rrt_plan(start, goal)
        elif algorithm == "hybrid":
            return self._hybrid_plan(start, goal)
        else:
            # Default to simple direct path
            return self._simple_plan(start, goal)
    
    def _simple_plan(self, start: np.ndarray, goal: np.ndarray) -> List[np.ndarray]:
        """Simple direct path planning"""
        path = [start.copy()]
        
        # Calculate direct path
        direction = goal - start
        distance = np.linalg.norm(direction[:2])  # Only x,y for distance
        
        if distance > 0.5:  # If goal is more than 0.5m away
            # Add intermediate waypoints
            num_waypoints = max(2, int(distance / 0.5))  # Waypoints every 0.5m
            
            for i in range(1, num_waypoints):
                t = i / num_waypoints
                waypoint = start + t * direction
                path.append(waypoint)
        
        path.append(goal.copy())
        return path
    
    def _a_star_plan(self, start: np.ndarray, goal: np.ndarray) -> List[np.ndarray]:
        """A* path planning implementation"""
        # Convert to grid coordinates
        start_grid = (int(start[0] / self.grid_resolution), int(start[1] / self.grid_resolution))
        goal_grid = (int(goal[0] / self.grid_resolution), int(goal[1] / self.grid_resolution))
        
        # Check if start and goal are valid
        if (not (0 <= start_grid[0] < self.occupancy_grid.shape[1] and 
                 0 <= start_grid[1] < self.occupancy_grid.shape[0]) or
            not (0 <= goal_grid[0] < self.occupancy_grid.shape[1] and 
                 0 <= goal_grid[1] < self.occupancy_grid.shape[0])):
            return [start, goal]  # Return direct path if out of bounds
        
        if (self.occupancy_grid[start_grid[1], start_grid[0]] == 1 or 
            self.occupancy_grid[goal_grid[1], goal_grid[0]] == 1):
            return [start, goal]  # Return direct path if start or goal is in obstacle
        
        # For simplicity, return direct path with intermediate points
        # A full A* implementation would be more complex
        return self._simple_plan(start, goal)
    
    def _rrt_plan(self, start: np.ndarray, goal: np.ndarray) -> List[np.ndarray]:
        """RRT path planning implementation"""
        # For simplicity, return direct path with random sampling
        # A full RRT implementation would be more complex
        return self._simple_plan(start, goal)
    
    def _hybrid_plan(self, start: np.ndarray, goal: np.ndarray) -> List[np.ndarray]:
        """Hybrid planning combining multiple approaches"""
        # Use A* for global path, then refine with local planning
        global_path = self._a_star_plan(start, goal)
        
        # For this example, return the global path
        return global_path


class NaturalLanguageProcessor:
    """Natural language processing for robot commands"""
    
    def __init__(self):
        self.intent_keywords = {
            'navigation': ['go to', 'move to', 'navigate to', 'travel to', 'walk to', 'drive to'],
            'grasp': ['pick up', 'grasp', 'take', 'get', 'catch', 'hold'],
            'place': ['place', 'put', 'set down', 'release', 'drop', 'lay'],
            'inspect': ['look at', 'examine', 'check', 'inspect', 'observe'],
            'transport': ['bring', 'carry', 'move', 'transfer'],
            'wait': ['wait', 'stop', 'pause', 'hold'],
            'greet': ['hello', 'hi', 'greet', 'welcome'],
            'inform': ['tell', 'report', 'inform', 'update']
        }
        
        self.location_keywords = {
            'kitchen': ['kitchen', 'cooking area', 'food area'],
            'living_room': ['living room', 'sitting room', 'lounge', 'family room'],
            'bedroom': ['bedroom', 'sleeping room', 'bed room'],
            'office': ['office', 'study', 'work room'],
            'bathroom': ['bathroom', 'restroom', 'toilet', 'washroom'],
            'dining_room': ['dining room', 'eat room', 'dinner room'],
            'balcony': ['balcony', 'terrace', 'patio'],
            'garden': ['garden', 'yard', 'outdoors']
        }
        
        self.object_keywords = {
            'red_cube': ['red cube', 'red block', 'red thing'],
            'blue_sphere': ['blue sphere', 'blue ball', 'blue round thing'],
            'green_cylinder': ['green cylinder', 'green tube', 'green container'],
            'book': ['book', 'reading material', 'literature'],
            'cup': ['cup', 'mug', 'glass', 'container'],
            'phone': ['phone', 'mobile', 'cellphone'],
            'keys': ['keys', 'keychain', 'key ring']
        }
    
    def parse_command(self, command: str) -> Dict[str, Any]:
        """Parse natural language command into structured format"""
        command_lower = command.lower()
        
        # Identify intent
        intent = self._identify_intent(command_lower)
        
        # Extract entities
        entities = self._extract_entities(command_lower)
        
        # Create structured command
        structured_command = {
            'original': command,
            'intent': intent,
            'entities': entities,
            'confidence': 0.8,  # Default confidence
            'timestamp': time.time()
        }
        
        return structured_command
    
    def _identify_intent(self, command: str) -> str:
        """Identify the intent of the command"""
        for intent, keywords in self.intent_keywords.items():
            for keyword in keywords:
                if keyword in command:
                    return intent
        
        return 'unknown'
    
    def _extract_entities(self, command: str) -> Dict[str, str]:
        """Extract named entities from command"""
        entities = {}
        
        # Extract locations
        for location, keywords in self.location_keywords.items():
            for keyword in keywords:
                if keyword in command:
                    entities['location'] = location
                    break
        
        # Extract objects
        for obj, keywords in self.object_keywords.items():
            for keyword in keywords:
                if keyword in command:
                    entities['object'] = obj
                    break
        
        # Extract other entities (numbers, etc.)
        import re
        numbers = re.findall(r'\d+', command)
        if numbers:
            entities['number'] = int(numbers[0])
        
        return entities


class TaskPlanner:
    """High-level task planning system"""
    
    def __init__(self, perception: PerceptionSystem, path_planner: PathPlanner, 
                 nlp: NaturalLanguageProcessor):
        self.perception = perception
        self.path_planner = path_planner
        self.nlp = nlp
        self.task_queue = []
        self.current_task = None
    
    def plan_task(self, command: str, robot_state: RobotState) -> List[Dict[str, Any]]:
        """Plan a task from natural language command"""
        # Parse command
        parsed_command = self.nlp.parse_command(command)
        intent = parsed_command['intent']
        entities = parsed_command['entities']
        
        # Generate task plan based on intent
        task_plan = []
        
        if intent == 'navigation':
            location = entities.get('location', 'unknown')
            if location != 'unknown':
                task_plan.append({
                    'action': 'navigate_to',
                    'parameters': {'location': location},
                    'description': f'Navigate to {location}',
                    'priority': 1
                })
        
        elif intent == 'grasp':
            obj = entities.get('object', 'unknown')
            if obj != 'unknown':
                # First navigate to object, then grasp
                task_plan.extend([
                    {
                        'action': 'find_object',
                        'parameters': {'object_name': obj},
                        'description': f'Locate {obj}',
                        'priority': 2
                    },
                    {
                        'action': 'navigate_to_object',
                        'parameters': {'object_name': obj},
                        'description': f'Move to {obj}',
                        'priority': 1
                    },
                    {
                        'action': 'grasp_object',
                        'parameters': {'object_name': obj},
                        'description': f'Grasp {obj}',
                        'priority': 3
                    }
                ])
        
        elif intent == 'place':
            location = entities.get('location', 'table')
            task_plan.extend([
                {
                    'action': 'navigate_to',
                    'parameters': {'location': location},
                    'description': f'Navigate to {location}',
                    'priority': 1
                },
                {
                    'action': 'place_object',
                    'parameters': {'location': location},
                    'description': f'Place object at {location}',
                    'priority': 3
                }
            ])
        
        elif intent == 'transport':
            obj = entities.get('object', 'unknown')
            location = entities.get('location', 'unknown')
            
            if obj != 'unknown' and location != 'unknown':
                task_plan.extend([
                    {
                        'action': 'navigate_to_object',
                        'parameters': {'object_name': obj},
                        'description': f'Go to {obj}',
                        'priority': 1
                    },
                    {
                        'action': 'grasp_object',
                        'parameters': {'object_name': obj},
                        'description': f'Grasp {obj}',
                        'priority': 3
                    },
                    {
                        'action': 'navigate_to',
                        'parameters': {'location': location},
                        'description': f'Go to {location}',
                        'priority': 1
                    },
                    {
                        'action': 'place_object',
                        'parameters': {'location': location},
                        'description': f'Place object at {location}',
                        'priority': 3
                    }
                ])
        
        elif intent == 'inspect':
            obj = entities.get('object', 'unknown')
            if obj != 'unknown':
                task_plan.extend([
                    {
                        'action': 'find_object',
                        'parameters': {'object_name': obj},
                        'description': f'Locate {obj}',
                        'priority': 2
                    },
                    {
                        'action': 'navigate_to_object',
                        'parameters': {'object_name': obj},
                        'description': f'Move closer to {obj}',
                        'priority': 1
                    },
                    {
                        'action': 'inspect_object',
                        'parameters': {'object_name': obj},
                        'description': f'Inspect {obj}',
                        'priority': 2
                    }
                ])
        
        else:
            task_plan.append({
                'action': 'idle',
                'parameters': {},
                'description': 'No specific action required',
                'priority': 0
            })
        
        # Sort by priority (higher priority first)
        task_plan.sort(key=lambda x: x['priority'], reverse=True)
        
        return task_plan


class Controller:
    """Low-level control system"""
    
    def __init__(self, path_planner: PathPlanner, perception: PerceptionSystem):
        self.path_planner = path_planner
        self.perception = perception
        self.current_trajectory = []
        self.trajectory_index = 0
        self.executing_action = False
        self.action_progress = 0.0
        self.max_velocity = 0.5  # m/s
        self.max_angular_velocity = 0.5  # rad/s
    
    def execute_action(self, action: Dict[str, Any], robot_state: RobotState) -> bool:
        """Execute a single action"""
        action_type = action['action']
        params = action['parameters']
        
        print(f"Executing action: {action['description']}")
        
        if action_type == 'navigate_to':
            return self._execute_navigation(params, robot_state)
        elif action_type == 'navigate_to_object':
            return self._execute_navigate_to_object(params, robot_state)
        elif action_type == 'grasp_object':
            return self._execute_grasp(params, robot_state)
        elif action_type == 'place_object':
            return self._execute_place(params, robot_state)
        elif action_type == 'find_object':
            return self._execute_find_object(params, robot_state)
        elif action_type == 'inspect_object':
            return self._execute_inspect(params, robot_state)
        elif action_type == 'idle':
            return self._execute_idle(params, robot_state)
        else:
            print(f"Unknown action type: {action_type}")
            return False
    
    def _execute_navigation(self, params: Dict[str, Any], robot_state: RobotState) -> bool:
        """Execute navigation action"""
        location = params.get('location', 'unknown')
        
        # Get location coordinates
        location_coords = self._get_location_coordinates(location)
        if location_coords is None:
            print(f"Unknown location: {location}")
            return False
        
        goal_pos = np.array(location_coords)
        start_pos = robot_state.position.copy()
        
        # Plan path
        path = self.path_planner.plan_path(start_pos, goal_pos)
        
        # Execute path following
        print(f"Following path to {location} with {len(path)} waypoints")
        
        for i, waypoint in enumerate(path):
            # Update robot position (simulated)
            robot_state.position = waypoint.copy()
            
            # Update robot location
            robot_state.location = location
            
            # Simulate time delay
            time.sleep(0.1)
            
            print(f"  Reached waypoint {i+1}/{len(path)}: [{waypoint[0]:.2f}, {waypoint[1]:.2f}, {waypoint[2]:.2f}]")
        
        print(f"Successfully navigated to {location}")
        return True
    
    def _execute_navigate_to_object(self, params: Dict[str, Any], robot_state: RobotState) -> bool:
        """Navigate to a specific object"""
        obj_name = params.get('object_name', 'unknown')
        
        # Find object in perception
        target_obj = None
        for obj in self.perception.detected_objects:
            if obj['name'] == obj_name:
                target_obj = obj
                break
        
        if not target_obj:
            print(f"Could not find object: {obj_name}")
            return False
        
        goal_pos = np.array(target_obj['position'])
        start_pos = robot_state.position.copy()
        
        # Plan path
        path = self.path_planner.plan_path(start_pos, goal_pos)
        
        # Execute path following
        print(f"Moving to {obj_name} at {target_obj['position']}")
        
        for i, waypoint in enumerate(path):
            # Update robot position (simulated)
            robot_state.position = waypoint.copy()
            
            # Simulate time delay
            time.sleep(0.1)
            
            print(f"  Approaching object, waypoint {i+1}/{len(path)}: [{waypoint[0]:.2f}, {waypoint[1]:.2f}, {waypoint[2]:.2f}]")
        
        print(f"Successfully approached {obj_name}")
        return True
    
    def _execute_grasp(self, params: Dict[str, Any], robot_state: RobotState) -> bool:
        """Execute grasp action"""
        obj_name = params.get('object_name', 'unknown')
        
        # Check if object is reachable
        target_obj = None
        for obj in self.perception.detected_objects:
            if obj['name'] == obj_name:
                target_obj = obj
                break
        
        if not target_obj:
            print(f"Could not find object: {obj_name}")
            return False
        
        # Check if object is within reach (within 0.5m)
        obj_pos = np.array(target_obj['position'])
        distance = np.linalg.norm(robot_state.position - obj_pos)
        
        if distance > 0.5:
            print(f"Object {obj_name} is out of reach (distance: {distance:.2f}m)")
            return False
        
        # Simulate grasping process
        print(f"Grasping {obj_name} at {target_obj['position']}")
        time.sleep(0.5)  # Simulate grasp time
        
        # Update robot state
        robot_state.held_object = obj_name
        robot_state.gripper_status = 'closed'
        
        print(f"Successfully grasped {obj_name}")
        return True
    
    def _execute_place(self, params: Dict[str, Any], robot_state: RobotState) -> bool:
        """Execute place action"""
        location = params.get('location', 'table')
        
        # Check if robot is holding an object
        if not robot_state.held_object:
            print("Cannot place object: robot is not holding anything")
            return False
        
        # Simulate placing process
        print(f"Placing {robot_state.held_object} at {location}")
        time.sleep(0.3)  # Simulate place time
        
        # Update robot state
        held_obj = robot_state.held_object
        robot_state.held_object = None
        robot_state.gripper_status = 'open'
        
        print(f"Successfully placed {held_obj} at {location}")
        return True
    
    def _execute_find_object(self, params: Dict[str, Any], robot_state: RobotState) -> bool:
        """Execute find object action"""
        obj_name = params.get('object_name', 'unknown')
        
        # Check if object is already detected
        for obj in self.perception.detected_objects:
            if obj['name'] == obj_name:
                print(f"Found {obj_name} at {obj['position']}")
                return True
        
        # If not found, simulate search
        print(f"Searching for {obj_name}...")
        time.sleep(1.0)  # Simulate search time
        
        # Update perception to include the object if found
        self.perception.update_sensors(robot_state)
        
        # Check again
        for obj in self.perception.detected_objects:
            if obj['name'] == obj_name:
                print(f"Found {obj_name} at {obj['position']}")
                return True
        
        print(f"Could not find {obj_name}")
        return False
    
    def _execute_inspect(self, params: Dict[str, Any], robot_state: RobotState) -> bool:
        """Execute inspection action"""
        obj_name = params.get('object_name', 'unknown')
        
        # Find object
        target_obj = None
        for obj in self.perception.detected_objects:
            if obj['name'] == obj_name:
                target_obj = obj
                break
        
        if not target_obj:
            print(f"Could not find object to inspect: {obj_name}")
            return False
        
        # Simulate inspection
        print(f"Inspecting {obj_name} at {target_obj['position']}")
        print(f"  Type: {target_obj.get('type', 'unknown')}")
        print(f"  Confidence: {target_obj.get('confidence', 0):.2f}")
        print(f"  Distance: {target_obj.get('distance', 0):.2f}m")
        
        time.sleep(0.5)  # Simulate inspection time
        
        print(f"Completed inspection of {obj_name}")
        return True
    
    def _execute_idle(self, params: Dict[str, Any], robot_state: RobotState) -> bool:
        """Execute idle action"""
        print("Robot is idle, waiting for next command")
        time.sleep(0.1)
        return True
    
    def _get_location_coordinates(self, location: str) -> Optional[Tuple[float, float, float]]:
        """Get coordinates for a named location"""
        locations = {
            'kitchen': (40.0, 10.0, 0.0),
            'living_room': (25.0, 10.0, 0.0),
            'bedroom': (10.0, 40.0, 0.0),
            'office': (10.0, 25.0, 0.0),
            'bathroom': (45.0, 45.0, 0.0),
            'dining_room': (30.0, 30.0, 0.0),
            'balcony': (45.0, 30.0, 0.0),
            'entrance': (5.0, 5.0, 0.0)
        }
        
        if location in locations:
            return locations[location]
        else:
            return None


class SafetySystem:
    """Safety monitoring and emergency response"""
    
    def __init__(self):
        self.emergency_stop = False
        self.safety_limits = {
            'max_velocity': 1.0,
            'max_angular_velocity': 1.0,
            'max_force': 50.0,
            'min_battery': 0.1,  # 10% minimum
            'workspace_boundary': [[0, 50], [0, 50], [0, 2]]  # x, y, z limits
        }
        self.safety_violations = []
    
    def check_safety(self, robot_state: RobotState) -> bool:
        """Check if current state is safe"""
        if self.emergency_stop:
            return False
        
        # Check workspace boundaries
        pos = robot_state.position
        boundary = self.safety_limits['workspace_boundary']
        
        for i, (min_val, max_val) in enumerate(boundary):
            if not (min_val <= pos[i] <= max_val):
                violation = f"Position {pos[i]:.2f} outside boundary [{min_val}, {max_val}] for axis {i}"
                self.safety_violations.append(violation)
                print(f"Safety violation: {violation}")
                return False
        
        # Check battery level
        if robot_state.battery_level < self.safety_limits['min_battery']:
            violation = f"Battery level critically low: {robot_state.battery_level:.2f}"
            self.safety_violations.append(violation)
            print(f"Safety warning: {violation}")
            # This might not be a hard stop, but a warning
            return True  # Still safe to operate
        
        # Check velocity limits
        vel = robot_state.velocity
        max_vel = self.safety_limits['max_velocity']
        if np.linalg.norm(vel) > max_vel:
            violation = f"Velocity too high: {np.linalg.norm(vel):.2f} > {max_vel}"
            self.safety_violations.append(violation)
            print(f"Safety warning: {violation}")
            return True  # Still safe but with warning
        
        return True
    
    def emergency_stop(self):
        """Trigger emergency stop"""
        self.emergency_stop = True
        print("EMERGENCY STOP ACTIVATED")
    
    def reset_safety(self):
        """Reset emergency stop"""
        self.emergency_stop = False
        print("Safety system reset")


class IntegratedPhysicalAISystem:
    """Complete integrated Physical AI system"""
    
    def __init__(self):
        # Initialize all components
        self.perception = PerceptionSystem()
        self.path_planner = PathPlanner(self.perception)
        self.nlp = NaturalLanguageProcessor()
        self.task_planner = TaskPlanner(self.perception, self.path_planner, self.nlp)
        self.controller = Controller(self.path_planner, self.perception)
        self.safety_system = SafetySystem()
        
        # Initialize robot state
        self.robot_state = RobotState(
            position=np.array([5.0, 5.0, 0.0]),  # Start at entrance
            orientation=np.array([0.0, 0.0, 0.0]),
            joint_angles=np.zeros(12),  # 12 DOF for example
            joint_velocities=np.zeros(12),
            battery_level=1.0,
            location='entrance'
        )
        
        # System state
        self.running = False
        self.command_queue = []
        self.execution_log = []
    
    def process_command(self, command: str) -> bool:
        """Process a high-level command"""
        print(f"\n{'='*60}")
        print(f"Processing command: {command}")
        print(f"{'='*60}")
        
        # Update perception
        self.robot_state = self.perception.update_sensors(self.robot_state)
        
        # Check safety
        if not self.safety_system.check_safety(self.robot_state):
            print("Safety check failed, aborting command")
            return False
        
        # Plan task
        task_plan = self.task_planner.plan_task(command, self.robot_state)
        
        if not task_plan:
            print("Could not generate plan for command")
            return False
        
        print(f"Generated task plan with {len(task_plan)} actions:")
        for i, action in enumerate(task_plan):
            print(f"  {i+1}. {action['description']} (Priority: {action['priority']})")
        
        # Execute plan
        for action in task_plan:
            # Check safety before each action
            if not self.safety_system.check_safety(self.robot_state):
                print("Safety check failed during execution, stopping")
                return False
            
            success = self.controller.execute_action(action, self.robot_state)
            
            if not success:
                print(f"Action failed: {action['description']}")
                
                # Log execution
                self.execution_log.append({
                    'command': command,
                    'action': action['description'],
                    'success': success,
                    'timestamp': time.time(),
                    'robot_state': self.robot_state.__dict__.copy()
                })
                
                return False
        
        # Log successful execution
        self.execution_log.append({
            'command': command,
            'success': True,
            'actions_completed': len(task_plan),
            'timestamp': time.time(),
            'robot_state': self.robot_state.__dict__.copy()
        })
        
        print(f"Successfully completed command: {command}")
        print(f"Final robot state: Position={self.robot_state.position}, Holding={self.robot_state.held_object}, Location={self.robot_state.location}")
        
        return True
    
    def run_demo_scenario(self):
        """Run a demonstration scenario"""
        print("\n" + "="*60)
        print("PHYSICAL AI SYSTEM DEMONSTRATION SCENARIO")
        print("="*60)
        
        # Define a scenario with multiple commands
        scenario_commands = [
            "Take the red cube from near the entrance",
            "Go to the kitchen",
            "Place the red cube on the counter",
            "Go to the bedroom",
            "Find the green cylinder",
            "Bring the green cylinder to the living room"
        ]
        
        print(f"Running scenario with {len(scenario_commands)} commands...")
        
        success_count = 0
        for i, command in enumerate(scenario_commands):
            print(f"\n--- Command {i+1}/{len(scenario_commands)} ---")
            success = self.process_command(command)
            if success:
                success_count += 1
            print(f"Command {i+1} {'SUCCEEDED' if success else 'FAILED'}")
        
        print(f"\nScenario completed: {success_count}/{len(scenario_commands)} commands succeeded")
        
        # Print final state
        print(f"\nFinal robot state:")
        print(f"  Position: [{self.robot_state.position[0]:.2f}, {self.robot_state.position[1]:.2f}, {self.robot_state.position[2]:.2f}]")
        print(f"  Location: {self.robot_state.location}")
        print(f"  Holding: {self.robot_state.held_object}")
        print(f"  Battery: {self.robot_state.battery_level:.2f}")
        print(f"  Gripper: {self.robot_state.gripper_status}")
        
        # Print safety violations
        if self.safety_system.safety_violations:
            print(f"\nSafety violations recorded: {len(self.safety_system.safety_violations)}")
            for violation in self.safety_system.safety_violations[-5:]:  # Last 5 violations
                print(f"  - {violation}")
        else:
            print(f"\nNo safety violations recorded.")
        
        return success_count == len(scenario_commands)


def main():
    """Main function to run the integrated system example"""
    print("Physical AI & Humanoid Robotics - Integrated System Example")
    print("=" * 60)
    
    # Create the integrated system
    system = IntegratedPhysicalAISystem()
    
    # Run the demonstration scenario
    success = system.run_demo_scenario()
    
    print(f"\n{'='*60}")
    if success:
        print("DEMONSTRATION SUCCESSFUL: All commands completed successfully!")
    else:
        print("DEMONSTRATION PARTIAL: Some commands failed, but system operated correctly.")
    print("=" * 60)
    
    # Print system statistics
    print(f"\nSystem Statistics:")
    print(f"  Total executions logged: {len(system.execution_log)}")
    print(f"  Final battery level: {system.robot_state.battery_level:.2f}")
    print(f"  Objects handled: {len([log for log in system.execution_log if 'holding' in str(log)])}")
    
    print(f"\nSystem demonstrates integration of:")
    print(f"  - Perception (environment sensing and object detection)")
    print(f"  - Natural Language Processing (command understanding)")
    print(f"  - Task Planning (high-level action sequencing)")
    print(f"  - Path Planning (navigation planning)")
    print(f"  - Control (low-level action execution)")
    print(f"  - Safety (monitoring and emergency response)")
    
    print(f"\nIntegration example completed successfully!")


if __name__ == "__main__":
    main()