# Todo Agent Lab — 13 Agent Roles

| # | Agent | Input | Output | Authority |
|---|---|---|---|---|
| A01 | Morning Radar | Canonical Task | overdue / due soon / stale / urgent findings | advisory |
| A02 | Task Doctor | Task fields | missing owner / due / description / checklist | advisory |
| A03 | HOLD Intelligence | HOLD task + description | hold governance gaps | advisory |
| A04 | Follow-up | Task + findings | follow-up draft | advisory |
| A05 | Next Action | Task + findings | suggested actions | advisory |
| A06 | Weekly Brief | all findings | executive KPI summary | advisory |
| A07 | Conversational Todo | question + analyzed results | task shortlist / answer | read-only |
| A08 | Meeting Intelligence | meeting note / transcript | action drafts + owner + due + confidence | draft only |
| A09 | Email Intelligence | subject + body + sender | task drafts + confidence | draft only |
| A10 | Evidence / Context | task + findings + source refs | evidence bundle + strength | advisory |
| A11 | RDC Shadow | executive state | feasibility / execution risk | shadow only |
| A12 | JEV Shadow | executive state + evidence summary | typed decision review | shadow only |
| A13 | Shadow Council | primary + RDC + JEV | consensus / conflict / evidence gap | advisory |

## Real workflow

```text
                 Meeting ----------------> Meeting Intelligence
                    |                              |
                    |                              v
                    |                         Action Draft
                    |
Business Input -----+---- Email ----------> Email Intelligence
                    |                              |
                    |                              v
                    |                         Action Draft
                    |
                    +---- Planner / Todo ------> Provider Adapter
                                                   |
                              +--------------------+
                              v
                       Canonical Task Model
                              |
          +-------------------+-------------------+
          |                   |                   |
          v                   v                   v
     Morning Radar        Task Doctor       HOLD Intelligence
          |                   |                   |
          +---------+---------+---------+---------+
                    |                   |
                    v                   v
            Evidence / Context      Findings Pool
                    |                   |
                    +--------+----------+
                             |
          +------------------+------------------+
          |                  |                  |
          v                  v                  v
      Follow-up          Next Action       Weekly Brief
                                                  |
                             +--------------------+
                             v
                    Primary Decision Draft
                         /             \
                        v               v
                   RDC Shadow       JEV Shadow
                        \               /
                         \             /
                          v           v
                         Shadow Council
                              |
                      Executive Proposal
                              |
                          Human Gate
                         /          \
                    Reject          Approve
                                      |
                                   Dry Run
                                      |
                              RDC Execution Plane
                               MCP / API / CLI / OI
                                      |
                               Microsoft Graph
                                      |
                          +-----------+----------+
                          v                      v
                     Read-back Verify         Audit
                          \                      /
                           +---------+----------+
                                     v
                                 KPI Feedback
```

Meeting and Email intelligence create drafts only. They do not bypass Human Gate.
