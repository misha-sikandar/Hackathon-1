---
sidebar_position: 26
---

# Week 9: Manipulation and Grasping

Welcome to Week 9 of our Physical AI & Humanoid Robotics journey! This week, we'll explore the fascinating world of robotic manipulation and grasping. Manipulation is a critical capability for humanoid robots, enabling them to interact with objects in their environment and perform complex tasks.

## Learning Objectives

By the end of this week, you will be able to:

1. Understand the fundamentals of robotic manipulation
2. Implement grasp planning algorithms
3. Design and control robotic arms for manipulation tasks
4. Apply machine learning to manipulation and grasping
5. Integrate perception with manipulation for object interaction
6. Evaluate manipulation performance and dexterity

## Introduction to Robotic Manipulation

Robotic manipulation involves the control of robot arms and end-effectors to interact with objects in the environment. For humanoid robots, manipulation is essential for performing daily tasks, assembly operations, and human-like interactions.

### Key Challenges in Manipulation

Robotic manipulation presents several challenges:

- **Dexterity**: Achieving human-like fine motor control
- **Grasp Planning**: Determining stable and effective grasps
- **Force Control**: Managing contact forces during manipulation
- **Coordination**: Coordinating multiple degrees of freedom
- **Perception**: Understanding object properties and spatial relationships
- **Adaptability**: Adjusting to novel objects and situations

### Manipulation vs. Human Dexterity

Human hands are incredibly dexterous, with 27 degrees of freedom and sophisticated sensory feedback. Robotic manipulation systems aim to approximate this capability:

- **Precision grasps**: Fine control for delicate objects
- **Power grasps**: Firm grip for heavy objects
- **Adaptive grasps**: Adjusting to object shape and weight
- **Multi-finger coordination**: Complex manipulation tasks

## Kinematics for Manipulation

### Forward and Inverse Kinematics

Kinematics is fundamental to manipulation, determining the relationship between joint angles and end-effector position:

```python
import numpy as np
import math
from scipy.spatial.transform import Rotation as R

class ManipulatorKinematics:
    def __init__(self, dh_parameters):
        """
        Manipulator kinematics using Denavit-Hartenberg parameters
        
        Args:
            dh_parameters: List of [a, alpha, d, theta_offset] for each joint
        """
        self.dh_params = dh_parameters
        self.num_joints = len(dh_params)
    
    def dh_transform(self, a, alpha, d, theta):
        """
        Calculate Denavit-Hartenberg transformation matrix
        """
        ct = math.cos(theta)
        st = math.sin(theta)
        ca = math.cos(alpha)
        sa = math.sin(alpha)
        
        transform = np.array([
            [ct, -st*ca, st*sa, a*ct],
            [st, ct*ca, -ct*sa, a*st],
            [0, sa, ca, d],
            [0, 0, 0, 1]
        ])
        
        return transform
    
    def forward_kinematics(self, joint_angles):
        """
        Calculate end-effector pose from joint angles
        
        Args:
            joint_angles: List of joint angles (radians)
            
        Returns:
            Transformation matrix from base to end-effector
        """
        if len(joint_angles) != self.num_joints:
            raise ValueError("Number of joint angles must match number of joints")
        
        # Initialize transformation matrix
        T = np.eye(4)
        
        for i in range(self.num_joints):
            a, alpha, d, theta_offset = self.dh_params[i]
            theta = joint_angles[i] + theta_offset
            
            T_joint = self.dh_transform(a, alpha, d, theta)
            T = T @ T_joint
        
        return T
    
    def jacobian(self, joint_angles):
        """
        Calculate geometric Jacobian matrix
        
        Args:
            joint_angles: List of joint angles (radians)
            
        Returns:
            6xN Jacobian matrix (linear and angular velocities)
        """
        T_total = np.eye(4)
        jacobian = np.zeros((6, self.num_joints))
        
        # Calculate transforms for each joint
        T_joints = []
        for i in range(self.num_joints):
            a, alpha, d, theta_offset = self.dh_params[i]
            theta = joint_angles[i] + theta_offset
            T_joint = self.dh_transform(a, alpha, d, theta)
            T_joints.append(T_total)
            T_total = T_total @ T_joint
        
        # End-effector position and orientation
        ee_pos = T_total[:3, 3]
        
        # Calculate Jacobian columns
        for i in range(self.num_joints):
            T_i = T_joints[i]
            z_i = T_i[:3, 2]  # z-axis of joint i
            r_ie = ee_pos - T_i[:3, 3]  # vector from joint i to end-effector
            
            # Linear velocity component
            jacobian[:3, i] = np.cross(z_i, r_ie)
            
            # Angular velocity component
            jacobian[3:, i] = z_i
        
        return jacobian

# Example: 3-DOF planar manipulator
dh_params_3dof = [
    [0.5, 0, 0, 0],    # Joint 1: revolute, a=0.5
    [0.4, 0, 0, 0],    # Joint 2: revolute, a=0.4
    [0.3, 0, 0, 0]     # Joint 3: revolute, a=0.3
]

kinematics = ManipulatorKinematics(dh_params_3dof)

# Test forward kinematics
joint_angles = [math.pi/4, -math.pi/6, math.pi/3]
ee_pose = kinematics.forward_kinematics(joint_angles)

print(f"End-effector pose with joint angles {joint_angles}:")
print(f"Position: [{ee_pose[0,3]:.3f}, {ee_pose[1,3]:.3f}, {ee_pose[2,3]:.3f}]")
print(f"Orientation matrix:\n{ee_pose[:3,:3]}")

# Calculate Jacobian
jacobian = kinematics.jacobian(joint_angles)
print(f"\nJacobian matrix shape: {jacobian.shape}")
print(f"Jacobian:\n{jacobian}")
```

### Inverse Kinematics Solutions

