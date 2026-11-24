# Moniepoint GTM Systems OS

## 1. Project Context

Build a GTM Systems OS for identifying, researching, qualifying and prioritising potential business customers for Moniepoint Business Banking and Payments in Nigeria.

The project combines commercial research, ICP development, buying-signal detection, account qualification, buying-persona research, workflow design and technical implementation.

The research currently focuses on:

- Retail supermarket chains
- FMCG distributors
- Other businesses with potentially complex financial and operational requirements, where supported by the evolving ICP research

The objective is to develop a reliable, evidence-led system that can identify relevant businesses, establish their fit, detect timely buying signals, investigate relevant buying roles and prepare credible commercial opportunities.

Treat ICP definitions, buying signals, customer pain points and commercial opportunities as research findings or hypotheses, not established facts.

Verify Moniepoint's product capabilities against authoritative sources before making product claims or proposing specific use cases.

## 2. Project Structure

Use the existing repository structure as the source of truth. Do not assume that folders contain files or implementations that have not been verified.

### Project context

- `context/`: Company context, brand, messaging and positioning.
  - `context/brand-kit/`
  - `context/docs/`
  - `context/messaging/`
  - `context/positioning/`

### ICP and signal research

- `icp/icp.md`: Ideal Customer Profile research.
- `icp/signals.md`: Buying-signal research and definitions.
- `research/icp/source_register.json`: Source register for ICP research.
- `research/signals/source_register.json`: Source register for buying-signal research.

### System design and workflow

- `architecture.md`: GTM system architecture.
- `workflow.md`: Account qualification, signal detection, routing and prospect preparation workflow.

### Buying personas and operational knowledge

- `knowledge-base/playbooks/personas.md`: Buying-persona definitions and buying-committee research.
- `knowledge-base/learnings/`: Operational learnings.

### Technical implementation

- `tools/`: Python scripts and supporting tools.
  - `tools/gemini_helper.py`: Gemini API helper.
  - `tools/generate_icp.py`: ICP research generation script.
  - `tools/generate_signals.py`: Buying-signal research generation script.
- `retrospective_audit.py`: Retrospective audit script.
- `.env`: Local environment configuration. Never expose its contents.
- `.claude/skills/icp-check/SKILL.md`: Project-specific ICP checking skill.

### Project records and deliverables

- `meetings/`: Meeting records.
- `output/`: Generated deliverables.
- `weekly-priorities/`: Weekly priorities and planning records.
- `work-log/`: Project activity logs and retrospective records.

### Repository and project documentation

- `CLAUDE.md`: Project-level instructions for Claude.
- `README.md`: Project overview and documentation.
- `.gitignore`: Git exclusion rules.
- `.git/`: Git repository metadata. Do not modify Git internals directly.

## 3. Source-of-Truth and Document Responsibilities

Keep the documents aligned without unnecessarily duplicating their responsibilities.

- `icp/icp.md` defines the researched target-customer profile and qualification criteria.
- `icp/signals.md` defines the researched buying signals and supporting evidence.
- `knowledge-base/playbooks/personas.md` defines buying roles, responsibilities and persona research requirements.
- `architecture.md` describes the system's components, relationships and technical design.
- `workflow.md` defines the operational qualification, signal detection, routing and prospect preparation process.
- `research/` preserves source registers and research provenance.
- `tools/` contains the existing technical implementation.
- `knowledge-base/` captures reusable operational knowledge and playbooks.

Read the relevant source documents before changing a dependent document or implementation.

Do not create competing definitions of the ICP, signals, personas, workflow statuses or routing logic.

When a change affects multiple documents, identify the dependencies and update only the documents necessary to maintain consistency.

## 4. Operating Rules

### 4.1 Evidence and research

- Cite verifiable sources for factual claims.
- Distinguish verified facts, inferences, hypotheses and unknowns.
- Preserve source URLs, publication dates, event dates and source identifiers where applicable.
- Do not fabricate evidence, source references, company details, contacts or buying authority.
- Do not treat a search result as verified evidence without checking the underlying source.
- Do not reuse source IDs across research registers without verification.
- Preserve the distinction between an event being announced, planned, ongoing or completed.
- Treat missing evidence as unknown, not automatically as negative evidence.

### 4.2 ICP and account qualification

- Follow the current ICP definition in `icp/icp.md`.
- Do not introduce qualification requirements that are not supported by the approved ICP.
- Keep mandatory qualification conditions separate from prioritisation heuristics.
- Do not allow a detected buying signal to override failed ICP qualification.
- Distinguish `PASS`, `FAIL` and `UNKNOWN` where the workflow requires explicit qualification outcomes.
- Do not classify an account as qualified when mandatory evidence is missing.
- Preserve the distinction between `DISQUALIFIED`, `FURTHER_RESEARCH` and qualified accounts.

