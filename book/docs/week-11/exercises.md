---
sidebar_position: 32
---

# Week 11 Exercises: LLM-Based Planning and Cognitive Robotics

This exercise sheet accompanies the Week 11 lessons on LLM-based planning and cognitive robotics. These exercises will help you practice and reinforce your understanding of using large language models for high-level planning and reasoning in Physical AI systems.

## Exercise 1: Implement an LLM-Based Task Planner

Create a system that uses an LLM to decompose high-level instructions into executable robot actions:

### Requirements:
- Use an LLM (e.g., OpenAI GPT, HuggingFace models) for planning
- Implement a structured way to represent robot capabilities
- Convert natural language instructions to action sequences
- Handle different types of robot tasks (navigation, manipulation, etc.)
- Evaluate the quality of generated plans

### Implementation Steps:
1. Set up LLM API access
2. Define robot capabilities and action space
3. Create prompt templates for planning
4. Implement plan generation from natural language
5. Test with various instructions

### LLM Planner Template:
```python
import openai
import json
from typing import Dict, List, Any

class LLMTaskPlanner:
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        openai.api_key = api_key
        self.model = model
        
        # Define robot capabilities
        self.capabilities = {
            "navigation": ["go_to", "move_to", "navigate_to"],
            "manipulation": ["pick_up", "place", "grasp", "release"],
            "interaction": ["speak", "listen", "greet"],
            "perception": ["find_object", "identify", "locate"]
        }
    
    def plan_from_instruction(self, instruction: str, robot_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate plan from natural language instruction"""
        # Implementation here
        pass
```

## Exercise 2: Create a Memory-Augmented Reasoning System

Implement a cognitive architecture that combines LLMs with memory systems:

### Requirements:
- Implement episodic memory for storing past experiences
- Create semantic memory for general knowledge
- Integrate memory retrieval with LLM reasoning
- Use memory to improve planning and decision making
- Evaluate memory-based reasoning performance

### Implementation Steps:
1. Implement episodic memory storage and retrieval
2. Create semantic memory for facts and knowledge
3. Integrate memory with LLM-based planning
4. Test with tasks requiring memory
5. Evaluate improvement from memory integration

### Memory System Template:
```python
import datetime
from typing import Dict, List, Any

class EpisodicMemory:
    def __init__(self, capacity: int = 100):
        self.capacity = capacity
        self.memories = []  # List of (timestamp, memory) tuples
    
    def add_memory(self, memory: Dict[str, Any]):
        """Add a new memory"""
        # Implementation here
        pass
    
    def retrieve_memories(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve relevant memories based on query"""
        # Implementation here
        pass

class SemanticMemory:
    def __init__(self):
        self.facts = {}  # Maps entity -> list of facts
        self.object_properties = {}  # Maps object -> properties
    
    def add_fact(self, subject: str, predicate: str, obj: str):
        """Add a fact to semantic memory"""
        # Implementation here
        pass
    
    def get_related_facts(self, entity: str) -> List[tuple]:
        """Get facts related to an entity"""
        # Implementation here
        pass
```

## Exercise 3: Implement Tool-Augmented LLM Planning

Create a system that uses LLMs with specialized tools for robotics:

### Requirements:
- Implement tool definitions for robot capabilities
- Use LLM to select and call appropriate tools
- Handle tool execution and results
- Plan multi-step tasks using tools
- Evaluate tool-based planning effectiveness

### Implementation Steps:
1. Define robot tools and their specifications
2. Implement tool calling mechanism
3. Create LLM prompting for tool selection
4. Handle tool execution and results
5. Test with complex multi-step tasks

### Tool System Template:
```python
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class ToolCall:
    name: str
    arguments: Dict[str, Any]

class ToolAugmentedPlanner:
    def __init__(self):
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
            # Add more tools
        }
    
    def plan_with_tools(self, instruction: str, robot_state: Dict[str, Any]) -> List[ToolCall]:
        """Generate plan using tools"""
        # Implementation here
        pass
```

## Exercise 4: Plan Verification and Validation

Implement a system to verify LLM-generated plans:

### Requirements:
- Check plan executability and safety
- Validate action sequences for consistency
- Identify potential failures before execution
- Provide plan corrections when needed
- Evaluate verification effectiveness

### Implementation Steps:
1. Implement action validators
2. Create plan consistency checker
3. Add safety verification
4. Implement plan correction
5. Test with various plan types

### Plan Verifier Template:
```python
class PlanVerifier:
    def __init__(self):
        self.action_validators = {
            "navigate_to": self.validate_navigation,
            "grasp_object": self.validate_grasp,
            # Add more validators
        }
    
    def verify_plan(self, plan: List[Dict[str, Any]], robot_capabilities: Dict[str, Any]) -> tuple:
        """Verify a plan for executability and safety"""
        # Implementation here
        pass
    
    def validate_navigation(self, params: Dict[str, Any], capabilities: Dict[str, Any]) -> tuple:
        """Validate navigation action"""
        # Implementation here
        pass
```