Inverse kinematics determines joint angles for a desired end-effector pose:

```python
from scipy.optimize import minimize
import warnings
warnings.filterwarnings('ignore')

class InverseKinematicsSolver:
    def __init__(self, kinematics_model, max_iterations=1000, tolerance=1e-6):
        """
        Inverse kinematics solver using numerical optimization
        
        Args:
            kinematics_model: Forward kinematics model
            max_iterations: Maximum number of optimization iterations
            tolerance: Solution tolerance
        """
        self.kinematics = kinematics_model
        self.max_iter = max_iterations
        self.tolerance = tolerance
    
    def ik_objective(self, joint_angles, target_pose):
        """
        Objective function for IK optimization
        """
        current_pose = self.kinematics.forward_kinematics(joint_angles)
        
        # Position error
        pos_error = np.linalg.norm(current_pose[:3, 3] - target_pose[:3, 3])
        
        # Orientation error (using Frobenius norm of rotation difference)
        rot_error = np.linalg.norm(current_pose[:3, :3] - target_pose[:3, :3], 'fro')
        
        # Weighted combination of position and orientation errors
        total_error = pos_error + 0.1 * rot_error
        
        return total_error
    
    def solve(self, target_pose, initial_guess=None):
        """
        Solve inverse kinematics for target pose
        
        Args:
            target_pose: 4x4 transformation matrix for desired end-effector pose
            initial_guess: Initial joint angle guess (optional)
            
        Returns:
            Joint angles that achieve the target pose (or closest achievable)
        """
        if initial_guess is None:
            initial_guess = np.zeros(self.kinematics.num_joints)
        
        # Define bounds for joint angles (commonly -pi to pi)
        bounds = [(-np.pi, np.pi) for _ in range(self.kinematics.num_joints)]
        
        # Solve optimization problem
        result = minimize(
            fun=self.ik_objective,
            x0=initial_guess,
            args=(target_pose,),
            method='L-BFGS-B',
            bounds=bounds,
            options={'maxiter': self.max_iter, 'ftol': self.tolerance}
        )
        
        if result.success:
            return result.x
        else:
            print(f"IK solution not found: {result.message}")
            return initial_guess  # Return initial guess if no solution found

# Example: Solve IK for 3-DOF manipulator
ik_solver = InverseKinematicsSolver(kinematics)

# Define target pose
target_pose = np.eye(4)
target_pose[0, 3] = 0.8  # x position
target_pose[1, 3] = 0.2  # y position
target_pose[2, 3] = 0.1  # z position

# Solve IK
solution = ik_solver.solve(target_pose)

print(f"\nIK Solution:")
print(f"Target position: [{target_pose[0,3]:.3f}, {target_pose[1,3]:.3f}, {target_pose[2,3]:.3f}]")

if solution is not None:
    # Verify solution
    solution_pose = kinematics.forward_kinematics(solution)
    print(f"Solution position: [{solution_pose[0,3]:.3f}, {solution_pose[1,3]:.3f}, {solution_pose[2,3]:.3f}]")
    print(f"Joint angles: {[f'{ang:.3f}' for ang in solution]}")
    
    # Calculate error
    pos_error = np.linalg.norm(target_pose[:3, 3] - solution_pose[:3, 3])
    print(f"Position error: {pos_error:.6f}")
```

## Grasp Planning and Analysis

### Grasp Representation

Grasps can be represented in various ways depending on the application:

```python
import numpy as np
from scipy.spatial.transform import Rotation as R
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Grasp:
    def __init__(self, position, orientation, finger_positions, grasp_type='parallel'):
        """
        Represents a robotic grasp
        
        Args:
            position: 3D position of grasp center [x, y, z]
            orientation: 3D orientation (rotation matrix or quaternion)
            finger_positions: Positions of finger contacts [[x1,y1,z1], [x2,y2,z2], ...]
            grasp_type: Type of grasp ('parallel', 'tripod', 'pinch', etc.)
        """
        self.position = np.array(position)
        self.orientation = np.array(orientation) if orientation.shape == (3,3) else R.from_quat(orientation).as_matrix()
        self.finger_positions = np.array(finger_positions)
        self.grasp_type = grasp_type
        
        # Calculate approach, binormal, and axis vectors
        self.approach = self.orientation[:, 2]  # z-axis of orientation
        self.binormal = self.orientation[:, 1]  # y-axis of orientation
        self.axis = self.orientation[:, 0]     # x-axis of orientation
    
    def to_dict(self):
        """Convert grasp to dictionary representation"""
        return {
            'position': self.position.tolist(),
            'orientation': self.orientation.tolist(),
            'finger_positions': self.finger_positions.tolist(),
            'grasp_type': self.grasp_type,
            'approach': self.approach.tolist(),
            'binormal': self.binormal.tolist(),
            'axis': self.axis.tolist()
        }
    
    def visualize(self, object_mesh=None):
        """Visualize the grasp in 3D"""
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot finger positions
        ax.scatter(
            self.finger_positions[:, 0], 
            self.finger_positions[:, 1], 
            self.finger_positions[:, 2], 
            c='red', s=100, label='Finger Contacts'
        )
        
        # Plot grasp frame
        origin = self.position
        scale = 0.1
        
        # Approach vector (blue)
        ax.quiver(origin[0], origin[1], origin[2], 
                 self.approach[0]*scale, self.approach[1]*scale, self.approach[2]*scale,
                 color='blue', arrow_length_ratio=0.1, label='Approach')
        
        # Binormal vector (green)
        ax.quiver(origin[0], origin[1], origin[2], 
                 self.binormal[0]*scale, self.binormal[1]*scale, self.binormal[2]*scale,
                 color='green', arrow_length_ratio=0.1, label='Binormal')
        
        # Axis vector (red)
        ax.quiver(origin[0], origin[1], origin[2], 
                 self.axis[0]*scale, self.axis[1]*scale, self.axis[2]*scale,
                 color='red', arrow_length_ratio=0.1, label='Axis')
        
        # Plot object if provided
        if object_mesh is not None:
            ax.plot_trisurf(object_mesh.vertices[:, 0], 
                           object_mesh.vertices[:, 1], 
                           object_mesh.vertices[:, 2], 
                           alpha=0.3)
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Grasp Visualization')
        ax.legend()
        
        plt.show()

# Example: Create a simple grasp
grasp_pos = [0.5, 0.3, 0.2]
grasp_orient = R.from_euler('xyz', [0, 0, np.pi/4]).as_matrix()  # 45-degree rotation around z
finger_pos = [
    [0.45, 0.3, 0.2],   # Left finger
    [0.55, 0.3, 0.2]    # Right finger
]

grasp = Grasp(grasp_pos, grasp_orient, finger_pos, 'parallel')
grasp_dict = grasp.to_dict()

print("Grasp representation:")
for key, value in grasp_dict.items():
    print(f"  {key}: {value}")
```

