# Moniepoint GTM Systems OS

## Project Context

Build a GTM system for identifying, researching, qualifying and prioritising potential business customers for Moniepoint Business Banking and Payments in Nigeria.

The research currently focuses on retail chains, FMCG distributors and other businesses with potentially complex financial and operational requirements.

Treat ICP definitions, buying signals and customer pain points as research findings or hypotheses, not established facts. Verify Moniepoint product capabilities against authoritative sources.

## Project Structure

- `context/`: Company context, brand, positioning and messaging.
- `icp/icp.md`: Ideal Customer Profile research.
- `icp/signals.md`: Buying-signal research.
- `architecture.md`: GTM system architecture.
- `workflow.md`: Account qualification and prospect preparation workflow.
- `research/`: Research source registers and evidence.
- `tools/`: Python scripts and Gemini API helpers.
- `.claude/skills/`: Project-specific AI skills.
- `knowledge-base/`: Operational learnings and playbooks.
- `meetings/`: Meeting records.
- `output/`: Generated deliverables.
- `weekly-priorities/`: Weekly priorities.
- `work-log/`: Project activity logs.

Read relevant project documents before performing tasks. Do not recreate existing files unnecessarily.

## Operating Rules

- **Evidence:** Cite verifiable sources for factual claims. Distinguish facts, inferences and hypotheses.
- **Research:** Preserve source URLs, dates and source identifiers. Do not fabricate evidence or reuse source IDs across research registers without verification.
- **Consistency:** Keep the ICP, signals, architecture and implementation aligned.
- **Code:** Use the existing Python and Gemini setup. Load credentials from environment variables. Never hardcode or expose API keys.
- **File handling:** Preserve existing work. Validate generated outputs before replacing files.
- **Implementation status:** Distinguish implemented functionality from proposed workflows and integrations. Do not describe a proposed Clay workflow as operational until it has been configured and tested.
- **Workflow:** Use `workflow.md` as the reference for the account qualification and prospect preparation process. Keep workflow decisions consistent with `architecture.md`.
- **Human approval:** Obtain approval before executing automated outbound sequences or external actions.
- **Writing:** Use clear, natural language. Never use em dashes.

## Working Instructions

Before making changes, inspect relevant files, understand existing implementations and identify dependencies.

When completing a task, validate the result and report what changed, what remains incomplete and any assumptions or limitations.
