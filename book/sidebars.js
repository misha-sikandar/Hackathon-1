/**
 * Creating an sidebar entry.
 * Consists of a sidebar item definition and the actual sidebar.
 */

/**
 * Creates a sidebar item definition.
 *
 * @typedef {Object} SidebarItemDoc
 * @property {'doc'} type - Item type
 * @property {string} id - Document ID
 */

/**
 * Creates a sidebar category definition.
 *
 * @typedef {Object} SidebarCategory
 * @property {'category'} type - Category type
 * @property {string} label - Category label
 * @property {Array<SidebarItemDoc|SidebarCategory>} items - Category items
 */

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
module.exports = {
  docsSidebar: [
    {
      type: 'doc',
      id: 'intro',
      label: 'Home'
    },
    {
      type: 'doc',
      id: 'syllabus',
      label: 'Course Syllabus'
    },
    {
      type: 'category',
      label: 'Week 1: Introduction to Physical AI',
      items: [
        {
          type: 'doc',
          id: 'week-01/index',
          label: 'Introduction to Physical AI'
        },
        {
          type: 'doc',
          id: 'week-01/exercises',
          label: 'Week 1 Exercises'
        }
      ]
    },
    {
      type: 'category',
      label: 'Week 2: ROS 2 Fundamentals',
      items: [
        {
          type: 'doc',
          id: 'week-02/ros2-fundamentals',
          label: 'ROS 2 Fundamentals'
        },
        {
          type: 'doc',
          id: 'week-02/exercises',
          label: 'Week 2 Exercises'
        }
      ]
    },
    {
      type: 'category',
      label: 'Week 3: URDF Modeling',
      items: [
        {
          type: 'doc',
          id: 'week-03/urdf-modeling',
          label: 'URDF Modeling'
        },
        {
          type: 'doc',
          id: 'week-03/exercises',
          label: 'Week 3 Exercises'
        }
      ]
    },
    {
      type: 'category',
      label: 'Week 4: Simulation with Gazebo & Unity',
      items: [
        {
          type: 'doc',
          id: 'week-04/gazebo-simulation',
          label: 'Gazebo Simulation'
        },
        {
          type: 'doc',
          id: 'week-04/unity-integration',
          label: 'Unity Integration'
        },
        {
          type: 'doc',
          id: 'week-04/exercises',
          label: 'Week 4 Exercises'
        }
      ]
    },
    {
      type: 'category',
      label: 'Week 5: NVIDIA Isaac',
      items: [
        {
          type: 'doc',
          id: 'week-05/isaac-sim-overview',
          label: 'Isaac Sim Overview'
        },
        {
          type: 'doc',
          id: 'week-05/perception-systems',
          label: 'Perception Systems'
        },
        {
          type: 'doc',
          id: 'week-05/exercises',
          label: 'Week 5 Exercises'
        }
      ]
    },
    {
      type: 'category',
      label: 'Week 6: SLAM & Navigation',
      items: [
        {
          type: 'doc',
          id: 'week-06/slam-navigation',
          label: 'SLAM & Navigation'
        },
        {
          type: 'doc',
          id: 'week-06/path-planning',
          label: 'Path Planning'
        },
        {
          type: 'doc',
          id: 'week-06/exercises',
          label: 'Week 6 Exercises'
        }
      ]
    },
    {
      type: 'category',
      label: 'Week 7: Vision-Language-Action',
      items: [
        {
          type: 'doc',
          id: 'week-07/vla-introduction',
          label: 'VLA Introduction'
        },
        {
          type: 'doc',
          id: 'week-07/multimodal-processing',
          label: 'Multimodal Processing'
        },
        {
          type: 'doc',
          id: 'week-07/exercises',
          label: 'Week 7 Exercises'
        }
      ]
    },
    {
      type: 'category',
      label: 'Week 8: Humanoid Locomotion',
      items: [
        {
          type: 'doc',
          id: 'week-08/humanoid-locomotion',
          label: 'Humanoid Locomotion'
        },
        {
          type: 'doc',
          id: 'week-08/balance-control',
          label: 'Balance Control'
        },
        {
          type: 'doc',
          id: 'week-08/exercises',
          label: 'Week 8 Exercises'
        }
      ]
    },
    {
      type: 'category',
      label: 'Week 9: Manipulation',
      items: [
        {
          type: 'doc',
          id: 'week-09/manipulation-basics',
          label: 'Manipulation Basics'
        },
        {
          type: 'doc',
          id: 'week-09/grasp-planning',
          label: 'Grasp Planning'
        },
        {
          type: 'doc',
          id: 'week-09/exercises',
          label: 'Week 9 Exercises'
        }
      ]
    },
    {
      type: 'category',
      label: 'Week 10: Conversational Robotics',
      items: [
        {
          type: 'doc',
          id: 'week-10/conversational-robots',
          label: 'Conversational Robots'
        },
        {
          type: 'doc',
          id: 'week-10/exercises',
          label: 'Week 10 Exercises'
        }
      ]
    },
    {
      type: 'category',
      label: 'Week 11: LLM-based Planning',
      items: [
        {
          type: 'doc',
          id: 'week-11/llm-cognitive-planning',
          label: 'LLM Cognitive Planning'
        },
        {
          type: 'doc',
          id: 'week-11/exercises',
          label: 'Week 11 Exercises'
        }
      ]
    },
    {
      type: 'category',
      label: 'Week 12: Sim-to-Real & Deployment',
      items: [
        {
          type: 'doc',
          id: 'week-12/sim-to-real-deployment',
          label: 'Sim-to-Real Deployment'
        },
        {
          type: 'doc',
          id: 'week-12/exercises',
          label: 'Week 12 Exercises'
        }
      ]
    },
    {
      type: 'category',
      label: 'Week 13: Capstone Project',
      items: [
        {
          type: 'doc',
          id: 'week-13/capstone-project',
          label: 'Capstone Project'
        },
        {
          type: 'doc',
          id: 'week-13/exercises',
          label: 'Week 13 Exercises'
        }
      ]
    },
    {
      type: 'category',
      label: 'Exercises & Examples',
      items: [
        {
          type: 'doc',
          id: 'exercises/weekly-exercises',
          label: 'All Weekly Exercises'
        },
        {
          type: 'doc',
          id: 'examples/README',
          label: 'Code Examples Overview'
        }
      ]
    }
  ],
};