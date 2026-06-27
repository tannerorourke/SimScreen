# SimScreen

A Claude Code–driven agentic system that simulates rigorous resume screening. Built as a tool for applicant's to replicate an AI-driven screening process (ATS keyword and skills matching, recruiter-level cultural and narrative assessment, hiring-manager-level technical depth) and help applicant's analyze their materials.

All you have to do is upload your resume and job description!

## Features

1. **Company research**: synthesizes mission, values, public hiring signals, product direction, and team structure from web sources.
2. **Applicant analysis** - deep, structured profile of the applicant from their materials (resumes, papers, projects, responses). Follows discovered URLs into iterative research. Runs as init (first build) or update (integrate new materials).
3. **JD parsing**: decomposes a job description into Hard, Soft, and Inferred requirements, plus Culture Signals and Anomalies.
4. **Application evaluation**: selects the best-matching resume version, classifies and scores applicant coverage across five weighted dimensions, and produces a final verdict (STRONG PASS through HARD REJECT).
5. **Gap analysis**: concrete follow-up actions for every gap, partial, and overqualification. Action types: `study`, `surface`, `reframe`, `accept`.


![1782529762803](image/README/1782529762803.png)

Any step can serve as the entry point - The orchestrator detects missing prerequisites, prints a numbered plan, and runs the chain after explicit user confirmation.

 `simscreen.skill` optionally can be downloaded and used as a single-session stateless version.

## How it works

1. Drop applicant materials into `application/` (resumes under `application/resumes/`).
2. Build the applicant profile first: `/profile` (or just "build my applicant profile"). Claude will output a `profile.md` in `/application`.
3. Ask the main session to run any phase. The orchestrator will print a plan, ask for confirmation, then execute.

Examples:

- "Research Anthropic and parse this JD: [URL or path]"
- "Evaluate me against the Google Software Engineer JD"
- "Run a gap analysis on all job descriptions for Microsoft"

### Generated Structure

- `companies/[company_name]`: holds all research and job descriptions/evalation/analysis.

  - `[company_name].md`: All company research
  - `[job_title].md`: Parsed job descriptions (job title based on user submitted file, or auto-generated).
    - "## Application Evaluation" and "## Gap Analysis" are appended after the parsed job description
- `application`: Applicant materials. Can be anything you'd like to serve as context when evaluating against a JD.

  - `resumes`: 1-many resumes. During 'Applicant Evaluation', the system determines the best resume if none is specified

## Requirements

- Claude Code
- Python 3.10+ (Optional, if you want log traces)
- `pandoc` on `PATH` (only needed if applicant materials include `.docx` or `.doc` files that Claude Code cannot read natively).

## Extensibility

To add a new step:

1. Define the subagent in `.claude/agents/[name].md` with minimum-required tools and a YAML frontmatter `description` that triggers correct auto-routing.
2. Add a row to `AGENTS.md`.
3. Update routing rules in `CLAUDE.md`.
4. Optionally add a slash command in `.claude/commands/`.

To port to a Python + Anthropic API harness, change the orchestration logic in `CLAUDE.md` into Python code - agent system prompts and artifact schemas are portable as-is.
