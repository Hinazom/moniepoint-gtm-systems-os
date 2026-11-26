# Moniepoint Business Banking & Payments

# GTM Signal Detection and Account Routing Workflow

## 1. Workflow Status Line

**STATUS:** Clay implementation specification | **MARKET:** Nigeria | **PREFERRED SIGNAL:** `FINANCE_RECRUITMENT` | **SECONDARY SIGNAL:** `MULTI_BRANCH_EXPANSION` | **ICP GATE:** Approved ICP qualification before signal-based prioritisation | **DELIVERY TARGET:** 100 production-grade enriched company records | **OUTPUT:** Evidence-backed, enriched and commercially routed accounts ready for human review.

| Attribute                         | Specification                                                            |
| --------------------------------- | ------------------------------------------------------------------------ |
| Workflow name                     | Moniepoint Business Banking and Payments GTM Signal Workflow             |
| Workflow status                   | Clay implementation specification                                        |
| Preferred automated signal        | `FINANCE_RECRUITMENT`                                                    |
| Supporting signal                 | `MULTI_BRANCH_EXPANSION`                                                 |
| Primary ICP segments              | FMCG Distributors, Petrol Station Networks, Retail Chains (Supermarkets) |
| Secondary ICP segments            | QSR Groups, Pharmacy Chains                                              |
| Emerging ICP segments             | Logistics/Haulage, Specialized Healthcare/Diagnostic Networks            |
| Market                            | Nigeria                                                                  |
| Commercial themes                 | Instant settlement, working capital, multi-location financial management |
| Research and preparation stack    | Python, DDGS, Trafilatura and Gemini API free tier                       |
| Execution and enrichment platform | Clay                                                                     |
| ICP authority                     | `icp/icp.md`                                                             |
| Signal authority                  | `icp/signals.md`                                                         |
| Workflow authority                | This document                                                            |
| Final production target           | 100 qualified, signal-verified and enriched company records              |

**Operating rule:** Finance recruitment is the principal detection and routing signal. Multi-branch expansion provides a supporting signal that can strengthen account prioritisation or independently support a segment-specific commercial angle. Neither signal can override ICP qualification.

**Delivery rule:** The target is 100 production-grade company records, not 20. Discovery results, incomplete research records, unverified signals and unqualified businesses do not count towards this target.

---

## 2. Mother Intent

Identify Nigerian businesses within Moniepoint's approved ICP that are investing in financial oversight or expanding their operations, then use those observable developments to identify credible opportunities for commercial conversations about business banking and payments.

The preferred signal, `FINANCE_RECRUITMENT`, identifies businesses recruiting for finance, treasury, financial control or related responsibilities. These vacancies can indicate investment in financial oversight and may provide a relevant reason to investigate how the business manages:

- Collections and cash management.
- Cash, POS and transfer reconciliation.
- Treasury and supplier-payment operations.
- Financial control across operating locations.
- Working-capital coordination.
- Consolidated financial reporting.

`MULTI_BRANCH_EXPANSION` provides supporting evidence of operational change. It helps establish whether the business is adding locations, distribution capacity or other infrastructure that could increase financial coordination requirements.

**The intended output is not a list of companies with finance vacancies or expansion announcements. It is a pipeline of 100 ICP-qualified company accounts with independently verified events, enriched company information, relevant buying-role research and a defensible commercial angle.**

### 2.1 Delivery target

The final workbook must contain at least 100 production-grade enriched company records.

The target applies to company accounts, not contacts, job vacancies, locations or duplicate company records.

The 100 accounts must:

1. Belong to one of the seven approved ICP segments.
2. Have verified Nigerian operating presence.
3. Pass all applicable mandatory segment-specific ICP requirements.
4. Have an identifiable company and operating entity.
5. Have at least one independently verified selected buying signal.
6. Have traceable ICP and signal evidence.
7. Have completed company enrichment.
8. Have a segment-specific commercial angle.
9. Have relevant buying-role research attempted and its outcome recorded.
10. Be available for human review.

The preferred signal remains `FINANCE_RECRUITMENT`. However, a qualified account with independently verified `MULTI_BRANCH_EXPANSION` can count towards the production target even if finance recruitment is not detected.

Accounts with neither verified signal remain useful research records but do not count towards the 100 production-grade target.

### 2.2 Research and execution boundaries

The workflow uses the following division of responsibility:

| Component            | Responsibility                                                                                          | Implementation                                        |
| -------------------- | ------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| Python               | Research orchestration, preparation, deduplication, validation and data handling                        | Existing local Python environment                     |
| DDGS                 | Public web discovery and search                                                                         | Existing Python research scripts                      |
| Trafilatura          | Extracting relevant text from accessible public web pages                                               | Existing Python research scripts                      |
| Gemini API free tier | Research assistance, structured extraction and classification                                           | Existing API integration, subject to free-tier limits |
| Clay                 | Company tables, enrichment, signal research, contact research, classification, segmentation and routing | Clay workbook                                         |
| Human review         | Evidence validation, commercial judgement and outreach approval                                         | Manual review                                         |

The existing Python research scripts generate ICP and signal intelligence documentation. They must not be represented as an already operational 100-account qualification or signal-detection engine.

Clay is the primary execution environment for the Week 2 company enrichment deliverable.

No Claude Code subscription, paid Gemini API plan, paid search API or additional automation platform is a prerequisite for implementing this workflow.

---

## 3. ICP Filter

### 3.1 Approved ICP scope

The workflow must cover all seven segments defined in `icp/icp.md`, retaining their original priority classifications.

| Priority  | Segment                                        | Segment code             | ICP qualification basis                                                                  |
| --------- | ---------------------------------------------- | ------------------------ | ---------------------------------------------------------------------------------------- |
| PRIMARY   | FMCG Distributors and Wholesalers              | `FMCG_DISTRIBUTOR`       | Multiple depots or significant warehousing, plus trade receivables or credit-based sales |
| PRIMARY   | Petrol Station Networks                        | `PETROL_STATION_NETWORK` | Owns or manages at least 3 stations and performs daily cash/POS reconciliation           |
| PRIMARY   | Retail Chains (Supermarkets)                   | `RETAIL_SUPERMARKET`     | Verifiable supermarket chain and attributable branch network                             |
| SECONDARY | Quick-Service Restaurant Groups                | `QSR_GROUP`              | Verifiable QSR group operating model                                                     |
| SECONDARY | Pharmacy Chains                                | `PHARMACY_CHAIN`         | Verifiable pharmacy chain operating model                                                |
| EMERGING  | Logistics and Haulage                          | `LOGISTICS_HAULAGE`      | Relevant commercial logistics, fleet or haulage operations                               |
| EMERGING  | Specialized Healthcare and Diagnostic Networks | `HEALTHCARE_DIAGNOSTICS` | Verifiable private healthcare or diagnostic operating network                            |

The segment priority determines the account's campaign priority. It does not establish qualification by itself.

The 100-company target must not be achieved by changing the approved ICP, weakening its qualification requirements or inventing additional numerical thresholds.

### 3.2 Mandatory account-level ICP filter

Every account must pass the general qualification checks and the applicable segment-specific requirements.

