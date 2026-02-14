---
sidebar_position: 27
---

# Grasp Planning and Execution in Robotic Manipulation

This lesson focuses on the critical aspect of grasp planning and execution in robotic manipulation. Grasp planning involves determining how to securely hold an object, which is fundamental for any manipulation task.

## Learning Objectives

By the end of this lesson, you will be able to:

1. Understand different grasp types and their applications
2. Implement geometric and physics-based grasp planners
3. Evaluate grasp quality using various metrics
4. Plan grasps for objects with different shapes and properties
5. Execute grasps with appropriate force control
6. Adapt grasps based on object properties and task requirements

## Grasp Taxonomies and Types

### Classification of Grasps

Robotic grasps can be classified in several ways:

```python
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial.transform import Rotation as R

class GraspClassifier:
    def __init__(self):
        """
        Classifier for different types of grasps
        """
        pass
    
    def classify_by_fingers(self, contact_points):
        """
        Classify grasp by number of contact points
        
        Args:
            contact_points: List of contact point positions
            
        Returns:
            Grasp type based on number of contacts
        """
        n_contacts = len(contact_points)
        
        if n_contacts == 2:
            return "Two-finger pinch"
        elif n_contacts == 3:
            return "Three-finger tripod"
        elif n_contacts == 4:
            return "Four-finger grasp"
        elif n_contacts >= 5:
            return "Power grasp (cylindrical)"
        else:
            return "Unknown grasp type"
    
    def classify_by_contact_type(self, contact_points, surface_normals):
        """
        Classify grasp by contact type (point vs. surface)
        
        Args:
            contact_points: List of contact point positions
            surface_normals: Surface normals at contact points
            
        Returns:
            Contact type classification
        """
        # Calculate curvature at contact points (simplified)
        curvatures = []
        for i, point in enumerate(contact_points):
            # In practice, this would use local surface patch analysis
            # For now, we'll use a simple proxy
            if len(contact_points) > 1:
                # Calculate distance to nearest neighbor
                min_dist = float('inf')
                for j, other_point in enumerate(contact_points):
                    if i != j:
                        dist = np.linalg.norm(np.array(point) - np.array(other_point))
                        min_dist = min(min_dist, dist)
                curvatures.append(1.0 / (min_dist + 1e-6))  # Inverse of distance as curvature proxy
        
        avg_curvature = np.mean(curvatures) if curvatures else 0
        
        if avg_curvature > 10:  # High curvature
            return "Point contact grasp"
        else:
            return "Surface contact grasp"
    
    def classify_by_wrench_space(self, contact_points, surface_normals, friction_coeff=0.7):
        """
        Classify grasp by wrench space properties
        
        Args:
            contact_points: List of contact point positions
            surface_normals: Surface normals at contact points
            friction_coeff: Friction coefficient
            
        Returns:
            Wrench space classification
        """
        n_contacts = len(contact_points)
        
        # For 3D objects:
        # - Form closure: 7+ frictional contacts or 12+ frictionless contacts
        # - Force closure: ability to resist arbitrary wrenches
        if n_contacts >= 7 and friction_coeff > 0:
            return "Form closure grasp"
        elif n_contacts >= 12:
            return "Frictionless form closure"
        else:
            # Check for force closure (simplified)
            # In practice, this involves checking if origin is in convex hull of wrenches
            return "Force closure grasp (potential)"

# Example: Classify different grasp types
classifier = GraspClassifier()

# Example 1: Two-finger pinch grasp
pinch_contacts = [[0.45, 0.3, 0.2], [0.55, 0.3, 0.2]]
pinch_normals = [[0, 0, 1], [0, 0, 1]]

print("Pinch Grasp Classification:")
print(f"  By fingers: {classifier.classify_by_fingers(pinch_contacts)}")
print(f"  By contact type: {classifier.classify_by_contact_type(pinch_contacts, pinch_normals)}")
print(f"  By wrench space: {classifier.classify_by_wrench_space(pinch_contacts, pinch_normals)}")

# Example 2: Tripod grasp
tripod_contacts = [[0.48, 0.28, 0.2], [0.52, 0.28, 0.2], [0.5, 0.32, 0.2]]
tripod_normals = [[0, 0, 1], [0, 0, 1], [0, 0, 1]]

print("\nTripod Grasp Classification:")
print(f"  By fingers: {classifier.classify_by_fingers(tripod_contacts)}")
print(f"  By contact type: {classifier.classify_by_contact_type(tripod_contacts, tripod_normals)}")
print(f"  By wrench space: {classifier.classify_by_wrench_space(tripod_contacts, tripod_normals)}")
```

### Power vs. Precision Grasps

Different grasp types serve different purposes:

```python
class GraspPurposeClassifier:
    def __init__(self):
        """
        Classify grasps by their intended purpose
        """
        pass
    
    def classify_precision_vs_power(self, grasp_params):
        """
        Classify grasp as precision or power based on parameters
        
        Args:
            grasp_params: Dictionary with grasp parameters
            
        Returns:
            'precision' or 'power' classification
        """
        # Parameters that indicate precision grasp:
        # - Small grasp aperture
        # - Low grip force
        # - Tip contact
        # - Fine manipulation needed
        
        aperture = grasp_params.get('aperture', 0.1)
        grip_force = grasp_params.get('grip_force', 10)
        contact_area = grasp_params.get('contact_area', 0.001)
        task_type = grasp_params.get('task_type', 'unknown')
        
        # Calculate precision indicators
        precision_score = 0
        precision_score += (0.05 / (aperture + 0.001))  # Smaller aperture = more precision
        precision_score += (5 / (grip_force + 1))       # Lower force = more precision
        precision_score += (0.0005 / (contact_area + 0.0001))  # Smaller contact = more precision
        
        if task_type in ['writing', 'assembly', 'delicate_handling']:
            precision_score += 2  # Task requires precision
        
        # Calculate power indicators
        power_score = 0
        power_score += aperture  # Larger aperture = more power
        power_score += grip_force / 10  # Higher force = more power
        power_score += contact_area * 1000  # Larger contact = more power
        
        if task_type in ['lifting', 'carrying', 'heavy_object']:
            power_score += 2  # Task requires power
        
        if precision_score > power_score:
            return 'precision', precision_score / (precision_score + power_score)
        else:
            return 'power', power_score / (precision_score + power_score)

# Example: Classify grasp purpose
grasp_classifier = GraspPurposeClassifier()

# Precision grasp example
precise_grasp = {
    'aperture': 0.02,  # 2cm aperture
    'grip_force': 2,   # Low force
    'contact_area': 0.0001,  # Small contact area
    'task_type': 'assembly'
}

grasp_type, confidence = grasp_classifier.classify_precision_vs_power(precise_grasp)
print(f"\nPrecision grasp example: {grasp_type} (confidence: {confidence:.2f})")

# Power grasp example
power_grasp = {
    'aperture': 0.08,  # 8cm aperture
    'grip_force': 50,  # High force
    'contact_area': 0.005,  # Large contact area
    'task_type': 'lifting'
}

grasp_type, confidence = grasp_classifier.classify_precision_vs_power(power_grasp)
print(f"Power grasp example: {grasp_type} (confidence: {confidence:.2f})")
```

## Geometric Grasp Planning

### Analytic Grasp Planning

Geometric approaches to grasp planning based on object shape:

```python
from scipy.spatial import ConvexHull, distance_matrix
import trimesh

class GeometricGraspPlanner:
    def __init__(self, gripper_width_range=(0.01, 0.15)):
        """
        Plan grasps based on geometric properties of objects
        
        Args:
            gripper_width_range: Min/max gripper width [min, max] in meters
        """
        self.min_width, self.max_width = gripper_width_range
    
    def find_parallel_grasps(self, object_mesh, num_grasps=10):
        """
        Find parallel jaw grasps for an object
        
        Args:
            object_mesh: Trimesh object representing the object
            num_grasps: Number of grasps to generate
            
        Returns:
            List of potential parallel jaw grasps
        """
        grasps = []
        
        # Get vertices and faces of the mesh
        vertices = object_mesh.vertices
        faces = object_mesh.faces
        
        # Sample points on the surface
        surface_points = self.sample_surface_points(object_mesh, num_samples=1000)
        
        # Find pairs of points that could form parallel jaw grasps
        for i in range(len(surface_points)):
            for j in range(i+1, len(surface_points)):
                p1 = surface_points[i]
                p2 = surface_points[j]
                
                # Calculate distance between points
                dist = np.linalg.norm(p1 - p2)
                
                # Check if distance is within gripper range
                if self.min_width <= dist <= self.max_width:
                    # Calculate midpoint (grasp center)
                    grasp_center = (p1 + p2) / 2
                    
                    # Calculate grasp orientation (perpendicular to line connecting points)
                    grasp_axis = (p2 - p1) / dist  # Normalized vector from p1 to p2
                    
                    # Find a perpendicular vector for the approach direction
                    # Use the cross product with a reference vector
                    if abs(grasp_axis[2]) < 0.9:  # Not too close to vertical
                        approach_dir = np.cross(grasp_axis, [0, 0, 1])
                    else:  # Use x-axis if grasp axis is nearly vertical
                        approach_dir = np.cross(grasp_axis, [1, 0, 0])
                    
                    approach_dir = approach_dir / np.linalg.norm(approach_dir)
                    
                    # Create rotation matrix
                    # Z-axis: approach direction, Y-axis: grasp axis, X-axis: cross product
                    z_axis = approach_dir
                    y_axis = grasp_axis
                    x_axis = np.cross(y_axis, z_axis)
                    x_axis = x_axis / np.linalg.norm(x_axis)
                    y_axis = np.cross(z_axis, x_axis)  # Recalculate to ensure orthogonality
                    
                    orientation = np.column_stack([x_axis, y_axis, z_axis])
                    
                    # Create grasp
                    grasp = {
                        'position': grasp_center,
                        'orientation': orientation,
                        'contact_points': [p1, p2],
                        'grasp_type': 'parallel',
                        'quality': self.estimate_grasp_quality([p1, p2], orientation)
                    }
                    
                    grasps.append(grasp)
        
        # Sort grasps by quality and return top ones
        grasps.sort(key=lambda x: x['quality'], reverse=True)
        return grasps[:num_grasps]
    
    def sample_surface_points(self, mesh, num_samples=1000):
        """
        Sample points uniformly on the surface of a mesh
        """
        # Use trimesh's built-in sampling
        if hasattr(mesh, 'sample'):
            return mesh.sample(num_samples)
        else:
            # Fallback: sample face centers weighted by area
            areas = mesh.area_faces
            probabilities = areas / np.sum(areas)
            sampled_faces = np.random.choice(len(mesh.faces), size=num_samples, p=probabilities)
            
            points = []
            for face_idx in sampled_faces:
                face = mesh.faces[face_idx]
                v1, v2, v3 = mesh.vertices[face]
                # Sample random point in triangle
                r1, r2 = np.random.random(), np.random.random()
                sqrt_r1 = np.sqrt(r1)
                point = (1 - sqrt_r1) * v1 + sqrt_r1 * (1 - r2) * v2 + sqrt_r1 * r2 * v3
                points.append(point)
            
            return np.array(points)
    
    def estimate_grasp_quality(self, contact_points, orientation):
        """
        Estimate grasp quality based on geometric properties
        """
        if len(contact_points) < 2:
            return 0.0
        
        p1, p2 = contact_points[0], contact_points[1]
        grasp_axis = (p2 - p1) / np.linalg.norm(p2 - p1)
        
        # Quality factors:
        # 1. Distance between contacts (should be appropriate for object size)
        contact_distance = np.linalg.norm(p2 - p1)
        
        # 2. Orientation alignment with object principal axes (if known)
        # For now, we'll use a simple heuristic
        
        # 3. Surface normal alignment
        # This would require surface normal information
        
        # Combine factors into quality score
        # Normalize distance to be between 0 and 1
        distance_quality = min(1.0, contact_distance / 0.1)  # 0.1m as reference
        
        # Return combined quality score
        return distance_quality

# Example: Plan grasps for a simple object
# Create a simple box mesh for demonstration
box_mesh = trimesh.creation.box(extents=[0.08, 0.06, 0.04])
box_mesh.apply_translation([0.5, 0.3, 0.2])  # Move to a position

planner = GeometricGraspPlanner(gripper_width_range=(0.02, 0.12))
candidate_grasps = planner.find_parallel_grasps(box_mesh, num_grasps=5)

print(f"\nFound {len(candidate_grasps)} candidate grasps for the box:")
for i, grasp in enumerate(candidate_grasps):
    print(f"Grasp {i+1}:")
    print(f"  Position: [{grasp['position'][0]:.3f}, {grasp['position'][1]:.3f}, {grasp['position'][2]:.3f}]")
    print(f"  Contact distance: {np.linalg.norm(grasp['contact_points'][0] - grasp['contact_points'][1]):.3f}m")
    print(f"  Quality: {grasp['quality']:.3f}")
```

