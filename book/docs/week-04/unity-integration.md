---
sidebar_position: 12
---

# Unity Integration for Digital Twins in Physical AI

This lesson focuses on Unity as a platform for creating high-fidelity digital twins for Physical AI systems. Unity offers photorealistic rendering and advanced physics simulation capabilities that complement traditional robotics simulators like Gazebo.

## Learning Objectives

By the end of this lesson, you will be able to:

1. Set up Unity for robotics applications
2. Create photorealistic digital twins of robots
3. Implement sensor simulation in Unity
4. Establish communication between Unity and ROS
5. Generate synthetic training data using Unity
6. Apply Unity for sim-to-real transfer in Physical AI

## Unity for Robotics Overview

Unity has emerged as a powerful platform for robotics simulation, offering several advantages:

### Photorealistic Rendering
Unity's rendering pipeline produces high-fidelity visuals that are essential for training perception systems that need to generalize to real-world conditions.

### Flexible Physics Engine
Unity's physics engine supports complex interactions, deformable objects, and multi-body dynamics that can enhance simulation realism.

### Asset Creation Tools
Unity provides extensive tools for creating and importing 3D models, environments, and animations.

### XR Integration
Unity has strong support for virtual and augmented reality, which can be valuable for teleoperation and immersive development experiences.

## Setting Up Unity for Robotics

### Prerequisites

1. **Unity Hub**: Download and install Unity Hub
2. **Unity Editor**: Install the latest LTS version (2022.3.x recommended)
3. **Unity Robotics Hub**: Collection of tools and samples for robotics
4. **ROS Integration**: Either ROS.NET or Unity ROS TCP Connector

### Installing Unity Robotics Hub

The Unity Robotics Hub provides essential tools:

1. **Unity-Robotics-Helpers**: Utilities for ROS communication
2. **Unity-Robotics-Demo**: Sample projects demonstrating robotics workflows
3. **Perception Package**: Tools for synthetic data generation
4. **ML-Agents**: Framework for reinforcement learning

### Basic Unity ROS Communication

Unity can communicate with ROS through rosbridge:

```csharp
using UnityEngine;
using RosSharp.RosBridgeClient;

public class UnityRosConnector : MonoBehaviour
{
    [Header("Connection Settings")]
    public string rosBridgeServerUrl = "ws://localhost:9090";
    
    private RosSocket rosSocket;
    
    void Start()
    {
        // Initialize ROS connection
        ConnectToRos();
    }
    
    void ConnectToRos()
    {
        try
        {
            WebSocketNativeClient webSocket = new WebSocketNativeClient(rosBridgeServerUrl);
            rosSocket = new RosSocket(webSocket);
            
            Debug.Log("Connected to ROS bridge");
            
            // Subscribe to topics
            rosSocket.Subscribe<sensor_msgs.JointState>(
                "/joint_states", 
                OnJointStatesReceived);
                
            // Advertise publishers
            rosSocket.Advertise<sensor_msgs.JointState>("/unity_joint_states");
        }
        catch (System.Exception e)
        {
            Debug.LogError($"Failed to connect to ROS: {e.Message}");
        }
    }
    
    void OnJointStatesReceived(sensor_msgs.JointState jointState)
    {
        // Process joint state message
        for (int i = 0; i < jointState.name.Count; i++)
        {
            string jointName = jointState.name[i];
            float position = (float)jointState.position[i];
            
            // Update corresponding joint in Unity
            UpdateJoint(jointName, position);
        }
    }
    
    void UpdateJoint(string jointName, float position)
    {
        Transform jointTransform = transform.Find(jointName);
        if (jointTransform != null)
        {
            // Assuming a revolute joint rotating around Z-axis
            jointTransform.localRotation = Quaternion.Euler(0, 0, Mathf.Rad2Deg * position);
        }
    }
    
    void OnDestroy()
    {
        if (rosSocket != null)
        {
            rosSocket.Close();
        }
    }
}
```

## Creating Digital Twins in Unity