| Filter                        | Qualification rule                                                                    | Evidence required                                                                    | Decision if unresolved or failed                                        |
| ----------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ | ----------------------------------------------------------------------- |
| Nigerian operating presence   | A Nigerian operating entity or verifiable Nigerian operating presence must exist      | Company website, operating address, corporate profile or credible business reporting | `RESEARCH_REQUIRED` until established; `DISQUALIFIED` if absent         |
| Business identity             | The business and relevant operating entity must be identifiable                       | Company name, website, legal/trading identity and entity relationship                | `RESEARCH_REQUIRED`                                                     |
| Approved segment              | The actual operating model must fit one of the seven approved segments                | Business activities, products, services and operating model                          | `OUT_OF_SCOPE` if outside approved segments                             |
| Active operations             | The business must be operational                                                      | Current operating activity, locations or credible recent evidence                    | `DISQUALIFIED` if dormant, inactive or permanently closed               |
| Segment-specific requirements | Applicable mandatory ICP requirements must be satisfied                               | Segment-specific evidence                                                            | `RESEARCH_REQUIRED` until verified; `DISQUALIFIED` if requirements fail |
| Operating complexity          | The business must have the operating characteristics relevant to its approved segment | Evidence of the actual operating model                                               | Do not assume complexity from industry classification alone             |

**Qualification decision:**

- `QUALIFIED`: General and applicable segment-specific requirements are verified.
- `RESEARCH_REQUIRED`: The business may fit, but evidence is incomplete.
- `DISQUALIFIED`: A mandatory qualification requirement fails or an anti-ICP exclusion applies.
- `OUT_OF_SCOPE`: The business does not belong to an approved ICP segment.

Only `QUALIFIED` accounts enter the qualified signal-prioritisation pipeline.

### 3.3 Segment-specific qualification rules

**A. FMCG Distributors and Wholesalers**

Both requirements are mandatory:

1. Multiple depots or significant warehousing.
2. Trade receivables or a credit-based sales model.

Relevant evidence includes depot or warehouse operations, distribution activity, trade credit arrangements and business descriptions.

Trading activity alone is insufficient.

**B. Petrol Station Networks**

Both requirements are mandatory:

1. Ownership or management of at least three petrol stations.
2. Daily cash/POS reconciliation.

Verify the stations and their relationship to the operating company. A single station does not qualify under this segment.

**C. Retail Chains (Supermarkets)**

The business must be a verifiable supermarket chain with an attributable branch network.

Do not qualify an ordinary retail business solely because it sells consumer goods. Do not invent a numerical minimum branch count because the approved ICP does not specify one.

**D. QSR Groups**

Verify that the business operates as a QSR group. A single restaurant or unrelated collection of food businesses does not automatically establish group-level operating complexity.

**E. Pharmacy Chains**

Verify that the business operates as a pharmacy chain. A single independent pharmacy does not automatically qualify.

**F. Logistics and Haulage**

Verify relevant commercial logistics, fleet or haulage operations. Industry membership alone is insufficient.

**G. Specialized Healthcare and Diagnostic Networks**

Verify a private operating entity and its relevant healthcare or diagnostic network operations. A public-sector infrastructure project without a qualifying private commercial operator does not qualify.

For segments where `icp/icp.md` does not establish numerical thresholds or additional mandatory conditions, this workflow must not invent them.

### 3.4 Anti-ICP exclusions

| Exclusion                                                                                               | Decision                                                                       |
| ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| Single-location microbusiness without evidence of meaningful scale or operational complexity            | `DISQUALIFIED`, unless documented evidence establishes relevant commercial fit |
| Informal sole proprietor without demonstrable financial infrastructure or relevant operating complexity | `DISQUALIFIED`, unless additional evidence establishes fit                     |
| Petrol station with fewer than three stations                                                           | `DISQUALIFIED` from `PETROL_STATION_NETWORK`                                   |
| FMCG trader without significant warehousing or distribution operations                                  | `DISQUALIFIED` unless the mandatory FMCG requirements are verified             |
| Retail business without a verifiable supermarket branch network                                         | `DISQUALIFIED` from `RETAIL_SUPERMARKET`                                       |
| Announced but unverified expansion                                                                      | `RESEARCH_REQUIRED`; announcement alone does not establish qualification       |
| Dormant, inactive or permanently closed business                                                        | `DISQUALIFIED`                                                                 |
| No verifiable Nigerian operating entity                                                                 | `DISQUALIFIED` if the operating entity cannot be established                   |
| Public-sector infrastructure project without a qualifying private operating entity                      | `DISQUALIFIED` from private-sector targeting                                   |
| Business outside the approved ICP segments                                                              | `OUT_OF_SCOPE`                                                                 |

### 3.5 ICP safeguards

- Finance recruitment cannot substitute for mandatory ICP qualification.
- A missing finance contact does not disqualify an otherwise qualified account.
- Lack of public evidence of payment friction is not evidence that payment friction does not exist.
- An expansion announcement is not proof of completed expansion.
- Industry classification is not proof of the required operating model.
- ICP qualification does not establish Moniepoint product suitability, credit eligibility or purchase intent.

---

## 4. Preferred Signal and Supporting Signal

### 4.1 Signal selection

The initial workflow is designed around `FINANCE_RECRUITMENT`.

| Selection  | Signal code              | Workflow role                                             | Strategic justification                                                                                                                         |
| ---------- | ------------------------ | --------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| PREFERRED  | `FINANCE_RECRUITMENT`    | Primary detection, verification and routing signal        | Strong data accessibility and a credible commercial conversation around financial oversight; buying reason and volume were assessed as moderate |
| SUPPORTING | `MULTI_BRANCH_EXPANSION` | Secondary detection, enrichment and prioritisation signal | Strong buying reason and natural commercial story, with moderate volume and detection reliability                                               |

The four-test assessment is a strategic evaluation from `icp/signals.md`, not measured conversion performance.

### 4.2 Signals table

| Signal                   | Observable event                                                                                   | ICP relevance                                                      | Detection requirements                                         | Verification requirements                                                                                   | Commercial interpretation                                                                  |
| ------------------------ | -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ | -------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| `FINANCE_RECRUITMENT`    | Current finance, treasury, financial control, accounting or relevant finance operations vacancy    | All approved segments                                              | Detect relevant vacancies and identify the advertised employer | Verify employer, vacancy status, responsibilities, seniority and connection to relevant financial workflows | Possible investment in financial oversight and finance operations                          |
| `MULTI_BRANCH_EXPANSION` | New branch, station, warehouse, depot, diagnostic centre or other segment-specific expansion event | All approved segments, using the event appropriate to each segment | Detect segment-specific operating expansion                    | Verify event, operating entity, attribution, operational status and location growth where applicable        | Possible increase in collections, reconciliation and multi-location financial coordination |

### 4.3 Preferred signal specification: `FINANCE_RECRUITMENT`

**Purpose:** Detect ICP-qualified businesses recruiting for finance responsibilities that may indicate investment in financial oversight or increasing financial-operational complexity.

**Role detection terms:**

- Finance Manager
- Financial Controller
- Treasury Manager
- Head of Finance
- Group Accountant
- Finance Operations Manager
- Treasury Lead
- Relevant accounting, reconciliation and internal-audit positions

A job title alone is insufficient. The responsibilities must be assessed.

**Relevant responsibilities include:**

- Treasury management.
- Cash management.
- Collections.
- Reconciliation.
- Financial control.
- Multi-location financial reporting.
- Supplier payments.
- Finance operations.