### Antipodal Grasp Planning

Finding grasps where contact points oppose each other:

```python
class AntipodalGraspPlanner:
    def __init__(self, min_normal_alignment=0.8, min_contact_distance=0.01, max_contact_distance=0.15):
        """
        Plan antipodal grasps where contact normals oppose each other
        
        Args:
            min_normal_alignment: Minimum dot product for antipodal condition (negative)
            min_contact_distance: Minimum distance between contact points
            max_contact_distance: Maximum distance between contact points
        """
        self.min_normal_alignment = min_normal_alignment
        self.min_distance = min_contact_distance
        self.max_distance = max_contact_distance
    
    def find_antipodal_grasps(self, object_mesh, num_grasps=10):
        """
        Find antipodal grasps for an object
        
        Args:
            object_mesh: Trimesh object representing the object
            num_grasps: Number of grasps to generate
            
        Returns:
            List of antipodal grasps
        """
        grasps = []
        
        # Sample points on the surface with normals
        surface_points = self.sample_surface_with_normals(object_mesh, num_samples=2000)
        
        # Extract points and normals
        points = np.array([p[0] for p in surface_points])
        normals = np.array([p[1] for p in surface_points])
        
        # Find pairs of points with opposing normals
        for i in range(len(points)):
            for j in range(i+1, len(points)):
                p1, n1 = points[i], normals[i]
                p2, n2 = points[j], normals[j]
                
                # Check if normals are roughly opposite (antipodal condition)
                dot_product = np.dot(n1, n2)
                
                # For antipodal grasp, normals should be roughly opposite
                if dot_product < self.min_normal_alignment:
                    # Check if distance is within graspable range
                    distance = np.linalg.norm(p1 - p2)
                    
                    if self.min_distance <= distance <= self.max_distance:
                        # Calculate grasp center and orientation
                        grasp_center = (p1 + p2) / 2
                        
                        # Grasp orientation: perpendicular to the line connecting contacts
                        grasp_axis = (p2 - p1) / distance  # Normalized vector from p1 to p2
                        
                        # Find a perpendicular vector for the approach direction
                        if abs(grasp_axis[2]) < 0.9:  # Not too close to vertical
                            approach_dir = np.cross(grasp_axis, [0, 0, 1])
                        else:  # Use x-axis if grasp axis is nearly vertical
                            approach_dir = np.cross(grasp_axis, [1, 0, 0])
                        
                        approach_dir = approach_dir / np.linalg.norm(approach_dir)
                        
                        # Create rotation matrix
                        z_axis = approach_dir
                        y_axis = grasp_axis
                        x_axis = np.cross(y_axis, z_axis)
                        x_axis = x_axis / np.linalg.norm(x_axis)
                        y_axis = np.cross(z_axis, x_axis)  # Recalculate to ensure orthogonality
                        
                        orientation = np.column_stack([x_axis, y_axis, z_axis])
                        
                        # Calculate grasp quality based on antipodality
                        quality = 1.0 - abs(dot_product)  # Higher quality for more opposite normals
                        
                        # Create grasp
                        grasp = {
                            'position': grasp_center,
                            'orientation': orientation,
                            'contact_points': [p1, p2],
                            'normals': [n1, n2],
                            'grasp_type': 'antipodal',
                            'quality': quality
                        }
                        
                        grasps.append(grasp)
        
        # Sort grasps by quality and return top ones
        grasps.sort(key=lambda x: x['quality'], reverse=True)
        return grasps[:num_grasps]
    
    def sample_surface_with_normals(self, mesh, num_samples=1000):
        """
        Sample points on the surface with their normals
        """
        # Sample points
        points = mesh.sample(num_samples)
        
        # Calculate closest points on mesh to get face indices
        closest_points, distances, face_indices = mesh.nearest.on_surface(points)
        
        # Get face normals for the sampled points
        face_normals = mesh.face_normals[face_indices]
        
        # Return points with their corresponding normals
        return [(points[i], face_normals[i]) for i in range(len(points))]

# Example: Find antipodal grasps
antipodal_planner = AntipodalGraspPlanner(min_normal_alignment=-0.8)
antipodal_grasps = antipodal_planner.find_antipodal_grasps(box_mesh, num_grasps=5)

print(f"\nFound {len(antipodal_grasps)} antipodal grasps for the box:")
for i, grasp in enumerate(antipodal_grasps):
    print(f"Antipodal Grasp {i+1}:")
    print(f"  Position: [{grasp['position'][0]:.3f}, {grasp['position'][1]:.3f}, {grasp['position'][2]:.3f}]")
    print(f"  Contact distance: {np.linalg.norm(grasp['contact_points'][0] - grasp['contact_points'][1]):.3f}m")
    print(f"  Normal alignment: {np.dot(grasp['normals'][0], grasp['normals'][1]):.3f}")
    print(f"  Quality: {grasp['quality']:.3f}")
```

