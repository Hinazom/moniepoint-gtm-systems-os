# Moniepoint GTM Systems OS

An evidence-led GTM Engineering project exploring how business intelligence, Ideal Customer Profile (ICP) research, buying signals, company enrichment and structured workflows can support customer acquisition for Moniepoint Business Banking and Payments in Nigeria.

**Market:** Nigeria  
**Product Focus:** Business banking, merchant payments, collections and settlements  
**Primary Campaign Cohort:** FMCG distributors, petrol station networks and retail chains/supermarkets  
**Project Status:** Research automation, ICP and signal intelligence completed; integrated GTM system under development

## Project Overview

The objective is to design and progressively implement an integrated GTM intelligence and execution system for identifying, researching, qualifying and prioritising businesses with potential banking and payment needs.

The system connects market research, account intelligence, observable business developments, company and contact enrichment, qualification workflows and CRM automation to produce evidence-backed prospect recommendations and structured sales preparation.

The project is organised around:

- Market and ICP research
- Segment-specific business qualification
- Buying-signal identification and verification
- Company and source enrichment
- Account prioritisation and routing
- Decision-maker and buying-committee research
- CRM integration and lifecycle management
- Workflow automation
- Prospect preparation and human review

The architecture separates ICP qualification from buying-signal detection. A business must first meet the applicable ICP requirements before its buying signals influence account prioritisation.

## ICP and Campaign Scope

The market research process investigates a broad range of Nigerian business sectors to identify commercially relevant opportunities for Moniepoint.

The approved ICP defines seven segments across three priority classifications.

| Priority  | Approved Segments                              |
| --------- | ---------------------------------------------- |
| Primary   | FMCG distributors and wholesalers              |
| Primary   | Petrol station networks                        |
| Primary   | Retail chains and supermarkets                 |
| Secondary | Quick-service restaurant groups                |
| Secondary | Pharmacy chains                                |
| Emerging  | Logistics and haulage businesses               |
| Emerging  | Specialised healthcare and diagnostic networks |

The primary campaign cohort consists of the three primary segments. Secondary and emerging segments remain within the approved research universe but are not automatically included in the primary campaign.

The project distinguishes between:

- **ICP fit:** Whether a business meets the applicable customer qualification criteria.
- **Buying signals:** Observable developments that may indicate a relevant commercial opportunity.
- **Prioritisation:** How qualified accounts are ranked using their evidence, signals and commercial relevance.
- **Contact readiness:** Whether sufficient company and decision-maker information exists to prepare a prospect for human review.

A missing public buying signal does not automatically disqualify an otherwise qualified business.

## Buying-Signal Framework

The preferred buying signal is **FINANCE_RECRUITMENT**, with **MULTI_BRANCH_EXPANSION** as a supporting signal.

The workflow investigates finance and treasury recruitment as a potential indicator of changing financial-management requirements, organisational complexity or investment in financial controls.

Expansion is treated as supporting context. New branches, stations, depots and outlets may increase the relevance of a finance recruitment signal, but expansion alone does not establish purchasing intent.

Signal detection, evidence verification, confidence assessment and account routing are treated as separate steps.

## Planned System Capabilities

The intended system extends beyond research automation into an integrated GTM intelligence and execution workflow.

The complete system is designed to connect:

1. **Market and ICP Intelligence:** Identify commercially relevant business segments and define evidence-backed account qualification criteria.
2. **Buying-Signal Intelligence:** Detect and assess observable business developments, including finance recruitment and multi-branch expansion.
3. **Company Enrichment:** Build structured company records using public business information and enrichment providers.
4. **Account Qualification:** Evaluate businesses against the approved ICP, applicable segment requirements and exclusion criteria.
5. **Signal Assessment and Prioritisation:** Associate verified buying signals with qualified accounts and determine their relative commercial priority.
6. **Audience Segmentation and Routing:** Classify accounts and route them through workflows according to ICP fit, signal evidence and qualification status.
7. **Decision-Maker Enrichment:** Identify relevant economic buyers, finance stakeholders and other members of the buying committee.
8. **CRM Integration:** Transfer approved account and contact records into HubSpot and organise them within a structured sales pipeline.
9. **Workflow Automation:** Connect Clay, HubSpot and n8n to support enrichment, qualification, record updates and workflow execution.
10. **Sales Preparation and Human Review:** Produce structured prospect intelligence and support controlled progression towards sales engagement.

These capabilities describe the intended end-to-end system. Their implementation is tracked separately below.

## Repository Structure

| File / Directory    | Purpose                                                                           |
| ------------------- | --------------------------------------------------------------------------------- |
| `CLAUDE.md`         | Project context and operating instructions                                        |
| `icp/`              | Approved ICP definitions and buying-signal research                               |
| `icp/icp.md`        | Market and segment-level ICP research                                             |
| `icp/signals.md`    | Buying-signal research, evidence assessment and detection framework               |
| `research/`         | Structured research evidence and source registers                                 |
| `research/icp/`     | ICP research source register and coverage data                                    |
| `research/signals/` | Buying-signal research source register                                            |
| `tools/`            | Python research and automation scripts                                            |
| `architecture.md`   | Overall GTM systems architecture                                                  |
| `workflow.md`       | Account qualification, signal detection, prioritisation and routing specification |
| `personas.md`       | Buying roles and decision-maker definitions                                       |
| `.claude/skills/`   | Project-specific research and ICP evaluation skills                               |
| `work-log/`         | Chronological project activity records                                            |