**Verification procedure:**

1. Identify the vacancy and advertised employer.
2. Verify that the employer is the target operating company or an attributable group entity.
3. Confirm that the vacancy is current.
4. Extract the advertised title and responsibilities.
5. Record seniority and functional relevance.
6. Determine whether the position appears newly created or replacement-based, where evidence permits.
7. Assess whether the responsibilities relate to the ICP's financial workflows.
8. Capture the source URL, publication date where available and detection date.

**Signal interpretation:**

A relevant finance vacancy may indicate that the company is strengthening financial oversight. It does not establish:

- Intent to change banking providers.
- Dissatisfaction with an existing payment provider.
- A settlement problem.
- A need for working-capital credit.
- Purchasing authority held by the advertised role.
- An immediate buying decision.

**False-positive controls:**

- Routine replacement accounting roles must not automatically be treated as growth signals.
- Generic finance vacancies without relevant responsibilities must not be classified as strong signals.
- Recruitment-agency advertisements must be attributed to the actual employer.
- A finance vacancy does not prove that the role is newly created.

### 4.4 Supporting signal specification: `MULTI_BRANCH_EXPANSION`

**Purpose:** Detect operational expansion that may strengthen the commercial relevance of a finance-recruitment signal or independently provide a credible reason to investigate financial coordination requirements.

| Segment                 | Segment-specific expansion events                                                                                           |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| FMCG Distributors       | New warehouse or depot commissioning; geographic distribution expansion; new regional distribution operations               |
| Petrol Station Networks | New station commissioning; additional operating stations; CNG/EV infrastructure investment; non-fuel retail diversification |
| Retail Chains           | New supermarket branches; geographic expansion                                                                              |
| QSR Groups              | Multi-outlet expansion; new operating restaurant locations                                                                  |
| Pharmacy Chains         | Pharmacy acquisitions; new pharmacy locations                                                                               |
| Logistics/Haulage       | Fleet expansion; new haulage contracts or relevant operational expansion                                                    |
| Healthcare/Diagnostics  | New diagnostic centres; new healthcare operating locations                                                                  |

Not every event in this table is a branch opening. CNG/EV investment, acquisitions, fleet expansion and new haulage contracts must retain their actual event classification. They must not automatically be represented as an increase in branch count.

**Verification procedure:**

1. Identify the reported event.
2. Establish the operating company's identity.
3. Verify that the event is attributable to the target account.
4. Distinguish completed or operational events from proposals and announcements.
5. Capture previous and current location counts where available and applicable.
6. Record the event date, source URL and detection date.
7. Record the actual event type.

**False-positive controls:**

- An announcement is not proof of an operational opening.
- A franchisee or third-party location must not automatically be attributed to the parent company.
- A vendor announcement must not be confused with independently verified customer deployment.
- A new contract or investment must not automatically be interpreted as a new physical location.
- CNG/EV investment does not establish liquidity shortage or credit demand.

### 4.5 Signal evaluation framework

Retain the four evaluation dimensions from `icp/signals.md`.

| Test                | Question                                  | Operational use                                                                                              |
| ------------------- | ----------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Clear buying reason | Why now?                                  | Determine whether the event provides a credible reason to investigate a financial or operational requirement |
| Enough volume       | Is there enough potential account volume? | Assess whether the signal can support repeatable account discovery                                           |
| Data you can get    | Can the event be detected?                | Assess source accessibility and verification feasibility                                                     |
| A natural story     | Can the event support a credible opener?  | Establish whether the event provides a relevant commercial conversation angle                                |

These assessments guide signal selection. They are not account-level proof of demand or conversion probability.

---

## 5. Signal Decision and Account Prioritisation

### 5.1 Signal decision rules

The workflow evaluates the two signals independently.

| Detected evidence                                   | Decision                          | Treatment                                                                                      |
| --------------------------------------------------- | --------------------------------- | ---------------------------------------------------------------------------------------------- |
| Verified finance recruitment only                   | `FINANCE_ONLY`                    | Preferred-signal account; route using the finance-recruitment angle                            |
| Verified expansion only                             | `EXPANSION_ONLY`                  | Supporting-signal account; route using the segment-specific expansion angle                    |
| Both signals independently verified                 | `BOTH`                            | Higher research priority; investigate whether finance responsibilities relate to the expansion |
| Neither selected signal detected                    | `NONE`                            | Retain as ICP-qualified; do not present as signal-qualified                                    |
| Signal detected but not attributable to the account | `RESEARCH_REQUIRED`               | Do not route as verified                                                                       |
| Signal detected but event cannot be verified        | `RESEARCH_REQUIRED` or `REJECTED` | Resolve the evidence gap or reject the event                                                   |
| Signal detected at an ICP-disqualified account      | No qualified routing              | Preserve research evidence if useful, but exclude from qualified pipeline                      |

### 5.2 Prioritisation hierarchy

1. Primary ICP account with both independently verified signals.
2. Primary ICP account with verified `FINANCE_RECRUITMENT`.
3. Primary ICP account with verified `MULTI_BRANCH_EXPANSION`.
4. Secondary ICP account with one or both verified signals.
5. Emerging ICP account with one or both verified signals.
6. ICP-qualified account with no selected signal.
7. Accounts with unresolved ICP or signal evidence remain in a research queue.

This hierarchy establishes research priority. It does not claim that one account is more likely to purchase.

### 5.3 Signal confidence

Signal confidence must be recorded separately from ICP qualification and account priority.

| Confidence   | Meaning                                                                                   |
| ------------ | ----------------------------------------------------------------------------------------- |
| `STRONG`     | Direct, attributable and sufficiently clear evidence supports the event and its relevance |
| `MODERATE`   | Credible evidence supports the event, but one or more details remain uncertain            |
| `WEAK`       | Indirect, incomplete or ambiguous evidence                                                |
| `UNASSESSED` | Confidence has not yet been evaluated                                                     |

A strong signal cannot compensate for failed ICP qualification.

---

## 6. Account Routing: Commercial Angle for Every Segment and Signal

The routing matrix is mandatory. Every approved segment must have a commercial angle for both selected signals.

The angle is a hypothesis for investigation, not a claim that the company has an established problem.

### 6.1 Primary ICP routing

| Primary segment              | `FINANCE_RECRUITMENT` angle                                                                                                                                                                                                | `MULTI_BRANCH_EXPANSION` angle                                                                                                                                                                |
| ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| FMCG Distributors            | Investigate how the finance function manages trade receivables, supplier payments, treasury oversight and collections across depots. Explore whether financial oversight requirements are changing as the business scales. | Investigate how new depots or regional distribution operations affect collections, trade-payment coordination, cash visibility and working-capital requirements.                              |
| Petrol Station Networks      | Investigate how the finance team manages daily cash/POS reconciliation, station-level collections, settlement visibility and financial control across the network.                                                         | Investigate how additional stations, CNG/EV infrastructure or non-fuel retail offerings change transaction management, settlement coordination and liquidity requirements across the network. |
| Retail Chains (Supermarkets) | Investigate how the finance function consolidates branch collections, reconciles cash/POS/transfers and manages financial reporting across outlets.                                                                        | Investigate how new supermarket branches affect centralised financial reporting, outlet collections, payment reconciliation and settlement coordination.                                      |