## Physics-Based Grasp Planning

### Force Closure Analysis

Analyzing whether a grasp can resist arbitrary forces and torques:

```python
from scipy.spatial import ConvexHull
import numpy as np

class ForceClosureAnalyzer:
    def __init__(self, friction_coeff=0.7):
        """
        Analyze force closure properties of grasps
        
        Args:
            friction_coeff: Coefficient of friction at contact points
        """
        self.friction_coeff = friction_coeff
    
    def check_force_closure_2d(self, contact_points, normals):
        """
        Check force closure for 2D case (simplified)
        
        Args:
            contact_points: List of 2D contact points
            normals: List of 2D surface normals at contact points
            
        Returns:
            Boolean indicating if force closure is achieved
        """
        n_contacts = len(contact_points)
        
        if n_contacts < 4:
            return False  # Need at least 4 contacts for 2D force closure with friction
        
        # For 2D with friction, we need to check if the origin is inside
        # the convex hull of the friction cones
        # This is a simplified check - in practice, this requires more complex computation
        
        # Calculate friction cone boundaries for each contact
        friction_cone_edges = []
        
        for i in range(n_contacts):
            point = np.array(contact_points[i])
            normal = np.array(normals[i]) / np.linalg.norm(normals[i])  # Normalize
            
            # Tangent vector (rotated normal by 90 degrees)
            tangent = np.array([-normal[1], normal[0]])
            
            # Friction cone edges
            edge1 = normal + self.friction_coeff * tangent
            edge2 = normal - self.friction_coeff * tangent
            
            friction_cone_edges.extend([edge1, edge2])
        
        # Check if origin is inside convex hull of friction cone edges
        # This is a simplified check - in practice, wrench space analysis is needed
        if len(friction_cone_edges) >= 3:
            # Create points around origin to check if it's enclosed
            hull = ConvexHull([edge[:2] for edge in friction_cone_edges])
            # This is a simplified check - proper implementation would use LP or other methods
            return True  # Placeholder - proper implementation needed
        
        return False
    
    def check_force_closure_3d(self, contact_points, normals):
        """
        Check force closure for 3D case (simplified)
        
        Args:
            contact_points: List of 3D contact points
            normals: List of 3D surface normals at contact points
            
        Returns:
            Boolean indicating if force closure is achieved
        """
        n_contacts = len(contact_points)
        
        # For 3D with friction, we need at least 7 contacts for force closure
        if n_contacts < 7:
            return False
        
        # Construct the grasp matrix G
        # Each contact contributes 6 rows (3 for forces, 3 for torques)
        G = []
        
        for i in range(n_contacts):
            point = np.array(contact_points[i])
            normal = np.array(normals[i]) / np.linalg.norm(normals[i])  # Normalize
            
            # Tangent vectors (two orthogonal to normal)
            if abs(normal[2]) < 0.9:
                t1 = np.cross(normal, [0, 0, 1])
            else:
                t1 = np.cross(normal, [1, 0, 0])
            t1 = t1 / np.linalg.norm(t1)
            t2 = np.cross(normal, t1)
            t2 = t2 / np.linalg.norm(t2)
            
            # Friction pyramid approximation (4 edges per contact)
            friction_edges = [
                normal + self.friction_coeff * t1,
                normal - self.friction_coeff * t1,
                normal + self.friction_coeff * t2,
                normal - self.friction_coeff * t2
            ]
            
            # For each friction edge, create a row in the grasp matrix
            for edge in friction_edges:
                # Force components
                G.append(list(edge) + [0, 0, 0])  # Force
                
                # Torque components (torque = r × force)
                torque = np.cross(point, edge)
                G.append([0, 0, 0] + list(torque))  # Torque
        
        G = np.array(G)
        
        # Check force closure: origin should be in interior of convex hull
        # This is equivalent to checking if the grasp can resist arbitrary wrenches
        # Proper implementation would use linear programming
        # For now, we'll use a simplified check based on rank
        
        # The grasp has force closure if the grasp matrix has full row rank (6 for 3D)
        rank = np.linalg.matrix_rank(G)
        return rank >= 6
    
    def calculate_grasp_matrix(self, contact_points, normals, object_com=None):
        """
        Calculate the grasp matrix for a given grasp configuration
        
        Args:
            contact_points: List of contact point positions
            normals: List of surface normals at contact points
            object_com: Center of mass of the object (optional)
            
        Returns:
            Grasp matrix G
        """
        if object_com is None:
            object_com = np.mean(contact_points, axis=0)  # Use centroid as COM approximation
        
        n_contacts = len(contact_points)
        G = np.zeros((6, 3*n_contacts))  # 6x3n grasp matrix
        
        for i in range(n_contacts):
            # Position of contact relative to object COM
            r = np.array(contact_points[i]) - np.array(object_com)
            
            # Normal direction (approach direction for grasp)
            n = np.array(normals[i]) / np.linalg.norm(normals[i])
            
            # Insert contact normal into force part of grasp matrix
            G[0:3, 3*i:3*i+3] = np.eye(3)  # Forces
            
            # Calculate torque contribution: torque = r × force
            # Torque part of grasp matrix
            G[3:6, 3*i:3*i+3] = np.array([
                [0, -r[2], r[1]],
                [r[2], 0, -r[0]],
                [-r[1], r[0], 0]
            ])
        
        return G

# Example: Analyze force closure
analyzer = ForceClosureAnalyzer(friction_coeff=0.6)

# Test with the antipodal grasps found earlier
for i, grasp in enumerate(antipodal_grasps[:3]):  # Test first 3 grasps
    contacts = grasp['contact_points']
    normals = grasp['normals']
    
    # For 3D force closure check
    has_force_closure = analyzer.check_force_closure_3d(contacts, normals)
    
    print(f"\nGrasp {i+1} Force Closure Analysis:")
    print(f"  Contact points: {len(contacts)}")
    print(f"  Has force closure: {has_force_closure}")
    
    # Calculate grasp matrix
    G = analyzer.calculate_grasp_matrix(contacts, normals)
    print(f"  Grasp matrix shape: {G.shape}")
    print(f"  Matrix rank: {np.linalg.matrix_rank(G)}")
```

