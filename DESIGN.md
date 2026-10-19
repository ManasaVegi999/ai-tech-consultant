# AI Tech Consultant — Design Document

## 1. Problem and Goal

Small software businesses spend significant time answering customer questions, searching help-center articles, replying to emails, and preparing project scopes after client meetings. These activities slow down delivery and increase the risk of incorrect answers, missed requirements, and unexpected costs.

The AI Tech Consultant is designed to support these activities through three connected modules:

1. **Knowledge Brain:** Searches public support articles and generates answers with source links.
2. **Inbox Agent:** Uses customer email details and relevant support articles to draft replies for human review.
3. **Meeting Scope Agent:** Extracts project requirements, deliverables, risks, action items, and deadlines from meeting notes.

The goal is to reduce repetitive work while keeping people responsible for important decisions.

## 2. Features and Design Decisions

### Task 1 — Knowledge Brain

The Knowledge Brain collects public support articles from Brilliant Directories and stores article information in `articles.json`. Its search function retrieves relevant articles using keyword matching. The API provides a search endpoint and a question-answering endpoint.

Gemini generates concise answers using retrieved article content. The response includes source titles and URLs so users can verify the information.

**Why these features were chosen:** A support assistant should provide evidence for its answers rather than invent product policies or unsupported features.

**Current limitations:** The current implementation stores a limited collection of articles and uses keyword matching. A complete daily sitemap synchronization process, change detection, image understanding, vector retrieval, and human-expert feedback loop are not yet implemented.

### Task 2 — Inbox Agent

The Inbox Agent accepts an email subject and body. It searches the Knowledge Brain's article collection, supplies relevant information to Gemini, and returns a draft reply with source links.

Every response includes `requires_human_review: true`. The application does not send emails automatically.

**Why this design was chosen:** Incorrect customer communications can damage trust. Human approval is a safer starting point than autonomous sending.

**Current limitations:** The application does not connect to a real email inbox, record human edits, learn from approved replies, or implement the required dataset of at least 50 realistic customer emails. Automatic sending after a defined history of unchanged drafts is not implemented.

### Task 3 — Meeting Scope Agent

The Meeting Scope Agent accepts meeting notes and extracts a project name, requirements, deliverables, risks, action items, and deadline. It also provides an endpoint that analyzes the included sample meeting notes.

**Why this design was chosen:** Structured information helps teams turn informal conversations into actionable work.

**Current limitations:** Extraction currently relies on simple Python rules. Developer-hour estimates, pricing proposals, multi-agent handoffs, long-transcript handling, and comparison between an initial meeting and a follow-up meeting are not implemented. The current extraction rules also need broader testing.

## 3. Architecture and Data Flow

The project uses FastAPI to expose HTTP endpoints. The main application runs on port 8000 and mounts the three existing applications under separate paths.

```
                    User / Client
                          |
                          v
              AI Tech Consultant API
                    Port 8000
                          |
           +--------------+--------------+
           |              |              |
           v              v              v
      /knowledge        /inbox         /meeting
           |              |              |
           v              v              v
      Knowledge Brain  Inbox Agent   Meeting Scope
           |              |
           v              v
       articles.json  Search articles
           |
           v
      Keyword retrieval
           |
           v
     Gemini answer generation
```

The Inbox Agent imports the Knowledge Brain's search function to reuse article retrieval. This is a direct Python function call rather than an HTTP call to the Knowledge Brain API. The modules are exposed through the main API, but this internal reuse means the architecture is not yet a fully service-to-service implementation.

The Meeting Scope Agent currently processes meeting notes independently and does not yet call the Knowledge Brain API to validate proposed solutions against existing product features.

## 4. Technology and Model Choices

- **Python:** Used for the three task implementations.
- **FastAPI:** Provides HTTP endpoints and interactive API documentation.
- **Pydantic:** Validates incoming request data.
- **BeautifulSoup and requests:** Used for collecting public support article content.
- **JSON:** Stores the current article collection.
- **Google GenAI SDK and Gemini:** Used for question answering and email drafting.
- **Git and GitHub:** Track and share the source code.

The current implementation uses Gemini Flash. This differs from the assignment requirement that Claude be at the center of the project. Claude integration and a measured comparison between models remain outstanding.

Model selection should consider answer correctness, source grounding, response latency, cost per task, and safe behavior on missing or misleading information. These metrics must be measured using the same test cases before choosing a production model.

## 5. Safety, Reliability, and Human Review

The Knowledge Brain instructs the model to use the supplied support articles as reference material and to acknowledge insufficient information. The Inbox Agent is explicitly instructed not to invent policies or claim that actions have been completed.

The Inbox Agent returns drafts for human review instead of sending messages automatically. The Meeting Scope Agent returns structured JSON that can be checked by a person before a proposal is used.

The project excludes the `.env` file and virtual environment through `.gitignore`. API credentials should be stored in environment variables and must never be committed to the repository.

Further reliability improvements should include input validation tests, model failure handling, retries with limits, logging, prompt versioning, and regression tests.

## 6. Evaluation Plan

Evaluation should cover all three tasks using representative and unseen inputs.

For the Knowledge Brain, tests should measure retrieval relevance, answer correctness, source accuracy, missing-information handling, and response latency.

For the Inbox Agent, tests should measure factual correctness, tone, source relevance, appropriate escalation, and whether unsupported claims are avoided.

For the Meeting Scope Agent, tests should measure the correctness of extracted requirements, deliverables, risks, action items, and deadlines. Follow-up meeting tests should measure whether changes to the original scope are identified.

At least 20 test cases per task and a comparison of at least two models are required by the assignment. Quality, cost, and speed results should be recorded from actual runs. No benchmark scores or cost claims are asserted in this document because those measurements have not yet been completed.

## 7. Future Improvements

1. Integrate Claude and compare models on a shared evaluation dataset.
2. Build reliable daily sitemap synchronization with incremental updates and removal detection.
3. Add image-aware article retrieval and improve search quality.
4. Create 50 or more realistic customer emails and record human feedback.
5. Add scope estimation, proposal generation, and follow-up meeting comparison.
6. Add automated tests, structured logging, and bounded retry handling.
7. Build a simple user interface for all three tasks.

## Conclusion

The current project provides a working API foundation for the Knowledge Brain, Inbox Agent, and Meeting Scope Agent. The main application exposes the three modules, and basic successful API responses have been verified. The limitations listed above identify the next steps required to meet the complete assignment specification.