### 6.2 Secondary ICP routing

| Secondary segment | `FINANCE_RECRUITMENT` angle                                                                                                                                   | `MULTI_BRANCH_EXPANSION` angle                                                                                                                               |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| QSR Groups        | Investigate how finance teams oversee outlet collections, daily reconciliation, supplier payments and consolidated reporting across restaurants.              | Investigate how additional restaurant outlets affect transaction coordination, collections, centralised POS management and consolidated financial reporting. |
| Pharmacy Chains   | Investigate how finance and accounting teams manage outlet reconciliation, supplier payments, inventory-related financial control and consolidated reporting. | Investigate whether acquisitions or new pharmacy locations create additional supplier-payment, collections and financial integration requirements.           |

### 6.3 Emerging ICP routing

| Emerging segment                           | `FINANCE_RECRUITMENT` angle                                                                                                                        | `MULTI_BRANCH_EXPANSION` angle                                                                                                                                  |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Logistics/Haulage                          | Investigate how finance teams manage fleet expenditure, driver payments, collections, supplier payments and financial oversight across operations. | Investigate whether fleet expansion or new haulage capacity increases expenditure coordination, driver-payment administration and working-capital requirements. |
| Specialized Healthcare/Diagnostic Networks | Investigate how finance teams manage patient collections, corporate payments, billing reconciliation and financial reporting across centres.       | Investigate whether new diagnostic centres create additional collection, billing, payment coordination and consolidated reporting requirements.                 |

### 6.4 Commercial angle construction

For every routed account, construct the angle from:

1. Verified ICP segment.
2. Verified signal event.
3. Relevant operating or financial workflow.
4. Potential Moniepoint value proposition.
5. A question or investigation point that does not assume an unverified problem.

**Preferred-signal rule:** When `FINANCE_RECRUITMENT` is verified, the finance-recruitment angle is the default commercial angle. If expansion is also verified, use the second signal to make the angle more specific, not to replace the preferred signal.

When only expansion is verified, use the segment-specific expansion angle.

### 6.5 Commercial value proposition mapping

| Observed business context                          | Potential Moniepoint relevance              | Permitted interpretation                                                   |
| -------------------------------------------------- | ------------------------------------------- | -------------------------------------------------------------------------- |
| Multi-location cash/POS/transfer operations        | Payment acceptance and financial management | Investigate collections and reconciliation requirements                    |
| Settlement timing and liquidity sensitivity        | Instant settlement                          | Explore whether settlement timing affects operating cash flow              |
| Trade receivables and supplier-payment obligations | Working capital                             | Investigate working-capital requirements without assuming credit demand    |
| Additional branches, stations, depots or centres   | Multi-location financial management         | Investigate consolidated reporting and outlet-level financial coordination |
| Finance function expansion                         | Financial oversight and treasury operations | Investigate changes in financial control and reporting requirements        |

---

## 7. Variables Contract

This section is the implementation contract for Clay. Field names, types, permitted values, relationships and conditional requirements must be consistent across the workflow.

### 7.1 Account variables

| Variable                          | Type     | Requirement              | Allowed values / format                                          | Purpose                                    |
| --------------------------------- | -------- | ------------------------ | ---------------------------------------------------------------- | ------------------------------------------ |
| `account_id`                      | Text     | Required                 | Unique stable identifier                                         | Account primary key                        |
| `company_name`                    | Text     | Required                 | Verified trading or company name                                 | Account identity                           |
| `legal_entity_name`               | Text     | Conditional              | Verified legal entity name                                       | Entity resolution                          |
| `company_website`                 | URL      | Required where available | Valid URL                                                        | Account verification                       |
| `company_domain`                  | Text     | Required where available | Normalised domain                                                | Deduplication and enrichment               |
| `country`                         | Text     | Required                 | `Nigeria` for qualified accounts                                 | Geographic qualification                   |
| `operating_location`              | Text     | Required                 | Verified Nigerian city/state or operating locations              | Operating footprint                        |
| `segment`                         | Category | Required                 | Approved seven segment codes                                     | ICP segment                                |
| `segment_priority`                | Category | Required                 | `PRIMARY`, `SECONDARY`, `EMERGING`                               | Campaign priority                          |
| `icp_qualification_status`        | Category | Required                 | `QUALIFIED`, `RESEARCH_REQUIRED`, `DISQUALIFIED`, `OUT_OF_SCOPE` | ICP decision                               |
| `operational_status`              | Category | Required                 | `ACTIVE`, `INACTIVE`, `UNKNOWN`                                  | Operating-status verification              |
| `icp_evidence_url`                | URL      | Conditional              | Source URL                                                       | Qualification evidence                     |
| `icp_evidence_summary`            | Text     | Conditional              | Factual summary                                                  | Qualification rationale                    |
| `operating_model_evidence`        | Text     | Required                 | Factual summary                                                  | Segment-specific operating-model proof     |
| `location_count`                  | Number   | Conditional              | Non-negative integer                                             | Known operating locations                  |
| `location_count_previous`         | Number   | Conditional              | Non-negative integer                                             | Previous known location count              |
| `location_count_current`          | Number   | Conditional              | Non-negative integer                                             | Current known location count               |
| `warehousing_evidence`            | Text     | FMCG only                | Evidence summary                                                 | Multiple depots or significant warehousing |
| `trade_receivables_evidence`      | Text     | FMCG only                | Evidence summary                                                 | Trade receivables or credit-based sales    |
| `station_reconciliation_evidence` | Text     | Petrol stations only     | Evidence summary                                                 | Daily cash/POS reconciliation              |
| `company_enrichment_status`       | Category | Required                 | `PENDING`, `ENRICHED`, `PARTIAL`, `FAILED`                       | Company enrichment outcome                 |
| `company_enrichment_source`       | Text     | Conditional              | Provider or source name                                          | Enrichment provenance                      |
| `company_enrichment_date`         | Date     | Conditional              | ISO date                                                         | Enrichment audit trail                     |

### 7.2 Signal evidence variables

Each detected event must have its own signal evidence record. An account can have multiple signal records.

