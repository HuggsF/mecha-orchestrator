---
name: mecha-backend-engineering
description: Enforces strict backend standards (Zod, Helmet, Husky) and Cognitive Transformer Reporting for agent squads.
---

# Mecha Backend Engineering & Cognitive Reports

As an agent of the DevOps and Engineering squads, you must enforce the following standards on all Node.js/Backend code:

## 1. Security & Validation (Zod + Helmet)
- **Zod**: All incoming payloads, API requests, and environment variables MUST be validated using `zod` schemas. Never trust raw `req.body`.
  - Export schemas alongside controllers (e.g., `createUserSchema`).
  - Use `zod` middleware for Express/Fastify.
- **Helmet**: Every web server must integrate `helmet` to secure HTTP headers by default (`app.use(helmet())`).

## 2. Git Workflow (Husky Pre-commits)
- All repositories must be configured with `husky`.
- The `pre-commit` hook MUST run linting (`eslint --fix`) and type-checking (`tsc --noEmit`).
- Commits that fail standard validation must be blocked. No bypasses allowed.

## 3. Cognitive + Transformer Reporting
- When generating reports, system status, or task summaries, use the **Cognitive Transformer Format**.
- **Structure**:
  - `[COGNITIVE STATE]`: The current understanding of the system (e.g., "Analyzing data flow anomalies").
  - `[TRANSFORMER LAYER]`: The specific technical transformation applied (e.g., "Applied Zod schema validation to User payload").
  - `[OUTPUT / TELEMETRY]`: The measurable result or metric.
- Do not use generic summary paragraphs. Keep reports modular, highly technical, and formatted like a machine log output.

## Execution Rules
- When tasked with setting up a new service, instantly install: `npm install zod helmet` and `npm install husky --save-dev`.
- Initialize husky (`npx husky init`) and set up the pre-commit hook automatically.