### 4.3 Buying signals

- Follow the signal definitions, recency windows and verification requirements in `icp/signals.md` and `workflow.md`.
- A detected signal establishes a reason to investigate, not proof of purchase intent, dissatisfaction or an existing operational problem.
- Do not infer payment friction, provider dissatisfaction or intent to switch from recruitment or expansion announcements alone.
- Verify the event, business attribution, source, dates and current status before treating a signal as confirmed.
- Keep signal detection outcomes separate from account qualification and workflow routing.

### 4.4 Buying personas

- Follow `knowledge-base/playbooks/personas.md`.
- Treat Champion, Economic Buyer and Influencer as buying responsibilities, not fixed job titles.
- Assign personas using verified responsibilities and authority.
- Do not automatically classify the person associated with a vacancy as the Champion.
- Do not infer economic authority from seniority or job title alone.
- Do not invent contact identities, email addresses, reporting lines or decision-making authority.
- Preserve `UNCLASSIFIED` where the available evidence does not support a reliable persona assignment.

### 4.5 System consistency

Keep the ICP, signals, personas, architecture, workflow and technical implementation aligned.

Before changing a definition or rule:

1. Identify its authoritative document.
2. Identify other documents or scripts that depend on it.
3. Check for contradictions with existing decisions.
4. Make the smallest necessary set of changes.
5. Validate consistency after the changes.

Do not silently change approved definitions, identifiers, statuses, variable names, recency windows or routing rules.

### 4.6 Code and technical implementation

- Inspect existing scripts before modifying or recreating them.
- Use the existing Python and Gemini setup where appropriate.
- Load credentials from environment variables.
- Never hardcode, print, expose or commit API keys and secrets.
- Preserve existing data structures, provenance fields and source-register conventions unless a change is necessary and justified.
- Validate generated JSON, file outputs and script behaviour.
- Handle missing data and API failures explicitly.
- Avoid unnecessary dependencies and duplicated functionality.
- Do not overwrite existing research or deliverables without checking their contents and intended use.

### 4.7 Implementation status

Clearly distinguish:

- Researched and documented
- Designed or specified
- Implemented in code
- Configured in an external platform
- Tested and validated
- Operational

A documented workflow is not automatically an implemented workflow.

A proposed Clay workflow, integration, automation or CRM process must not be described as operational until it has actually been configured and tested.

Do not claim successful execution, reliable detection, production readiness or measured performance without supporting evidence.

### 4.8 Workflow and human approval

- Use `workflow.md` as the authoritative reference for account qualification, signal detection, routing and prospect preparation.
- Keep workflow decisions consistent with `architecture.md`.
- Preserve the defined execution order, validation requirements and human-review checkpoints.
- Obtain human approval before executing automated outbound sequences or other external actions.
- Do not contact prospects, publish information or modify external systems without the required authorisation.

### 4.9 Git and file handling

- Preserve existing work and repository history.
- Inspect `git status` before making changes that could affect tracked files.
- Do not modify `.git/` internals directly.
- Respect `.gitignore`.
- Never commit `.env`, credentials or other secrets.
- Avoid unnecessary file creation, renaming or restructuring.
- Validate changes before replacing existing files.
- Do not delete research evidence, logs or previous deliverables without explicit justification and approval.

### 4.10 Writing and documentation

- Use clear, precise and natural language.
- Avoid generic AI-sounding business language.
- Never use em dashes.
- Preserve meaningful technical terminology, identifiers and established project conventions.
- Do not dilute factual claims or invent performance metrics.
- Explain uncertainty and limitations explicitly.
- Prefer precise, actionable documentation over unnecessary verbosity.

## 5. Working Instructions

Before starting a task:

1. Read the relevant project documents and inspect the existing implementation.
2. Identify the authoritative source for the requested change.
3. Check dependencies and existing conventions.
4. Determine whether the task concerns research, documentation, architecture, code or external implementation.
5. Confirm the intended scope before making changes that could affect unrelated project components.

When implementing a task:

1. Preserve existing work.
2. Make only the changes required by the task.
3. Maintain consistency across dependent documents and scripts.
4. Do not introduce unsupported assumptions or functionality.
5. Validate the result against the original requirement.

When completing a task, report:

- **Changed:** Files and specific sections modified.
- **Validation:** Checks performed and their results.
- **Unchanged:** Relevant files or sections deliberately left untouched.
- **Outstanding:** Incomplete work, dependencies or required human decisions.
- **Assumptions and limitations:** Anything that could affect the reliability or interpretation of the result.

Do not claim a task is complete merely because files have been edited. Completion requires validation against the requested outcome.
