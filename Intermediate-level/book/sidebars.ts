import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // Manual sidebar configuration to control navigation order
  tutorialSidebar: [
    'intro',
    'author',
    {
      type: 'category',
      label: 'Preface',
      items: [
        'preface/introduction',
      ],
    },
    {
      type: 'category',
      label: 'Foundations',
      items: [
        'foundations/core-concepts',
      ],
    },
    {
      type: 'category',
      label: 'Brain',
      items: [
        'brain/cognitive-architectures',
      ],
    },
    {
      type: 'category',
      label: 'Simulation',
      items: [
        'simulation/virtual-environments',
      ],
    },
    {
      type: 'category',
      label: 'VLAs (Vision-Language-Actions)',
      items: [
        'vla/multimodal-models',
      ],
    },
    {
      type: 'category',
      label: 'ROS2 Integration',
      items: [
        'ros2/getting-started',
      ],
    },
    {
      type: 'category',
      label: 'Capstone Projects',
      items: [
        'capstone/building-a-robot',
      ],
    },
    {
      type: 'category',
      label: 'Appendices',
      items: [
        'appendices/setup',
        'appendices/projects',
        'appendices/glossary',
        'appendices/references',
      ],
    },
  ],
};

export default sidebars;
