---
sidebar_position: 31
---

# Week 11: LLM-Based Planning and Cognitive Robotics

Welcome to Week 11 of our Physical AI & Humanoid Robotics journey! This week, we'll explore how Large Language Models (LLMs) can be used for high-level planning and cognitive reasoning in robotic systems. This represents a significant advancement in embodied AI, where robots can understand and execute complex, natural language instructions.

## Learning Objectives

By the end of this week, you will be able to:

1. Understand the integration of LLMs with robotic systems
2. Implement LLM-based task decomposition and planning
3. Design cognitive architectures for robotic reasoning
4. Create systems that combine LLMs with traditional planning
5. Evaluate LLM-based planning performance and reliability
6. Address challenges in LLM-robot integration

## Introduction to LLM-Based Planning

Large Language Models have revolutionized natural language understanding and generation. When integrated with robotic systems, they enable robots to:

- Interpret complex, natural language instructions
- Decompose high-level tasks into executable actions
- Reason about the world and plan accordingly
- Adapt to new situations using learned knowledge
- Explain their actions and decisions

### Why LLMs Matter for Physical AI

LLMs bring several advantages to Physical AI systems:

- **Natural Language Interface**: Enable communication using everyday language
- **World Knowledge**: Leverage vast amounts of learned world knowledge
- **Reasoning Capabilities**: Perform logical reasoning and planning
- **Generalization**: Apply learned patterns to new situations
- **Explainability**: Provide natural language explanations for actions

### Challenges in LLM-Robot Integration

However, integrating LLMs with robots presents challenges:

- **Grounding**: Connecting abstract language concepts to physical reality
- **Reliability**: Ensuring consistent, safe behavior
- **Real-time Constraints**: Meeting timing requirements for robot control
- **Embodiment**: Incorporating robot-specific constraints and capabilities
- **Verification**: Ensuring plans are physically executable

## LLM Integration Architectures

### Direct Integration Approach

The simplest approach connects LLMs directly to robot actions:

```python
import openai
import json
from typing import Dict, List, Any

class DirectLLMPlanner:
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        """
        Direct integration of LLM with robot planning
        
        Args:
            api_key: OpenAI API key
            model: LLM model to use
        """
        openai.api_key = api_key
        self.model = model
        
        # Robot capabilities
        self.capabilities = {
            "navigation": ["go_to", "move_to", "navigate_to"],
            "manipulation": ["pick_up", "place", "grasp", "release"],
            "interaction": ["speak", "listen", "greet"],
            "perception": ["find_object", "identify", "locate"]
        }
    
    def plan_from_instruction(self, instruction: str, robot_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate a plan from natural language instruction
        
        Args:
            instruction: Natural language instruction
            robot_state: Current robot state
            
        Returns:
            List of actions to execute
        """
        prompt = f"""
        You are a robot planning system. Given the following instruction and robot state,
        decompose the task into a sequence of executable actions.
        
        Robot capabilities: {json.dumps(self.capabilities)}
        Current robot state: {json.dumps(robot_state)}
        Instruction: {instruction}
        
        Respond with a JSON list of actions. Each action should have:
        - "action": the action type
        - "parameters": action parameters
        - "description": brief description of the action
        
        Example response:
        [
            {{
                "action": "navigate_to",
                "parameters": {{"location": "kitchen"}},
                "description": "Move to the kitchen"
            }},
            {{
                "action": "find_object",
                "parameters": {{"object": "red cup"}},
                "description": "Locate the red cup"
            }}
        ]
        
        Response (JSON only):
        """
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1  # Low temperature for more consistent outputs
        )
        
        try:
            # Parse the response
            plan_json = json.loads(response.choices[0].message.content.strip())
            return plan_json
        except json.JSONDecodeError:
            print(f"Failed to parse LLM response: {response.choices[0].message.content}")
            return []
    
    def execute_plan(self, plan: List[Dict[str, Any]], robot_interface) -> bool:
        """
        Execute a plan generated by the LLM
        
        Args:
            plan: List of actions to execute
            robot_interface: Interface to control the robot
            
        Returns:
            True if plan executed successfully, False otherwise
        """
        for i, action in enumerate(plan):
            print(f"Executing action {i+1}/{len(plan)}: {action['description']}")
            
            action_type = action['action']
            params = action['parameters']
            
            # Execute the action based on type
            success = self.execute_single_action(action_type, params, robot_interface)
            
            if not success:
                print(f"Action failed: {action}")
                return False
        
        return True
    
    def execute_single_action(self, action_type: str, params: Dict[str, Any], robot_interface) -> bool:
        """
        Execute a single action on the robot
        
        Args:
            action_type: Type of action to execute
            params: Action parameters
            robot_interface: Interface to control the robot
            
        Returns:
            True if action executed successfully, False otherwise
        """
        # This is a simplified implementation
        # In practice, this would interface with actual robot systems
        try:
            if action_type in self.capabilities['navigation']:
                # Example: robot_interface.navigate_to(params['location'])
                print(f"  Navigating to {params.get('location', 'unknown location')}")
                return True
            elif action_type in self.capabilities['manipulation']:
                # Example: robot_interface.grasp_object(params['object'])
                print(f"  Manipulating {params.get('object', 'unknown object')}")
                return True
            elif action_type in self.capabilities['interaction']:
                # Example: robot_interface.speak(params['text'])
                print(f"  Interacting: {params.get('text', 'no text provided')}")
                return True
            elif action_type in self.capabilities['perception']:
                # Example: robot_interface.locate_object(params['object'])
                print(f"  Perceiving: {params.get('object', 'unknown object')}")
                return True
            else:
                print(f"  Unknown action type: {action_type}")
                return False
        except Exception as e:
            print(f"  Error executing action: {e}")
            return False

# Example usage
def example_direct_integration():
    # This would require a valid OpenAI API key
    # planner = DirectLLMPlanner(api_key="your-api-key")
    
    # Example robot state
    robot_state = {
        "location": "living_room",
        "battery_level": 0.85,
        "gripper_status": "open",
        "objects_detected": ["red cup", "blue bottle", "book"]
    }
    
    # Example instruction
    instruction = "Go to the kitchen, find the red cup, and bring it to the living room"
    
    # In practice:
    # plan = planner.plan_from_instruction(instruction, robot_state)
    # print(f"Generated plan: {json.dumps(plan, indent=2)}")
    
    print("Direct LLM integration example completed.")

# Run example
example_direct_integration()
```