| Variable                        | Type          | Requirement              | Allowed values / format                                   | Purpose                          |
| ------------------------------- | ------------- | ------------------------ | --------------------------------------------------------- | -------------------------------- |
| `signal_id`                     | Text          | Required                 | Unique stable identifier                                  | Signal evidence primary key      |
| `account_id`                    | Text          | Required                 | Existing account ID                                       | Link signal to account           |
| `signal_type`                   | Category      | Required                 | `FINANCE_RECRUITMENT`, `MULTI_BRANCH_EXPANSION`           | Selected signal                  |
| `signal_priority`               | Category      | Required                 | `PRIMARY`, `SECONDARY`                                    | Signal hierarchy                 |
| `signal_event_type`             | Category/text | Required                 | Specific event code or description                        | Preserve actual event            |
| `signal_detected_date`          | Date          | Required                 | ISO date                                                  | Detection date                   |
| `signal_event_date`             | Date          | Conditional              | ISO date                                                  | Event or publication date        |
| `signal_source_url`             | URL           | Required when detected   | Direct source URL                                         | Evidence traceability            |
| `signal_evidence_summary`       | Text          | Required when detected   | Factual description                                       | What the source establishes      |
| `signal_detection_status`       | Category      | Required                 | `DETECTED`, `NOT_DETECTED`, `RESEARCH_REQUIRED`           | Detection outcome                |
| `signal_verification_status`    | Category      | Required when detected   | `VERIFIED`, `UNVERIFIED`, `REJECTED`, `RESEARCH_REQUIRED` | Verification outcome             |
| `signal_confidence`             | Category      | Required when assessed   | `STRONG`, `MODERATE`, `WEAK`, `UNASSESSED`                | Evidence confidence              |
| `signal_recency_days`           | Number        | Conditional              | Non-negative integer                                      | Event age where calculable       |
| `finance_role_title`            | Text          | Finance recruitment only | Advertised job title                                      | Role identification              |
| `finance_role_responsibilities` | Text          | Finance recruitment only | Extracted responsibilities                                | Role relevance                   |
| `finance_role_relevance`        | Boolean       | Finance recruitment only | `TRUE`, `FALSE`                                           | Relevance to financial workflows |
| `finance_role_type`             | Category      | Conditional              | `NEW_ROLE`, `REPLACEMENT`, `UNKNOWN`                      | Recruitment interpretation       |
| `expansion_type`                | Category/text | Expansion only           | Segment-specific event type                               | Expansion classification         |
| `expansion_verification`        | Text          | Expansion only           | Factual verification summary                              | Evidence of operating event      |

**Status distinction:**

- `signal_detection_status` records whether a signal was detected.
- `signal_verification_status` records whether a detected event was verified.
- `signal_confidence` records the strength of the supporting evidence.

These fields must not be merged into one status field.

### 7.3 Routing variables

| Variable                       | Type     | Requirement                  | Allowed values / format                                                                                                   | Purpose                                 |
| ------------------------------ | -------- | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- |
| `signal_combination`           | Category | Required                     | `FINANCE_ONLY`, `EXPANSION_ONLY`, `BOTH`, `NONE`                                                                          | Verified signal combination             |
| `account_research_priority`    | Category | Required                     | `HIGH`, `MEDIUM`, `LOW`, `HOLD`                                                                                           | Research queue                          |
| `preferred_signal_present`     | Boolean  | Required                     | `TRUE`, `FALSE`                                                                                                           | Whether finance recruitment is verified |
| `commercial_angle`             | Text     | Required for routed accounts | Segment- and signal-specific angle                                                                                        | Commercial investigation hypothesis     |
| `moniepoint_value_proposition` | Category | Conditional                  | `INSTANT_SETTLEMENT`, `WORKING_CAPITAL`, `MULTI_LOCATION_FINANCIAL_MANAGEMENT`, `PAYMENT_ACCEPTANCE`, `FINANCIAL_CONTROL` | Potential product relevance             |
| `workflow_state`               | Category | Required                     | Defined in Section 9                                                                                                      | Current workflow stage                  |
| `human_review_status`          | Category | Required                     | `PENDING`, `APPROVED`, `REJECTED`, `NEEDS_RESEARCH`                                                                       | Human review outcome                    |
| `outreach_approval_status`     | Category | Required                     | `NOT_REVIEWED`, `APPROVED`, `REJECTED`                                                                                    | Outreach control                        |
| `last_reviewed_date`           | Date     | Conditional                  | ISO date                                                                                                                  | Review audit trail                      |

### 7.4 Contact variables

Contact enrichment is linked to the account but does not determine ICP qualification.

| Variable                      | Type          | Requirement                         | Allowed values / format                                                    | Purpose                      |
| ----------------------------- | ------------- | ----------------------------------- | -------------------------------------------------------------------------- | ---------------------------- |
| `contact_id`                  | Text          | Required for contact record         | Unique stable identifier                                                   | Contact primary key          |
| `account_id`                  | Text          | Required                            | Existing account ID                                                        | Link contact to account      |
| `persona_name`                | Text          | Conditional                         | Verified contact name                                                      | Contact identity             |
| `persona_title`               | Text          | Conditional                         | Verified job title                                                         | Role identification          |
| `persona_function`            | Category      | Conditional                         | `OWNER`, `MANAGING_DIRECTOR`, `FINANCE`, `TREASURY`, `OPERATIONS`, `OTHER` | Functional classification    |
| `persona_seniority`           | Category/text | Conditional                         | Verified seniority                                                         | Buying-role context          |
| `persona_source_url`          | URL           | Conditional                         | Direct source URL                                                          | Contact evidence             |
| `contact_verification_status` | Category      | Required for contact record         | `VERIFIED`, `UNVERIFIED`, `RESEARCH_REQUIRED`                              | Contact verification         |
| `contact_relevance`           | Category      | Conditional                         | `ECONOMIC_BUYER`, `INFLUENCER`, `RELEVANT_FUNCTION`, `UNKNOWN`             | Buying-role relevance        |
| `work_email`                  | Email         | Conditional                         | Business email                                                             | Contactability               |
| `email_verification_status`   | Category      | Conditional                         | `VERIFIED`, `UNVERIFIED`, `RISKY`, `NOT_FOUND`                             | Email validation             |
| `email_matches_company`       | Boolean       | Conditional                         | `TRUE`, `FALSE`                                                            | Company-domain check         |
| `send_ready`                  | Boolean       | Required for outreach-ready contact | `TRUE`, `FALSE`                                                            | Final contact readiness gate |

### 7.5 Data integrity rules

1. `account_id`, `signal_id` and `contact_id` must be stable identifiers.
2. Every signal evidence record must reference an existing `account_id`.
3. Every contact record must reference an existing `account_id`.
4. A single account may have multiple signal records and multiple contact records.
5. Do not populate unknown values with invented estimates.
6. Use null or blank values for unavailable information.
7. Preserve the source URL for every qualification and signal decision.
8. Keep ICP qualification separate from signal detection and verification.
9. Keep signal confidence separate from account priority.
10. Keep contact verification separate from account qualification.
11. A verified signal requires attributable evidence and a factual evidence summary.
12. An account cannot be `QUALIFIED` until its applicable mandatory ICP requirements are verified.
13. A signal cannot be used to infer purchase intent, payment friction, credit eligibility or purchasing authority.
14. Company enrichment must not overwrite the evidence used for ICP qualification.
15. A missing email or contact must not change a qualified account's ICP status.

---

## 8. Workflow Execution Specification

### Stage 1: Account Discovery

**Objective:** Identify potential Nigerian businesses within the seven approved ICP segments.

**Actions:**

1. Discover businesses in the approved segments.
2. Capture company name, website, domain and known operating locations.
3. Identify the likely operating entity.
4. Assign a provisional segment and priority.
5. Record the discovery source.
6. Deduplicate candidate companies using normalised company domains where available, supported by company-name and legal-entity checks.

**Output:** `DISCOVERED` account.

Discovery results are candidates, not qualified accounts. Search-result volume must not be reported as the number of qualified companies.

### Stage 2: ICP Qualification

**Objective:** Establish whether the business meets the approved ICP.

**Actions:**

1. Verify Nigerian operating presence.
2. Verify business and operating-entity identity.
3. Establish active operating status.
4. Confirm actual segment and operating model.
5. Apply applicable segment-specific mandatory requirements.
6. Check anti-ICP exclusions.
7. Capture qualification evidence.
8. Assign the ICP qualification status.

**Decision:**

