---
sidebar_position: 2
---

# Environment Setup

Before diving into Physical AI concepts, you'll need to set up your development environment. This guide walks you through installing the necessary tools and verifying your setup.

## System Requirements

### Minimum Specifications
- **Operating System**: Ubuntu 22.04 LTS (recommended) or Windows 10/11 with WSL2
- **CPU**: 8+ cores, Intel i7 or AMD Ryzen 7 equivalent
- **RAM**: 16GB minimum, 32GB recommended
- **GPU**: NVIDIA RTX 3070 or better with CUDA support
- **Storage**: 50GB free space for ROS 2, Gazebo, and simulation environments

### Recommended Specifications
- **CPU**: 16+ cores, Intel i9 or AMD Threadripper
- **RAM**: 64GB
- **GPU**: NVIDIA RTX 4080 or better (for complex simulations)
- **Storage**: 100GB SSD

## Installing ROS 2 Humble Hawksbill

ROS 2 (Robot Operating System 2) provides the middleware and tools for distributed robotics development.

### On Ubuntu 22.04

1. **Add the ROS 2 repository**:
   ```bash
   sudo apt update && sudo apt install curl gnupg lsb-release
   curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key | sudo gpg --dearmor -o /usr/share/keyrings/ros-archive-keyring.gpg
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(source /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
   ```

2. **Install ROS 2 packages**:
   ```bash
   sudo apt update
   sudo apt install ros-humble-desktop-full
   sudo apt install python3-colcon-common-extensions
   ```

3. **Source ROS 2 in your shell**:
   ```bash
   echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
   source ~/.bashrc
   ```

4. **Verify installation**:
   ```bash
   ros2 topic list
   ```

### On Windows with WSL2

1. Install WSL2 with Ubuntu 22.04
2. Follow the Ubuntu installation steps above
3. Install an X-server (like VcXsrv) for GUI applications

## Installing Gazebo Garden

Gazebo Garden provides physics-based simulation for testing robotics algorithms.

1. **Add the Gazebo repository**:
   ```bash
   wget https://packages.osrfoundation.org/gazebo.gpg -O - | sudo gpg --dearmor -o /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
   echo "deb [arch=amd64 signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null
   ```

2. **Install Gazebo Garden**:
   ```bash
   sudo apt update
   sudo apt install gz-garden
   ```

3. **Verify installation**:
   ```bash
   gz sim
   ```

## Installing NVIDIA Isaac Sim (Optional but Recommended)

NVIDIA Isaac Sim provides advanced GPU-accelerated simulation capabilities.

1. **Requirements**:
   - NVIDIA GPU with RTX capabilities
   - CUDA-compatible driver (470+)
   - Isaac Sim license (free for academic use)

2. **Installation**:
   Follow the official installation guide at: https://nvidia-isaac-sim.github.io/isaac-sim/installation.html

## Setting Up Development Tools

### Python Environment

1. **Install Python 3.10+**:
   ```bash
   sudo apt update
   sudo apt install python3.10 python3.10-dev python3.10-venv python3-pip
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv ~/ros2_env
   source ~/ros2_env/bin/activate
   pip install --upgrade pip
   ```

### Node.js for Docusaurus

1. **Install Node.js 18+**:
   ```bash
   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
   sudo apt-get install -y nodejs
   ```

2. **Verify installation**:
   ```bash
   node --version
   npm --version
   ```

## Verifying Your Setup

1. **Test ROS 2**:
   ```bash
   # In one terminal
   ros2 run demo_nodes_cpp talker

   # In another terminal
   ros2 run demo_nodes_py listener
   ```

   You should see messages passing between the nodes.

2. **Test Gazebo**:
   ```bash
   gz sim -v 4
   ```

   This should launch the Gazebo GUI.

3. **Test Python integration**:
   ```bash
   python3 -c "import rclpy; print('ROS 2 Python client working')"
   ```

## Troubleshooting Common Issues

### ROS 2 Not Found
```bash
# Ensure ROS 2 is sourced
source /opt/ros/humble/setup.bash
```

### Gazebo Performance Issues
- Ensure your graphics drivers support OpenGL 3.3+
- Check that NVIDIA drivers are properly installed if using GPU acceleration
- Close unnecessary applications to free up GPU resources

### Permission Issues
- Add yourself to the dialout group for serial communication:
  ```bash
  sudo usermod -a -G dialout $USER
  ```
- Log out and back in for changes to take effect

## Next Steps

Once your environment is properly set up, you can:

1. Clone this book's repository
2. Install Docusaurus dependencies with `npm install`
3. Start the development server with `npm start`
4. Begin with Week 1: Theory Foundations

Your development environment is now ready for the exciting journey into Physical AI and humanoid robotics!