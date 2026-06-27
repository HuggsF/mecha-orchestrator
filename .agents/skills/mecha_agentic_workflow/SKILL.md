---
name: mecha-agentic-workflow
description: Defines the interaction loop and UI generation strategy for the Mecha Orchestrator IDE.
---

# Mecha Agentic Workflow

When tasked with expanding or modifying the Mecha IDE, you must act as a seamless extension of the Architect. 

## 1. Direct UI Manipulation
- **Understand the Layout**: The IDE uses a multi-pane layout (Activity Bar, Left Nav, Chat Editor, Right Panels). Modifications should preserve the draggable boundaries (`leftW`, `reviewW`, `filesW`).
- **Prompt Injection Cards**: When creating interfaces for agents, use preempted prompts (e.g., `/knot auditor: ...`) bound to the UI so users can instantly interact with specialized squads.

## 2. Aesthetic & Narrative Integration
- **Lore-Driven Design**: Base UI decisions on the established technical architecture mapping (e.g., Telemetry to Architect, Code Review to Engineering).
- **Empty States**: Do not use generic empty states. Use creative, monospace "letter soup" layouts, ASCII art, and status indicators like `[+] ONLINE` or `Awaiting telemetry`.

## 3. Execution Paradigm
- **Immediate Action**: If the instructions are clear (like "do a little letter soup"), immediately modify the relevant React component (`App.tsx`) using `replace_file_content` without asking for unnecessary permissions or creating long plans.
- **Git Synchronization**: Always track changes in the repository to preserve the "SSOT" (Single Source of Truth).