- All applicable requirements verified: `QUALIFIED`.
- Evidence incomplete: `RESEARCH_REQUIRED`.
- Mandatory requirements fail: `DISQUALIFIED`.
- Outside approved segments: `OUT_OF_SCOPE`.

**Gate:** Only `QUALIFIED` accounts proceed to qualified signal prioritisation.

### Stage 3: Preferred Signal Detection

**Objective:** Detect `FINANCE_RECRUITMENT` at ICP-qualified accounts.

**Actions:**

1. Search for current finance, treasury, financial control, accounting and relevant finance operations vacancies.
2. Identify the advertised employer.
3. Match the vacancy to the account's operating entity.
4. Capture job title, responsibilities, source and detection date.
5. Record the detection outcome.

**Output:** Finance-recruitment signal evidence record.

### Stage 4: Supporting Signal Detection

**Objective:** Detect `MULTI_BRANCH_EXPANSION` events that can strengthen or independently support commercial routing.

**Actions:**

1. Search for the expansion events applicable to the account's segment.
2. Identify the event and operating entity.
3. Capture the event source and date.
4. Record the actual event type.
5. Link the evidence to the account.

**Output:** Expansion signal evidence record, where detected.

### Stage 5: Signal Verification

**Objective:** Establish whether each detected event is attributable, current and supported by sufficient evidence.

**Finance recruitment checks:**

- Correct employer.
- Current vacancy.
- Relevant responsibilities.
- Role seniority and function.
- New role or replacement status where ascertainable.
- Source and detection date.

**Expansion checks:**

- Actual event.
- Correct operating entity.
- Attribution to target account.
- Operational status versus announcement or proposal.
- Location counts where available and applicable.
- Source and detection date.

**Output:** Each signal receives its own detection status, verification status and confidence assessment.

### Stage 6: Signal Prioritisation

**Objective:** Prioritise ICP-qualified accounts based on verified signal evidence.

**Actions:**

1. Determine whether finance recruitment is verified.
2. Determine whether expansion is verified.
3. Calculate the verified signal combination.
4. Apply the prioritisation hierarchy in Section 5.
5. Record the account's research priority.

**Output:** `signal_combination` and `account_research_priority`.

An account with no detected signal remains ICP-qualified but does not count towards the 100 production-grade target.

### Stage 7: Account and Persona Enrichment

**Objective:** Build a useful account record and identify relevant buying roles.

**Actions:**

1. Confirm the company website, domain and operating entity.
2. Capture known business locations and segment-specific operating evidence.
3. Enrich company information using available Clay providers and accessible public sources.
4. Research relevant finance, treasury, operations and executive contacts.
5. Record names, titles, functions and source URLs where available.
6. Classify contact relevance using the buying-role guidance below.
7. Record unresolved contact research rather than inventing contact details.
8. Record enrichment status and the source/provider used.

**Buying-role guidance:**

| Segment                 | Relevant buying roles                                                                  |
| ----------------------- | -------------------------------------------------------------------------------------- |
| FMCG Distributors       | Owner/Founder, Managing Director, Finance Controller, Treasury Manager                 |
| Petrol Station Networks | Owner, Managing Director, Operations Director                                          |
| Retail Chains           | Finance leadership, financial controllers and relevant executive/operations leadership |
| QSR Groups              | Finance leadership and operations leadership                                           |
| Pharmacy Chains         | Finance/accounting leadership and relevant executive leadership                        |
| Logistics/Haulage       | Finance leadership, operations leadership and business ownership                       |
| Healthcare/Diagnostics  | Finance leadership and relevant executive or operating leadership                      |

A missing contact does not disqualify an account. Contact research must be attempted and the outcome recorded, but an account must not be removed from the 100-company target solely because a named contact or email cannot be found.

### Stage 8: Commercial Routing

**Objective:** Assign a defensible commercial angle based on verified ICP and signal evidence.

**Actions:**

1. Retrieve the verified segment.
2. Retrieve the preferred signal status.
3. Retrieve the supporting signal status.
4. Select the corresponding routing-matrix angle.
5. If both signals are verified, combine their implications without duplicating or overstating them.
6. Map the potential Moniepoint value proposition.
7. Save the commercial angle to the account record.

**Routing precedence:**

- Verified finance recruitment: finance-recruitment angle is the default.
- Verified finance recruitment and expansion: use the finance-recruitment angle strengthened by the verified expansion event.
- Expansion only: use the segment-specific expansion angle.
- No verified signal: retain as ICP-qualified but do not classify as signal-qualified.

### Stage 9: Human Review

**Objective:** Ensure that qualification, signal evidence and commercial interpretation are defensible before outreach.

**Reviewer checks:**

- Is the account inside the approved ICP?
- Are applicable mandatory segment requirements verified?
- Is the operating entity correctly identified?
- Is the preferred signal verified where claimed?
- Is the supporting signal verified where claimed?
- Are the sources attributable and credible?
- Is the commercial angle supported by the actual event?
- Is the proposed persona relevant?
- Does the proposed conversation avoid unsupported pain claims?

**Decision:**

- `APPROVED`: Account can proceed to outreach approval.
- `NEEDS_RESEARCH`: Additional evidence required.
- `REJECTED`: Incorrect account, failed ICP qualification or invalid signal.

### Stage 10: Outreach Approval

**Objective:** Approve an evidence-backed account and contact for commercial outreach.

Outreach must:

- Reference a verified event.
- Use the correct segment-specific angle.
- Ask a relevant question about the business's financial or operational workflows.
- Avoid claiming unverified settlement problems, liquidity shortages, credit demand or dissatisfaction with existing providers.
- Avoid implying that Moniepoint has assessed the company's financial or credit eligibility.

**Output:** `OUTREACH_READY` account and contact records.

---

## 9. Workflow States and Transition Rules

| Current state                | Condition                                                   | Next state                                |
| ---------------------------- | ----------------------------------------------------------- | ----------------------------------------- |
| `DISCOVERED`                 | Account identity established                                | `ICP_REVIEW`                              |
| `DISCOVERED`                 | Identity unresolved                                         | `RESEARCH_REQUIRED`                       |
| `ICP_REVIEW`                 | All applicable mandatory requirements verified              | `ICP_QUALIFIED`                           |
| `ICP_REVIEW`                 | Mandatory requirements fail                                 | `DISQUALIFIED`                            |
| `ICP_REVIEW`                 | Outside approved segments                                   | `OUT_OF_SCOPE`                            |
| `ICP_QUALIFIED`              | Preferred signal search begins                              | `FINANCE_SIGNAL_DETECTION`                |
| `FINANCE_SIGNAL_DETECTION`   | Finance vacancy identified                                  | `SIGNAL_VERIFICATION`                     |
| `FINANCE_SIGNAL_DETECTION`   | No relevant vacancy detected                                | `EXPANSION_SIGNAL_DETECTION`              |
| `SIGNAL_VERIFICATION`        | Finance vacancy verified or rejected                        | `EXPANSION_SIGNAL_DETECTION`              |
| `EXPANSION_SIGNAL_DETECTION` | Expansion event identified or no event found                | `SIGNAL_VERIFICATION` or `SIGNAL_SCORING` |
| `SIGNAL_VERIFICATION`        | Expansion event verified or rejected                        | `SIGNAL_SCORING`                          |
| `SIGNAL_SCORING`             | Signal combination and priority assigned                    | `ACCOUNT_ENRICHMENT`                      |
| `ACCOUNT_ENRICHMENT`         | Account and contact research completed or outcomes recorded | `COMMERCIAL_ROUTING`                      |
| `COMMERCIAL_ROUTING`         | Commercial angle assigned                                   | `HUMAN_REVIEW`                            |
| `HUMAN_REVIEW`               | Reviewer approves                                           | `OUTREACH_REVIEW`                         |
| `HUMAN_REVIEW`               | More evidence needed                                        | `RESEARCH_REQUIRED`                       |
| `HUMAN_REVIEW`               | Reviewer rejects                                            | `REJECTED`                                |
| `OUTREACH_REVIEW`            | Outreach approved                                           | `OUTREACH_READY`                          |
| `OUTREACH_REVIEW`            | Outreach rejected                                           | `REJECTED`                                |

