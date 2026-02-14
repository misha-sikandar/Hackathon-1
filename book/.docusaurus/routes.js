import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/__docusaurus/debug',
    component: ComponentCreator('/__docusaurus/debug', '5ff'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/config',
    component: ComponentCreator('/__docusaurus/debug/config', '5ba'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/content',
    component: ComponentCreator('/__docusaurus/debug/content', 'a2b'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/globalData',
    component: ComponentCreator('/__docusaurus/debug/globalData', 'c3c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/metadata',
    component: ComponentCreator('/__docusaurus/debug/metadata', '156'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/registry',
    component: ComponentCreator('/__docusaurus/debug/registry', '88c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/routes',
    component: ComponentCreator('/__docusaurus/debug/routes', '000'),
    exact: true
  },
  {
    path: '/docs',
    component: ComponentCreator('/docs', 'e43'),
    routes: [
      {
        path: '/docs',
        component: ComponentCreator('/docs', '26b'),
        routes: [
          {
            path: '/docs',
            component: ComponentCreator('/docs', '605'),
            routes: [
              {
                path: '/docs/',
                component: ComponentCreator('/docs/', '0ee'),
                exact: true
              },
              {
                path: '/docs/examples/',
                component: ComponentCreator('/docs/examples/', '92c'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/exercises/weekly-exercises',
                component: ComponentCreator('/docs/exercises/weekly-exercises', '7ba'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/intro',
                component: ComponentCreator('/docs/intro', '058'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/intro/',
                component: ComponentCreator('/docs/intro/', '45d'),
                exact: true
              },
              {
                path: '/docs/intro/overview',
                component: ComponentCreator('/docs/intro/overview', '8f3'),
                exact: true
              },
              {
                path: '/docs/intro/setup',
                component: ComponentCreator('/docs/intro/setup', '187'),
                exact: true
              },
              {
                path: '/docs/syllabus',
                component: ComponentCreator('/docs/syllabus', '1c8'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/week-01/',
                component: ComponentCreator('/docs/week-01/', 'a39'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/week-01/exercises',
                component: ComponentCreator('/docs/week-01/exercises', 'c36'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/week-01/theory-foundations',
                component: ComponentCreator('/docs/week-01/theory-foundations', '3c8'),
                exact: true
              },
              {
                path: '/docs/week-02/',
                component: ComponentCreator('/docs/week-02/', 'e96'),
                exact: true
              },
              {
                path: '/docs/week-02/exercises',
                component: ComponentCreator('/docs/week-02/exercises', '788'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/week-02/nodes-topics-services',
                component: ComponentCreator('/docs/week-02/nodes-topics-services', 'c78'),
                exact: true
              },
              {
                path: '/docs/week-02/ros2-fundamentals',
                component: ComponentCreator('/docs/week-02/ros2-fundamentals', '49a'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/week-03/',
                component: ComponentCreator('/docs/week-03/', 'c51'),
                exact: true
              },
              {
                path: '/docs/week-03/exercises',
                component: ComponentCreator('/docs/week-03/exercises', '427'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/week-03/tf-transforms',
                component: ComponentCreator('/docs/week-03/tf-transforms', '59b'),
                exact: true
              },
              {
                path: '/docs/week-03/urdf-modeling',
                component: ComponentCreator('/docs/week-03/urdf-modeling', '5fd'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/week-04/',
                component: ComponentCreator('/docs/week-04/', 'f6f'),
                exact: true
              },
              {
                path: '/docs/week-04/exercises',
                component: ComponentCreator('/docs/week-04/exercises', 'be9'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/week-04/gazebo-simulation',
                component: ComponentCreator('/docs/week-04/gazebo-simulation', '4ce'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/week-04/simulation-concepts',
                component: ComponentCreator('/docs/week-04/simulation-concepts', '6c5'),
                exact: true
              },
              {
                path: '/docs/week-04/unity-integration',
                component: ComponentCreator('/docs/week-04/unity-integration', '0ef'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/week-05/',
                component: ComponentCreator('/docs/week-05/', 'd07'),
                exact: true
              },
              {
                path: '/docs/week-05/exercises',
                component: ComponentCreator('/docs/week-05/exercises', 'da7'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/week-05/isaac-sim-overview',
                component: ComponentCreator('/docs/week-05/isaac-sim-overview', '384'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/week-05/perception-systems',
                component: ComponentCreator('/docs/week-05/perception-systems', 'dd9'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/week-06/',
                component: ComponentCreator('/docs/week-06/', '3b3'),
                exact: true
              },
              {
                path: '/docs/week-06/exercises',
                component: ComponentCreator('/docs/week-06/exercises', '9f1'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/week-06/path-planning',
                component: ComponentCreator('/docs/week-06/path-planning', '327'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/week-06/slam-navigation',
                component: ComponentCreator('/docs/week-06/slam-navigation', '741'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/week-07/',
                component: ComponentCreator('/docs/week-07/', '7b6'),
                exact: true
              },
              {
                path: '/docs/week-07/exercises',
                component: ComponentCreator('/docs/week-07/exercises', '2dd'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/week-07/multimodal-processing',
                component: ComponentCreator('/docs/week-07/multimodal-processing', '6aa'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/week-07/vla-introduction',
                component: ComponentCreator('/docs/week-07/vla-introduction', '211'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/week-08/',
                component: ComponentCreator('/docs/week-08/', '03d'),
                exact: true
              },
              {
                path: '/docs/week-08/balance-control',
                component: ComponentCreator('/docs/week-08/balance-control', 'b70'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/week-08/exercises',
                component: ComponentCreator('/docs/week-08/exercises', 'b48'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/week-08/humanoid-locomotion',
                component: ComponentCreator('/docs/week-08/humanoid-locomotion', '038'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/week-08/manipulation-interaction',
                component: ComponentCreator('/docs/week-08/manipulation-interaction', '5f8'),
                exact: true
              },
              {
                path: '/docs/week-09/exercises',
                component: ComponentCreator('/docs/week-09/exercises', 'eaa'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/week-09/grasp-planning',
                component: ComponentCreator('/docs/week-09/grasp-planning', '569'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/week-09/manipulation-basics',
                component: ComponentCreator('/docs/week-09/manipulation-basics', 'ad6'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/week-10/conversational-robots',
                component: ComponentCreator('/docs/week-10/conversational-robots', '09c'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/week-10/exercises',
                component: ComponentCreator('/docs/week-10/exercises', '9a4'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/week-11/exercises',
                component: ComponentCreator('/docs/week-11/exercises', '5dd'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/week-11/llm-cognitive-planning',
                component: ComponentCreator('/docs/week-11/llm-cognitive-planning', '3f1'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/week-12/exercises',
                component: ComponentCreator('/docs/week-12/exercises', '413'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/week-12/sim-to-real-deployment',
                component: ComponentCreator('/docs/week-12/sim-to-real-deployment', '477'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/week-13/capstone-project',
                component: ComponentCreator('/docs/week-13/capstone-project', '9bc'),
                exact: true,
                sidebar: "docsSidebar"
              },
              {
                path: '/docs/week-13/exercises',
                component: ComponentCreator('/docs/week-13/exercises', '9b3'),
                exact: true,
                sidebar: "docsSidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/',
    component: ComponentCreator('/', 'fd5'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