### Tool-Augmented LLM Approach

A more sophisticated approach uses LLMs with specialized tools for robotics:

```python
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class ToolCall:
    """Represents a call to a specific tool"""
    name: str
    arguments: Dict[str, Any]

class ToolAugmentedPlanner:
    def __init__(self):
        """
        LLM planner that uses specialized tools for robotics
        """
        self.tools = {
            "navigate_to_location": {
                "name": "navigate_to_location",
                "description": "Navigate the robot to a specific location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string", "description": "The location to navigate to"}
                    },
                    "required": ["location"]
                }
            },
            "find_object": {
                "name": "find_object", 
                "description": "Find a specific object in the environment",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "object_name": {"type": "string", "description": "The name of the object to find"},
                        "location_hint": {"type": "string", "description": "Optional hint about where to look"}
                    },
                    "required": ["object_name"]
                }
            },
            "grasp_object": {
                "name": "grasp_object",
                "description": "Grasp a specific object",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "object_name": {"type": "string", "description": "The name of the object to grasp"},
                        "grasp_type": {"type": "string", "description": "Type of grasp (e.g., 'precision', 'power')"}
                    },
                    "required": ["object_name"]
                }
            },
            "place_object": {
                "name": "place_object",
                "description": "Place a grasped object at a location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string", "description": "Where to place the object"},
                        "object_name": {"type": "string", "description": "The name of the object to place"}
                    },
                    "required": ["location", "object_name"]
                }
            },
            "get_robot_state": {
                "name": "get_robot_state",
                "description": "Get the current state of the robot",
                "parameters": {
                    "type": "object",
                    "properties": {},
                }
            }
        }
    
    def plan_with_tools(self, instruction: str, robot_state: Dict[str, Any]) -> List[ToolCall]:
        """
        Generate a plan using LLM with specialized tools
        
        Args:
            instruction: Natural language instruction
            robot_state: Current robot state
            
        Returns:
            List of tool calls to execute
        """
        # In practice, this would call an LLM with tool definitions
        # For this example, we'll simulate the process
        
        print(f"Planning for instruction: {instruction}")
        print(f"Current state: {robot_state}")
        
        # Simulate LLM thinking process
        if "bring" in instruction.lower() and "red cup" in instruction.lower():
            # Simulate tool calls that the LLM would generate
            tool_calls = [
                ToolCall(name="navigate_to_location", arguments={"location": "kitchen"}),
                ToolCall(name="find_object", arguments={"object_name": "red cup"}),
                ToolCall(name="grasp_object", arguments={"object_name": "red cup", "grasp_type": "precision"}),
                ToolCall(name="navigate_to_location", arguments={"location": "living room"}),
                ToolCall(name="place_object", arguments={"location": "table", "object_name": "red cup"})
            ]
            return tool_calls
        else:
            # For other instructions, return a generic plan
            return [ToolCall(name="get_robot_state", arguments={})]
    
    def execute_tool_call(self, tool_call: ToolCall, robot_interface) -> Dict[str, Any]:
        """
        Execute a tool call on the robot
        
        Args:
            tool_call: Tool call to execute
            robot_interface: Interface to control the robot
            
        Returns:
            Result of the tool execution
        """
        print(f"Executing tool: {tool_call.name} with args: {tool_call.arguments}")
        
        # Simulate tool execution
        if tool_call.name == "navigate_to_location":
            location = tool_call.arguments.get("location", "unknown")
            print(f"  Navigating to {location}")
            return {"status": "success", "message": f"Navigated to {location}"}
        elif tool_call.name == "find_object":
            obj_name = tool_call.arguments.get("object_name", "unknown")
            location_hint = tool_call.arguments.get("location_hint", "anywhere")
            print(f"  Searching for {obj_name} in {location_hint}")
            return {"status": "success", "found": True, "location": "kitchen_counter"}
        elif tool_call.name == "grasp_object":
            obj_name = tool_call.arguments.get("object_name", "unknown")
            grasp_type = tool_call.arguments.get("grasp_type", "precision")
            print(f"  Grasping {obj_name} with {grasp_type} grasp")
            return {"status": "success", "grasped_object": obj_name}
        elif tool_call.name == "place_object":
            location = tool_call.arguments.get("location", "unknown")
            obj_name = tool_call.arguments.get("object_name", "unknown")
            print(f"  Placing {obj_name} at {location}")
            return {"status": "success", "placed_at": location}
        elif tool_call.name == "get_robot_state":
            print("  Retrieving robot state")
            return robot_interface.get_state() if robot_interface else {"location": "unknown", "battery": 1.0}
        else:
            return {"status": "error", "message": f"Unknown tool: {tool_call.name}"}

# Example usage
def example_tool_augmented():
    planner = ToolAugmentedPlanner()
    
    robot_state = {
        "location": "living_room",
        "battery_level": 0.85,
        "held_object": None
    }
    
    instruction = "Please bring the red cup from the kitchen to the living room"
    
    # Plan with tools
    tool_calls = planner.plan_with_tools(instruction, robot_state)
    
    print(f"\nGenerated tool calls:")
    for i, call in enumerate(tool_calls):
        print(f"  {i+1}. {call.name}({call.arguments})")
    
    # Simulate robot interface
    class MockRobotInterface:
        def get_state(self):
            return {"location": "living_room", "battery": 0.85, "gripper": "open"}
    
    robot_interface = MockRobotInterface()
    
    # Execute tool calls
    print(f"\nExecuting tool calls:")
    for call in tool_calls:
        result = planner.execute_tool_call(call, robot_interface)
        print(f"  Result: {result}")

example_tool_augmented()
```

