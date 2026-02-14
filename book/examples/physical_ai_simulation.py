"""
Physical AI & Humanoid Robotics - Simulation Example

This file demonstrates a simple simulation environment for Physical AI concepts.
It includes a basic robot model, environment, and simulation loop.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle, Circle
import time
import math


class SimpleRobot:
    """Simple robot model for simulation"""
    
    def __init__(self, x=0, y=0, theta=0):
        self.x = x
        self.y = y
        self.theta = theta  # Heading angle
        self.vx = 0
        self.vy = 0
        self.vtheta = 0  # Angular velocity
        self.size = 0.5  # Robot size (radius)
        self.held_object = None
        self.battery_level = 1.0
    
    def update(self, dt):
        """Update robot state based on velocities"""
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.theta += self.vtheta * dt
        
        # Keep theta in [-pi, pi]
        self.theta = math.atan2(math.sin(self.theta), math.cos(self.theta))
    
    def move_to(self, target_x, target_y, max_speed=1.0):
        """Simple movement toward target"""
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0.1:  # If not close to target
            # Normalize direction
            dx /= distance
            dy /= distance
            
            # Set velocity toward target
            self.vx = dx * min(max_speed, distance)
            self.vy = dy * min(max_speed, distance)
            self.vtheta = 0  # No rotation for now
        else:
            # Stop when close to target
            self.vx = 0
            self.vy = 0
            self.vtheta = 0
    
    def grasp_object(self, obj_name):
        """Grasp an object"""
        self.held_object = obj_name
        print(f"Robot grasped {obj_name}")
    
    def place_object(self):
        """Place the held object"""
        if self.held_object:
            obj_name = self.held_object
            self.held_object = None
            print(f"Robot placed {obj_name}")
            return obj_name
        return None


class SimpleEnvironment:
    """Simple environment for simulation"""
    
    def __init__(self):
        self.width = 20
        self.height = 15
        self.obstacles = [
            {'x': 5, 'y': 5, 'width': 2, 'height': 6},  # Wall
            {'x': 12, 'y': 8, 'width': 4, 'height': 2},  # Table
            {'x': 2, 'y': 2, 'width': 1, 'height': 1}   # Small obstacle
        ]
        self.objects = [
            {'name': 'red_cube', 'x': 3, 'y': 3, 'radius': 0.3, 'color': 'red'},
            {'name': 'blue_sphere', 'x': 14, 'y': 10, 'radius': 0.3, 'color': 'blue'},
            {'name': 'green_cylinder', 'x': 16, 'y': 13, 'radius': 0.3, 'color': 'green'}
        ]
        self.locations = {
            'kitchen': (15, 5),
            'living_room': (5, 12),
            'bedroom': (18, 12)
        }
    
    def is_collision(self, x, y, robot_size=0.5):
        """Check if position collides with obstacles"""
        for obs in self.obstacles:
            if (obs['x'] - robot_size <= x <= obs['x'] + obs['width'] + robot_size and
                obs['y'] - robot_size <= y <= obs['y'] + obs['height'] + robot_size):
                return True
        return False
    
    def get_object_at(self, x, y, radius=0.5):
        """Get object at position"""
        for obj in self.objects:
            dist = math.sqrt((obj['x'] - x)**2 + (obj['y'] - y)**2)
            if dist <= radius:
                return obj
        return None


class PhysicalAISimulator:
    """Simulation environment for Physical AI concepts"""
    
    def __init__(self):
        self.robot = SimpleRobot(x=1, y=1)
        self.environment = SimpleEnvironment()
        self.targets = []  # Queue of targets to visit
        self.commands = []  # Queue of commands to execute
        self.simulation_time = 0
        self.dt = 0.1  # Time step
        self.running = False
        self.command_history = []
    
    def add_command(self, command):
        """Add a command to the queue"""
        self.commands.append(command)
        self.command_history.append({
            'time': self.simulation_time,
            'command': command
        })
    
    def process_commands(self):
        """Process queued commands"""
        if not self.commands:
            return
        
        command = self.commands[0]
        
        if command.startswith("go_to "):
            location = command[6:]  # Remove "go_to " prefix
            if location in self.environment.locations:
                target_x, target_y = self.environment.locations[location]
                self.targets.append((target_x, target_y))
                print(f"Added target: {location} at ({target_x}, {target_y})")
                self.commands.pop(0)  # Remove processed command
        
        elif command.startswith("grasp "):
            obj_name = command[6:]  # Remove "grasp " prefix
            # Find object near robot
            nearby_obj = self.environment.get_object_at(self.robot.x, self.robot.y, radius=1.0)
            if nearby_obj and nearby_obj['name'] == obj_name:
                self.robot.grasp_object(obj_name)
                # Remove object from environment
                self.environment.objects = [obj for obj in self.environment.objects if obj['name'] != obj_name]
                self.commands.pop(0)  # Remove processed command
            else:
                print(f"Could not find {obj_name} near robot")
        
        elif command == "place":
            placed_obj = self.robot.place_object()
            if placed_obj:
                # Add object back to environment at robot's position
                self.environment.objects.append({
                    'name': placed_obj,
                    'x': self.robot.x,
                    'y': self.robot.y,
                    'radius': 0.3,
                    'color': 'gray'  # Change color when placed
                })
            self.commands.pop(0)  # Remove processed command
    
    def update(self):
        """Update simulation state"""
        if self.targets:
            # Move toward next target
            target_x, target_y = self.targets[0]
            self.robot.move_to(target_x, target_y)
            
            # Check if reached target
            dist_to_target = math.sqrt((self.robot.x - target_x)**2 + (self.robot.y - target_y)**2)
            if dist_to_target < 0.5:  # Close enough
                print(f"Reached target: ({target_x}, {target_y})")
                self.targets.pop(0)  # Remove reached target
        
        # Update robot
        self.robot.update(self.dt)
        
        # Update simulation time
        self.simulation_time += self.dt
        
        # Process commands
        self.process_commands()
    
    def run_simulation(self, duration=20):
        """Run the simulation for a specified duration"""
        self.running = True
        start_time = time.time()
        
        print(f"Starting simulation for {duration} seconds...")
        
        while self.simulation_time < duration and self.running:
            self.update()
            
            # Add some commands during simulation
            if self.simulation_time > 2 and not any("kitchen" in cmd for cmd in self.commands):
                self.add_command("go_to kitchen")
            elif self.simulation_time > 8 and not any("grasp" in cmd for cmd in self.commands):
                self.add_command("grasp red_cube")
            elif self.simulation_time > 12 and not any("living_room" in cmd for cmd in self.commands):
                self.add_command("go_to living_room")
            elif self.simulation_time > 16 and not any("place" in cmd for cmd in self.commands):
                self.add_command("place")
            
            time.sleep(0.01)  # Small delay to prevent overwhelming the CPU
        
        print(f"Simulation completed after {self.simulation_time:.2f} seconds")
        print(f"Robot final position: ({self.robot.x:.2f}, {self.robot.y:.2f})")
        print(f"Robot holding: {self.robot.held_object}")
    
    def visualize(self):
        """Create a visualization of the environment"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        def animate(frame):
            ax.clear()
            
            # Draw environment boundaries
            ax.add_patch(Rectangle((0, 0), self.environment.width, self.environment.height, 
                                 fill=False, edgecolor='black', linewidth=2))
            
            # Draw obstacles
            for obs in self.environment.obstacles:
                ax.add_patch(Rectangle((obs['x'], obs['y']), obs['width'], obs['height'], 
                                     color='gray', alpha=0.5))
            
            # Draw objects
            for obj in self.environment.objects:
                ax.add_patch(Circle((obj['x'], obj['y']), obj['radius'], 
                                  color=obj['color'], alpha=0.7))
                ax.text(obj['x'], obj['y'], obj['name'], ha='center', va='center', fontsize=8)
            
            # Draw locations
            for loc_name, (loc_x, loc_y) in self.environment.locations.items():
                ax.plot(loc_x, loc_y, 'ks', markersize=8)
                ax.text(loc_x, loc_y, loc_name, ha='center', va='bottom', fontsize=9)
            
            # Draw robot
            robot_circle = Circle((self.robot.x, self.robot.y), self.robot.size, 
                                color='blue', alpha=0.7)
            ax.add_patch(robot_circle)
            
            # Draw robot orientation
            end_x = self.robot.x + self.robot.size * math.cos(self.robot.theta)
            end_y = self.robot.y + self.robot.size * math.sin(self.robot.theta)
            ax.arrow(self.robot.x, self.robot.y, end_x - self.robot.x, end_y - self.robot.y,
                    head_width=0.2, head_length=0.2, fc='red', ec='red')
            
            # Draw targets
            for i, (tx, ty) in enumerate(self.targets):
                ax.plot(tx, ty, 'ro', markersize=10)
                ax.text(tx, ty, f'Target {i+1}', ha='center', va='bottom', fontsize=10)
            
            ax.set_xlim(-1, self.environment.width + 1)
            ax.set_ylim(-1, self.environment.height + 1)
            ax.set_aspect('equal')
            ax.grid(True, alpha=0.3)
            ax.set_title(f'Physical AI Simulation (Time: {self.simulation_time:.2f}s)')
        
        ani = animation.FuncAnimation(fig, animate, frames=200, interval=100, blit=False)
        plt.show()
        
        return ani


def main():
    """Main function to run the simulation example"""
    print("Physical AI & Humanoid Robotics - Simulation Example")
    print("=" * 50)
    
    # Create simulator
    simulator = PhysicalAISimulator()
    
    # Add initial command
    simulator.add_command("go_to kitchen")
    
    # Run simulation
    simulator.run_simulation(duration=20)
    
    # Visualize the environment
    print("\nStarting visualization...")
    ani = simulator.visualize()
    
    print("\nSimulation example completed!")
    print(f"Command history: {len(simulator.command_history)} commands processed")


if __name__ == "__main__":
    main()