### Importing Robot Models

Unity supports various 3D model formats (FBX, OBJ, DAE). For best results with robotics:

1. **URDF to Unity Conversion**: Use tools like `urdf-importer` to convert URDF models
2. **Maintain Hierarchy**: Preserve joint relationships in the transform hierarchy
3. **Correct Scaling**: Ensure proper meter-to-Unity-unit conversion (1 Unity unit = 1 meter)

### Robot Model Setup

```csharp
using UnityEngine;

public class RobotController : MonoBehaviour
{
    [System.Serializable]
    public class JointConfig
    {
        public string jointName;
        public Transform jointTransform;
        public JointType jointType;
        public float minAngle;
        public float maxAngle;
        public float maxVelocity;
    }
    
    public enum JointType
    {
        Revolute,
        Prismatic,
        Fixed
    }
    
    [SerializeField] private JointConfig[] joints;
    [SerializeField] private ArticulationBody[] articulationBodies;
    
    void Start()
    {
        InitializeRobot();
    }
    
    void InitializeRobot()
    {
        // Set up joint constraints based on configuration
        foreach (var joint in joints)
        {
            if (joint.jointTransform.GetComponent<ArticulationBody>() != null)
            {
                ConfigureJoint(joint);
            }
        }
    }
    
    void ConfigureJoint(JointConfig config)
    {
        ArticulationBody body = config.jointTransform.GetComponent<ArticulationBody>();
        
        switch (config.jointType)
        {
            case JointType.Revolute:
                body.jointType = ArticulationJointType.RevoluteJoint;
                
                ArticulationDrive drive = body.linearXDrive;
                drive.lowerLimit = config.minAngle;
                drive.upperLimit = config.maxAngle;
                drive.maxForce = 1000;
                drive.damping = 10;
                
                body.linearXDrive = drive;
                break;
                
            case JointType.Prismatic:
                body.jointType = ArticulationJointType.PrismaticJoint;
                // Configure prismatic joint similarly
                break;
                
            case JointType.Fixed:
                body.jointType = ArticulationJointType.FixedJoint;
                break;
        }
    }
    
    public void SetJointPositions(float[] positions)
    {
        if (positions.Length != joints.Length)
        {
            Debug.LogError("Joint position array length mismatch");
            return;
        }
        
        for (int i = 0; i < joints.Length; i++)
        {
            if (joints[i].jointType == JointType.Revolute)
            {
                ArticulationBody body = joints[i].jointTransform.GetComponent<ArticulationBody>();
                ArticulationDrive drive = body.linearXDrive;
                drive.target = positions[i];
                body.linearXDrive = drive;
            }
        }
    }
}
```

## Sensor Simulation in Unity

### Camera Sensors

Unity's cameras can simulate various types of visual sensors:

