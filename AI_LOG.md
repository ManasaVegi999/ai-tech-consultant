# AI Log — AI Tech Consultant

## 1. Project Approach

I used Cursor to develop the AI Tech Consultant in small, testable steps. I built three modules and connected them through a main FastAPI application.

## 2. Useful Prompts

### Prompt 1 — Knowledge Brain

Build a Python FastAPI service that collects public support articles, searches for relevant information, and answers questions using retrieved article content. Return source links with each answer.

### Prompt 2 — Inbox Agent

Build an API that accepts a customer email, retrieves relevant Knowledge Brain articles, and drafts a professional reply. Do not send the email automatically. Require human review and return source links.

### Prompt 3 — Meeting Scope Agent

Build a Python API that extracts project requirements, deliverables, risks, action items, and deadlines from meeting notes. Return the result as structured JSON.

### Prompt 4 — Main API Integration

Connect the three modules to one FastAPI application using separate URL prefixes. Preserve the individual module endpoints and make them accessible through the main application.

### Prompt 5 — Testing and Debugging

Help me test each API through Swagger UI, understand HTTP status codes, and fix endpoint or server configuration problems without changing working modules unnecessarily.

## 3. A Design Decision I Made

I kept human review enabled for email drafts because incorrect replies could mislead customers. The agent generates a draft and supporting sources, but a person remains responsible for approving the message.

## 4. Limitations I Identified

The current implementation uses keyword-based article retrieval, simple rule-based meeting extraction, and Gemini for generation. Daily article synchronization, image understanding, the required email feedback dataset, complete meeting-scope estimation, Claude integration, and measured model comparisons still need implementation.

## 5. Rejected or Deferred Ideas

I deferred automatic email sending because the system does not yet have a validated feedback history or reliable quality thresholds. I also deferred claiming model performance, cost savings, or accuracy percentages because these need to be measured with real test cases.

## 6. Next Improvements

- Add automated tests for all three modules.
- Build at least 20 evaluation cases per task.
- Compare at least two models using the same test inputs.
- Measure latency and estimate actual model costs.
- Improve article synchronization and retrieval.
- Add meeting-scope estimates and follow-up change detection.

**Note:** This log summarizes the development approach and decisions. It does not claim that every listed prompt or improvement has been fully implemented.