### Grasp Quality Metrics

Quantifying the quality of potential grasps:

```python
class GraspQualityEvaluator:
    def __init__(self, friction_coeff=0.7):
        """
        Evaluate the quality of robotic grasps using multiple metrics
        
        Args:
            friction_coeff: Coefficient of friction at contact points
        """
        self.friction_coeff = friction_coeff
        self.analyzer = ForceClosureAnalyzer(friction_coeff=friction_coeff)
    
    def epsilon_quality(self, grasp_matrix, force_limit=20.0):
        """
        Calculate epsilon quality metric (smallest singular value of grasp matrix)
        
        Args:
            grasp_matrix: 6x3n grasp matrix
            force_limit: Maximum force that can be applied at each contact
            
        Returns:
            Epsilon quality metric
        """
        # Calculate singular values of the grasp matrix
        singular_vals = np.linalg.svd(grasp_matrix, compute_uv=False)
        
        # Epsilon is the smallest singular value
        epsilon = min(singular_vals)
        
        return epsilon
    
    def volume_quality(self, grasp_matrix):
        """
        Calculate volume quality metric (product of singular values)
        
        Args:
            grasp_matrix: 6x3n grasp matrix
            
        Returns:
            Volume quality metric
        """
        singular_vals = np.linalg.svd(grasp_matrix, compute_uv=False)
        
        # Volume is the product of all singular values
        volume = np.prod(singular_vals)
        
        return volume
    
    def min_distance_quality(self, contact_points):
        """
        Calculate quality based on minimum distance between contacts
        
        Args:
            contact_points: List of contact point positions
            
        Returns:
            Minimum distance quality
        """
        if len(contact_points) < 2:
            return 0.0
        
        min_dist = float('inf')
        for i in range(len(contact_points)):
            for j in range(i+1, len(contact_points)):
                dist = np.linalg.norm(
                    np.array(contact_points[i]) - np.array(contact_points[j])
                )
                min_dist = min(min_dist, dist)
        
        # Normalize to [0,1] range
        # Assuming max possible distance is 0.3m (adjust as needed)
        max_expected_dist = 0.3
        quality = min(1.0, min_dist / max_expected_dist)
        
        return quality
    
    def grasp_width_quality(self, contact_points, optimal_width=0.05):
        """
        Calculate quality based on grasp width
        
        Args:
            contact_points: List of contact point positions
            optimal_width: Optimal grasp width for the object
            
        Returns:
            Grasp width quality
        """
        if len(contact_points) < 2:
            return 0.0
        
        # Calculate actual grasp width
        width = np.linalg.norm(
            np.array(contact_points[0]) - np.array(contact_points[1])
        )
        
        # Quality decreases as we move away from optimal width
        # Use Gaussian-like function centered at optimal width
        deviation = abs(width - optimal_width) / optimal_width
        quality = np.exp(-2 * deviation**2)  # Gaussian falloff
        
        return quality
    
    def normal_alignment_quality(self, normals):
        """
        Calculate quality based on normal alignment (for antipodal grasps)
        
        Args:
            normals: List of surface normals at contact points
            
        Returns:
            Normal alignment quality
        """
        if len(normals) < 2:
            return 0.0
        
        # For antipodal grasps, normals should be opposite
        n1 = np.array(normals[0]) / np.linalg.norm(normals[0])
        n2 = np.array(normals[1]) / np.linalg.norm(normals[1])
        
        # Dot product of opposing normals should be -1
        dot_product = np.dot(n1, n2)
        
        # Quality is higher when normals are more opposite
        # Range [-1, 1] mapped to [0, 1]
        quality = (1 + dot_product) / 2
        
        return quality
    
    def evaluate_grasp(self, grasp_config, object_properties=None):
        """
        Evaluate a grasp using multiple quality metrics
        
        Args:
            grasp_config: Dictionary with grasp configuration
            object_properties: Dictionary with object properties (optional)
            
        Returns:
            Dictionary with quality metrics
        """
        contact_points = grasp_config['contact_points']
        normals = grasp_config.get('normals', [])
        
        # Calculate grasp matrix
        G = self.analyzer.calculate_grasp_matrix(contact_points, normals)
        
        # Calculate various quality metrics
        qualities = {}
        
        # Epsilon quality
        qualities['epsilon'] = self.epsilon_quality(G)
        
        # Volume quality
        qualities['volume'] = self.volume_quality(G)
        
        # Minimum distance quality
        qualities['min_distance'] = self.min_distance_quality(contact_points)
        
        # Grasp width quality
        optimal_width = object_properties.get('size', 0.05) if object_properties else 0.05
        qualities['width'] = self.grasp_width_quality(contact_points, optimal_width)
        
        # Normal alignment quality (if normals are provided)
        if len(normals) >= 2:
            qualities['normal_alignment'] = self.normal_alignment_quality(normals)
        
        # Combined quality score (weighted average)
        weights = {
            'epsilon': 0.2,
            'volume': 0.2,
            'min_distance': 0.15,
            'width': 0.15,
            'normal_alignment': 0.3 if 'normal_alignment' in qualities else 0.0
        }
        
        total_weight = sum(weights.values())
        combined_quality = sum(
            qualities.get(metric, 0) * weight 
            for metric, weight in weights.items()
        ) / total_weight if total_weight > 0 else 0
        
        qualities['combined'] = combined_quality
        
        return qualities

# Example: Evaluate grasp qualities
evaluator = GraspQualityEvaluator(friction_coeff=0.6)

print("\nGrasp Quality Evaluation:")
for i, grasp in enumerate(antipodal_grasps[:3]):  # Evaluate first 3 grasps
    qualities = evaluator.evaluate_grasp(grasp, {'size': 0.08})
    
    print(f"\nGrasp {i+1} Qualities:")
    for metric, value in qualities.items():
        print(f"  {metric}: {value:.3f}")
```