### Grasp Quality Metrics

Evaluating the quality of potential grasps:

```python
class GraspQualityEvaluator:
    def __init__(self):
        """
        Evaluates the quality of robotic grasps
        """
        pass
    
    def force_closure(self, contact_points, normals, friction_coeff=0.7):
        """
        Check if a grasp achieves force closure
        
        Args:
            contact_points: Array of contact point positions
            normals: Array of surface normals at contact points
            friction_coeff: Friction coefficient
            
        Returns:
            Boolean indicating if force closure is achieved
        """
        # This is a simplified check - in practice, this involves complex convex hull computations
        # For a 3D object, we need at least 7 frictional contacts or 12 frictionless contacts for force closure
        # For 2D, we need at least 4 frictional contacts or 6 frictionless contacts
        
        n_contacts = len(contact_points)
        
        # Simplified check: assume force closure if we have enough contacts
        # In reality, this requires checking if the origin is inside the convex hull of wrenches
        if n_contacts >= 7:  # For 3D with friction
            return True
        elif n_contacts >= 12:  # For 3D without friction
            return True
        else:
            return False
    
    def grasp_width(self, contact_points):
        """
        Calculate the grasp width (distance between fingers)
        """
        if len(contact_points) < 2:
            return 0.0
        
        # Calculate distance between first two contact points
        dist = np.linalg.norm(np.array(contact_points[0]) - np.array(contact_points[1]))
        return dist
    
    def grasp_stability(self, grasp, object_properties):
        """
        Evaluate grasp stability based on object properties
        
        Args:
            grasp: Grasp object
            object_properties: Dictionary with object properties (mass, COM, etc.)
            
        Returns:
            Stability score (0-1)
        """
        # Calculate if grasp is aligned with object's principal axes
        # This is a simplified stability evaluation
        
        # Get object's center of mass
        obj_com = np.array(object_properties.get('center_of_mass', [0, 0, 0]))
        
        # Calculate distance from grasp center to object COM
        com_distance = np.linalg.norm(grasp.position - obj_com)
        
        # Calculate if grasp is near the object
        if com_distance > 0.3:  # 30cm threshold
            return 0.2  # Low stability if grasp is far from object
        
        # Calculate grasp width relative to object size
        obj_size = object_properties.get('size', 0.1)  # Default 10cm
        grasp_width = self.grasp_width(grasp.finger_positions)
        
        # Ideal grasp width is roughly 1.2x object size
        ideal_width = obj_size * 1.2
        width_ratio = grasp_width / ideal_width
        
        # Score based on width ratio (close to 1.0 is ideal)
        width_score = 1.0 - abs(width_ratio - 1.0)
        width_score = max(0.0, min(1.0, width_score))
        
        # Calculate if grasp is aligned with object orientation
        # This would require object orientation information
        alignment_score = 0.8  # Default score
        
        # Combine scores
        stability_score = 0.4 * width_score + 0.4 * alignment_score + 0.2 * (1.0 - min(1.0, com_distance))
        
        return stability_score
    
    def grasp_dexterity(self, grasp, joint_limits):
        """
        Evaluate grasp dexterity based on joint configuration
        
        Args:
            grasp: Grasp object with joint angles
            joint_limits: Joint limit ranges
            
        Returns:
            Dexterity score (0-1)
        """
        # Calculate how close the joints are to their limits
        # Higher dexterity when joints are in comfortable middle range
        if not hasattr(grasp, 'joint_angles') or grasp.joint_angles is None:
            return 0.5  # Default score if no joint info available
        
        joint_angles = np.array(grasp.joint_angles)
        joint_limits = np.array(joint_limits)
        
        # Calculate distance from center of joint range
        centers = (joint_limits[:, 0] + joint_limits[:, 1]) / 2
        ranges = joint_limits[:, 1] - joint_limits[:, 0]
        
        distances = np.abs(joint_angles - centers) / (ranges / 2)
        avg_distance = np.mean(distances)
        
        # Dexterity increases as we move away from joint limits (0 = at limit, 1 = at center)
        dexterity_score = 1.0 - avg_distance
        dexterity_score = max(0.0, min(1.0, dexterity_score))
        
        return dexterity_score

# Example: Evaluate grasp quality
evaluator = GraspQualityEvaluator()

# Object properties
obj_props = {
    'center_of_mass': [0.5, 0.3, 0.1],
    'size': 0.08,  # 8cm object
    'mass': 0.5    # 500g object
}

# Evaluate the grasp created earlier
stability_score = evaluator.grasp_stability(grasp, obj_props)
print(f"\nGrasp stability score: {stability_score:.3f}")

# Example with more contacts for force closure check
contact_points = np.array([
    [0.48, 0.28, 0.18],
    [0.52, 0.28, 0.18],
    [0.5, 0.32, 0.18],
    [0.5, 0.28, 0.22],
    [0.48, 0.30, 0.16],
    [0.52, 0.30, 0.16],
    [0.5, 0.26, 0.20]
])

normals = np.array([
    [0, 0, -1],  # Top surface
    [0, 0, -1],  # Top surface
    [0, 1, 0],   # Side surface
    [0, 0, 1],   # Bottom surface
    [-1, 0, 0],  # Side surface
    [1, 0, 0],   # Side surface
    [0, -1, 0]   # Side surface
])

force_closure = evaluator.force_closure(contact_points, normals)
print(f"Force closure achieved: {force_closure}")
```