## Exercise 5: Hybrid LLM-Traditional Planning

Combine LLM-based high-level planning with traditional motion planning:

### Requirements:
- Integrate LLM task planning with traditional motion planning
- Handle navigation planning using traditional algorithms
- Coordinate high-level and low-level planning
- Implement error handling between planning levels
- Evaluate hybrid planning performance

### Implementation Steps:
1. Implement traditional motion planner (e.g., A*)
2. Create interface between LLM and motion planner
3. Handle plan coordination
4. Implement error recovery
5. Test hybrid system performance

### Hybrid Planner Template:
```python
import numpy as np

class TraditionalMotionPlanner:
    def __init__(self, map_resolution: float = 0.1):
        self.resolution = map_resolution
    
    def plan_path(self, start: tuple, goal: tuple, occupancy_grid: np.ndarray) -> list:
        """Plan path using traditional algorithm"""
        # Implementation here
        pass

class HybridPlanningSystem:
    def __init__(self, llm_planner, motion_planner):
        self.llm_planner = llm_planner
        self.motion_planner = motion_planner
    
    def execute_high_level_instruction(self, instruction: str, robot_state: Dict[str, Any], 
                                    occupancy_grid: np.ndarray) -> bool:
        """Execute instruction using hybrid planning"""
        # Implementation here
        pass
```

## Exercise 6: Context-Aware Planning

Create a system that maintains context across planning sessions:

### Requirements:
- Track conversation and task context
- Handle pronouns and references
- Maintain task history
- Adapt planning based on context
- Evaluate context preservation

### Implementation Steps:
1. Implement context tracking
2. Create reference resolution
3. Handle context updates
4. Adapt planning based on context
5. Test with multi-turn interactions

## Exercise 7: Evaluation Framework for LLM Planning

Develop metrics and methods to evaluate LLM-based planning:

### Requirements:
- Define metrics for plan quality and success
- Implement logging and monitoring
- Create evaluation protocols
- Test with real or simulated robots
- Analyze performance data

### Implementation Steps:
1. Define evaluation metrics
2. Implement logging system
3. Create evaluation protocols
4. Conduct experiments
5. Analyze and report results

### Evaluation Template:
```python
class LLMPlanningEvaluator:
    def __init__(self):
        self.metrics = {
            'success_rate': [],
            'planning_time': [],
            'execution_time': [],
            'plan_quality': [],
            'safety_violations': [],
            'semantic_accuracy': []
        }
    
    def evaluate_planning_performance(self, planner, test_cases: list) -> dict:
        """Evaluate planning performance on test cases"""
        # Implementation here
        pass
```

## Exercise 8: Safety and Ethics in LLM Planning

Address safety and ethical considerations in LLM-based planning:

### Requirements:
- Implement safety checks for generated plans
- Add ethical guidelines enforcement
- Handle potentially harmful instructions
- Create safe failure modes
- Evaluate safety effectiveness

### Implementation Steps:
1. Define safety constraints
2. Implement safety checks
3. Add ethical guidelines
4. Create safe failure modes
5. Test with potentially unsafe inputs

## Challenge Exercise: Complete LLM-Based Cognitive Robot

Create a complete system that includes:

### Requirements:
- LLM-based high-level planning
- Memory-augmented reasoning
- Tool-augmented execution
- Plan verification and validation
- Hybrid planning with traditional methods
- Context-aware interaction
- Safety and ethics enforcement
- Performance evaluation framework

### Additional Requirements:
- Demonstrate on a complex task
- Evaluate performance on multiple metrics
- Include failure analysis and robustness evaluation
- Document the complete system architecture

## Submission Requirements

For each exercise, submit:
1. Source code for all implementations
2. Testing and evaluation scripts
3. Configuration files and parameters
4. Performance benchmarks and metrics
5. Documentation of challenges and solutions
6. Comparative analysis where applicable
7. Sample inputs and outputs

## Evaluation Criteria

- Correct implementation of LLM integration
- Quality of planning and reasoning
- Effectiveness of memory systems
- Performance of verification systems
- Robustness to errors and edge cases
- Understanding of LLM-robot integration challenges
- Creativity in solving the challenge exercise

## Resources

- OpenAI API: https://platform.openai.com/
- Hugging Face: https://huggingface.co/
- LangChain: https://python.langchain.com/
- LLM-based Robotics Papers:
  - "Language Models as Zero-Shot Planners" by Chen et al.
  - "Inner Monologue" by Singh et al.
  - "SayCan: Do as I Can, Not as I Say" by Brohan et al.