## Grasp Execution and Force Control

### Grasp Execution Pipeline

Implementing a complete grasp execution pipeline:

```python
class GraspExecutionPipeline:
    def __init__(self, robot_interface, grasp_planner, quality_evaluator):
        """
        Complete pipeline for grasp planning and execution
        
        Args:
            robot_interface: Interface to control the robot
            grasp_planner: Grasp planning component
            quality_evaluator: Grasp quality evaluation component
        """
        self.robot = robot_interface
        self.planner = grasp_planner
        self.evaluator = quality_evaluator
        
        # Execution parameters
        self.approach_distance = 0.1  # 10cm approach distance
        self.lift_distance = 0.05     # 5cm lift after grasp
        self.max_grasp_force = 30     # Maximum grasp force in Newtons
        self.slip_detection_threshold = 0.1  # Threshold for slip detection
    
    def plan_grasp(self, object_mesh, object_properties=None):
        """
        Plan a grasp for an object
        
        Args:
            object_mesh: Mesh representation of the object
            object_properties: Dictionary with object properties
            
        Returns:
            Best grasp configuration
        """
        # Generate candidate grasps
        candidate_grasps = self.planner.find_antipodal_grasps(object_mesh, num_grasps=10)
        
        if not candidate_grasps:
            return None
        
        # Evaluate each grasp
        evaluated_grasps = []
        for grasp in candidate_grasps:
            quality_metrics = self.evaluator.evaluate_grasp(grasp, object_properties)
            evaluated_grasps.append((grasp, quality_metrics['combined']))
        
        # Sort by quality and return the best
        evaluated_grasps.sort(key=lambda x: x[1], reverse=True)
        
        return evaluated_grasps[0][0]  # Return the best grasp configuration
    
    def execute_approach(self, grasp_pose):
        """
        Execute approach motion to the grasp position
        
        Args:
            grasp_pose: Pose to approach [x, y, z, qx, qy, qz, qw]
        """
        # Calculate approach pose (above the grasp position)
        approach_pos = np.array(grasp_pose[:3])
        grasp_orientation = grasp_pose[3:]  # Quaternion
        
        # Move up along the approach direction (z-axis of grasp frame)
        approach_direction = self.get_approach_direction(grasp_orientation)
        approach_pos = approach_pos + approach_direction * self.approach_distance
        
        approach_pose = np.concatenate([approach_pos, grasp_orientation])
        
        # Move to approach position
        self.robot.move_to_pose(approach_pose)
        
        print(f"Approached to position: {approach_pos}")
    
    def execute_grasp(self, grasp_pose, grasp_force=None):
        """
        Execute the grasp at the specified pose
        
        Args:
            grasp_pose: Grasp pose [x, y, z, qx, qy, qz, qw]
            grasp_force: Force to apply (if None, use default)
        """
        if grasp_force is None:
            grasp_force = min(self.max_grasp_force, 10)  # Default force
        
        # Move to grasp position
        self.robot.move_to_pose(grasp_pose)
        
        # Close the gripper with specified force
        self.robot.close_gripper(force=grasp_force)
        
        print(f"Grasp executed at {grasp_pose[:3]} with force {grasp_force}N")
    
    def execute_lift(self, grasp_pose):
        """
        Execute lift motion after successful grasp
        
        Args:
            grasp_pose: Original grasp pose [x, y, z, qx, qy, qz, qw]
        """
        # Calculate lift pose (above the grasp position)
        lift_pos = np.array(grasp_pose[:3])
        grasp_orientation = grasp_pose[3:]  # Quaternion
        
        # Move up along the approach direction (z-axis of grasp frame)
        approach_direction = self.get_approach_direction(grasp_orientation)
        lift_pos = lift_pos + approach_direction * self.lift_distance
        
        lift_pose = np.concatenate([lift_pos, grasp_orientation])
        
        # Move to lift position
        self.robot.move_to_pose(lift_pose)
        
        print(f"Lifted to position: {lift_pos}")
    
    def get_approach_direction(self, orientation_quat):
        """
        Get the approach direction from orientation quaternion
        
        Args:
            orientation_quat: Quaternion [qx, qy, qz, qw]
            
        Returns:
            Approach direction vector
        """
        # Convert quaternion to rotation matrix
        r = R.from_quat(orientation_quat)
        rot_matrix = r.as_matrix()
        
        # The approach direction is typically the z-axis of the gripper frame
        approach_dir = rot_matrix[:, 2]  # Third column is z-axis
        
        return approach_dir
    
    def execute_full_grasp(self, object_mesh, object_properties=None):
        """
        Execute the complete grasp pipeline
        
        Args:
            object_mesh: Mesh representation of the object
            object_properties: Dictionary with object properties
            
        Returns:
            Success status and execution log
        """
        execution_log = []
        
        # Step 1: Plan grasp
        execution_log.append("Planning grasp...")
        best_grasp = self.plan_grasp(object_mesh, object_properties)
        
        if best_grasp is None:
            execution_log.append("No valid grasp found")
            return False, execution_log
        
        # Convert grasp to pose format [x, y, z, qx, qy, qz, qw]
        grasp_pos = best_grasp['position']
        grasp_rot_matrix = best_grasp['orientation']
        grasp_quat = R.from_matrix(grasp_rot_matrix).as_quat()
        
        grasp_pose = np.concatenate([grasp_pos, grasp_quat])
        
        execution_log.append(f"Best grasp planned at {grasp_pos}")
        
        # Step 2: Approach the object
        execution_log.append("Executing approach motion...")
        self.execute_approach(grasp_pose)
        
        # Step 3: Execute grasp
        execution_log.append("Executing grasp...")
        self.execute_grasp(grasp_pose)
        
        # Step 4: Check grasp success (simplified)
        execution_log.append("Checking grasp success...")
        grasp_successful = self.check_grasp_success()
        
        if not grasp_successful:
            execution_log.append("Grasp failed - releasing object")
            self.robot.open_gripper()
            return False, execution_log
        
        # Step 5: Lift the object
        execution_log.append("Lifting object...")
        self.execute_lift(grasp_pose)
        
        execution_log.append("Grasp execution completed successfully")
        return True, execution_log
    
    def check_grasp_success(self):
        """
        Check if the grasp was successful (simplified implementation)
        
        Returns:
            Boolean indicating grasp success
        """
        # In practice, this would check:
        # - Gripper force/torque sensors
        # - Object pose estimation
        # - Slip detection algorithms
        # - Visual confirmation
        
        # For this example, we'll simulate success with 80% probability
        return np.random.random() < 0.8

# Mock robot interface for demonstration
class MockRobotInterface:
    def move_to_pose(self, pose):
        """Mock movement to pose"""
        print(f"Moving to pose: [{pose[0]:.3f}, {pose[1]:.3f}, {pose[2]:.3f}]")
    
    def close_gripper(self, force):
        """Mock gripper close"""
        print(f"Closing gripper with force: {force}N")
    
    def open_gripper(self):
        """Mock gripper open"""
        print("Opening gripper")

# Example: Execute grasp pipeline
mock_robot = MockRobotInterface()
grasp_planner = AntipodalGraspPlanner(min_normal_alignment=-0.8)
quality_evaluator = GraspQualityEvaluator(friction_coeff=0.6)

pipeline = GraspExecutionPipeline(mock_robot, grasp_planner, quality_evaluator)

# Execute grasp on the box mesh
success, log = pipeline.execute_full_grasp(box_mesh, {'size': 0.08, 'mass': 0.1})

print("\nGrasp Execution Log:")
for entry in log:
    print(f"  - {entry}")

print(f"\nGrasp execution successful: {success}")
```

