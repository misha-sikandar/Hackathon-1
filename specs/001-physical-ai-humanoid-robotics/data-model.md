# Data Model: Physical AI & Humanoid Robotics Book

## Educational Content Entities

### Book Module
- **name**: String - Module/week identifier (e.g., "Week 1: Theory Foundations")
- **description**: String - Brief overview of module content
- **learning_objectives**: Array<String> - Specific skills/knowledge to acquire
- **prerequisites**: Array<String> - Required knowledge from previous modules
- **duration_weeks**: Number - Estimated time to complete (typically 1)
- **difficulty_level**: Enum - Beginner, Intermediate, Advanced
- **related_modules**: Array<String> - Cross-references to related content

### Chapter
- **title**: String - Chapter title within module
- **content_type**: Enum - Theory, Tutorial, Exercise, Reference
- **estimated_reading_time**: Number - Minutes to complete
- **dependencies**: Array<String> - Previous chapters required
- **learning_outcomes**: Array<String> - Specific outcomes after completion
- **resources**: Array<Resource> - Associated files, code, media

### Hands-On Lab
- **name**: String - Lab exercise title
- **objective**: String - Primary goal of the lab
- **simulation_environment**: String - Gazebo/Unity/NVIDIA Isaac environment
- **required_components**: Array<String> - ROS 2 packages, sensors, actuators
- **step_by_step_guide**: Array<String> - Sequential instructions
- **expected_results**: String - What success looks like
- **troubleshooting_tips**: Array<String> - Common issues and solutions

### Code Example
- **title**: String - Descriptive name for the example
- **language**: String - Programming language (Python, C++, etc.)
- **category**: Enum - ROS 2, Perception, Control, Navigation, etc.
- **complexity**: Number - Difficulty rating (1-5)
- **simulation_compatible**: Boolean - Whether it runs in simulation
- **hardware_compatible**: Boolean - Whether it runs on physical hardware
- **code_snippet**: String - The actual code content
- **explanation**: String - Explanation of how the code works

### Resource
- **type**: Enum - Image, Video, Code, Document, Simulation
- **title**: String - Descriptive name
- **file_path**: String - Location in static resources
- **size_mb**: Number - File size for download consideration
- **usage_context**: String - Where this resource is referenced
- **license**: String - Usage rights information

## Simulation Environment Entities

### Robot Model
- **name**: String - Robot identifier (e.g., "SimpleBot", "HumanoidA")
- **urdf_file**: String - Path to URDF description
- **sensors**: Array<String> - Sensor types included
- **actuators**: Array<String> - Actuator types included
- **capabilities**: Array<String> - What the robot can do
- **simulation_scenes**: Array<String> - Compatible simulation environments

### Simulation Scene
- **name**: String - Scene identifier
- **description**: String - What the scene represents
- **world_file**: String - Path to Gazebo/Unity world file
- **objects**: Array<String> - Static objects in the scene
- **environmental_conditions**: Object - Lighting, physics parameters
- **compatible_robots**: Array<String> - Robots that work in this scene

## Learning Assessment Entities

### Exercise
- **title**: String - Exercise name
- **module**: String - Associated module
- **type**: Enum - Quiz, Coding, Simulation, Analysis
- **difficulty**: Number - Rating 1-5
- **estimated_completion_time**: Number - Minutes to complete
- **solution**: String - Solution or approach
- **evaluation_criteria**: Array<String> - How to assess success

### Capstone Project
- **title**: String - Project name
- **description**: String - Project overview
- **requirements**: Array<String> - Functional requirements
- **deliverables**: Array<String> - What students submit
- **evaluation_rubric**: Object - Grading criteria
- **timeline**: Object - Milestones and deadlines
- **supporting_resources**: Array<String> - Additional materials