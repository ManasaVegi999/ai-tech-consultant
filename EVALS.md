# Evaluation Report — AI Tech Consultant

## 1. Evaluation Goals

Evaluate the three modules for functional correctness, answer usefulness, source relevance, input validation, safety, and response time.

**Important:** Test cases listed below are planned tests unless explicitly identified as tested. Planned cases must not be counted as completed evaluations.

## 2. Knowledge Brain — 20 Test Cases

| ID  | Test input                                | Expected result                                              |
| --- | ----------------------------------------- | ------------------------------------------------------------ |
| K01 | Search for membership plans               | Relevant articles and source links                           |
| K02 | Ask how to post an event                  | Answer grounded in retrieved articles                        |
| K03 | Search for payment settings               | Relevant support articles                                    |
| K04 | Ask an unrelated question                 | No unsupported answer                                        |
| K05 | Submit an empty search query              | Validation or empty-result response                          |
| K06 | Search for account settings               | Relevant articles, if available                              |
| K07 | Ask how to edit a profile                 | Relevant guidance, if available                              |
| K08 | Search using different capitalization     | Search behaves consistently                                  |
| K09 | Search using extra spaces                 | Graceful handling of whitespace                              |
| K10 | Use a common misspelling                  | Relevant results if supported; otherwise no-results response |
| K11 | Search for a nonexistent feature          | No fabricated article                                        |
| K12 | Ask a question with no relevant source    | Honest limitation                                            |
| K13 | Ask a question about an article's details | Answer supported by retrieved content                        |
| K14 | Search for a very broad term              | Results remain relevant where possible                       |
| K15 | Search for a specific support topic       | Relevant results ranked or returned                          |
| K16 | Submit a very long query                  | Graceful handling                                            |
| K17 | Request the source URLs                   | Available source links are returned                          |
| K18 | Send malformed request data               | Appropriate error response                                   |
| K19 | Simulate unavailable model service        | Graceful error handling, if testable                         |
| K20 | Repeat the same query                     | Consistent, relevant results                                 |

## 3. Inbox Agent — 20 Test Cases

| ID  | Test input                                           | Expected result                                      |
| --- | ---------------------------------------------------- | ---------------------------------------------------- |
| I01 | Email asking how to post an event                    | Helpful draft with relevant sources                  |
| I02 | Email asking about membership                        | Relevant draft                                       |
| I03 | Customer complaint                                   | Polite, professional response                        |
| I04 | Email with missing subject                           | Graceful handling                                    |
| I05 | Unrelated customer request                           | No unsupported claims; human review                  |
| I06 | Email with an empty body                             | Validation or safe response                          |
| I07 | Email asking about account settings                  | Relevant draft if sources exist                      |
| I08 | Email asking about payment settings                  | Source-grounded draft                                |
| I09 | Angry customer email                                 | Calm and empathetic tone                             |
| I10 | Email containing spelling mistakes                   | Understandable draft where possible                  |
| I11 | Email with a very long body                          | Graceful handling                                    |
| I12 | Email asking for a refund without policy evidence    | No invented refund policy                            |
| I13 | Email requesting sensitive account changes           | Appropriate caution and human review                 |
| I14 | Email with missing customer details                  | Avoid assumptions                                    |
| I15 | Email with multiple questions                        | Address supported questions or identify gaps         |
| I16 | Email containing a suspicious link                   | Do not blindly trust or follow the link              |
| I17 | Email asking for a feature not in the knowledge base | State uncertainty rather than inventing instructions |
| I18 | Malformed request payload                            | Appropriate error response                           |
| I19 | Model service unavailable                            | Graceful error handling, if testable                 |
| I20 | Repeat the same email                                | Consistent draft quality and review flag             |

## 4. Meeting Scope Agent — 20 Test Cases

| ID  | Test input                                    | Expected result                           |
| --- | --------------------------------------------- | ----------------------------------------- |
| M01 | Sample shopping website meeting               | Project and requirements extracted        |
| M02 | Meeting with a stated deadline                | Deadline included                         |
| M03 | Meeting with identified risks                 | Risks included                            |
| M04 | Meeting with assigned tasks                   | Action items included                     |
| M05 | Empty meeting notes                           | Validation or clear error                 |
| M06 | Notes containing a project name               | Project name extracted                    |
| M07 | Notes containing several requirements         | Requirements identified                   |
| M08 | Notes listing deliverables                    | Deliverables identified                   |
| M09 | Notes with an explicit technology stack       | Technologies captured if supported        |
| M10 | Notes mentioning a dependency                 | Dependency captured if supported          |
| M11 | Notes with an unclear deadline                | Uncertainty preserved                     |
| M12 | Notes with conflicting deadlines              | Conflict not silently resolved            |
| M13 | Notes with no named project                   | Missing project handled gracefully        |
| M14 | Notes with no assigned owners                 | No owners invented                        |
| M15 | Notes containing multiple action items        | Action items extracted                    |
| M16 | Very long meeting transcript                  | Graceful handling                         |
| M17 | Notes containing a scope change               | Change identified if supported            |
| M18 | Notes containing an estimate request          | No unsupported estimate presented as fact |
| M19 | Malformed request payload                     | Appropriate error response                |
| M20 | Meeting notes containing unrelated discussion | Relevant project details prioritized      |

## 5. Initial Functional Test Results

The following endpoint checks were completed through Swagger UI during development.

| Module          | Endpoint             | Observed result |
| --------------- | -------------------- | --------------- |
| Main API        | POST /ask            | HTTP 200        |
| Knowledge Brain | GET /search          | HTTP 200        |
| Knowledge Brain | POST /ask            | HTTP 200        |
| Inbox Agent     | POST /draft-reply    | HTTP 200        |
| Meeting Scope   | POST /analyze-sample | HTTP 200        |

These checks confirm that the tested requests returned successfully. They do not establish the accuracy of all outputs or the completion of the 60 test cases above.

## 6. Model Comparison

A controlled comparison has not yet been completed.

| Metric           | Measurement method                                                           |
| ---------------- | ---------------------------------------------------------------------------- |
| Answer quality   | Rate outputs against predefined expected answers                             |
| Source relevance | Check whether cited sources support the answer                               |
| Latency          | Record elapsed time for each request                                         |
| Cost             | Calculate from actual token usage and the selected model's published pricing |
| Reliability      | Record successful requests, failures, and timeouts                           |

Compare at least two models using the same test inputs and comparable settings. Report measured results only; do not invent scores or performance figures.

## 7. Current Limitations

- The 60 test cases above are a planned test set, not 60 completed tests.
- Keyword-based retrieval may miss relevant articles.
- Meeting extraction uses simple rules and may miss context in longer transcripts.
- Model quality, latency, and cost require systematic measurement.
- Email sending is disabled; drafts require human review.
- Additional assignment requirements, including knowledge-base updates and learning from feedback, need separate verification.

## 8. Next Steps

1. Run the planned test cases and record actual outcomes.
2. Expand testing where edge cases are not adequately covered.
3. Compare two models with identical inputs.
4. Measure answer quality, latency, and estimated cost.
5. Verify the remaining feature requirements before final submission.