# Agents

Specialist subagents that perform the four phases of SimScreen evaluation. The main session (governed by `CLAUDE.md`) orchestrates and never performs agent-level work itself.

Each agent's full system prompt lives in `.claude/agents/[name].md`. This file is the index.

## Inventory

### `company-researcher`
- **Role:** Build a grounded, sourced company profile.
- **Inputs:** Company name; optional JD context.
- **Output:** `companies/[name]/[name].md`.
- **Tools:** `WebSearch`, `WebFetch`, `Read`, `Write`, `Edit`.
- **Key constraints:** Cite every claim with a fetched URL. Never fabricate. Edit additively if the file exists.

### `jd-parser`
- **Role:** Decompose one job description into Hard / Soft / Inferred requirements, Culture Signals, and Anomalies.
- **Inputs:** A JD file path or URL; the corresponding `companies/[name]/[name].md` must exist.
- **Output:** `companies/[name]/[job_title].md`.
- **Tools:** `Read`, `WebFetch`, `Write`, `Edit`.
- **Key constraints:** `## Source` is written once and never edited afterward. URL fetch failure → exit immediately, no fabrication. Inferred requirements are never blended into Hard.

### `application-evaluator`
- **Role:** Score the applicant against the parsed JD. Best-matching resume selection is an internal subroutine.
- **Inputs:** A fully parsed `[job_title].md`; `application/**`.
- **Output:** Appends `## Applicant Evaluation` to `[job_title].md`.
- **Tools:** `Read`, `Glob`, `Edit`.
- **Key constraints:** Append-only. Adversarial and objective - no flattery. Surface conflicts to the orchestrator before replacing an existing section.

### `gap-analyzer`
- **Role:** Map applicant evidence to JD requirements, classify gaps, recommend follow-up actions.
- **Inputs:** `[job_title].md` with the Applicant Evaluation section present.
- **Output:** Appends `## Gap Analysis` to `[job_title].md` by default.
- **Tools:** `Read`, `Edit`.
- **Key constraints:** Distinguish confirmed gaps from ambiguity - conflating them undermines downstream action. The default target is `[job_title].md`; any other target requires explicit orchestrator confirmation.

## Cross-agent invariants

- **Append-only.** If a target section already exists, surface to the orchestrator. Never silently overwrite.
- **No subagent spawns another subagent.** Fan-out is the orchestrator's job.
- **Source immutability.** The `## Source` block in any `[job_title].md` is set once by `jd-parser` and read-only for every other agent.
- **Logged automatically.** The `PostToolUse` hook captures every tool call. Subagents do not log manually.
- **Objectivity.** No agent flatters. Ambiguity is surfaced, not hidden. Confidence is named when evidence is partial.