## Grasp Planning Algorithms

### Antipodal Grasp Planning

Finding grasps where contact points oppose each other:

```python
class AntipodalGraspPlanner:
    def __init__(self, robot_hand_span=0.15, min_grasp_width=0.02, max_grasp_width=0.12):
        """
        Plan antipodal grasps for parallel jaw grippers
        
        Args:
            robot_hand_span: Maximum reach of the robot hand
            min_grasp_width: Minimum grasp width
            max_grasp_width: Maximum grasp width
        """
        self.hand_span = robot_hand_span
        self.min_width = min_grasp_width
        self.max_width = max_grasp_width
    
    def find_antipodal_grasps(self, point_cloud, normals, num_grasps=10):
        """
        Find antipodal grasps from point cloud data
        
        Args:
            point_cloud: Nx3 array of 3D points
            normals: Nx3 array of surface normals at each point
            num_grasps: Number of grasps to return
            
        Returns:
            List of potential grasps
        """
        grasps = []
        
        # Convert to numpy arrays
        points = np.array(point_cloud)
        normals = np.array(normals)
        
        # Find pairs of points that could form antipodal grasps
        n_points = len(points)
        
        for i in range(n_points):
            for j in range(i+1, n_points):
                p1, n1 = points[i], normals[i]
                p2, n2 = points[j], normals[j]
                
                # Check if normals are roughly opposite (antipodal condition)
                dot_product = np.dot(n1, n2)
                
                # For antipodal grasp, normals should be roughly opposite
                if dot_product < -0.8:  # Threshold for "opposite" direction
                    # Check if distance is within graspable range
                    distance = np.linalg.norm(p1 - p2)
                    
                    if self.min_width <= distance <= self.max_width:
                        # Calculate grasp center and orientation
                        grasp_center = (p1 + p2) / 2
                        
                        # Grasp orientation: perpendicular to the line connecting contacts
                        grasp_axis = (p2 - p1) / distance  # Normalized vector from p1 to p2
                        approach_dir = np.cross(grasp_axis, [0, 0, 1])  # Perpendicular to grasp axis
                        if np.linalg.norm(approach_dir) < 0.1:  # If parallel to z-axis
                            approach_dir = np.cross(grasp_axis, [1, 0, 0])  # Use x-axis instead
                        approach_dir = approach_dir / np.linalg.norm(approach_dir)
                        
                        # Create rotation matrix
                        # Z-axis: approach direction, Y-axis: normalized grasp axis, X-axis: cross product
                        z_axis = approach_dir
                        y_axis = grasp_axis
                        x_axis = np.cross(y_axis, z_axis)
                        x_axis = x_axis / np.linalg.norm(x_axis)
                        y_axis = np.cross(z_axis, x_axis)  # Recalculate to ensure orthogonality
                        
                        orientation = np.column_stack([x_axis, y_axis, z_axis])
                        
                        # Create grasp
                        finger_positions = [p1, p2]
                        grasp = Grasp(grasp_center, orientation, finger_positions, 'parallel')
                        
                        # Calculate grasp quality
                        grasp_quality = 1.0 - abs(dot_product)  # Higher quality for more opposite normals
                        
                        grasps.append((grasp, grasp_quality))
        
        # Sort grasps by quality and return top ones
        grasps.sort(key=lambda x: x[1], reverse=True)
        
        return [g[0] for g in grasps[:num_grasps]]

# Example: Plan antipodal grasps
planner = AntipodalGraspPlanner()

# Simulate a point cloud of an object (e.g., a cylinder)
theta = np.linspace(0, 2*np.pi, 20)
height = np.linspace(-0.05, 0.05, 10)
points = []
normals = []

for h in height:
    for t in theta:
        # Points on cylinder surface
        x = 0.5 + 0.05 * np.cos(t)
        y = 0.3 + 0.05 * np.sin(t)
        z = h
        points.append([x, y, z])
        
        # Normals pointing outward from cylinder axis
        nx = np.cos(t)
        ny = np.sin(t)
        nz = 0
        normals.append([nx, ny, nz])

# Add top and bottom surface points
for t in np.linspace(0, 2*np.pi, 10):
    # Top surface
    x = 0.5 + 0.04 * np.cos(t)
    y = 0.3 + 0.04 * np.sin(t)
    z = 0.05
    points.append([x, y, z])
    normals.append([0, 0, 1])  # Normal pointing up
    
    # Bottom surface
    x = 0.5 + 0.04 * np.cos(t)
    y = 0.3 + 0.04 * np.sin(t)
    z = -0.05
    points.append([x, y, z])
    normals.append([0, 0, -1])  # Normal pointing down

# Find antipodal grasps
candidate_grasps = planner.find_antipodal_grasps(points, normals, num_grasps=5)

print(f"\nFound {len(candidate_grasps)} antipodal grasps")
for i, grasp in enumerate(candidate_grasps[:3]):  # Show first 3
    print(f"Grasp {i+1}:")
    print(f"  Position: [{grasp.position[0]:.3f}, {grasp.position[1]:.3f}, {grasp.position[2]:.3f}]")
    print(f"  Finger distance: {np.linalg.norm(grasp.finger_positions[0] - grasp.finger_positions[1]):.3f}m")
```

