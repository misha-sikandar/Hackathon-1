# Quickstart Guide: Physical AI & Humanoid Robotics Book

## Prerequisites

Before starting with the Physical AI & Humanoid Robotics book, ensure your system meets the following requirements:

### System Requirements
- **Operating System**: Ubuntu 22.04 LTS (recommended) or Windows 10/11 with WSL2
- **RAM**: 16GB minimum, 32GB recommended
- **GPU**: NVIDIA RTX 3070 or better with CUDA support
- **CPU**: 8+ cores, Intel i7 or AMD Ryzen 7 equivalent
- **Storage**: 50GB free space for ROS 2, Gazebo, and simulation environments

### Software Requirements
- **ROS 2**: Humble Hawksbill (LTS version)
- **Gazebo**: Garden edition
- **Python**: 3.10 or higher
- **Node.js**: 18.x or higher
- **Git**: Latest version
- **Docker**: For containerized simulation environments

## Setup Environment

### 1. Install ROS 2 Humble
```bash
# Add ROS 2 repository
sudo apt update && sudo apt install curl gnupg lsb-release
curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key | sudo gpg --dearmor -o /usr/share/keyrings/ros-archive-keyring.gpg

# Add the repository to your sources list
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(source /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Install ROS 2 packages
sudo apt update
sudo apt install ros-humble-desktop-full
sudo apt install python3-colcon-common-extensions
```

### 2. Install Gazebo Garden
```bash
# Add Gazebo repository
wget https://packages.osrfoundation.org/gazebo.gpg -O - | sudo gpg --dearmor -o /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null

# Install Gazebo Garden
sudo apt update
sudo apt install gz-garden
```

### 3. Install NVIDIA Isaac Sim (Optional but Recommended)
Follow the installation guide at: https://nvidia-isaac-sim.github.io/isaac-sim/installation.html

### 4. Clone and Setup the Book Repository
```bash
git clone [repository-url]
cd physical-ai-humanoid-robotics-book

# Install Node.js dependencies for Docusaurus
npm install
```

### 5. Verify Installation
```bash
# Source ROS 2
source /opt/ros/humble/setup.bash

# Test ROS 2 installation
ros2 topic list

# Test Gazebo installation
gz sim
```

## Running Examples

### Starting with Week 1 Examples
```bash
# Navigate to the book directory
cd book

# Start the Docusaurus development server
npm start

# In a new terminal, run the first week's example
cd examples/week-01
python3 theory_foundations_example.py
```

### Running Simulation Examples
```bash
# Source ROS 2 environment
source /opt/ros/humble/setup.bash

# Launch a sample simulation
ros2 launch examples_bringup simple_robot_world.launch.py
```

## First Chapter: Theory Foundations

The first chapter covers the theoretical foundations of embodied intelligence. To get started:

1. Read `docs/intro/index.md` and `docs/intro/theory-foundations.md`
2. Follow the setup guide in `docs/intro/setup.md`
3. Run the foundational examples in `static/examples/week-01/`
4. Complete the exercises in `docs/week-01/exercises.md`

## Troubleshooting Common Issues

### ROS 2 Not Found
```bash
# Add ROS 2 sourcing to your bashrc
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### Gazebo Not Launching
- Ensure your graphics drivers support OpenGL 3.3+
- Check that NVIDIA drivers are properly installed if using GPU acceleration

### Simulation Performance Issues
- Close unnecessary applications to free up RAM/CPU
- Reduce Gazebo's physics update rate in world files
- Use simpler robot models for initial testing

## Next Steps

After completing the setup:
1. Browse the book locally at http://localhost:3000
2. Proceed to Week 2: ROS 2 fundamentals
3. Work through the hands-on exercises
4. Join the community discussion forum for questions and collaboration