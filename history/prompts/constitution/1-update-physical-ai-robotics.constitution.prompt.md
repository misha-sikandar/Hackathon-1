---
id: 1
title: Update Physical AI Robotics
stage: constitution
date: 2026-01-27
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: user
command: /sp.constitution
labels: [constitution, robotics, ai]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```text
You are an expert AI curriculum designer, robotics engineer, and technical author.

Your task is to write a professional, industry-grade technical book using Docusaurus.
The book focuses on Physical AI and Humanoid Robotics, emphasizing embodied intelligence:
AI systems that perceive, reason, and act in the physical world.

Core principles:
- Accuracy over hype
- Engineering-first explanations
- Practical, simulation-driven learning
- ROS 2, Gazebo, Unity, NVIDIA Isaac, and Vision-Language-Action systems
- Clear progression from theory → simulation → deployment
- Assume readers are CS/AI students transitioning into robotics

Writing rules:
- Use clear, concise technical English
- Prefer diagrams, code snippets, and system architecture explanations
- Avoid marketing language
- Explain "why" before "how"
- Keep chapters modular and self-contained
- Follow modern robotics and AI best practices (ROS 2 Humble/Iron)

Output format:
- Docusaurus-compatible Markdown
- Logical sidebar structure
- Ready for
```

## Response snapshot

Updated the project constitution to reflect the Physical AI and Humanoid Robotics book project, incorporating the core principles of accuracy over hype, engineering-first explanations, simulation-driven learning, progressive learning path, modern robotics standards, and practical application focus. The constitution now governs all content creation for the robotics book project with specific technology stack requirements and curriculum standards.

## Outcome

- ✅ Impact: Updated constitution to align with Physical AI and Robotics book project
- 🧪 Tests: none
- 📁 Files: .specify/memory/constitution.md updated
- 🔁 Next prompts: Continue with book content creation
- 🧠 Reflection: Successfully transformed template constitution into project-specific governance document

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin creating book content based on constitution