```csharp
using UnityEngine;
using RosSharp.RosBridgeClient;
using Sensor_msgs = RosSharp.Messages.Sensor_msgs;

public class UnityCameraSensor : MonoBehaviour
{
    [Header("Camera Settings")]
    public Camera cameraComponent;
    public int imageWidth = 640;
    public int imageHeight = 480;
    public string sensorTopic = "/unity_camera/image_raw";
    
    [Header("ROS Connection")]
    public RosSocket rosSocket;
    
    private RenderTexture renderTexture;
    private Texture2D texture2D;
    private byte[] imageData;
    
    void Start()
    {
        InitializeCamera();
        InitializeRenderTexture();
    }
    
    void InitializeCamera()
    {
        cameraComponent.enabled = false; // Disable during initialization
        cameraComponent.aspect = (float)imageWidth / imageHeight;
        cameraComponent.orthographicSize = imageHeight / 2.0f;
    }
    
    void InitializeRenderTexture()
    {
        renderTexture = new RenderTexture(imageWidth, imageHeight, 24);
        texture2D = new Texture2D(imageWidth, imageHeight, TextureFormat.RGB24, false);
        imageData = new byte[imageWidth * imageHeight * 3];
    }
    
    void Update()
    {
        CaptureImage();
    }
    
    void CaptureImage()
    {
        // Set camera target texture
        cameraComponent.targetTexture = renderTexture;
        cameraComponent.Render();
        
        // Copy render texture to texture2D
        RenderTexture.active = renderTexture;
        texture2D.ReadPixels(new Rect(0, 0, imageWidth, imageHeight), 0, 0);
        texture2D.Apply();
        
        // Convert to ROS image format
        imageData = texture2D.GetRawTextureData();
        
        // Create and publish ROS image message
        if (rosSocket != null)
        {
            var imageMsg = CreateImageMessage(imageData);
            rosSocket.Publish(sensorTopic, imageMsg);
        }
        
        // Clean up
        cameraComponent.targetTexture = null;
        RenderTexture.active = null;
    }
    
    Sensor_msgs.Image CreateImageMessage(byte[] pixelData)
    {
        var imageMsg = new Sensor_msgs.Image();
        
        imageMsg.header = new RosSharp.Messages.Std_msgs.Header();
        imageMsg.header.frame_id = "unity_camera_optical_frame";
        imageMsg.header.stamp = new TimeStamp();
        
        imageMsg.height = (uint)imageHeight;
        imageMsg.width = (uint)imageWidth;
        imageMsg.encoding = "rgb8";
        imageMsg.is_bigendian = false;
        imageMsg.step = (uint)(imageWidth * 3); // 3 bytes per pixel (RGB)
        imageMsg.data = pixelData;
        
        return imageMsg;
    }
}
```

### LiDAR Simulation

Unity can simulate LiDAR sensors using raycasting:

```csharp
using UnityEngine;
using System.Collections.Generic;

public class UnityLidarSensor : MonoBehaviour
{
    [Header("LiDAR Settings")]
    public int horizontalResolution = 360;
    public int verticalResolution = 1;
    public float minAngle = -Mathf.PI;
    public float maxAngle = Mathf.PI;
    public float maxRange = 10.0f;
    public float updateRate = 10.0f; // Hz
    
    [Header("Raycast Settings")]
    public LayerMask detectionLayers = -1;
    public float rayThickness = 0.01f;
    
    private float updateInterval;
    private float lastUpdateTime;
    
    void Start()
    {
        updateInterval = 1.0f / updateRate;
        lastUpdateTime = -updateInterval; // Allow first update immediately
    }
    
    void Update()
    {
        if (Time.time - lastUpdateTime >= updateInterval)
        {
            SimulateLidarScan();
            lastUpdateTime = Time.time;
        }
    }
    
    void SimulateLidarScan()
    {
        List<float> ranges = new List<float>();
        
        float angleStep = (maxAngle - minAngle) / horizontalResolution;
        
        for (int i = 0; i < horizontalResolution; i++)
        {
            float angle = minAngle + i * angleStep;
            
            Vector3 direction = new Vector3(
                Mathf.Cos(angle),
                0,
                Mathf.Sin(angle)
            );
            
            RaycastHit hit;
            if (Physics.Raycast(transform.position, direction, out hit, maxRange, detectionLayers))
            {
                ranges.Add(hit.distance);
            }
            else
            {
                ranges.Add(maxRange); // No obstacle detected
            }
        }
        
        // Publish ranges to ROS or use for other purposes
        ProcessLidarData(ranges.ToArray());
    }
    
    void ProcessLidarData(float[] ranges)
    {
        // Convert ranges to ROS LiDAR message format
        // This would typically involve sending to ROS via rosbridge
        Debug.Log($"Lidar scan: {ranges.Length} points, min={Min(ranges)}, max={Max(ranges)}");
    }
    
    float Min(float[] arr)
    {
        float min = float.MaxValue;
        foreach (float val in arr)
        {
            if (val < min) min = val;
        }
        return min;
    }
    
    float Max(float[] arr)
    {
        float max = float.MinValue;
        foreach (float val in arr)
        {
            if (val > max) max = val;
        }
        return max;
    }
}
```