## Research and Automation

The current Python research scripts automate parts of the market and buying-signal research process.

### Market and ICP Research

The ICP research script uses:

- DuckDuckGo Search (`DDGS`) for public-source discovery.
- Trafilatura for webpage retrieval and text extraction.
- Gemini 3.1 Flash Lite for evidence-assisted research synthesis.
- JSON for structured source registration.
- Markdown for the resulting ICP research document.

It investigates multiple Nigerian business sectors rather than assuming the initial campaign segments are the only commercially viable opportunities.

The process records source URLs, research queries, retrieval timestamps, evidence types, extraction outcomes, research coverage and search failures.

### Buying-Signal Research

The buying-signal research script reads the approved `icp/icp.md` document as its authoritative campaign definition.

It investigates observable developments across all seven approved ICP segments and generates `icp/signals.md`.

Its research areas include:

- Finance, treasury and accounting recruitment.
- New branches, stations, depots and facilities.
- Business expansion and acquisitions.
- Supplier and distribution agreements.
- Payment infrastructure changes.
- Financial-management and reconciliation developments.
- Working-capital and operational changes.

The script preserves source evidence and distinguishes extracted webpage content from search-snippet-only evidence.

### Evidence Management

Both research processes maintain structured source registers to support traceability and subsequent validation.

Research outputs are saved as Markdown, while source metadata and evidence are retained in JSON.

The research automation supports evidence discovery and synthesis. It does not independently establish that every generated finding is correct. Material claims and company-level signals require source validation.

## Technology

- Python
- Gemini API
- Gemini 3.1 Flash Lite
- DuckDuckGo Search (`DDGS`)
- Trafilatura
- JSON
- Markdown
- Git and GitHub
- Clay
- HubSpot
- n8n

Clay, HubSpot and n8n form part of the intended system implementation. Their integration and operational status are tracked in the implementation table below.

## Current Implementation

The project currently includes:

- Automated public-source discovery across multiple Nigerian business sectors.
- Webpage extraction and search-snippet fallback.
- Structured ICP research and source registration.
- Gemini-assisted market and buying-signal research synthesis.
- Evidence coverage reporting and source provenance.
- An approved seven-segment ICP structure.
- A documented buying-signal research framework.
- A documented GTM systems architecture.
- An account qualification and routing workflow specification.

The Python scripts currently automate research discovery, extraction, source registration and research synthesis. They form the research foundation for the broader account-level system.

The complete account-level GTM workflow is not yet implemented as an automated production system. Clay enrichment, automated account qualification and prioritisation, decision-maker enrichment, CRM integration and workflow orchestration are being developed through the programme's subsequent deliverables.

## Implementation Status

The project is being developed incrementally through the programme's weekly deliverables.

| Component                                        | Current Status |
| ------------------------------------------------ | -------------- |
| GitHub repository and Context OS                 | Completed      |
| ICP and market research automation               | Implemented    |
| Buying-signal research automation                | Implemented    |
| ICP, signals and architecture documentation      | Documented     |
| Account-level Clay enrichment                    | Pending        |
| Clay audience segmentation and routing workflow  | Pending        |
| HubSpot pipeline and lifecycle workflow          | Pending        |
| n8n automation connected to Clay                 | Pending        |
| Integrated GTM playbook and system demonstration | Pending        |

The Python research scripts currently automate public-source discovery, webpage extraction, evidence registration and Gemini-assisted research synthesis. They form the research foundation for the broader account-level system.

Clay, HubSpot and n8n will provide the enrichment, qualification, routing, CRM and orchestration capabilities as the implementation progresses.

**The distinction is deliberate:** the architecture defines the complete intended system, while the implementation status records what has actually been built and validated.

## System Design Principles

- **Evidence before assumptions:** Material company claims must be supported by traceable evidence.
- **ICP before intent:** Establish account eligibility before using buying signals to prioritise it.
- **Separate facts from inference:** Distinguish verified facts, reasonable inferences, hypotheses and unknown information.
- **Preserve research provenance:** Retain source URLs, evidence types, retrieval information and research limitations.
- **Validate company attribution:** Associate signals with the correct company, operating entity, subsidiary or parent organisation.
- **Control false positives:** Account for stale vacancies, unverified expansion announcements, syndicated reporting and misleading signals.
- **Do not confuse absence of evidence with negative evidence:** An undetected signal is not proof that a business lacks the underlying need.
- **Human approval before engagement:** Research automation must not independently authorise external sales engagement.
- **Separate proposed architecture from implemented functionality:** Documented future capabilities must not be presented as operational integrations.

## Project Objective

Build a repeatable GTM intelligence system that turns public business information into structured account research, evidence-backed qualification, buying-signal assessment, audience segmentation, decision-maker intelligence and sales-ready prospect preparation.

The intended outcome is a system that helps identify not simply which businesses resemble Moniepoint's target customers, but which qualified businesses have observable developments that make them more relevant to a commercial conversation.

**Repository:** [GitHub: Moniepoint GTM Systems OS](https://github.com/Hinazom/moniepoint-gtm-systems-os)