## Cognitive Architecture for LLM-Based Planning

### Memory-Augmented Reasoning

Incorporating memory systems with LLMs for better reasoning:

```python
import datetime
from typing import Dict, List, Any, Optional
import json

class EpisodicMemory:
    def __init__(self, capacity: int = 100):
        """
        Store episodic memories of robot experiences
        
        Args:
            capacity: Maximum number of memories to store
        """
        self.capacity = capacity
        self.memories = []  # List of (timestamp, memory) tuples
    
    def add_memory(self, memory: Dict[str, Any]):
        """Add a new memory"""
        timestamp = datetime.datetime.now().isoformat()
        self.memories.append((timestamp, memory))
        
        # Keep only the most recent memories
        if len(self.memories) > self.capacity:
            self.memories = self.memories[-self.capacity:]
    
    def retrieve_memories(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant memories based on query
        (Simplified implementation - in practice, use vector similarity)
        """
        # For this example, return the most recent memories
        # In practice, implement semantic search
        recent_memories = [mem for _, mem in self.memories[-k:]]
        return recent_memories
    
    def serialize(self) -> str:
        """Serialize memories to string"""
        return json.dumps([{"timestamp": ts, "memory": mem} for ts, mem in self.memories])

class SemanticMemory:
    def __init__(self):
        """
        Store general knowledge and facts learned by the robot
        """
        self.facts = {}  # Maps entity -> list of facts
        self.object_properties = {}  # Maps object -> properties
        self.location_mappings = {}  # Maps location names to coordinates
    
    def add_fact(self, subject: str, predicate: str, obj: str):
        """Add a fact to semantic memory"""
        if subject not in self.facts:
            self.facts[subject] = []
        self.facts[subject].append((predicate, obj))
    
    def add_object_property(self, obj_name: str, property_name: str, value: Any):
        """Add a property to an object"""
        if obj_name not in self.object_properties:
            self.object_properties[obj_name] = {}
        self.object_properties[obj_name][property_name] = value
    
    def add_location_mapping(self, location_name: str, coordinates: Dict[str, float]):
        """Add a location mapping"""
        self.location_mappings[location_name] = coordinates
    
    def get_related_facts(self, entity: str) -> List[tuple]:
        """Get facts related to an entity"""
        return self.facts.get(entity, [])
    
    def get_object_properties(self, obj_name: str) -> Dict[str, Any]:
        """Get properties of an object"""
        return self.object_properties.get(obj_name, {})
    
    def get_location_coordinates(self, location_name: str) -> Optional[Dict[str, float]]:
        """Get coordinates for a location"""
        return self.location_mappings.get(location_name)

class LLMCognitiveArchitecture:
    def __init__(self, llm_planner):
        """
        Cognitive architecture integrating LLM with memory systems
        
        Args:
            llm_planner: LLM-based planner component
        """
        self.llm_planner = llm_planner
        self.episodic_memory = EpisodicMemory(capacity=50)
        self.semantic_memory = SemanticMemory()
        self.working_memory = {}  # Current task context
    
    def process_instruction(self, instruction: str, robot_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Process an instruction using the cognitive architecture
        
        Args:
            instruction: Natural language instruction
            robot_state: Current robot state
            
        Returns:
            List of actions to execute
        """
        # Retrieve relevant episodic memories
        recent_memories = self.episodic_memory.retrieve_memories(instruction, k=3)
        
        # Gather relevant semantic knowledge
        semantic_knowledge = self._gather_semantic_knowledge(instruction)
        
        # Combine information for LLM planning
        context = {
            "instruction": instruction,
            "robot_state": robot_state,
            "recent_memories": recent_memories,
            "semantic_knowledge": semantic_knowledge,
            "working_memory": self.working_memory
        }
        
        # Generate plan using LLM
        plan = self.llm_planner.plan_from_context(context)
        
        # Store the interaction in episodic memory
        memory_entry = {
            "instruction": instruction,
            "plan": plan,
            "state_before": robot_state.copy(),
            "timestamp": datetime.datetime.now().isoformat()
        }
        self.episodic_memory.add_memory(memory_entry)
        
        return plan
    
    def _gather_semantic_knowledge(self, instruction: str) -> Dict[str, Any]:
        """Gather relevant semantic knowledge for the instruction"""
        # Extract entities from instruction (simplified)
        entities = self._extract_entities(instruction)
        
        knowledge = {
            "object_properties": {},
            "location_info": {},
            "general_facts": []
        }
        
        for entity in entities:
            # Get object properties
            obj_props = self.semantic_memory.get_object_properties(entity)
            if obj_props:
                knowledge["object_properties"][entity] = obj_props
            
            # Get location coordinates
            loc_coords = self.semantic_memory.get_location_coordinates(entity)
            if loc_coords:
                knowledge["location_info"][entity] = loc_coords
            
            # Get related facts
            facts = self.semantic_memory.get_related_facts(entity)
            if facts:
                knowledge["general_facts"].extend(facts)
        
        return knowledge
    
    def _extract_entities(self, instruction: str) -> List[str]:
        """Extract entities from instruction (simplified)"""
        # This is a simplified entity extraction
        # In practice, use NLP techniques or LLMs
        import re
        
        # Common object types
        objects = re.findall(r'\b(red|blue|green|cup|bottle|book|phone|table|chair|box)\b', instruction.lower())
        locations = re.findall(r'\b(kitchen|living room|bedroom|office|bathroom|garage|garden)\b', instruction.lower())
        
        return list(set(objects + locations))
    
    def update_semantic_memory(self, new_knowledge: Dict[str, Any]):
        """Update semantic memory with new knowledge"""
        # Add object properties
        for obj_name, props in new_knowledge.get("object_properties", {}).items():
            for prop_name, value in props.items():
                self.semantic_memory.add_object_property(obj_name, prop_name, value)
        
        # Add location mappings
        for loc_name, coords in new_knowledge.get("location_mappings", {}).items():
            self.semantic_memory.add_location_mapping(loc_name, coords)
        
        # Add general facts
        for subject, predicate, obj in new_knowledge.get("facts", []):
            self.semantic_memory.add_fact(subject, predicate, obj)

# Example usage
def example_cognitive_architecture():
    # Create a simple planner for the cognitive architecture
    class SimpleLLMPlanner:
        def plan_from_context(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
            instruction = context["instruction"]
            print(f"Planning for: {instruction}")
            
            # Simple planning based on instruction
            if "bring" in instruction.lower():
                return [
                    {"action": "navigate_to", "params": {"location": "kitchen"}, "desc": "Go to kitchen"},
                    {"action": "find_object", "params": {"object": "cup"}, "desc": "Find cup"},
                    {"action": "grasp_object", "params": {"object": "cup"}, "desc": "Grasp cup"},
                    {"action": "navigate_to", "params": {"location": "living room"}, "desc": "Return to living room"},
                    {"action": "place_object", "params": {"location": "table"}, "desc": "Place cup on table"}
                ]
            else:
                return [{"action": "idle", "params": {}, "desc": "No specific action needed"}]
    
    # Create cognitive architecture
    planner = SimpleLLMPlanner()
    cognitive_arch = LLMCognitiveArchitecture(planner)
    
    # Add some semantic knowledge
    cognitive_arch.update_semantic_memory({
        "object_properties": {
            "red cup": {"color": "red", "type": "cup", "grasp_force": 5.0}
        },
        "location_mappings": {
            "kitchen": {"x": 1.0, "y": 2.0, "z": 0.0},
            "living room": {"x": 0.0, "y": 0.0, "z": 0.0}
        },
        "facts": [
            ("kitchen", "contains", "cup"),
            ("red cup", "color", "red"),
            ("red cup", "grasp_type", "precision")
        ]
    })
    
    # Process an instruction
    robot_state = {"location": "living room", "held_object": None}
    instruction = "Please bring the red cup from the kitchen"
    
    plan = cognitive_arch.process_instruction(instruction, robot_state)
    
    print(f"\nGenerated plan:")
    for i, action in enumerate(plan):
        print(f"  {i+1}. {action['desc']}")

example_cognitive_architecture()
```

