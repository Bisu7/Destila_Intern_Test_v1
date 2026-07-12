# AI Usage Report

> **This is mandatory and graded.** Be honest — we are evaluating your ability to drive AI tools effectively, not whether you avoided them. Concealing or fabricating AI use is a rejection signal.

## Tools Used

- **AI Coding Assistant**: I used an AI assistant primarily as a productivity multiplier for structural cleanup, styling, and debugging. I defined the core business logic, database schema, and frontend component architecture, and then used the AI to help flesh out the React component syntax and ensure consistent CSS styling.
- I also leaned heavily on the AI to help format and draft the final `README.md` and `APPROACH.md` files based on my direct notes and pipeline design.

## Where AI Was Wrong & How I Caught It

While setting up the Docker environment, the AI initially suggested a `node:18-alpine` base image for the frontend container. However, when I ran the build, Vite threw a syntax error (`SyntaxError: The requested module 'node:util' does not provide an export named 'styleText'`). I recognized this as a Node.js version mismatch issue, as newer versions of Vite/Rolldown rely on features only available in Node v20+. I instructed the AI to bump the Dockerfile to `node:20-alpine`, which immediately resolved the crash.

## AI vs Hand-Written Split

I drove the implementation, writing the core business logic, API design, and determining how to handle the data anomalies. The AI handled the repetitive typing, CSS boilerplate, and documentation formatting. 

- AI-generated (minor edits): **40%** (Mostly boilerplate React components, CSS, Docker setup, and the README documentation).
- Heavily edited / hand-written: **60%** (Core Python backend logic, API design, database schemas, and data ingestion rules).