### Machine Learning for Grasp Planning

Using machine learning to predict grasp success:

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
import numpy as np

class GraspDataset(Dataset):
    def __init__(self, grasp_data, labels):
        """
        Dataset for grasp learning
        
        Args:
            grasp_data: Features for each grasp (e.g., geometric features)
            labels: Binary labels (0=failed, 1=successful)
        """
        self.grasp_features = torch.FloatTensor(grasp_data)
        self.labels = torch.LongTensor(labels)
    
    def __len__(self):
        return len(self.labels)
    
    def __getitem__(self, idx):
        return self.grasp_features[idx], self.labels[idx]

class GraspSuccessPredictor(nn.Module):
    def __init__(self, input_dim=10, hidden_dims=[64, 32, 16]):
        """
        Neural network to predict grasp success
        
        Args:
            input_dim: Dimension of input features
            hidden_dims: Dimensions of hidden layers
        """
        super(GraspSuccessPredictor, self).__init__()
        
        layers = []
        prev_dim = input_dim
        
        for hidden_dim in hidden_dims:
            layers.append(nn.Linear(prev_dim, hidden_dim))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(0.2))
            prev_dim = hidden_dim
        
        # Output layer: binary classification (success/failure)
        layers.append(nn.Linear(prev_dim, 2))
        
        self.network = nn.Sequential(*layers)
    
    def forward(self, x):
        return self.network(x)

class MLPGraspPlanner:
    def __init__(self, model_path=None):
        """
        Grasp planner using machine learning
        
        Args:
            model_path: Path to pre-trained model (optional)
        """
        self.input_dim = 10  # Example: position (3), orientation (4), width (1), object_size (1), etc.
        self.model = GraspSuccessPredictor(input_dim=self.input_dim)
        
        if model_path:
            self.model.load_state_dict(torch.load(model_path))
        
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
        self.criterion = nn.CrossEntropyLoss()
    
    def extract_features(self, grasp, object_info):
        """
        Extract features from grasp and object for prediction
        
        Args:
            grasp: Grasp object
            object_info: Dictionary with object information
            
        Returns:
            Feature vector
        """
        # Example features (in practice, these would be more sophisticated)
        features = []
        
        # Position features
        features.extend(grasp.position)
        
        # Orientation features (first column of rotation matrix)
        features.extend(grasp.orientation[:, 0])
        
        # Grasp width
        width = np.linalg.norm(grasp.finger_positions[0] - grasp.finger_positions[1])
        features.append(width)
        
        # Object size
        obj_size = object_info.get('size', 0.1)
        features.append(obj_size)
        
        # Object mass
        obj_mass = object_info.get('mass', 0.1)
        features.append(obj_mass)
        
        # Fill up to input dimension with zeros if needed
        while len(features) < self.input_dim:
            features.append(0.0)
        
        return np.array(features[:self.input_dim])
    
    def predict_grasp_success(self, grasp, object_info):
        """
        Predict the success probability of a grasp
        
        Args:
            grasp: Grasp object
            object_info: Dictionary with object information
            
        Returns:
            Probability of success (0-1)
        """
        features = self.extract_features(grasp, object_info)
        features_tensor = torch.FloatTensor(features).unsqueeze(0)
        
        self.model.eval()
        with torch.no_grad():
            output = self.model(features_tensor)
            probabilities = F.softmax(output, dim=1)
            success_prob = probabilities[0, 1].item()  # Probability of success class
        
        return success_prob
    
    def plan_grasps_ml(self, candidate_grasps, object_info, top_k=5):
        """
        Plan grasps using ML predictions
        
        Args:
            candidate_grasps: List of candidate grasps
            object_info: Dictionary with object information
            top_k: Number of top grasps to return
            
        Returns:
            List of (grasp, success_probability) tuples ranked by probability
        """
        grasp_scores = []
        
        for grasp in candidate_grasps:
            prob = self.predict_grasp_success(grasp, object_info)
            grasp_scores.append((grasp, prob))
        
        # Sort by success probability
        grasp_scores.sort(key=lambda x: x[1], reverse=True)
        
        return grasp_scores[:top_k]
    
    def train(self, training_data, epochs=100):
        """
        Train the grasp success predictor
        
        Args:
            training_data: List of (grasp_features, label) tuples
            epochs: Number of training epochs
        """
        # Prepare data
        features = [item[0] for item in training_data]
        labels = [item[1] for item in training_data]
        
        dataset = GraspDataset(features, labels)
        dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
        
        self.model.train()
        for epoch in range(epochs):
            total_loss = 0
            for batch_features, batch_labels in dataloader:
                self.optimizer.zero_grad()
                outputs = self.model(batch_features)
                loss = self.criterion(outputs, batch_labels)
                loss.backward()
                self.optimizer.step()
                total_loss += loss.item()
            
            if epoch % 20 == 0:
                print(f"Epoch {epoch}, Loss: {total_loss/len(dataloader):.4f}")

# Example: Use ML-based grasp planning
ml_planner = MLPGraspPlanner()

# Simulate training data (in practice, this would come from real robot experiments)
training_data = []
for _ in range(1000):
    # Generate random grasp features
    features = np.random.rand(ml_planner.input_dim).astype(np.float32)
    # Generate random labels (50% success rate for this example)
    label = np.random.randint(0, 2)
    training_data.append((features, label))

# Train the model
print("\nTraining ML grasp predictor...")
ml_planner.train(training_data, epochs=50)

# Plan grasps using ML
obj_info = {'size': 0.08, 'mass': 0.5}
top_grasps = ml_planner.plan_grasps_ml(candidate_grasps, obj_info, top_k=3)