## Planning with Uncertainty and Verification

### Plan Verification and Validation

Ensuring LLM-generated plans are executable and safe:

```python
from typing import Dict, List, Any, Tuple
import re

class PlanVerifier:
    def __init__(self):
        """
        Verify and validate LLM-generated plans
        """
        self.action_validators = {
            "navigate_to": self.validate_navigation,
            "grasp_object": self.validate_grasp,
            "place_object": self.validate_placement,
            "find_object": self.validate_find,
        }
    
    def verify_plan(self, plan: List[Dict[str, Any]], robot_capabilities: Dict[str, Any]) -> Tuple[bool, List[str], List[Dict[str, Any]]]:
        """
        Verify a plan for executability and safety
        
        Args:
            plan: List of actions to verify
            robot_capabilities: Robot's capabilities and constraints
            
        Returns:
            (is_valid, error_messages, corrected_plan)
        """
        errors = []
        corrected_plan = []
        
        for i, action in enumerate(plan):
            action_type = action.get("action", "")
            params = action.get("parameters", {})
            
            # Check if action is supported
            if action_type not in self.action_validators:
                errors.append(f"Action {i+1}: Unsupported action type '{action_type}'")
                continue
            
            # Validate specific action
            is_valid, error_msg, corrected_params = self.action_validators[action_type](params, robot_capabilities)
            
            if not is_valid:
                errors.append(f"Action {i+1} ({action_type}): {error_msg}")
            
            # Add corrected action to plan
            corrected_action = action.copy()
            corrected_action["parameters"] = corrected_params
            corrected_plan.append(corrected_action)
        
        # Check for logical consistency
        consistency_errors = self.check_plan_consistency(plan)
        errors.extend(consistency_errors)
        
        return len(errors) == 0, errors, corrected_plan
    
    def validate_navigation(self, params: Dict[str, Any], capabilities: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
        """Validate navigation action"""
        location = params.get("location")
        
        if not location:
            return False, "Missing location parameter", params
        
        # Check if location is known
        known_locations = capabilities.get("known_locations", [])
        if location not in known_locations:
            return False, f"Unknown location: {location}", params
        
        # Check navigation constraints
        max_distance = capabilities.get("max_navigation_distance", 10.0)
        estimated_distance = capabilities.get("location_distances", {}).get(location, 0.0)
        
        if estimated_distance > max_distance:
            return False, f"Location {location} is too far (distance: {estimated_distance}m, max: {max_distance}m)", params
        
        return True, "", params
    
    def validate_grasp(self, params: Dict[str, Any], capabilities: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
        """Validate grasp action"""
        obj_name = params.get("object_name") or params.get("object")
        
        if not obj_name:
            return False, "Missing object parameter", params
        
        # Check if object is within reach
        max_reach = capabilities.get("max_grasp_distance", 1.0)
        object_distance = params.get("distance", 0.5)  # Assume distance is provided
        
        if object_distance > max_reach:
            return False, f"Object {obj_name} is out of reach (distance: {object_distance}m, max: {max_reach}m)", params
        
        # Check if gripper is free
        gripper_status = capabilities.get("gripper_status", "open")
        if gripper_status != "open":
            return False, f"Gripper is not open (status: {gripper_status})", params
        
        # Validate grasp type
        grasp_type = params.get("grasp_type", "precision")
        supported_grasps = capabilities.get("supported_grasps", ["precision", "power"])
        
        if grasp_type not in supported_grasps:
            # Correct to a supported grasp type
            corrected_params = params.copy()
            corrected_params["grasp_type"] = supported_grasps[0]  # Use first supported type
            return True, f"Grasp type {grasp_type} not supported, using {supported_grasps[0]}", corrected_params
        
        return True, "", params
    
    def validate_placement(self, params: Dict[str, Any], capabilities: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
        """Validate place action"""
        location = params.get("location")
        obj_name = params.get("object_name") or params.get("object")
        
        if not location:
            return False, "Missing location parameter", params
        
        if not obj_name:
            return False, "Missing object parameter", params
        
        # Check if location is valid for placement
        valid_placement_areas = capabilities.get("valid_placement_areas", ["table", "counter", "shelf"])
        if location not in valid_placement_areas:
            return False, f"Invalid placement location: {location}", params
        
        # Check if gripper is holding an object
        held_object = capabilities.get("held_object")
        if not held_object:
            return False, "Cannot place object: gripper is not holding anything", params
        
        return True, "", params
    
    def validate_find(self, params: Dict[str, Any], capabilities: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
        """Validate find action"""
        obj_name = params.get("object_name") or params.get("object")
        
        if not obj_name:
            return False, "Missing object parameter", params
        
        # Check if object detection is possible
        supported_objects = capabilities.get("detectable_objects", [])
        if obj_name not in supported_objects:
            return False, f"Object {obj_name} may not be detectable", params
        
        return True, "", params
    
    def check_plan_consistency(self, plan: List[Dict[str, Any]]) -> List[str]:
        """Check for logical consistency in the plan"""
        errors = []
        
        # Check for conflicting actions
        for i in range(len(plan) - 1):
            current_action = plan[i]
            next_action = plan[i + 1]
            
            current_type = current_action.get("action", "")
            next_type = next_action.get("action", "")
            
            # Check for impossible sequences
            if (current_type == "grasp_object" and next_type == "grasp_object" and 
                current_action.get("parameters", {}).get("object") == 
                next_action.get("parameters", {}).get("object")):
                errors.append(f"Action {i+2}: Cannot grasp the same object twice")
            
            # Check for missing preconditions
            if next_type == "place_object" and current_type != "grasp_object":
                errors.append(f"Action {i+2}: Cannot place object without grasping it first")
        
        return errors

# Example usage
def example_plan_verification():
    verifier = PlanVerifier()
    
    # Example plan that might have issues
    plan = [
        {
            "action": "navigate_to",
            "parameters": {"location": "kitchen"},
            "description": "Go to kitchen"
        },
        {
            "action": "grasp_object", 
            "parameters": {"object": "red cup", "grasp_type": "invalid_grasp"},
            "description": "Grasp the red cup"
        },
        {
            "action": "navigate_to",
            "parameters": {"location": "bedroom"},  # Invalid location
            "description": "Go to bedroom"
        },
        {
            "action": "place_object",
            "parameters": {"location": "floor", "object": "red cup"},  # Invalid placement
            "description": "Place cup on floor"
        }
    ]
    
    # Robot capabilities
    capabilities = {
        "known_locations": ["kitchen", "living room", "office"],
        "max_navigation_distance": 5.0,
        "max_grasp_distance": 0.8,
        "gripper_status": "open",
        "held_object": None,
        "supported_grasps": ["precision", "power"],
        "valid_placement_areas": ["table", "counter", "shelf"],
        "detectable_objects": ["red cup", "blue bottle", "book"]
    }
    
    # Verify the plan
    is_valid, errors, corrected_plan = verifier.verify_plan(plan, capabilities)
    
    print("Plan Verification Results:")
    print(f"Is Valid: {is_valid}")
    print(f"Errors: {len(errors)}")
    for error in errors:
        print(f"  - {error}")
    
    print(f"\nCorrected Plan:")
    for i, action in enumerate(corrected_plan):
        print(f"  {i+1}. {action['action']} with params: {action['parameters']}")

example_plan_verification()
```