An account with no detected signal can remain ICP-qualified for future monitoring. It must not be represented as a signal-qualified prospect or counted towards the 100 production-grade target.

An account with unresolved qualification or signal evidence must not progress as though the relevant condition has been verified.

---

## 10. Clay Implementation Architecture

The initial Clay implementation uses a company-first architecture. Company qualification and signal verification must precede contact enrichment.

This prevents spending enrichment credits on companies that fail the ICP or have no verified selected signal.

### 10.1 Accounts table

**Purpose:** Maintain the account-level ICP decision, signal summary, company enrichment, research priority and commercial routing.

Core fields:

- `account_id`
- `company_name`
- `legal_entity_name`
- `company_website`
- `company_domain`
- `country`
- `operating_location`
- `segment`
- `segment_priority`
- `icp_qualification_status`
- `operational_status`
- `operating_model_evidence`
- `icp_evidence_url`
- `location_count`
- `company_enrichment_status`
- `company_enrichment_source`
- `preferred_signal_present`
- `signal_combination`
- `account_research_priority`
- `commercial_angle`
- `moniepoint_value_proposition`
- `workflow_state`
- `human_review_status`
- `outreach_approval_status`

### 10.2 Signal Evidence table

**Purpose:** Store each detected event independently, preserving its source, verification and interpretation.

Core fields:

- `signal_id`
- `account_id`
- `signal_type`
- `signal_priority`
- `signal_event_type`
- `signal_detected_date`
- `signal_event_date`
- `signal_source_url`
- `signal_evidence_summary`
- `signal_detection_status`
- `signal_verification_status`
- `signal_confidence`
- `signal_recency_days`
- `finance_role_title`
- `finance_role_responsibilities`
- `finance_role_relevance`
- `finance_role_type`
- `expansion_type`
- `expansion_verification`

### 10.3 Contacts table

**Purpose:** Store relevant buying-role contacts independently of the account qualification decision.

Core fields:

- `contact_id`
- `account_id`
- `persona_name`
- `persona_title`
- `persona_function`
- `persona_seniority`
- `persona_source_url`
- `contact_verification_status`
- `contact_relevance`
- `work_email`
- `email_verification_status`
- `email_matches_company`
- `send_ready`

### 10.4 Table relationships

- `Accounts` is the parent account table.
- `Signal Evidence` contains one or more events linked to an account through `account_id`.
- `Contacts` contains one or more contacts linked to an account through `account_id`.
- Account qualification must not be overwritten by signal detection.
- Signal evidence must not be overwritten by contact enrichment.
- Contact availability must not determine account qualification.
- Account-level signal combination must be derived from independently verified signal records.

### 10.5 Clay build and credit controls

The Clay workbook must be built with automatic runs disabled during configuration and testing.

Execution order:

1. Import and deduplicate the candidate company list.
2. Validate the company identifiers and domains.
3. Apply free research and qualification checks where possible.
4. Run the qualification logic before paid enrichment.
5. Test each paid enrichment column on one record before running it across the table.
6. Test AI classification on two or three representative records before scaling.
7. Inspect output quality and provider credit consumption.
8. Run company enrichment once per unique qualified account.
9. Detect and verify the selected signals.
10. Perform contact enrichment only after the account passes the applicable gates.
11. Run email verification only for contacts being considered for outreach.
12. Reconcile the final table against the 100-record acceptance criteria.

Do not run expensive enrichment on duplicate domains, disqualified companies or records that have not passed the necessary qualification gates.

Where multiple providers can supply the same field, prefer a free or lower-cost source first, provided the source is sufficiently reliable for the field being populated.

A missing result must remain missing or be marked `RESEARCH_REQUIRED`. Do not manufacture a value to fill a column.

### 10.6 Research stack integration

Python research outputs may be imported into Clay as prepared candidate records or evidence inputs.

The existing research stack has the following permitted uses:

| Tool                 | Permitted use                                                                                                    | Limitation                                                                                             |
| -------------------- | ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Python               | Prepare search batches, normalise records, deduplicate domains, validate fields and calculate workflow summaries | Does not independently establish truth without supporting evidence                                     |
| DDGS                 | Discover public company pages, vacancies and expansion references                                                | Search results are discovery evidence, not final verification                                          |
| Trafilatura          | Extract accessible page text for inspection and structured analysis                                              | Extraction success does not establish source accuracy or event validity                                |
| Gemini API free tier | Extract facts, classify evidence and produce structured research outputs                                         | Outputs must be checked against source material; free-tier limits apply                                |
| Clay                 | Enrich accounts and contacts, organise evidence, classify, route and manage the workbook                         | Provider availability, credit consumption and field coverage depend on the connected services and plan |

The workflow must not depend on Claude Code or a paid model subscription.

### 10.7 Workbook views

The workbook should provide clear views for:

1. `All Accounts`
2. `ICP Qualified`
3. `Primary ICP`
4. `Secondary ICP`
5. `Emerging ICP`
6. `Finance Recruitment`
7. `Expansion`
8. `Both Signals`
9. `Research Required`
10. `Human Review`
11. `Outreach Ready`
12. `Excluded Accounts`

Views must reflect actual field values. They must not imply that an account is qualified, verified or outreach-ready when it has not passed the relevant gate.

### 10.8 Outreach readiness gates

A contact must not be marked `send_ready = TRUE` merely because an email address is present.

The final gate requires:

- Account is ICP-qualified.
- At least one selected signal is independently verified.
- Contact identity and company association are credible.
- Contact role is relevant to the intended conversation.
- Email verification status is acceptable.
- Email domain association has been checked.
- Human review has approved the account and proposed outreach.

Where email verification is unavailable, the contact must not be represented as email-verified.

`OUTREACH_READY` means approved for human-controlled outreach. It does not mean a message has been sent or a CRM record has been synchronised.

---

## 11. Acceptance Criteria and Delivery Standard

### 11.1 Final delivery target

**Required delivery: at least 100 production-grade enriched company records.**

The target is 100 distinct company accounts after deduplication, not 100 contacts, locations, job vacancies or search results.

The 100 records must not be padded with unqualified companies, duplicate subsidiaries, unverifiable operating entities or unverified buying signals.

### 11.2 Account qualification

- [ ] Company identity is verified.
- [ ] Nigerian operating presence is established.
- [ ] Approved segment is correctly assigned.
- [ ] Segment priority is correctly assigned.
- [ ] Active operating status is established.
- [ ] Applicable mandatory segment requirements are evidenced.
- [ ] Anti-ICP exclusions have been checked.
- [ ] Qualification evidence is traceable.
- [ ] Company domain has been normalised and deduplicated where available.

