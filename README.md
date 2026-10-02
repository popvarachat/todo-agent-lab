# Todo Agent Lab

Forkable AI/Agent layer for task systems, starting with Microsoft Planner.

The project keeps the existing task system as the source of truth while adding
monitoring, quality checks, prioritization, summaries and suggested actions.

## Why

Traditional task boards still require people to:
- open the board and scan work manually
- remember which task needs follow-up
- detect stale work themselves
- create weekly summaries by hand
- maintain task quality consistently

Todo Agent Lab adds an agent layer without forcing a database migration.

## Architecture

```text
Task System
   |
Provider Adapter
   |
Canonical Task Model
   |
Agent Layer
   +-- Morning Radar
   +-- Stale Detector
   +-- Task Doctor
   +-- Weekly Brief
   +-- Suggested Actions
   |
Human Gate
   |
Report / future write-back
```

Current release defaults to **read-only**.

## Supported providers

- Microsoft Planner: working and tested
- JSON file: working, useful for demos and custom integrations
- Microsoft To Do: adapter included; requires delegated Graph Tasks permission

The agent logic is provider-independent. New systems only need to implement
`TaskProvider` and map fields into the canonical `Task` model.

## Quick start - Microsoft Planner

Requirements:
- Python 3.10+
- Azure CLI
- Microsoft 365 account with access to the Planner plan

```powershell
git clone <your-fork-url>
cd todo-agent-lab
Copy-Item config\settings.example.json config\settings.json
az login
.\scripts\connect_planner.ps1 -PlanUrl "<paste Planner URL>"
```

Put the detected `plan_id` into `config/settings.json`, then:

```powershell
python -m todo_agent.cli --config config\settings.json
```

Reports are written to `output/`.

## Current agents

### Morning Radar
Ranks active tasks using due status, staleness and priority.

### Stale Detector
Flags tasks that have no meaningful checklist activity for a configurable period.
The current implementation is intentionally conservative and will be expanded
with comments/email/meeting evidence in later versions.

### Task Doctor
Checks missing owner, due date, description and checklist.

### Weekly Brief
Produces aggregate counts for active, overdue, stale, due-soon, urgent and
task-quality findings.

### Suggested Actions
Generates safe recommendations such as follow-up, assign owner, set due date,
add definition of done or review a HOLD task.

## Safety model

There are three intended operating modes:

1. READ - inspect and report only
2. SUGGEST - propose actions but change nothing
3. WRITE - future opt-in write-back behind a Human Gate

The repository currently ships in READ/SUGGEST mode.
No automatic Planner write-back is enabled.

## Portability

Forking users should only need to:
1. authenticate with their own account
2. select their own task source
3. edit a small config file
4. run the same agents

See `docs/PORTABILITY.md`.

## Example configuration

```json
{
  "provider": "microsoft_planner",
  "plan_id": "YOUR_PLAN_ID",
  "timezone": "Asia/Bangkok",
  "stale_days": 14,
  "due_soon_days": 7,
  "read_only": true,
  "human_gate": true
}
```

For a local demo, use `provider: json_file` with `examples/sample_tasks.json`.

## Roadmap

- [x] Planner adapter
- [x] Canonical task model
- [x] Morning Radar
- [x] Stale Detector
- [x] Task Doctor
- [x] Weekly Brief
- [x] Suggested Actions
- [x] JSON adapter
- [x] Microsoft To Do adapter scaffold
- [ ] Microsoft To Do consent/setup helper
- [ ] Meeting -> Task
- [ ] Email -> Task
- [ ] HOLD intelligence
- [ ] Follow-up agent
- [ ] Human-approved write-back
- [ ] Conversational task interface

## License

MIT

## v0.2 agentic workflow

The repository now includes all 10 planned use-case paths at pilot level:

1. Morning Radar
2. Follow-up proposal generation
3. Meeting intake
4. Email intake
5. Smart priority ranking
6. Stale detection
7. HOLD governance
8. Task Doctor
9. Weekly executive brief
10. Conversational task query

### Human-approved write-back

Write-back is implemented but intentionally fail-closed.

```powershell
# 1) Generate a proposal using a JSON payload file
python -m todo_agent.cli propose-write --task-id "<TASK_ID>" --action-type patch_task --payload-file ".\\my_change.json" --reason "approved business reason"

# 2) Dry-run the proposal first
python -m todo_agent.cli approve <PROPOSAL_ID>

# 3) Execute only after human approval
python -m todo_agent.cli approve <PROPOSAL_ID> --execute --confirm YES
```

Supported write operations:
- patch Planner task
- patch Planner task details
- create Planner task

Every executed write is appended to `output/audit.jsonl`.

### Meeting / Email intake without paid AI API

```powershell
python -m todo_agent.cli intake --kind meeting --file examples\\meeting_notes.txt
python -m todo_agent.cli intake --kind email --file examples\\email_sample.txt
```

These create drafts only. ChatGPT / OI can enrich the draft before any Planner write is proposed.