## Integration with Traditional Planning Systems

### Hybrid LLM-Traditional Planning

Combining LLM-based high-level planning with traditional motion planning:

```python
import numpy as np
from typing import Dict, List, Any, Optional
import heapq

class TraditionalMotionPlanner:
    def __init__(self, map_resolution: float = 0.1):
        """
        Traditional motion planner (e.g., A* or RRT)
        
        Args:
            map_resolution: Resolution of the occupancy grid
        """
        self.resolution = map_resolution
    
    def plan_path(self, start: tuple, goal: tuple, occupancy_grid: np.ndarray) -> Optional[List[tuple]]:
        """
        Plan a path using traditional algorithm (A* implementation)
        
        Args:
            start: Start position (x, y)
            goal: Goal position (x, y)  
            occupancy_grid: 2D occupancy grid (0 = free, 1 = occupied)
            
        Returns:
            List of waypoints or None if no path found
        """
        start_x, start_y = start
        goal_x, goal_y = goal
        
        # Convert to grid coordinates
        start_grid = (int(start_x / self.resolution), int(start_y / self.resolution))
        goal_grid = (int(goal_x / self.resolution), int(goal_y / self.resolution))
        
        # Check if start and goal are valid
        if (start_grid[0] < 0 or start_grid[0] >= occupancy_grid.shape[1] or 
            start_grid[1] < 0 or start_grid[1] >= occupancy_grid.shape[0] or
            occupancy_grid[start_grid[1], start_grid[0]] == 1):
            return None
        
        if (goal_grid[0] < 0 or goal_grid[0] >= occupancy_grid.shape[1] or 
            goal_grid[1] < 0 or goal_grid[1] >= occupancy_grid.shape[0] or
            occupancy_grid[goal_grid[1], goal_grid[0]] == 1):
            return None
        
        # A* algorithm
        def heuristic(pos, goal):
            return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])  # Manhattan distance
        
        def neighbors(pos):
            x, y = pos
            neighbors_list = []
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]:
                nx, ny = x + dx, y + dy
                if (0 <= nx < occupancy_grid.shape[1] and 
                    0 <= ny < occupancy_grid.shape[0] and 
                    occupancy_grid[ny, nx] == 0):
                    # Add diagonal movement cost
                    cost = 1.0 if abs(dx) + abs(dy) == 1 else 1.414  # 1 for straight, 1.414 for diagonal
                    neighbors_list.append(((nx, ny), cost))
            return neighbors_list
        
        # A* implementation
        frontier = [(0, start_grid)]
        came_from = {start_grid: None}
        cost_so_far = {start_grid: 0}
        
        while frontier:
            _, current = heapq.heappop(frontier)
            
            if current == goal_grid:
                break
            
            for next_pos, move_cost in neighbors(current):
                new_cost = cost_so_far[current] + move_cost
                
                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = new_cost + heuristic(next_pos, goal_grid)
                    heapq.heappush(frontier, (priority, next_pos))
                    came_from[next_pos] = current
        
        # Reconstruct path
        if goal_grid not in came_from:
            return None  # No path found
        
        path = []
        current = goal_grid
        while current is not None:
            # Convert back to world coordinates
            world_x = current[0] * self.resolution
            world_y = current[1] * self.resolution
            path.append((world_x, world_y))
            current = came_from[current]
        
        path.reverse()
        return path

class HybridPlanningSystem:
    def __init__(self, llm_planner, motion_planner):
        """
        Hybrid system combining LLM-based task planning with traditional motion planning
        
        Args:
            llm_planner: High-level LLM-based planner
            motion_planner: Low-level motion planner
        """
        self.llm_planner = llm_planner
        self.motion_planner = motion_planner
        self.location_map = {}  # Maps location names to coordinates
        self.object_map = {}    # Maps object names to locations
    
    def execute_high_level_instruction(self, instruction: str, robot_state: Dict[str, Any], 
                                    occupancy_grid: np.ndarray) -> bool:
        """
        Execute a high-level instruction using hybrid planning
        
        Args:
            instruction: Natural language instruction
            robot_state: Current robot state
            occupancy_grid: Current occupancy grid
            
        Returns:
            True if successful, False otherwise
        """
        # Step 1: Use LLM to decompose high-level task
        high_level_plan = self.llm_planner.plan_from_instruction(instruction, robot_state)
        
        print(f"High-level plan: {high_level_plan}")
        
        # Step 2: Execute each high-level action with appropriate low-level planning
        for action in high_level_plan:
            action_type = action.get("action", "")
            params = action.get("parameters", {})
            
            if action_type == "navigate_to":
                success = self.execute_navigation_action(params, robot_state, occupancy_grid)
            elif action_type == "grasp_object":
                success = self.execute_grasp_action(params, robot_state)
            elif action_type == "place_object":
                success = self.execute_place_action(params, robot_state)
            else:
                print(f"Unknown action type: {action_type}")
                success = False
            
            if not success:
                print(f"Action failed: {action}")
                return False
        
        return True
    
    def execute_navigation_action(self, params: Dict[str, Any], robot_state: Dict[str, Any], 
                                occupancy_grid: np.ndarray) -> bool:
        """
        Execute navigation action using motion planner
        """
        location_name = params.get("location", "")
        
        if location_name not in self.location_map:
            print(f"Unknown location: {location_name}")
            return False
        
        goal_pos = self.location_map[location_name]
        start_pos = (robot_state.get("x", 0.0), robot_state.get("y", 0.0))
        
        print(f"Navigating from {start_pos} to {goal_pos}")
        
        # Plan path using traditional planner
        path = self.motion_planner.plan_path(start_pos, goal_pos, occupancy_grid)
        
        if path is None:
            print(f"No path found to {location_name}")
            return False
        
        print(f"Found path with {len(path)} waypoints")
        
        # In practice, execute the path on the robot
        # For simulation:
        robot_state["x"] = goal_pos[0]
        robot_state["y"] = goal_pos[1]
        
        return True
    
    def execute_grasp_action(self, params: Dict[str, Any], robot_state: Dict[str, Any]) -> bool:
        """
        Execute grasp action
        """
        object_name = params.get("object", "")
        
        if object_name not in self.object_map:
            print(f"Object {object_name} location unknown")
            return False
        
        object_pos = self.object_map[object_name]
        robot_pos = (robot_state.get("x", 0.0), robot_state.get("y", 0.0))
        
        # Check if object is reachable
        distance = np.sqrt((object_pos[0] - robot_pos[0])**2 + (object_pos[1] - robot_pos[1])**2)
        max_reach = robot_state.get("max_reach", 0.8)
        
        if distance > max_reach:
            print(f"Object {object_name} is out of reach (distance: {distance:.2f}m, max: {max_reach}m)")
            return False
        
        print(f"Grasping object {object_name} at {object_pos}")
        
        # Update robot state
        robot_state["held_object"] = object_name
        
        return True
    
    def execute_place_action(self, params: Dict[str, Any], robot_state: Dict[str, Any]) -> bool:
        """
        Execute place action
        """
        location_name = params.get("location", "")
        
        if location_name not in self.location_map:
            print(f"Unknown location: {location_name}")
            return False
        
        if not robot_state.get("held_object"):
            print("Cannot place object: robot is not holding anything")
            return False
        
        location_pos = self.location_map[location_name]
        robot_pos = (robot_state.get("x", 0.0), robot_state.get("y", 0.0))
        
        # Check if location is reachable
        distance = np.sqrt((location_pos[0] - robot_pos[0])**2 + (location_pos[1] - robot_pos[1])**2)
        max_reach = robot_state.get("max_reach", 0.8)
        
        if distance > max_reach:
            print(f"Placement location {location_name} is out of reach (distance: {distance:.2f}m, max: {max_reach}m)")
            return False
        
        print(f"Placing object {robot_state['held_object']} at {location_name}")
        
        # Update robot state
        robot_state["held_object"] = None
        
        return True

# Example usage
def example_hybrid_planning():
    # Create a simple LLM planner for the example
    class SimpleLLMPlanner:
        def plan_from_instruction(self, instruction: str, robot_state: Dict[str, Any]) -> List[Dict[str, Any]]:
            # Simple parsing for demonstration
            if "kitchen" in instruction.lower() and "cup" in instruction.lower():
                return [
                    {"action": "navigate_to", "parameters": {"location": "kitchen"}},
                    {"action": "grasp_object", "parameters": {"object": "red cup"}},
                    {"action": "navigate_to", "parameters": {"location": "living_room"}},
                    {"action": "place_object", "parameters": {"location": "table"}}
                ]
            else:
                return []
    
    # Create planners
    llm_planner = SimpleLLMPlanner()
    motion_planner = TraditionalMotionPlanner(map_resolution=0.1)
    hybrid_system = HybridPlanningSystem(llm_planner, motion_planner)
    
    # Set up location and object mappings
    hybrid_system.location_map = {
        "kitchen": (5.0, 3.0),
        "living_room": (2.0, 1.0),
        "office": (1.0, 4.0),
        "table": (2.2, 1.2)
    }
    
    hybrid_system.object_map = {
        "red cup": (5.2, 3.1)
    }
    
    # Create a simple occupancy grid (10x10, with some obstacles)
    occupancy_grid = np.zeros((10, 10))
    # Add some obstacles
    occupancy_grid[4:6, 2:8] = 1  # Horizontal wall
    
    # Set initial robot state
    robot_state = {
        "x": 1.0,
        "y": 1.0,
        "held_object": None,
        "max_reach": 0.8
    }
    
    # Execute instruction
    instruction = "Go to the kitchen, pick up the red cup, and bring it to the living room"
    success = hybrid_system.execute_high_level_instruction(instruction, robot_state, occupancy_grid)
    
    print(f"\nInstruction execution {'successful' if success else 'failed'}")
    print(f"Final robot state: {robot_state}")

example_hybrid_planning()
```