## Unity Perception Package

The Unity Perception package enables synthetic data generation for training AI models:

```csharp
using UnityEngine;
using Unity.Perception.GroundTruth;
using Unity.Perception.Randomization;
using System.Collections.Generic;

public class PerceptionSetup : MonoBehaviour
{
    [Header("Dataset Capture Settings")]
    public float captureInterval = 1.0f;
    public string datasetPath = "Assets/Datasets/";
    
    [Header("Annotation Settings")]
    public bool captureRgb = true;
    public bool captureDepth = true;
    public bool captureSegmentation = true;
    
    private DatasetCapture datasetCapture;
    private List<AnnotationDefinition> annotationDefinitions;
    
    void Start()
    {
        SetupPerceptionPipeline();
    }
    
    void SetupPerceptionPipeline()
    {
        // Add dataset capture component
        datasetCapture = GetComponent<Camera>().gameObject.AddComponent<DatasetCapture>();
        datasetCapture.capturePeriod = captureInterval;
        datasetCapture.datasetPath = datasetPath;
        
        // Configure annotation definitions
        annotationDefinitions = new List<AnnotationDefinition>();
        
        if (captureRgb)
        {
            var rgbDef = ScriptableObject.CreateInstance<AnnotationDefinition>();
            rgbDef.modality = Modality.Rgb;
            annotationDefinitions.Add(rgbDef);
        }
        
        if (captureDepth)
        {
            var depthDef = ScriptableObject.CreateInstance<AnnotationDefinition>();
            depthDef.modality = Modality.Depth;
            annotationDefinitions.Add(depthDef);
        }
        
        if (captureSegmentation)
        {
            var segDef = ScriptableObject.CreateInstance<AnnotationDefinition>();
            segDef.modality = Modality.InstanceSegmentation;
            annotationDefinitions.Add(segDef);
        }
        
        // Register annotation definitions
        var annotationManager = FindObjectOfType<AnnotationManager>();
        if (annotationManager != null)
        {
            annotationManager.annotationDefinitions.AddRange(annotationDefinitions);
        }
        
        // Add segmentation labelers to objects
        AddSegmentationLabelers();
    }
    
    void AddSegmentationLabelers()
    {
        // Find all objects that should be segmented
        var segmentableObjects = FindObjectsOfType<GameObject>();
        
        foreach (var obj in segmentableObjects)
        {
            // Add segmentation labeler if object should be segmented
            if (ShouldBeSegmented(obj))
            {
                var labeler = obj.AddComponent<SegmentationLabeler>();
                labeler.label = GetObjectLabel(obj);
            }
        }
    }
    
    bool ShouldBeSegmented(GameObject obj)
    {
        // Define criteria for which objects should be segmented
        // This could be based on tags, layers, or other properties
        return obj.CompareTag("Segmentable");
    }
    
    string GetObjectLabel(GameObject obj)
    {
        // Return a unique label for the object
        return obj.name;
    }
}
```

## Domain Randomization in Unity

Domain randomization helps improve sim-to-real transfer by varying environmental conditions:

```csharp
using UnityEngine;
using Unity.Perception.Randomization;
using Unity.Perception.Randomization.Parameters;
using Unity.Perception.Randomization.Samplers;

public class UnityDomainRandomizer : MonoBehaviour
{
    [Header("Lighting Randomization")]
    public Light mainLight;
    public ColorParameter lightColorParam;
    public FloatParameter lightIntensityParam;
    
    [Header("Material Randomization")]
    public GameObject[] randomizableObjects;
    public ColorParameter materialColorParam;
    public FloatParameter roughnessParam;
    
    [Header("Environment Randomization")]
    public GameObject[] environmentPrefabs;
    public FloatParameter objectPositionVariation;
    public FloatParameter objectRotationVariation;
    
    void Start()
    {
        // Initialize parameters if not set
        if (lightColorParam == null) lightColorParam = ScriptableObject.CreateInstance<ColorParameter>();
        if (lightIntensityParam == null) lightIntensityParam = ScriptableObject.CreateInstance<FloatParameter>();
        if (materialColorParam == null) materialColorParam = ScriptableObject.CreateInstance<ColorParameter>();
        if (roughnessParam == null) roughnessParam = ScriptableObject.CreateInstance<FloatParameter>();
        if (objectPositionVariation == null) objectPositionVariation = ScriptableObject.CreateInstance<FloatParameter>();
        if (objectRotationVariation == null) objectRotationVariation = ScriptableObject.CreateInstance<FloatParameter>();
        
        // Set default ranges
        lightIntensityParam.min = 0.5f;
        lightIntensityParam.max = 1.5f;
        
        roughnessParam.min = 0.1f;
        roughnessParam.max = 0.9f;
        
        objectPositionVariation.min = -0.5f;
        objectPositionVariation.max = 0.5f;
        
        objectRotationVariation.min = -15f;
        objectRotationVariation.max = 15f;
    }
    
    [ContextMenu("Randomize Scene")]
    public void RandomizeScene()
    {
        // Randomize lighting
        if (mainLight != null)
        {
            mainLight.color = lightColorParam.Sample();
            mainLight.intensity = lightIntensityParam.Sample();
        }
        
        // Randomize materials
        foreach (var obj in randomizableObjects)
        {
            var renderer = obj.GetComponent<Renderer>();
            if (renderer != null)
            {
                var material = renderer.material;
                material.color = materialColorParam.Sample();
                
                // Randomize roughness if using Standard shader
                if (material.HasProperty("_Metallic"))
                {
                    material.SetFloat("_Metallic", 0.0f); // Non-metallic
                }
                if (material.HasProperty("_Smoothness"))
                {
                    float roughness = roughnessParam.Sample();
                    material.SetFloat("_Smoothness", 1.0f - roughness);
                }
            }
        }
        
        // Randomize object positions and rotations
        foreach (var obj in randomizableObjects)
        {
            if (obj != transform.root.gameObject) // Don't move the root
            {
                Vector3 positionVariation = new Vector3(
                    objectPositionVariation.Sample(),
                    objectPositionVariation.Sample(),
                    objectPositionVariation.Sample()
                );
                
                Vector3 rotationVariation = new Vector3(
                    objectRotationVariation.Sample(),
                    objectRotationVariation.Sample(),
                    objectRotationVariation.Sample()
                );
                
                obj.transform.localPosition += positionVariation;
                obj.transform.localEulerAngles += rotationVariation;
            }
        }
    }
}
```

## Unity for Reinforcement Learning

Unity ML-Agents can be used for training control policies:

```csharp
using Unity.MLAgents;
using Unity.MLAgents.Sensors;
using Unity.MLAgents.Actuators;
using UnityEngine;

public class UnityRobotAgent : Agent
{
    [Header("Robot Configuration")]
    public RobotController robotController;
    public Transform target;
    public float movementSpeed = 1.0f;
    
    [Header("Reward Settings")]
    public float reachTargetReward = 10.0f;
    public float distancePenaltyFactor = -0.1f;
    public float timePenalty = -0.01f;
    
    private Vector3 initialPosition;
    
    public override void Initialize()
    {
        initialPosition = transform.position;
    }
    
    public override void OnEpisodeBegin()
    {
        // Reset robot position
        transform.position = initialPosition;
        transform.rotation = Quaternion.identity;
        
        // Randomize target position
        Vector3 randomTargetOffset = new Vector3(
            Random.Range(-5f, 5f),
            0,
            Random.Range(-5f, 5f)
        );
        target.position = initialPosition + randomTargetOffset;
    }
    
    public override void CollectObservations(VectorSensor sensor)
    {
        // Add robot position relative to origin
        sensor.AddObservation(transform.position - initialPosition);
        
        // Add target position relative to robot
        sensor.AddObservation(target.position - transform.position);
        
        // Add robot orientation
        sensor.AddObservation(transform.rotation.eulerAngles);
        
        // Add joint angles if available
        // sensor.AddObservation(robotController.GetCurrentJointPositions());
    }
    
    public override void OnActionReceived(ActionBuffers actions)
    {
        // Interpret actions and move robot
        float movementX = actions.ContinuousActions[0];
        float movementZ = actions.ContinuousActions[1];
        
        Vector3 movement = new Vector3(movementX, 0, movementZ) * movementSpeed * Time.deltaTime;
        transform.Translate(movement);
        
        // Calculate distance to target
        float distanceToTarget = Vector3.Distance(transform.position, target.position);
        
        // Give reward based on proximity to target
        SetReward(distanceToTarget * distancePenaltyFactor + timePenalty);
        
        // End episode if target reached
        if (distanceToTarget < 1.0f)
        {
            SetReward(reachTargetReward);
            EndEpisode();
        }
        
        // End episode if robot moves too far away
        if (Vector3.Distance(transform.position, initialPosition) > 20.0f)
        {
            EndEpisode();
        }
    }
    
    public override void Heuristic(in ActionBuffers actionsOut)
    {
        // For manual control during testing
        var continuousActionsOut = actionsOut.ContinuousActions;
        continuousActionsOut[0] = Input.GetAxis("Horizontal");
        continuousActionsOut[1] = Input.GetAxis("Vertical");
    }
}
```

## Best Practices for Unity in Physical AI

### 1. Performance Optimization

- Use occlusion culling for large environments
- Implement Level of Detail (LOD) for complex models
- Optimize materials and shaders for real-time performance
- Use object pooling for frequently instantiated objects

### 2. Fidelity Considerations

- Balance visual quality with performance requirements
- Validate sensor simulation against real hardware
- Account for Unity's rendering pipeline differences
- Consider temporal consistency in sensor data

### 3. Integration Strategies

- Use rosbridge for ROS communication
- Implement proper coordinate system conversions
- Handle timing differences between Unity and ROS
- Ensure deterministic behavior for reproducible experiments

### 4. Data Generation

- Implement diverse scenarios for robust training
- Use domain randomization to improve generalization
- Annotate data consistently with real-world equivalents
- Maintain synchronized timestamps across modalities

## Comparison: Unity vs Gazebo

| Aspect | Unity | Gazebo |
|--------|-------|--------|
| Visual Quality | Photorealistic | Good, but less detailed |
| Physics Accuracy | Good for most tasks | Highly accurate for robotics |
| Ease of Environment Creation | Very easy with tools | Requires SDF/XML knowledge |
| Sensor Simulation | Custom implementation needed | Built-in sensor models |
| Performance | High-quality rendering can be demanding | Optimized for robotics simulation |
| Community | Growing robotics community | Established robotics community |

## Looking Ahead

Unity provides powerful capabilities for creating high-fidelity digital twins that complement traditional robotics simulators. The combination of photorealistic rendering and flexible physics makes it ideal for training perception systems and generating synthetic datasets.

Next, we'll explore NVIDIA Isaac, which provides GPU-accelerated perception and manipulation capabilities that leverage the power of Unity and other simulation platforms for advanced Physical AI applications.

## Exercises

1. Create a Unity scene with a robot model and establish ROS communication
2. Implement a camera sensor simulation in Unity and visualize the output
3. Set up domain randomization for lighting and materials in your Unity scene
4. Use Unity's Perception package to generate synthetic training data
5. Implement a simple reinforcement learning task using Unity ML-Agents

## Further Reading

- Unity Robotics Hub: https://github.com/Unity-Technologies/Unity-Robotics-Hub
- Unity Perception Package: https://docs.unity3d.com/Packages/com.unity.perception@latest
- Unity ML-Agents: https://github.com/Unity-Technologies/ml-agents
- ROS Integration: https://github.com/Unity-Technologies/Unity-Robotics-Helpers