### 11.3 Company enrichment

- [ ] Company website and domain have been captured where available.
- [ ] Operating location has been researched.
- [ ] Segment-specific operating information has been captured.
- [ ] Relevant company information has been enriched.
- [ ] Enrichment source or provider has been recorded.
- [ ] Enrichment outcome has been recorded.
- [ ] Unknown fields remain blank or explicitly unresolved.
- [ ] Company enrichment has not been confused with ICP qualification.

### 11.4 Preferred signal verification

- [ ] Finance recruitment has been searched for.
- [ ] Any detected vacancy is attributable to the target company.
- [ ] Vacancy status has been checked.
- [ ] Role responsibilities have been captured.
- [ ] Financial-workflow relevance has been assessed.
- [ ] Source URL and detection date have been recorded.
- [ ] Verification status and confidence have been assigned.

### 11.5 Supporting signal verification

- [ ] Segment-specific expansion events have been searched for.
- [ ] Any detected event is attributable to the target company.
- [ ] Actual event type has been preserved.
- [ ] Operational status has been checked.
- [ ] Source URL and detection date have been recorded.
- [ ] Verification status and confidence have been assigned.

### 11.6 Commercial routing

- [ ] Verified signal combination is recorded.
- [ ] Account priority is assigned.
- [ ] Segment-specific commercial angle is assigned.
- [ ] Relevant Moniepoint value proposition is identified.
- [ ] No unsupported pain point is asserted.
- [ ] Human review decision is recorded.
- [ ] Outreach approval is recorded separately.

### 11.7 Contact enrichment

- [ ] Relevant buying roles have been researched.
- [ ] Contact sources are recorded where contacts are identified.
- [ ] Contact verification status is recorded.
- [ ] Missing contact information is not used to disqualify the account.
- [ ] Email verification status is recorded where an email is obtained.
- [ ] `send_ready` is controlled by the defined readiness conditions.

### 11.8 What counts as one production-grade record

A company counts towards the 100-record target only when:

1. It is one distinct company account after deduplication.
2. It is ICP-qualified.
3. Its segment and priority are correctly assigned.
4. Its operating model and applicable mandatory requirements are supported by evidence.
5. Its company record has been enriched with relevant available business information.
6. At least one of the two selected signals is independently verified.
7. The signal event, source and detection date are recorded.
8. A segment-specific commercial angle is assigned.
9. Relevant buying-role research has been attempted and its outcome recorded.
10. The record is traceable and ready for human review.

A verified named contact or deliverable email address is desirable and must be captured where available, but missing contact information does not invalidate an otherwise production-grade company account.

A company with no verified selected signal does not count towards the 100, even if it is otherwise ICP-qualified and enriched.

A company with unresolved mandatory qualification conditions does not count towards the 100.

### 11.9 Final reporting metrics

The completed workbook should make the following counts visible:

| Metric                             | What it measures                                                      |
| ---------------------------------- | --------------------------------------------------------------------- |
| Companies discovered               | Initial candidate volume                                              |
| Unique companies                   | Deduplicated company accounts                                         |
| ICP qualified                      | Accounts passing mandatory qualification                              |
| Research required                  | Accounts with unresolved evidence                                     |
| Disqualified                       | Accounts failing mandatory requirements                               |
| Out of scope                       | Accounts outside the approved segments                                |
| Finance recruitment detected       | Accounts with a detected finance vacancy                              |
| Finance recruitment verified       | Accounts with independently verified finance vacancies                |
| Expansion detected                 | Accounts with a detected expansion event                              |
| Expansion verified                 | Accounts with independently verified expansion events                 |
| Both signals verified              | Accounts with both selected signals independently verified            |
| Signal-qualified accounts          | Accounts with at least one verified selected signal                   |
| Company enriched                   | Accounts with completed company enrichment                            |
| Contact research completed         | Accounts for which buying-role research has been attempted            |
| Contacts identified                | Relevant contacts identified                                          |
| Verified emails                    | Contacts with acceptable email verification                           |
| Outreach ready                     | Contacts and accounts passing all human and technical readiness gates |
| Production-grade enriched accounts | Distinct accounts meeting all ten conditions in Section 11.8          |

The final production count must be at least 100.

---

## 12. Operating Safeguards

1. **ICP before signal:** Never qualify an account because it has a finance vacancy or expansion announcement.
2. **Preferred signal discipline:** `FINANCE_RECRUITMENT` remains the principal automated signal. Expansion supports rather than silently replaces it.
3. **Entity attribution:** Verify that each event belongs to the target operating company.
4. **Evidence before interpretation:** Record what the source establishes before assigning a commercial implication.
5. **No invented pain:** Do not transfer industry-wide payment friction to an individual account without account-level evidence.
6. **No false urgency:** Recruitment or expansion does not automatically establish immediate purchase intent.
7. **No false credit inference:** Capital expenditure, fleet growth or trade receivables do not prove credit eligibility or demand.
8. **No false buyer authority:** A finance or treasury title does not establish purchasing authority.
9. **No false expansion:** Proposed, announced and completed events must remain distinguishable.
10. **No contact-based exclusion:** Missing contacts do not invalidate otherwise qualified accounts.
11. **No product-fit overclaim:** ICP qualification and signal verification do not establish Moniepoint product eligibility.
12. **No invented ICP thresholds:** Do not add numerical or operational qualification requirements that the approved ICP has not established.
13. **No unsupported enrichment:** AI-generated fields must be traceable to source evidence.
14. **No duplicate enrichment:** Do not spend enrichment credits repeatedly on the same company domain without a documented reason.
15. **No automatic outreach:** Enrichment and routing do not authorise automatic sending.
16. **No false implementation claims:** Planned Python, Clay or CRM capabilities must not be described as implemented until they have been tested.
17. **No unnecessary paid dependencies:** The workflow must remain implementable with the existing Python research stack and available Clay functionality, subject to actual provider and plan limits.

---

## 13. Final Workflow Logic

The workflow operates in this order:

`ACCOUNT DISCOVERY`
→ `COMPANY DEDUPLICATION`
→ `ICP QUALIFICATION`
→ `FINANCE RECRUITMENT DETECTION`
→ `FINANCE RECRUITMENT VERIFICATION`
→ `EXPANSION DETECTION`
→ `EXPANSION VERIFICATION`
→ `SIGNAL SCORING`
→ `COMPANY ENRICHMENT`
→ `PERSONA RESEARCH`
→ `COMMERCIAL ROUTING`
→ `HUMAN REVIEW`
→ `OUTREACH APPROVAL`

The authority of each document remains distinct:

- `icp/icp.md` determines **which businesses are eligible**.
- `icp/signals.md` determines **which observable events are relevant and which signals are selected for automation**.
- `workflow.md` determines **how the preferred signal is detected, verified, scored, enriched, routed and converted into an evidence-backed account for human review**.

**The workflow's defining output:** At least 100 distinct ICP-qualified Nigerian businesses with completed company enrichment, at least one independently verified selected buying signal, a segment-specific commercial angle, traceable evidence and documented buying-role research. Finance recruitment remains the preferred signal. Verified expansion can independently qualify an account for the production target when finance recruitment is absent.