## Evaluation of LLM-Based Planning

### Performance Metrics

Evaluating LLM-based planning systems:

```python
import time
import statistics
from typing import Dict, List, Any

class LLMPlanningEvaluator:
    def __init__(self):
        """
        Evaluate LLM-based planning systems
        """
        self.metrics = {
            'success_rate': [],
            'planning_time': [],
            'execution_time': [],
            'plan_quality': [],
            'safety_violations': [],
            'semantic_accuracy': []
        }
    
    def evaluate_planning_performance(self, planner, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Evaluate planning performance on test cases
        
        Args:
            planner: LLM-based planner to evaluate
            test_cases: List of test cases with expected outcomes
            
        Returns:
            Performance metrics
        """
        results = []
        
        for i, test_case in enumerate(test_cases):
            print(f"Evaluating test case {i+1}/{len(test_cases)}")
            
            start_time = time.time()
            
            # Generate plan
            instruction = test_case['instruction']
            robot_state = test_case['initial_state']
            
            plan = planner.plan_from_instruction(instruction, robot_state)
            
            planning_time = time.time() - start_time
            
            # Execute plan (simulated)
            execution_start = time.time()
            success = self.simulate_plan_execution(plan, test_case['expected_outcome'])
            execution_time = time.time() - execution_start
            
            # Evaluate plan quality
            plan_quality = self.evaluate_plan_quality(plan, test_case['expected_outcome'])
            
            # Check for safety violations
            safety_violations = self.check_safety_violations(plan)
            
            # Calculate semantic accuracy
            semantic_accuracy = self.calculate_semantic_accuracy(instruction, plan, test_case['expected_actions'])
            
            # Store results
            result = {
                'test_id': i,
                'success': success,
                'planning_time': planning_time,
                'execution_time': execution_time,
                'plan_quality': plan_quality,
                'safety_violations': safety_violations,
                'semantic_accuracy': semantic_accuracy
            }
            
            results.append(result)
        
        # Calculate aggregate metrics
        metrics = {}
        if results:
            metrics['success_rate'] = statistics.mean([r['success'] for r in results])
            metrics['avg_planning_time'] = statistics.mean([r['planning_time'] for r in results])
            metrics['avg_execution_time'] = statistics.mean([r['execution_time'] for r in results])
            metrics['avg_plan_quality'] = statistics.mean([r['plan_quality'] for r in results])
            metrics['avg_safety_violations'] = statistics.mean([r['safety_violations'] for r in results])
            metrics['avg_semantic_accuracy'] = statistics.mean([r['semantic_accuracy'] for r in results])
            
            # Calculate standard deviations
            metrics['planning_time_std'] = statistics.stdev([r['planning_time'] for r in results]) if len(results) > 1 else 0
            metrics['execution_time_std'] = statistics.stdev([r['execution_time'] for r in results]) if len(results) > 1 else 0
        
        return metrics
    
    def simulate_plan_execution(self, plan: List[Dict[str, Any]], expected_outcome: Dict[str, Any]) -> bool:
        """
        Simulate plan execution to determine success
        """
        # This is a simplified simulation
        # In practice, this would interface with a robot simulator
        if not plan:
            return False  # Empty plan is unsuccessful
        
        # Check if plan achieves expected outcome
        # This is a simplified check
        expected_location = expected_outcome.get('final_location')
        if expected_location:
            # Check if last navigation action matches expected location
            for action in reversed(plan):
                if action.get('action') == 'navigate_to':
                    if action.get('parameters', {}).get('location') == expected_location:
                        return True
                    else:
                        return False
        
        return True  # Simplified success condition
    
    def evaluate_plan_quality(self, plan: List[Dict[str, Any]], expected_outcome: Dict[str, Any]) -> float:
        """
        Evaluate the quality of a generated plan
        """
        if not plan:
            return 0.0
        
        # Quality factors:
        # 1. Completeness (does it include all necessary steps?)
        expected_actions = expected_outcome.get('required_actions', [])
        plan_actions = [action['action'] for action in plan]
        
        completeness = len(set(expected_actions) & set(plan_actions)) / len(set(expected_actions)) if expected_actions else 1.0
        
        # 2. Efficiency (is it not unnecessarily long?)
        efficiency = max(0, 1 - (len(plan) - len(expected_actions)) / max(len(expected_actions), 1))
        
        # 3. Correctness (are actions in the right order?)
        correctness = 1.0
        for i, exp_action in enumerate(expected_actions):
            if i < len(plan_actions) and plan_actions[i] != exp_action:
                correctness *= 0.8  # Penalty for wrong order
        
        # Combine factors
        quality = (completeness * 0.4 + efficiency * 0.3 + correctness * 0.3)
        return min(1.0, max(0.0, quality))
    
    def check_safety_violations(self, plan: List[Dict[str, Any]]) -> int:
        """
        Check for safety violations in the plan
        """
        violations = 0
        
        for action in plan:
            action_type = action.get('action', '')
            
            # Check for potentially unsafe actions
            if action_type == 'grasp_object':
                # Check if object is fragile and grasp type is appropriate
                obj_properties = action.get('object_properties', {})
                grasp_type = action.get('parameters', {}).get('grasp_type', 'power')
                
                if obj_properties.get('fragile') and grasp_type == 'power':
                    violations += 1
            
            elif action_type == 'navigate_to':
                # Check if location is safe
                location = action.get('parameters', {}).get('location', '')
                if location in ['construction_zone', 'restricted_area']:
                    violations += 1
        
        return violations
    
    def calculate_semantic_accuracy(self, instruction: str, plan: List[Dict[str, Any]], 
                                  expected_actions: List[str]) -> float:
        """
        Calculate how semantically accurate the plan is to the instruction
        """
        if not expected_actions:
            return 1.0
        
        plan_actions = [action['action'] for action in plan]
        
        # Calculate overlap between expected and planned actions
        intersection = len(set(expected_actions) & set(plan_actions))
        union = len(set(expected_actions) | set(plan_actions))
        
        if union == 0:
            return 1.0
        
        # Jaccard similarity
        jaccard = intersection / union
        
        # Also consider the proportion of expected actions that were planned
        recall = len(set(expected_actions) & set(plan_actions)) / len(set(expected_actions))
        
        # F1 score
        if jaccard + recall == 0:
            f1 = 0.0
        else:
            f1 = 2 * (jaccard * recall) / (jaccard + recall)
        
        return f1

# Example evaluation
def example_evaluation():
    # Create a simple planner for evaluation
    class TestLLMPlanner:
        def plan_from_instruction(self, instruction: str, robot_state: Dict[str, Any]) -> List[Dict[str, Any]]:
            # Simple rule-based planner for testing
            plan = []
            
            if "kitchen" in instruction.lower():
                plan.append({"action": "navigate_to", "parameters": {"location": "kitchen"}})
            
            if "cup" in instruction.lower():
                plan.append({"action": "grasp_object", "parameters": {"object": "cup"}})
            
            if "living room" in instruction.lower():
                plan.append({"action": "navigate_to", "parameters": {"location": "living_room"}})
            
            if "table" in instruction.lower():
                plan.append({"action": "place_object", "parameters": {"location": "table"}})
            
            return plan
    
    # Create evaluator and planner
    evaluator = LLMPlanningEvaluator()
    planner = TestLLMPlanner()
    
    # Define test cases
    test_cases = [
        {
            "instruction": "Go to the kitchen and bring the red cup to the living room table",
            "initial_state": {"location": "office", "held_object": None},
            "expected_outcome": {
                "final_location": "living_room",
                "held_object": None,
                "required_actions": ["navigate_to", "grasp_object", "navigate_to", "place_object"]
            },
            "expected_actions": ["navigate_to", "grasp_object", "navigate_to", "place_object"]
        },
        {
            "instruction": "Navigate to the bedroom",
            "initial_state": {"location": "living_room", "held_object": None},
            "expected_outcome": {
                "final_location": "bedroom",
                "required_actions": ["navigate_to"]
            },
            "expected_actions": ["navigate_to"]
        }
    ]
    
    # Evaluate the planner
    metrics = evaluator.evaluate_planning_performance(planner, test_cases)
    
    print("\nLLM Planning Evaluation Results:")
    for metric, value in metrics.items():
        print(f"  {metric}: {value:.3f}")

example_evaluation()
```