## Adaptive Grasp Planning

### Learning-Based Grasp Adaptation

Using machine learning to improve grasp planning:

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np

class GraspFeatureExtractor:
    def __init__(self):
        """
        Extract features for grasp evaluation
        """
        pass
    
    def extract_features(self, grasp_config, object_properties):
        """
        Extract features for a grasp configuration
        
        Args:
            grasp_config: Grasp configuration dictionary
            object_properties: Object properties dictionary
            
        Returns:
            Feature vector for the grasp
        """
        features = []
        
        # Grasp position features
        pos = grasp_config['position']
        features.extend(pos)
        
        # Grasp orientation features (first column of rotation matrix)
        orient = grasp_config['orientation']
        features.extend(orient[:, 0])  # X-axis of gripper frame
        
        # Contact point features
        contacts = grasp_config['contact_points']
        if len(contacts) >= 2:
            # Distance between first two contacts
            dist = np.linalg.norm(np.array(contacts[0]) - np.array(contacts[1]))
            features.append(dist)
            
            # Individual contact positions (flatten)
            for contact in contacts[:2]:  # Use first 2 contacts
                features.extend(contact)
        else:
            # Pad with zeros if not enough contacts
            features.extend([0, 0, 0, 0, 0, 0, 0])  # dist + 2 contacts
        
        # Object properties
        obj_size = object_properties.get('size', 0.1)
        obj_mass = object_properties.get('mass', 0.1)
        features.extend([obj_size, obj_mass])
        
        # Fill up to fixed size with zeros
        while len(features) < 20:  # Fixed size for NN
            features.append(0.0)
        
        return features[:20]  # Ensure fixed size

class GraspSuccessNet(nn.Module):
    def __init__(self, input_size=20, hidden_sizes=[64, 32, 16]):
        """
        Neural network to predict grasp success
        
        Args:
            input_size: Size of input feature vector
            hidden_sizes: Sizes of hidden layers
        """
        super(GraspSuccessNet, self).__init__()
        
        layers = []
        prev_size = input_size
        
        for hidden_size in hidden_sizes:
            layers.append(nn.Linear(prev_size, hidden_size))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(0.2))
            prev_size = hidden_size
        
        # Output layer: probability of success (binary classification)
        layers.append(nn.Linear(prev_size, 2))  # Success/failure
        layers.append(nn.Softmax(dim=1))
        
        self.network = nn.Sequential(*layers)
    
    def forward(self, x):
        return self.network(x)

