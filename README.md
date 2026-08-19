# OpsPilot — Agentic SRE Incident Triage & Response Copilot

An AI agent that investigates production incidents the way an on-call engineer would: gathering metrics, logs, and deployment history, then producing a grounded root-cause analysis — without executing any state-changing action without human approval.

## The Problem

When a production alert fires, an on-call engineer manually checks metrics, searches logs, reviews recent deployments, and cross-references runbooks before deciding what to do. This is slow and repetitive — and much of it follows a predictable pattern.

OpsPilot automates the *investigation* step using an LLM-orchestrated agent, while keeping a human in the loop for any action that would change system state.

## How It Works

1. An incident alert is submitted (in production, this would come from a monitoring webhook like Datadog; in this demo, it's submitted manually to simulate that trigger).
2. A LangGraph agent calls three tools — `get_service_metrics`, `search_logs`, `get_recent_deployments` — to gather evidence.
3. The evidence is passed to an LLM (Groq, `openai/gpt-oss-20b`) with a grounding prompt that explicitly forbids speculation beyond the evidence.
4. The LLM returns a structured (Pydantic-validated) analysis: likely cause, severity, recommended action, confidence, and whether the action requires approval.
5. If the action would change system state (rollback, restart, scale), it's stored as **pending** — the agent proposes, a human disposes.
6. A Next.js dashboard displays incidents and lets a human approve or reject pending actions.

## Architecture

- **Backend:** FastAPI (Python), LangGraph for agent orchestration
- **LLM:** Groq (`openai/gpt-oss-20b`)
- **Data validation:** Pydantic schemas for all tool inputs/outputs and LLM responses
- **Frontend:** Next.js (TypeScript, Tailwind CSS)
- **Storage:** In-memory (swappable for PostgreSQL in a future iteration)

Tool interfaces are production-shaped; their underlying data sources are simulated for reproducible local development and evaluation — the function signatures (`get_service_metrics(service: str) -> dict`, etc.) match what a real Datadog/PagerDuty integration would look like.

## Safety Design

The agent never executes a state-changing action on its own. Every recommendation is classified as `requires_approval: true/false` by the LLM based on whether it would change system state (rollback, restart, config change) versus being purely informational (investigate, monitor). State-changing recommendations are held in a `pending` status until a human explicitly approves or rejects them via the dashboard.

## Evaluation

An automated evaluation harness (`scripts/run_evaluation.py`) runs the agent against 7 hand-designed incident scenarios covering different failure modes (deployment regression, cache pressure, service crash, connection pool exhaustion, memory leak, third-party outage, disk exhaustion).

- **Cause accuracy: 100%** (LLM-as-judge scoring — semantic match against ground truth, not exact text match)
- **Severity accuracy: 57.1%**

**Honest note on these numbers:** manual review found the LLM judge for cause-matching was somewhat lenient — 2 of 7 scenarios were partial matches rather than exact matches on manual inspection. The severity ground truth was self-authored during scenario design rather than externally validated, so some of the severity disagreement reflects differing but reasonable judgment calls rather than agent error. The full per-scenario report is saved to `data/evaluation_report.json`.

## Running Locally

### Backend
```bash
cd apps/api
uv venv
uv sync
# create a .env file at the project root with GROQ_API_KEY=your_key
uv run uvicorn app.main:app --reload
```

### Frontend
```bash
cd apps/web
npm install
npm run dev
```

### Evaluation
```bash
python scripts/run_evaluation.py
```

## Project Structure

```
opspilot/
├── apps/
│   ├── api/        # FastAPI backend, LangGraph agent, tools
│   └── web/         # Next.js dashboard
├── data/
│   ├── incidents/    # Simulated incident scenarios
│   ├── runbooks/      # Matching runbooks for RAG-style reference
│   └── evaluation_report.json
├── scripts/
│   ├── test_graph.py
│   └── run_evaluation.py
```


## Known Limitations & Next Steps

- Storage is in-memory; a restart clears incident history (PostgreSQL planned)
- Evaluation judge occasionally over-credits partial cause matches — a stricter rubric is a planned improvement
- No RAG retrieval yet for runbooks — currently referenced as static context; vector search over runbooks is a natural next step
- Only one LLM provider is wired in (Groq); provider abstraction would allow easy swapping