## Best Practices for LLM-Based Planning

### 1. System Design
- Use modular architecture to separate LLM reasoning from robot control
- Implement proper error handling and fallback mechanisms
- Design for interpretability and explainability
- Include safety checks and validation layers

### 2. Integration Strategies
- Combine LLMs with traditional planning for robustness
- Use tools and APIs to ground LLM outputs in reality
- Implement verification steps for safety-critical actions
- Maintain human oversight for complex tasks

### 3. Performance Optimization
- Cache frequently accessed information
- Use appropriate LLM models for your use case
- Implement efficient memory systems
- Optimize for real-time constraints where needed

### 4. Evaluation and Monitoring
- Continuously monitor system performance
- Collect data on failure cases for improvement
- Implement user feedback mechanisms
- Regularly update and retrain models

## Looking Ahead

This week we explored LLM-based planning and cognitive robotics, which represents a significant advancement in how robots understand and execute high-level tasks. Next week, we'll focus on sim-to-real transfer and deployment considerations for taking these systems from simulation to real-world applications.

## Exercises

1. Implement an LLM-based planner for a specific robotic task
2. Create a cognitive architecture with memory systems
3. Develop a verification system for LLM-generated plans
4. Design a hybrid planning system combining LLMs with traditional planners
5. Evaluate your LLM-based planning system on various metrics

## Further Reading

- "Language Models as Zero-Shot Planners" by Chen et al.
- "Inner Monologue" by Singh et al.
- "SayCan: Do as I Can, Not as I Say" by Brohan et al.
- "RT-1: Robotics Transformer for Real-World Control at Scale" by Brohan et al.