print(f"\nTop 3 grasps by ML prediction:")
for i, (grasp, prob) in enumerate(top_grasps):
    print(f"Grasp {i+1}: Success probability = {prob:.3f}")
    print(f"  Position: [{grasp.position[0]:.3f}, {grasp.position[1]:.3f}, {grasp.position[2]:.3f}]")
```

## Force Control in Manipulation

### Impedance Control

Impedance control allows robots to behave like springs, making them compliant during manipulation:

```python
class ImpedanceController:
    def __init__(self, stiffness_diag=[1000, 1000, 1000, 100, 100, 100], 
                 damping_diag=None, dt=0.001):
        """
        Impedance controller for compliant manipulation
        
        Args:
            stiffness_diag: Diagonal elements of stiffness matrix [x, y, z, rx, ry, rz]
            damping_diag: Diagonal elements of damping matrix (defaults to critical damping)
            dt: Control loop time step
        """
        self.stiffness = np.diag(stiffness_diag)
        self.dt = dt
        
        if damping_diag is None:
            # Critical damping: damping = 2 * sqrt(stiffness)
            damping_diag = [2 * np.sqrt(k) for k in stiffness_diag]
        
        self.damping = np.diag(damping_diag)
        
        # State variables
        self.desired_pos = np.zeros(6)  # [x, y, z, rx, ry, rz]
        self.current_pos = np.zeros(6)
        self.velocity = np.zeros(6)
        self.force = np.zeros(6)
    
    def update(self, current_pos, external_force=None):
        """
        Update impedance controller
        
        Args:
            current_pos: Current end-effector position/orientation [x, y, z, rx, ry, rz]
            external_force: External force applied to end-effector [fx, fy, fz, mx, my, mz]
            
        Returns:
            Desired force to apply
        """
        if external_force is None:
            external_force = np.zeros(6)
        
        # Calculate position error
        pos_error = self.desired_pos - current_pos
        
        # Update velocity (numerical differentiation)
        if hasattr(self, 'prev_pos'):
            self.velocity = (current_pos - self.prev_pos) / self.dt
        else:
            self.velocity = np.zeros(6)
        
        self.prev_pos = current_pos.copy()
        
        # Calculate impedance force
        spring_force = self.stiffness @ pos_error
        damping_force = self.damping @ self.velocity
        
        # Total impedance force
        impedance_force = spring_force + damping_force
        
        # Desired force = impedance force - external force
        # (external force is subtracted because it affects the system)
        desired_force = impedance_force - external_force
        
        return desired_force
    
    def set_desired_pose(self, pose):
        """
        Set desired end-effector pose
        
        Args:
            pose: Desired pose [x, y, z, rx, ry, rz]
        """
        self.desired_pos = np.array(pose)

# Example: Impedance control for compliant manipulation
impedance_ctrl = ImpedanceController(
    stiffness_diag=[500, 500, 500, 50, 50, 50],  # Lower stiffness for compliance
    dt=0.01
)

# Set a desired position
impedance_ctrl.set_desired_pose([0.5, 0.3, 0.2, 0, 0, 0])

# Simulate interaction with environment
time_steps = np.arange(0, 5, 0.01)
current_pos = np.array([0.5, 0.3, 0.2, 0, 0, 0])  # Start at desired position
applied_forces = []
positions = []
desired_positions = []

for t in time_steps:
    # Simulate external force (e.g., hitting an object at t=2s)
    external_force = np.zeros(6)
    if 2.0 < t < 2.5:
        external_force[2] = -20  # Push in Z direction
    
    # Update controller
    desired_force = impedance_ctrl.update(current_pos, external_force)
    
    # Simulate robot dynamics (simplified)
    # F = ma, so acceleration = F/m (assuming m=1 for simplicity)
    acceleration = desired_force * 0.1  # Scale factor for realistic movement
    current_pos += self.velocity * 0.01 + 0.5 * acceleration * (0.01 ** 2)
    self.velocity += acceleration * 0.01
    
    # Record data
    applied_forces.append(desired_force.copy())
    positions.append(current_pos.copy())
    desired_positions.append(impedance_ctrl.desired_pos.copy())

applied_forces = np.array(applied_forces)
positions = np.array(positions)
desired_positions = np.array(desired_positions)

# Visualization
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))

# Plot applied forces
ax1.plot(time_steps, applied_forces[:, 0], label='Fx', linewidth=2)
ax1.plot(time_steps, applied_forces[:, 1], label='Fy', linewidth=2)
ax1.plot(time_steps, applied_forces[:, 2], label='Fz', linewidth=2)
ax1.set_ylabel('Applied Force (N)')
ax1.set_title('Impedance Controller: Applied Forces')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot position tracking
ax2.plot(time_steps, positions[:, 0], label='Actual X', linewidth=2)
ax2.plot(time_steps, desired_positions[:, 0], label='Desired X', linestyle='--', linewidth=2)
ax2.set_ylabel('Position X (m)')
ax2.set_title('Position Tracking')
ax2.legend()
ax2.grid(True, alpha=0.3)

ax3.plot(time_steps, positions[:, 2], label='Actual Z', linewidth=2)
ax3.plot(time_steps, desired_positions[:, 2], label='Desired Z', linestyle='--', linewidth=2)
ax3.set_xlabel('Time (s)')
ax3.set_ylabel('Position Z (m)')
ax3.set_title('Z Position During Interaction')
ax3.legend()
ax3.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("Impedance control simulation completed.")
```

## Integration with Perception Systems

### Vision-Based Grasp Planning

Integrating computer vision with grasp planning:

```python
import cv2
import numpy as np
from scipy.spatial.transform import Rotation as R

