# Use Cases

| # | Use case | Current implementation |
|---|---|---|
| 1 | Morning MD Radar | Working |
| 2 | Auto Follow-up Agent | Draft messages + approval queue |
| 3 | Meeting -> Task | Meeting text intake -> draft action items |
| 4 | Email -> Task | Email text intake -> draft action items |
| 5 | Smart Priority | Rule-based score/ranking |
| 6 | Stale Task Detector | Working |
| 7 | HOLD Intelligence | HOLD governance checks |
| 8 | AI Task Doctor | Working |
| 9 | Executive Weekly Brief | Working |
| 10 | Conversational Planner | CLI natural-language style filtering |

## Safety boundary

Read and analysis run automatically.
External communication, task creation and task modification are proposals first.
Planner write-back requires an explicit proposal plus approval execution with confirmation.

## Human-approved write flow

```text
Agent finding
   |
Action proposal
   |
output/proposals.json
   |
Human review
   |
Dry run
   |
Explicit execute + YES
   |
Microsoft Graph write
   |
Audit log
```
