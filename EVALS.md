# Evaluation Report — AI Tech Consultant

## 1. Evaluation Goals

The goal is to check whether the three modules return useful results, handle errors safely, and respond within a reasonable time.

## 2. Knowledge Brain — Test Cases

| ID  | Test input                   | Expected result                               |
| --- | ---------------------------- | --------------------------------------------- |
| K01 | Search for membership plans  | Relevant articles and source links            |
| K02 | Ask how to post an event     | Answer based on retrieved articles            |
| K03 | Search for payment settings  | Relevant support articles                     |
| K04 | Ask an unrelated question    | Honest response when sources are insufficient |
| K05 | Submit an empty search query | Clear validation or empty-result response     |

## 3. Inbox Agent — Test Cases

| ID  | Test input                            | Expected result                              |
| --- | ------------------------------------- | -------------------------------------------- |
| I01 | Email asking how to post an event     | Helpful draft with sources                   |
| I02 | Email asking about membership         | Relevant draft                               |
| I03 | Complaint from a customer             | Polite, professional response                |
| I04 | Email with missing subject            | Graceful handling                            |
| I05 | Email containing an unrelated request | No unsupported claims; human review required |

## 4. Meeting Scope Agent — Test Cases

| ID  | Test input                      | Expected result                    |
| --- | ------------------------------- | ---------------------------------- |
| M01 | Sample shopping website meeting | Extracted project and requirements |
| M02 | Meeting with a stated deadline  | Deadline included                  |
| M03 | Meeting with identified risks   | Risks included                     |
| M04 | Meeting with assigned tasks     | Action items included              |
| M05 | Empty meeting notes             | Clear validation or error response |

## 5. Initial Functional Test Results

The following endpoints were tested through Swagger UI during development.

| Module          | Endpoint             | Observed result |
| --------------- | -------------------- | --------------- |
| Main API        | POST /ask            | HTTP 200        |
| Knowledge Brain | GET /search          | HTTP 200        |
| Knowledge Brain | POST /ask            | HTTP 200        |
| Inbox Agent     | POST /draft-reply    | HTTP 200        |
| Meeting Scope   | POST /analyze-sample | HTTP 200        |

These results confirm that the tested requests worked. They do not establish overall accuracy or reliability.

## 6. Model Comparison Plan

A fair comparison requires the same prompts and test cases for each model.

| Metric           | Measurement method                                                           |
| ---------------- | ---------------------------------------------------------------------------- |
| Answer quality   | Human rating against an expected answer                                      |
| Source relevance | Check whether cited articles support the answer                              |
| Latency          | Record elapsed time for each request                                         |
| Cost             | Calculate using the model's current published pricing and actual token usage |
| Reliability      | Record successful responses, failures, and timeouts                          |

No comparative model scores are reported yet because a controlled evaluation has not been completed.

## 7. Current Limitations

- The current test set is small and is not yet the required 20 or more cases per task.
- Keyword retrieval may miss relevant articles.
- Meeting extraction uses simple rules and may miss details in long transcripts.
- Model quality, latency, and cost need systematic measurement.
- Automatic email sending is intentionally disabled; human review is required.

## 8. Next Steps

1. Expand each task's evaluation set to at least 20 cases.
2. Run every case and record the actual output.
3. Compare at least two models using identical inputs.
4. Record measured quality, latency, and estimated cost.
5. Test invalid inputs and failure cases before claiming reliability.