class VisionBasedGrasper:
    def __init__(self):
        """
        System that combines vision with grasp planning
        """
        self.grasp_planner = AntipodalGraspPlanner()
        self.ml_planner = MLPGraspPlanner()
        
        # Camera parameters (example values)
        self.fx = 525.0  # Focal length x
        self.fy = 525.0  # Focal length y
        self.cx = 319.5  # Principal point x
        self.cy = 239.5  # Principal point y
    
    def process_camera_input(self, rgb_image, depth_image):
        """
        Process camera input to extract object information
        
        Args:
            rgb_image: RGB image from camera
            depth_image: Depth image from camera
            
        Returns:
            Dictionary with object information
        """
        # This is a simplified example
        # In practice, this would involve:
        # 1. Object detection and segmentation
        # 2. Pose estimation
        # 3. Point cloud generation
        
        # For this example, we'll simulate extracting object information
        height, width = depth_image.shape
        
        # Find object in center of image (simplified)
        center_x, center_y = width // 2, height // 2
        
        # Get depth at center (simplified)
        object_depth = depth_image[center_y, center_x]
        
        if object_depth == 0 or object_depth > 2.0:  # Invalid depth
            object_depth = 1.0  # Default distance
        
        # Convert pixel coordinates to 3D world coordinates
        object_x = (center_x - self.cx) * object_depth / self.fx
        object_y = (center_y - self.cy) * object_depth / self.fy
        object_z = object_depth
        
        object_pos = [object_x, object_y, object_z]
        
        # Estimate object size (simplified)
        # In practice, this would come from segmentation
        object_size = 0.1  # Default size
        
        return {
            'position': object_pos,
            'size': object_size,
            'mass': 0.3,  # Estimated mass
            'surface_normals': []  # Would be computed from point cloud
        }
    
    def generate_grasps_from_vision(self, rgb_image, depth_image):
        """
        Generate grasps based on visual input
        
        Args:
            rgb_image: RGB image from camera
            depth_image: Depth image from camera
            
        Returns:
            List of candidate grasps
        """
        # Process visual input
        obj_info = self.process_camera_input(rgb_image, depth_image)
        
        # Generate point cloud from depth image (simplified)
        height, width = depth_image.shape
        points = []
        normals = []
        
        # Sample points from depth image
        step = 10  # Sample every 10th pixel
        for y in range(0, height, step):
            for x in range(0, width, step):
                depth_val = depth_image[y, x]
                if depth_val > 0 and depth_val < 2.0:  # Valid depth
                    # Convert to 3D
                    world_x = (x - self.cx) * depth_val / self.fx
                    world_y = (y - self.cy) * depth_val / self.fy
                    world_z = depth_val
                    
                    points.append([world_x, world_y, world_z])
                    
                    # Estimate normal (simplified - in practice, use normal estimation algorithms)
                    normals.append([0, 0, 1])  # Assume mostly upward facing
        
        if len(points) < 10:  # Not enough points for grasp planning
            return []
        
        # Plan grasps using antipodal method
        grasps = self.grasp_planner.find_antipodal_grasps(points, normals, num_grasps=10)
        
        # Transform grasps to robot base frame if needed
        # (For this example, we'll assume they're already in the right frame)
        
        return grasps
    
    def select_best_grasp(self, candidate_grasps, obj_info):
        """
        Select the best grasp using ML prediction
        
        Args:
            candidate_grasps: List of candidate grasps
            obj_info: Object information
            
        Returns:
            Best grasp and its success probability
        """
        if not candidate_grasps:
            return None, 0.0
        
        # Use ML planner to rank grasps
        ranked_grasps = self.ml_planner.plan_grasps_ml(candidate_grasps, obj_info, top_k=1)
        
        if ranked_grasps:
            return ranked_grasps[0][0], ranked_grasps[0][1]  # grasp, probability
        else:
            return candidate_grasps[0], 0.5  # Default to first grasp with medium confidence

# Example: Vision-based grasping pipeline
vision_grasper = VisionBasedGrasper()

# Simulate camera inputs (in practice, these would come from actual sensors)
rgb_img = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)  # Simulated RGB image
depth_img = np.ones((480, 640)) * 1.0  # Simulated depth image (1 meter away)

# Add some "object" to depth image
center_y, center_x = 240, 320
for i in range(-20, 21):
    for j in range(-20, 21):
        if 0 <= center_y+i < 480 and 0 <= center_x+j < 640:
            depth_img[center_y+i, center_x+j] = 0.8  # Object at 80cm

# Process vision input
obj_info = vision_grasper.process_camera_input(rgb_img, depth_img)
print(f"\nObject detected at position: [{obj_info['position'][0]:.3f}, {obj_info['position'][1]:.3f}, {obj_info['position'][2]:.3f}]")

# Generate grasps from vision
candidate_grasps = vision_grasper.generate_grasps_from_vision(rgb_img, depth_img)
print(f"Generated {len(candidate_grasps)} candidate grasps from vision")

# Select best grasp
if candidate_grasps:
    best_grasp, success_prob = vision_grasper.select_best_grasp(candidate_grasps, obj_info)
    print(f"Best grasp success probability: {success_prob:.3f}")
    print(f"Best grasp position: [{best_grasp.position[0]:.3f}, {best_grasp.position[1]:.3f}, {best_grasp.position[2]:.3f}]")
else:
    print("No valid grasps found from vision input")
