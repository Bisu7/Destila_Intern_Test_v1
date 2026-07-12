# AI Usage Report

> **This is mandatory and graded.** Be honest — we are evaluating your ability to drive AI tools effectively, not whether you avoided them. Concealing or fabricating AI use is a rejection signal.

## Tools Used

- **AI Coding Assistant**: I used an AI assistant primarily as a productivity multiplier for structural cleanup, styling, and debugging. I defined the core business logic, database schema, and frontend component architecture, and then used the AI to help flesh out the React component syntax and ensure consistent CSS styling.
- I also leaned heavily on the AI to help format and draft the final `README.md` and `APPROACH.md` files based on my direct notes and pipeline design.

## Where AI Was Wrong & How I Caught It

When building the backend data pipeline, the AI initially wrote the `detect_exceptions.py` script to blindly insert rows into the `exceptions` table every time a deficit was detected. I recognized immediately that this was a massive architectural error: because the pipeline was not idempotent, re-running the script would duplicate every single exception in the database and silently destroy any manual status updates (like `acknowledged` or `resolved`) made by the operators in the UI. I caught this before the code was even executed. I instructed the AI to rewrite the schema to enforce a unique constraint on `(product_code, date)` and change the insertion logic to an "upsert" that updates the deficit metrics but explicitly preserves the existing operational `status` column. This prevented a critical data corruption issue.

## AI vs Hand-Written Split

I drove the implementation, writing the core business logic, API design, and determining how to handle the data anomalies. The AI handled the repetitive typing, CSS boilerplate, and documentation formatting. 

- AI-generated (minor edits): **40%** (Mostly boilerplate React components, CSS, Docker setup, and the README documentation).
- Heavily edited / hand-written: **60%** (Core Python backend logic, API design, database schemas, and data ingestion rules).
