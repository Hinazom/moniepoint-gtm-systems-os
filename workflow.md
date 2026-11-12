# Workflow: Account Qualification and Prospect Preparation

## 1. Workflow Objective

Turn a newly discovered Nigerian business into an evidence-backed, qualified prospect for Moniepoint Business Banking and Payments.

The workflow assesses whether the business fits the target customer profile, identifies relevant buying signals, prioritises the account and prepares it for human review.

The workflow does not automatically contact prospects or assume that a company intends to change its banking provider.

## 2. Trigger

A new business is identified through company websites, business directories, industry publications, expansion announcements or other public sources.

The company is added to the account research queue.

## 3. Required Inputs

- Company name
- Company website, where available
- Industry and business model
- Headquarters and operating locations
- Available information about branches, outlets, warehouses or distribution facilities
- Publicly observable expansion or recruitment activity
- Source URLs and publication dates

Missing information must be recorded as unknown rather than assumed.

## 4. Workflow Steps

### Step 1: Account discovery

Identify a Nigerian business within one of the target segments:

- Supermarket and retail chains
- FMCG distributors
- Wholesale and distribution businesses
- Fuel and service station operators
- Other commercially relevant businesses

Capture the company name, website, industry and discovery source.

### Step 2: Initial ICP screening

Assess whether the business has a potentially relevant business model.

Check:

- Does it operate in a target industry?
- Does it have physical commercial operations?
- Does its business model potentially involve recurring payment collection or complex financial operations?
- Does it operate in Nigeria?

Decision:

- Potential fit: proceed to enrichment.
- Outside target profile: disqualify with a reason.
- Insufficient information: send for further research.

### Step 3: Company enrichment

Collect additional company information from publicly available sources.

Research:

- Number of operating locations, where verifiable.
- Geographic footprint.
- Business size indicators.
- Distribution facilities and warehouses.
- Business expansion.
- Finance, treasury and operations recruitment.
- Available evidence of payment collection and financial operations.

Record the source and date for each material finding.

### Step 4: Buying-signal assessment

Check for relevant developments:

- Finance or treasury recruitment.
- New branches or geographic expansion.
- Warehouse, logistics or operations recruitment.
- Other developments that may indicate increasing operational complexity.

For every detected signal, record:

- Signal type.
- Supporting evidence.
- Source URL.
- Publication date.
- Recency.
- Relevance to the potential Moniepoint opportunity.
- Confidence level.

A buying signal is an indicator of potential relevance, not proof of purchase intent.

### Step 5: ICP qualification

Assess the company's overall commercial and operational fit independently of its buying signals.

Consider:

- Industry and business model.
- Physical footprint.
- Transaction characteristics.
- Financial and operational complexity.
- Potential relevance of verified Moniepoint products and services.

Assign:

- ICP fit score: 1–10.
- Qualification outcome: Qualified, Disqualified or Further Research Required.
- Written rationale supported by evidence.

The absence of a buying signal does not automatically disqualify an otherwise suitable business.

### Step 6: Account prioritisation

Prioritise qualified accounts using:

- ICP fit.
- Operational complexity.
- Relevant buying signals.
- Signal recency.
- Evidence quality.
- Potential commercial relevance.

Record the priority and explain why the account deserves attention.

### Step 7: Buyer identification

Identify relevant decision-makers using publicly available company information.

Potential roles include:

- Founder or Managing Director.
- Chief Financial Officer.
- Head of Finance.
- Treasury Manager.
- Financial Controller.

Record the person's name, role, company and source where verified.

Do not invent contact details or assume that a particular role controls purchasing decisions.

### Step 8: Prospect preparation

Prepare a structured prospect record containing:

| Field          | Description                                 |
| -------------- | ------------------------------------------- |
| Company        | Business name                               |
| Website        | Company website                             |
| Industry       | Business sector                             |
| Locations      | Verified operating footprint                |
| ICP score      | Score from 1–10                             |
| Qualification  | Qualified, Disqualified or Further Research |
| Buying signals | Detected signals and evidence               |
| Priority       | Account priority                            |
| Buyer          | Identified decision-maker, if available     |
| Evidence       | Supporting source URLs and dates            |
| Rationale      | Reason for qualification and prioritisation |
| Research gaps  | Information still requiring verification    |

Clay is the proposed environment for organising and enriching these prospect records. Its integrations, data sources and automation steps must be configured and tested before the workflow can be described as operational.

### Step 9: Human review and approval

A human reviewer checks:

- Company identity and relevance.
- Accuracy of enrichment data.
- ICP qualification and scoring.
- Buying-signal interpretation.
- Buyer identification.
- Evidence quality.
- Recommended next action.

Decision:

- Approved: prospect is ready for CRM entry or outbound preparation.
- Further research: return the record for additional verification.
- Rejected: retain the reason for rejection.

No automated outbound activity takes place before approval.

## 5. Workflow Output

The final output is an approved, evidence-backed prospect record containing:

- Company information.
- ICP qualification and score.
- Buying signals.
- Account priority.
- Identified decision-maker, where available.
- Evidence and source references.
- Recommended next action.

The approved record is ready for downstream CRM entry or outbound activation.

## 6. Exception Handling

| Situation                       | Action                                       |
| ------------------------------- | -------------------------------------------- |
| Company cannot be verified      | Hold for further research                    |
| Branch count unavailable        | Record as unknown                            |
| Conflicting company information | Flag for verification                        |
| No buying signals detected      | Continue ICP assessment                      |
| Weak or outdated evidence       | Lower confidence or request further research |
| No decision-maker identified    | Retain the account and flag the contact gap  |
| Company does not fit the ICP    | Disqualify with a documented reason          |

## 7. Implementation Status

**Workflow specification:** Defined.

**Existing implementation:** Python scripts currently support public-source research, webpage extraction and AI-assisted ICP and signal documentation.

**Proposed implementation:** Account-level discovery, enrichment, qualification, prioritisation and prospect preparation using Clay and supporting tools.

**Not yet implemented:** A fully automated account-level workflow, tested Clay integrations, human approval interface and CRM or outbound activation.

The workflow should only be described as operational after its individual steps have been configured and tested.