```

## Manipulation Task Planning

### Pick-and-Place Task

Implementing a complete pick-and-place task:

```python
class PickPlacePlanner:
    def __init__(self, robot_workspace_limits=None):
        """
        Plan pick-and-place tasks
        
        Args:
            robot_workspace_limits: Dictionary with 'min' and 'max' workspace limits
        """
        self.workspace_limits = robot_workspace_limits or {
            'min': [-1.0, -1.0, 0.0],
            'max': [1.0, 1.0, 1.5]
        }
        
        # Initialize components
        self.vision_grasper = VisionBasedGrasper()
        self.impedance_ctrl = ImpedanceController()
    
    def is_in_workspace(self, position):
        """
        Check if a position is within robot workspace
        
        Args:
            position: 3D position [x, y, z]
            
        Returns:
            Boolean indicating if position is reachable
        """
        pos = np.array(position)
        min_limits = np.array(self.workspace_limits['min'])
        max_limits = np.array(self.workspace_limits['max'])
        
        return np.all(pos >= min_limits) & np.all(pos <= max_limits)
    
    def plan_approach_motion(self, grasp_pose, approach_distance=0.1):
        """
        Plan approach motion to grasp pose
        
        Args:
            grasp_pose: Target grasp pose [x, y, z, rx, ry, rz]
            approach_distance: Distance to approach from (meters)
            
        Returns:
            Approach pose
        """
        grasp_pos = np.array(grasp_pose[:3])
        grasp_rot = R.from_rotvec(grasp_pose[3:])  # Assuming pose uses rotation vector
        
        # Calculate approach direction (opposite to approach vector in grasp frame)
        approach_dir = grasp_rot.apply([0, 0, -1])  # -Z direction in grasp frame
        approach_pos = grasp_pos + approach_dir * approach_distance
        
        return np.concatenate([approach_pos, grasp_pose[3:]])
    
    def execute_pick_place(self, pickup_rgb, pickup_depth, place_position):
        """
        Execute complete pick-and-place task
        
        Args:
            pickup_rgb: RGB image at pickup location
            pickup_depth: Depth image at pickup location
            place_position: 3D position to place object [x, y, z]
            
        Returns:
            Success status and execution log
        """
        execution_log = []
        
        # Step 1: Analyze pickup location
        execution_log.append("Analyzing pickup location...")
        obj_info = self.vision_grasper.process_camera_input(pickup_rgb, pickup_depth)
        
        if not self.is_in_workspace(obj_info['position']):
            execution_log.append(f"Object at {obj_info['position']} is outside workspace")
            return False, execution_log
        
        # Step 2: Generate grasps
        execution_log.append("Generating candidate grasps...")
        candidate_grasps = self.vision_grasper.generate_grasps_from_vision(pickup_rgb, pickup_depth)
        
        if not candidate_grasps:
            execution_log.append("No valid grasps found")
            return False, execution_log
        
        # Step 3: Select best grasp
        execution_log.append("Selecting best grasp...")
        best_grasp, success_prob = self.vision_grasper.select_best_grasp(candidate_grasps, obj_info)
        
        if success_prob < 0.3:  # Low confidence grasp
            execution_log.append(f"Best grasp has low success probability ({success_prob:.3f}), aborting")
            return False, execution_log
        
        # Step 4: Plan approach motion
        execution_log.append("Planning approach motion...")
        grasp_pose = np.concatenate([best_grasp.position, [0, 0, 0]])  # Simplified orientation
        approach_pose = self.plan_approach_motion(grasp_pose)
        
        # Check if approach pose is in workspace
        if not self.is_in_workspace(approach_pose[:3]):
            execution_log.append("Approach pose is outside workspace")
            return False, execution_log
        
        # Step 5: Verify place position
        execution_log.append("Verifying place position...")
        if not self.is_in_workspace(place_position):
            execution_log.append(f"Place position {place_position} is outside workspace")
            return False, execution_log
        
        # Step 6: Simulate execution (in practice, this would control the real robot)
        execution_log.append("Executing pick-and-place maneuver...")
        
        # This is where actual robot control would happen
        # 1. Move to approach position
        # 2. Move to grasp position
        # 3. Close gripper
        # 4. Lift object
        # 5. Move to place approach position
        # 6. Move to place position
        # 7. Open gripper
        # 8. Retract
        
        execution_log.append("Pick-and-place completed successfully")
        return True, execution_log

# Example: Execute pick-and-place task
pick_place_planner = PickPlacePlanner()

# Simulate camera inputs for pickup location (reuse previous simulation)
pickup_rgb = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
pickup_depth = depth_img.copy()  # Use the same depth image as before

# Define place position
place_pos = [0.6, 0.0, 0.1]  # Place in front of robot

# Execute task
success, log = pick_place_planner.execute_pick_place(pickup_rgb, pickup_depth, place_pos)

print("\nPick-and-Place Execution Log:")
for entry in log:
    print(f"  - {entry}")

print(f"\nTask completed successfully: {success}")
```

## Best Practices for Manipulation

### 1. Control Strategy Selection
- Use position control for free-space motions
- Switch to force control for contact-rich tasks
- Implement impedance control for compliant interaction
- Use hybrid position/force control when needed

### 2. Grasp Planning Considerations
- Consider object properties (shape, weight, fragility)
- Account for robot hand limitations
- Plan for multiple grasp attempts
- Include grasp verification steps

### 3. Perception Integration
- Combine multiple sensors for robust perception
- Implement outlier rejection for noisy data
- Use machine learning to improve grasp prediction
- Continuously update object models during manipulation

### 4. Safety and Robustness
- Implement force limits to prevent damage
- Include collision detection and avoidance
- Plan for failure recovery
- Test extensively in simulation before real-world deployment

## Looking Ahead

This week we explored robotic manipulation and grasping, which are essential capabilities for humanoid robots. Next week, we'll dive into conversational robotics, focusing on how robots can interact with humans through natural language and other modalities.

## Exercises

1. Implement a grasp planner for a specific robot hand
2. Create a force control system for compliant manipulation
3. Develop a machine learning model for grasp success prediction
4. Integrate vision with manipulation for object picking
5. Design a complete manipulation task planner

## Further Reading

- "Handbook of Robotics" by Siciliano and Khatib
- "Robotics: Modelling, Planning and Control" by Siciliano et al.
- "Learning Synergies for Robotic Grasping" by Monteiro et al.
- "Deep Learning for Detecting Robotic Grasps" by Redmon and Angelova