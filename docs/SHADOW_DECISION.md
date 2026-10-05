# RDC + JEV Shadow Decision Layer

Todo Agent remains the primary business workflow engine.

## Roles

- **Todo Agent**: primary task intelligence and proposal engine.
- **RDC Shadow**: checks operational feasibility, execution risk, and readiness.
- **JEV Shadow**: independent typed decision coprocessor using the existing shared RDC JEV runtime.
- **Human Gate**: final approval authority for controlled writes.

## Decision flow

```text
Task / Context
   |
Todo Agent Primary Analysis
   |
   +--> RDC Shadow Review
   |
   +--> JEV Shadow Review
   |
Shadow Council
   |
Executive Proposal
   |
Human Gate
   |
Dry Run -> Write -> Verify -> Audit
```

Both shadows are advisory only. They do not bypass hard policy, safety rules, or human approval.

## JEV integration

The project reuses the shared RDC runtime:

`%LOCALAPPDATA%\UAIOS\RDC\rdc-jev.cmd`

Expected JEV mode: `READY_SHADOW`.

The repository contains no JEV API key. Credentials remain in the existing Windows Credential Manager integration.

## Cost control

JEV is called once per executive analyze cycle using a batched `profile full` review, rather than once per task.
