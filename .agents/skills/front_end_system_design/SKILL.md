---
name: front-end-system-design
description: Guidelines and best practices for creating beautiful, modern frontend system designs in React/Vite for Mecha.
---

# Front-End System Design (Mecha Standard)

When designing front-end interfaces, follow these creative and technical standards:

## 1. Aesthetics (The "Mecha" Look)
- **Dark Mode by Default**: Use `#0c0c0e` for the absolute background, with subtle layered elevations (e.g., `#121216`, `#16161a`).
- **Accent Colors**: Violet, Cyan, and Emerald for statuses.
- **Typography**: Minimal, monospace for technical details (e.g., `text-[10px] tracking-widest`), and sans-serif for reading.

## 2. Layouts
- **Grid Layouts**: Mimic modern IDEs (like KIRO, Cursor) with an Activity Bar (leftmost), Primary Sidebar, Main Editor/Chat, and Right-side auxiliary panels (Git, Files).
- **Interactive Resizing**: All columns must be draggable and resizable using standard mouse events (`mousedown`, `mousemove`, `mouseup`).

## 3. "Letter Soup" Creativity
- Don't just put "Loading...". Use creative ASCII art, letter soups, or dynamic typographic elements for empty states.
- Embed the essence of "SUPER PROMPTS KNOT" and "MECHA" into the DNA of the application's empty states and placeholders.
- Treat text as a structural element, not just information. 

## 4. Components
- Use raw SVG icons inline for performance and easy styling.
- Keep components modular, but feel free to inline small stylistic choices (Tailwind) to iterate quickly.