class LearningBasedGraspPlanner:
    def __init__(self, model_path=None):
        """
        Grasp planner using learned models
        
        Args:
            model_path: Path to pre-trained model (optional)
        """
        self.feature_extractor = GraspFeatureExtractor()
        self.net = GraspSuccessNet()
        
        if model_path:
            self.net.load_state_dict(torch.load(model_path))
        
        self.optimizer = optim.Adam(self.net.parameters(), lr=0.001)
        self.criterion = nn.CrossEntropyLoss()
    
    def predict_success_probability(self, grasp_config, object_properties):
        """
        Predict the probability of grasp success
        
        Args:
            grasp_config: Grasp configuration
            object_properties: Object properties
            
        Returns:
            Probability of success [0, 1]
        """
        # Extract features
        features = self.feature_extractor.extract_features(grasp_config, object_properties)
        features_tensor = torch.FloatTensor(features).unsqueeze(0)
        
        # Get prediction
        self.net.eval()
        with torch.no_grad():
            output = self.net(features_tensor)
            # Probability of success class (index 1)
            success_prob = output[0, 1].item()
        
        return success_prob
    
    def plan_grasps_with_learning(self, object_mesh, object_properties, num_candidates=10):
        """
        Plan grasps using learning-based evaluation
        
        Args:
            object_mesh: Object mesh
            object_properties: Object properties
            num_candidates: Number of candidate grasps to consider
            
        Returns:
            Ranked list of grasps with success probabilities
        """
        # Generate candidate grasps using geometric planner
        geom_planner = AntipodalGraspPlanner(min_normal_alignment=-0.7)
        candidates = geom_planner.find_antipodal_grasps(object_mesh, num_grasps=num_candidates)
        
        # Evaluate each grasp using the learned model
        evaluated_grasps = []
        for grasp in candidates:
            prob = self.predict_success_probability(grasp, object_properties)
            evaluated_grasps.append((grasp, prob))
        
        # Sort by success probability
        evaluated_grasps.sort(key=lambda x: x[1], reverse=True)
        
        return evaluated_grasps
    
    def train(self, training_data, epochs=100):
        """
        Train the grasp success prediction model
        
        Args:
            training_data: List of (grasp_features, label) tuples
                          label: 0 for failure, 1 for success
            epochs: Number of training epochs
        """
        # Create dataset
        class GraspDataset(Dataset):
            def __init__(self, data):
                self.features = torch.FloatTensor([item[0] for item in data])
                self.labels = torch.LongTensor([item[1] for item in data])
            
            def __len__(self):
                return len(self.labels)
            
            def __getitem__(self, idx):
                return self.features[idx], self.labels[idx]
        
        dataset = GraspDataset(training_data)
        dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
        
        self.net.train()
        for epoch in range(epochs):
            total_loss = 0
            correct = 0
            total = 0
            
            for features, labels in dataloader:
                self.optimizer.zero_grad()
                outputs = self.net(features)
                loss = self.criterion(outputs, labels)
                loss.backward()
                self.optimizer.step()
                
                total_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
            
            accuracy = 100 * correct / total
            if epoch % 20 == 0:
                print(f'Epoch {epoch}, Loss: {total_loss/len(dataloader):.4f}, Accuracy: {accuracy:.2f}%')

# Example: Learning-based grasp planning
learning_planner = LearningBasedGraspPlanner()

# Simulate training data (in practice, this would come from real robot experiments)
print("\nSimulating training data collection...")
training_data = []
for _ in range(500):  # 500 training examples
    # Generate random grasp features
    features = np.random.rand(20).astype(np.float32)
    # Generate labels with some correlation to features
    # Higher values in first few features correlate with success
    success_likelihood = np.mean(features[:5])
    label = 1 if np.random.rand() < success_likelihood else 0
    training_data.append((features, label))

# Train the model
print("Training grasp success prediction model...")
learning_planner.train(training_data, epochs=100)

# Plan grasps using the learned model
print(f"\nPlanning grasps with learning-based evaluation:")
ranked_grasps = learning_planner.plan_grasps_with_learning(
    box_mesh, 
    {'size': 0.08, 'mass': 0.1}, 
    num_candidates=5
)

for i, (grasp, prob) in enumerate(ranked_grasps):
    print(f"Grasp {i+1}: Success probability = {prob:.3f}")
    print(f"  Position: [{grasp['position'][0]:.3f}, {grasp['position'][1]:.3f}, {grasp['position'][2]:.3f}]")
    print(f"  Contact distance: {np.linalg.norm(grasp['contact_points'][0] - grasp['contact_points'][1]):.3f}m")
```

## Best Practices for Grasp Planning

### 1. Grasp Planning Strategy
- Use multiple grasp planners and combine results
- Consider object properties (shape, weight, fragility)
- Plan for multiple grasp attempts
- Include grasp verification steps

### 2. Quality Evaluation
- Use multiple quality metrics for robust evaluation
- Consider task-specific requirements
- Account for robot hand limitations
- Include uncertainty in quality estimates

### 3. Execution Considerations
- Plan smooth approach and lift motions
- Use appropriate force control
- Implement slip detection and recovery
- Test extensively in simulation before real-world deployment

### 4. Learning and Adaptation
- Collect data from real grasp attempts
- Use machine learning to improve predictions
- Adapt to new object categories
- Continuously update models based on experience

## Looking Ahead

This lesson covered grasp planning and execution in robotic manipulation. The next lesson will focus on integrating manipulation with other robot capabilities, including navigation and task planning, to perform complex manipulation tasks in real-world environments.

## Exercises

1. Implement a grasp planner for a specific robot hand
2. Create a physics-based grasp quality evaluator
3. Develop a learning-based grasp success predictor
4. Design a complete grasp execution pipeline
5. Evaluate your grasp planner on various object shapes

## Further Reading

- "Robotic Grasping and Clustering Objects" by ten Pas and Platt
- "Deep Learning for Detecting Robotic Grasps" by Redmon and Angelova
- "A Taxonomy of Grasping and Manipulation" by Feix et al.
- "Learning Synergies for Robotic Grasping" by Monteiro et al.