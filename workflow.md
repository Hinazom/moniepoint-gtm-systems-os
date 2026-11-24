# Workflow Specification: Moniepoint Business Banking and Payments

## Finance and Treasury Recruitment + Multi-Branch Expansion

## 1. Workflow Overview

- **Workflow:** ICP qualification and signal-based account prioritisation
- **Market:** Nigerian retail supermarket chains and FMCG distributors
- **Primary signal:** Finance and Treasury Recruitment
- **Secondary signal:** Multi-Branch Expansion
- **Platform:** Clay, public-source research and downstream CRM preparation
- **Purpose:** Identify qualified businesses with observable developments that create a credible reason to investigate their banking, collections, settlements and financial operations.
- **Automation boundary:** Research, qualify, classify, prioritise and prepare accounts for human review. Do not infer purchase intent, assert unverified operational problems or initiate outreach without approval.
- **Build status:** Specification only. The existing Python research foundation supports research but is not an operational Clay workflow.

This specification defines the workflow's states, decision rules, signal requirements, routing logic, commercial angles, variables and acceptance criteria. It is an operational design, not a list of research instructions.

## 2. Mother Intent

Identify Nigerian retail supermarket chains and FMCG distributors that:

1. Meet the mandatory ICP qualification conditions.
2. Have relevant business collections, settlements or supplier-payment requirements.
3. Demonstrate one or both of the following observable developments:
   - **Finance and Treasury Recruitment:** Recruitment for relevant finance, treasury, accounting, financial control or financial operations roles.
   - **Multi-Branch Expansion:** Opening new physical retail outlets or expanding a distribution footprint into additional locations or geographic markets.

Use verified developments to prioritise accounts for commercial investigation of Moniepoint Business Banking and Payments.

A signal is a reason to investigate, not proof of a payment problem, dissatisfaction with an existing provider or intent to purchase.

Every account record must distinguish:

- Verified account facts.
- Source-backed signal evidence.
- ICP qualification decisions.
- Commercial interpretation.
- Purchasing intent, if independently established.

## 3. Workflow Status Line

**Normal progression:**

`DISCOVERED → IDENTITY_VERIFIED → ICP_SCREENED → ICP_QUALIFIED → SIGNAL_RESEARCH → SIGNAL_REVIEWED → ROUTED → HUMAN_REVIEW → APPROVED → CRM_READY`

| Status              | Entry condition and required action                                                          |
| ------------------- | -------------------------------------------------------------------------------------------- |
| `DISCOVERED`        | Candidate business identified. Create a provisional account record.                          |
| `IDENTITY_VERIFIED` | Business identity and Nigerian operations supported by evidence. Check for duplicates.       |
| `ICP_SCREENED`      | Evaluate all mandatory ICP conditions and record each result.                                |
| `ICP_QUALIFIED`     | All mandatory ICP conditions pass. Initiate both signal searches.                            |
| `SIGNAL_RESEARCH`   | Finance recruitment and expansion searches are initiated and tracked independently.          |
| `SIGNAL_REVIEWED`   | Both searches have terminal outcomes. Validate evidence and search coverage.                 |
| `ROUTED`            | Apply the routing rules using ICP segment and both signal outcomes.                          |
| `HUMAN_REVIEW`      | Reviewer checks qualification, evidence, commercial angle and proposed next action.          |
| `APPROVED`          | Reviewer approves the account and proposed next action.                                      |
| `CRM_READY`         | Required fields and approval are present. Account is eligible for authorised CRM processing. |

**Exception statuses:**

`ICP_DISQUALIFIED`, `RESEARCH_BLOCKED`, `DUPLICATE`, `EVIDENCE_REJECTED`, `PROCESSING_ERROR`, `HUMAN_REJECTED`, `ON_HOLD`.

**Status controls:**

- `workflow_status` represents lifecycle progression.
- `icp_outcome` represents qualification.
- `signal_search_status` represents research execution.
- `signal_outcome` represents the result of a signal search.
- `routing_outcome` represents the next commercial action.
- These fields must not substitute for one another.
- An ICP-qualified account may have no detected buying signals and remain eligible for monitoring.
- A failed or incomplete search must never be recorded as `NOT_DETECTED`.
- Both signal searches must have terminal outcomes before the account reaches `SIGNAL_REVIEWED`.
- AI-generated recommendations cannot approve an account.
- `CRM_READY` means approved for CRM processing, not that synchronisation has occurred.

## 4. ICP Filter

An account must pass every mandatory qualification condition before signal research begins. A strong signal cannot compensate for failed ICP fit.

### 4.1 Approved Segments

| Segment              | Inclusion definition                                                                                             |
| -------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `RETAIL_SUPERMARKET` | Business operating physical supermarket or grocery retail outlets.                                               |
| `FMCG_DISTRIBUTOR`   | Business wholesaling or distributing fast-moving consumer goods to retailers, resellers or commercial customers. |

Only these two segments are in scope for this workflow.

Fuel stations, unrelated SMEs, online-only retailers and businesses outside these definitions are excluded, even if they demonstrate a potentially relevant signal.

### 4.2 Mandatory Qualification Conditions

| Condition                | PASS                                                                                                                                       | FAIL                                                                     | Insufficient evidence |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------ | --------------------- |
| Nigerian presence        | Current Nigerian business operations supported by evidence.                                                                                | No Nigerian operations established or operations definitively ceased.    | `UNKNOWN`             |
| Business identity        | Operating entity distinguishable through credible sources.                                                                                 | Candidate is the wrong entity or identity is disproved.                  | `UNKNOWN`             |
| Segment fit              | Business activity matches one approved segment.                                                                                            | Business is outside both approved segments.                              | `UNKNOWN`             |
| Active operations        | Current commercial activity supported.                                                                                                     | Business is dormant or relevant operations have ceased.                  | `UNKNOWN`             |
| Physical operating model | Physical retail outlets or genuine wholesale/distribution operations supported.                                                            | Exclusively online retail or no qualifying physical business operations. | `UNKNOWN`             |
| Payments relevance       | Meaningful recurring business collections, settlements or supplier-payment requirements are plausible and supported by the business model. | No meaningful relevance to the proposition is established.               | `UNKNOWN`             |

**ICP decision rules:**

- `QUALIFIED`: All six mandatory conditions are `PASS`.
- `DISQUALIFIED`: At least one mandatory condition definitively fails.
- `FURTHER_RESEARCH`: No condition definitively fails, but at least one remains `UNKNOWN`.
- Missing information is not a negative finding.
- A detected buying signal cannot override an ICP failure.

### 4.3 Fit Tier and Prioritisation

The ICP distinguishes stronger-fit accounts from reasonable-fit accounts. These tiers guide prioritisation; they do not replace the mandatory qualification decision.

| Fit tier         | Qualification profile                                                                                                                           |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `EXCELLENT_FIT`  | Businesses with five or more physical locations, high-frequency transaction activity and a relevant finance or treasury recruitment profile.    |
| `REASONABLE_FIT` | Single-location, high-volume retailers, including large supermarkets, or distributors with a credible need for consolidated payment management. |
| `UNASSESSED`     | Qualified account whose available evidence is not sufficient to assign a fit tier.                                                              |

**Interpretation rules:**

- Five or more locations is an initial prioritisation heuristic, not a mandatory ICP threshold.
- A single-location business is not automatically disqualified if it otherwise meets the approved segment definition and mandatory conditions.
- A distributor does not need to operate retail outlets. Its wholesale and distribution model must be verified.
- High transaction volume and collection complexity should be evidenced where possible, not assumed from company size.
- Finance recruitment is also a buying signal. Its presence may contribute to an `EXCELLENT_FIT` assessment but must be recorded separately as signal evidence.
- Businesses fully dependent on B2B e-invoicing with no meaningful in-person collection or other relevant payment-management requirements are poor fit. Verify the actual business model before disqualification.

## 5. Signal Definitions and Detection

The workflow researches two selected signals. Operational Complexity Signals, such as warehouse or logistics recruitment, remain tertiary research indicators and are not part of this workflow's routing logic.

| Signal                               | Qualifying event                                                                                                                            | Evidence requirements                                                                                                                                                                                      | Recency            |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ |
| `FINANCE_RECRUITMENT` (primary)      | Attributable vacancy for a role with substantive finance, treasury, accounting, financial control or financial operations responsibilities. | Employer matches the account or verified subsidiary; relevant role and responsibilities; direct vacancy URL; publication date; vacancy status or independent confirmation that recruitment remains active. | Previous 180 days  |
| `MULTI_BRANCH_EXPANSION` (secondary) | Specific opening, announced opening or geographic expansion of physical outlets or distribution operations.                                 | Target business or verified subsidiary; identifiable expansion event; location or market where available; direct source URL; publication date; event date or period; event status.                         | Previous 12 months |

### 5.1 Signal-Specific Rules

**Finance and Treasury Recruitment**

Relevant roles may include:

- Treasury Manager.
- Finance Manager.
- Financial Controller.
- Finance Operations Manager.
- Finance Analyst.
- Relevant accounting or treasury operations roles.

A job title alone is insufficient. Verify the responsibilities and employer attribution. A vacancy at a similarly named company or unrelated subsidiary does not qualify.

Vacancy status must be recorded as `OPEN`, `CLOSED`, `EXPIRED` or `UNKNOWN`. An unknown status is not proof of active recruitment.

**Multi-Branch Expansion**

For retail supermarkets, qualifying developments include:

- Opening a new supermarket outlet.
- An officially announced new outlet.
- Expansion into a new city or state through physical retail operations.

For FMCG distributors, qualifying developments include:

- Opening a new distribution depot or warehouse as part of an expanded distribution footprint.
- Entry into a new geographic distribution market.
- A specific expansion of distribution operations into additional locations.

A warehouse, office or facility announcement does not automatically qualify. Verify that it represents a genuine expansion of the company's retail or distribution operations.

Expansion status must be recorded as:

- `COMPLETED`
- `ANNOUNCED`
- `PLANNED`
- `UNVERIFIED`

An attributable announcement can qualify as a detected development, but must not be described as an already operational location.

Planned, speculative, stale or unattributable developments do not qualify as current detected signals. Retain relevant candidate or historical evidence with its correct status.

The 180-day and 12-month windows are initial operating assumptions. Validate them during implementation.

### 5.2 Search Status and Signal Outcome

Each qualified account must have two independent search records: one for finance recruitment and one for expansion.

**Search status**

| Status                  | Meaning                                                            |
| ----------------------- | ------------------------------------------------------------------ |
| `NOT_STARTED`           | Search has not begun.                                              |
| `IN_PROGRESS`           | Search is underway.                                                |
| `COMPLETED`             | Defined research process completed and coverage assessed.          |
| `FAILED`                | Search failed before a reliable conclusion could be reached.       |
| `INSUFFICIENT_COVERAGE` | Search ran, but its coverage cannot support a reliable conclusion. |

**Signal outcome**

| Outcome        | Meaning                                                                          |
| -------------- | -------------------------------------------------------------------------------- |
| `DETECTED`     | At least one event meets all signal-specific evidence requirements.              |
| `NOT_DETECTED` | Search completed with sufficient coverage and no qualifying event was found.     |
| `UNVERIFIED`   | A relevant candidate was found, but evidence requirements remain unmet.          |
| `HISTORICAL`   | Relevant evidence exists, but the event falls outside the active recency window. |
| `UNKNOWN`      | Presence or absence cannot reliably be established.                              |

**Outcome precedence and controls:**

1. `DETECTED` applies when at least one verified, in-window event qualifies.
2. `UNVERIFIED` applies when relevant candidate evidence remains unresolved and no verified qualifying event exists.
3. `HISTORICAL` applies when relevant evidence exists only outside the active recency window.
4. `NOT_DETECTED` applies only when the search is `COMPLETED`, coverage is sufficient and no qualifying or unresolved candidate event remains.
5. `FAILED`, `INSUFFICIENT_COVERAGE` and unfinished searches produce `UNKNOWN`.

If a search contains both a verified qualifying event and an unresolved candidate, the outcome is `DETECTED`, while the unresolved candidate remains separately recorded.

A verified event must link to its evidence record. Search outcomes must not be inferred from a search-status label alone.

### 5.3 Minimum Search Coverage

A search can be marked `COMPLETED` with sufficient coverage only when:

- The defined search process has been executed.
- The configured source categories for that signal have been checked.
- Relevant candidate results have been assessed for attribution, relevance and recency.
- Material errors or unresolved gaps do not prevent a reliable conclusion.
- Sources checked, limitations and unresolved gaps have been recorded.

Source categories should include relevant company channels, credible business publications and suitable job platforms for the signal being investigated.

A fixed number of searches or sources alone does not establish sufficient coverage. Search depth and source categories must be configured and tested during implementation.

### 5.4 Signal Selection: Four-Test Assessment

The two selected signals are assessed against four tests to establish their commercial and operational suitability for the workflow.

| Test                    | Assessment question                                                                                                 |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Clear buying reason** | Does the signal explain why the account is worth investigating now?                                                 |
| **Enough volume**       | Does the signal occur frequently enough within the target market to contribute meaningfully to pipeline generation? |
| **Data you can get**    | Can available tools and public sources detect the signal reliably and provide verifiable evidence?                  |
| **A natural story**     | Does the signal provide an honest, relevant opening for a commercial conversation?                                  |

#### Signal Scorecard

| Test                    | `FINANCE_RECRUITMENT`                                                                                                                                                                                                                                    | `MULTI_BRANCH_EXPANSION`                                                                                                                                                                                                                                                          |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Clear buying reason** | **MODERATE:** A relevant finance or treasury vacancy creates a timely reason to investigate the company's financial operations and the capabilities it is recruiting for. Recruitment does not establish payment friction or intent to change providers. | **STRONG:** A verified outlet opening or distribution expansion creates a timely reason to investigate whether existing banking, collection and payment arrangements support the expanded operation. Expansion does not establish that existing arrangements are inadequate.      |
| **Enough volume**       | **MODERATE:** Finance and treasury vacancies occur across businesses, but the frequency of qualifying vacancies within Nigerian supermarkets and FMCG distributors must be validated against actual research results.                                    | **MODERATE:** Physical outlet and distribution-footprint expansion events provide relevant opportunities, but their frequency within the target market must be established through research.                                                                                      |
| **Data you can get**    | **STRONG:** Vacancies can be discovered through company career pages, job platforms and professional networks. Employer attribution, role responsibilities, publication date and vacancy status require verification.                                    | **MODERATE:** Expansion can be discovered through company announcements, websites, credible business publications and social media. Evidence may be fragmented, outdated or insufficiently specific about the operating entity, location or event status.                         |
| **A natural story**     | **STRONG:** A verified vacancy provides an honest opening to discuss the financial responsibilities and workflows the company is recruiting to support. The discussion must reflect the actual vacancy rather than assume an existing problem.           | **STRONG:** A verified expansion provides an honest opening to discuss how collections, settlements and payments are coordinated across the growing retail or distribution footprint. The discussion must distinguish completed expansion from announced or planned developments. |

#### Selection Decision

- `FINANCE_RECRUITMENT` remains the **primary signal** because it offers a relevant reason to investigate the finance function, has discoverable evidence sources and provides a credible commercial conversation angle.
- `MULTI_BRANCH_EXPANSION` remains the **secondary signal** because it provides a clear growth-related reason to investigate financial and payment operations, although event frequency and evidence coverage require validation.

#### Validation Requirements

The qualitative ratings are initial selection assessments, not measured market performance. In particular, the **Enough volume** and **Data you can get** assessments must be validated during implementation.

Track the following for each signal:

- Number of candidate events discovered within the defined recency window.
- Number and percentage of candidates attributable to the correct target business.
- Number and percentage of candidates meeting the signal's verification requirements.
- Number of resulting ICP-qualified accounts.
- Number of qualified accounts with sufficient evidence to enter the intended routing process.

Review the ratings against observed research results and adjust them if actual detection frequency, evidence quality or target-market coverage does not support the initial assessment.

A signal's score does not override mandatory ICP qualification, evidence requirements or human review. Neither signal establishes purchase intent or a confirmed need to change banking or payment providers.

## 6. Routing and Commercial Angles

Routing is determined by the verified ICP segment and the two signal outcomes. Each segment-signal combination must produce a relevant, evidence-based commercial angle.

Commercial angles are discovery hypotheses. They must not claim that an account has a confirmed payment problem or needs to change providers.

### 6.1 Segment-by-Signal Commercial Angle Matrix

| ICP segment          | Finance and Treasury Recruitment                                                                                                                                                                                                                   | Multi-Branch Expansion                                                                                                                                                                                                                       |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `RETAIL_SUPERMARKET` | Explore how the finance or treasury function manages collections, settlement visibility and reconciliation across existing outlets as the business recruits for the verified role. Tailor the discussion to the vacancy's actual responsibilities. | Explore how collections, settlements and financial visibility are coordinated across the retail network as the business opens or announces additional outlets or enters a new market. State whether the expansion is completed or announced. |
| `FMCG_DISTRIBUTOR`   | Explore how the finance function manages retailer collections, supplier obligations and financial visibility as the business recruits for the verified role. Tailor the discussion to the vacancy's actual responsibilities.                       | Explore how retailer collections, settlements and supplier-payment coordination are managed across the distribution footprint as the business expands into new locations or markets. State the verified nature of the expansion.             |

### 6.2 Signal Combination and Routing Rules

Apply these rules only to `QUALIFIED` accounts after both searches have terminal outcomes.

| Finance outcome       | Expansion outcome     | Routing outcome          | Priority     | Required commercial action                                                                                                                                           |
| --------------------- | --------------------- | ------------------------ | ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DETECTED`            | `DETECTED`            | `COMBINED_SIGNALS`       | `HIGHEST`    | Retain both verified events. Use the segment-specific finance and expansion angles. Choose the lead discussion topic from the actual vacancy and expansion evidence. |
| `DETECTED`            | `NOT_DETECTED`        | `FINANCE_RECRUITMENT`    | `HIGH`       | Use the finance recruitment angle for the segment. Do not imply expansion.                                                                                           |
| `NOT_DETECTED`        | `DETECTED`            | `MULTI_BRANCH_EXPANSION` | `HIGH`       | Use the expansion angle for the segment. Do not imply finance recruitment.                                                                                           |
| `NOT_DETECTED`        | `NOT_DETECTED`        | `ICP_MONITORING`         | `MONITORING` | Retain the qualified account for future monitoring. Do not create a signal-led outreach claim.                                                                       |
| Any other combination | Any other combination | `FURTHER_RESEARCH`       | `RESEARCH`   | Resolve incomplete, failed, unverified or historical evidence before releasing the account for signal-led outreach.                                                  |

**Additional routing rules:**

- Any `UNKNOWN`, `UNVERIFIED` or `HISTORICAL` outcome results in `FURTHER_RESEARCH`, unless the other search combination is already covered by a higher-confidence detected result. In all cases, unresolved evidence must remain visible.
- A verified signal must not be discarded because the other search is incomplete.
- If one signal is `DETECTED` and the other is unresolved, preserve the detected event and its provisional commercial angle. Keep the overall route at `FURTHER_RESEARCH`.
- Historical or unverified evidence never substitutes for `DETECTED`.
- An account with no detected signals is not automatically disqualified.
- ICP failures route to `ICP_DISQUALIFIED`, not to signal-led prospecting.
- ICP uncertainty routes to `FURTHER_RESEARCH` before signal research begins.

### 6.3 Required Routing Output

Every routed account must contain:

- Verified account identity and business segment.
- ICP outcome, fit tier and qualification rationale.
- Results of all six mandatory ICP conditions.
- Both signal search statuses and outcomes.
- Linked candidate and verified evidence records.
- Signal combination.
- Routing outcome and investigation priority.
- Segment-specific commercial angle.
- Supported role or persona to research.
- Routing rationale.
- Unresolved evidence gaps.
- Recommended next action.

If no individual contact has been verified, leave contact identity blank. Record the relevant role to research instead.

## 7. Variables Contract

Use three linked record types:

1. `account`: one record per distinct operating business.
2. `signal_search`: one record per account and signal type, with separate records for subsequent attempts.
3. `signal_evidence`: one record per candidate or verified event.

Fields are required unless explicitly marked nullable or conditionally required. Unknown values must remain null or use the defined `UNKNOWN` enum. Never fabricate missing values.

### 7.1 Account Record

| Field                         | Type         | Contract                                                                                                      |
| ----------------------------- | ------------ | ------------------------------------------------------------------------------------------------------------- |
| `account_id`                  | String       | Required. Stable unique account identifier.                                                                   |
| `company_name`                | String       | Required. Verified business name.                                                                             |
| `company_domain`              | String/null  | Nullable if unavailable.                                                                                      |
| `company_website`             | URL/null     | Nullable if unavailable.                                                                                      |
| `country`                     | String       | Required. Verified country of operation.                                                                      |
| `operating_locations`         | String array | Required where locations are established; otherwise null with research gap recorded.                          |
| `business_segment`            | Enum         | Required: `RETAIL_SUPERMARKET` or `FMCG_DISTRIBUTOR`.                                                         |
| `business_description`        | String       | Required. Evidence-based description of actual business activity.                                             |
| `branch_count`                | Integer/null | Nullable. Verified physical retail outlet count only. Unknown is null, not zero.                              |
| `warehouse_depot_count`       | Integer/null | Nullable. Verified distribution facility count only. Unknown is null, not zero.                               |
| `identity_source_url`         | URL          | Required to verify identity.                                                                                  |
| `identity_verified_at`        | Datetime     | Required when identity is verified.                                                                           |
| `geographic_fit`              | Enum         | Required: `PASS`, `FAIL` or `UNKNOWN`.                                                                        |
| `identity_fit`                | Enum         | Required: `PASS`, `FAIL` or `UNKNOWN`.                                                                        |
| `segment_fit`                 | Enum         | Required: `PASS`, `FAIL` or `UNKNOWN`.                                                                        |
| `active_operations_fit`       | Enum         | Required: `PASS`, `FAIL` or `UNKNOWN`.                                                                        |
| `physical_operations_fit`     | Enum         | Required: `PASS`, `FAIL` or `UNKNOWN`.                                                                        |
| `business_relevance_fit`      | Enum         | Required: `PASS`, `FAIL` or `UNKNOWN`.                                                                        |
| `icp_outcome`                 | Enum         | Required: `QUALIFIED`, `DISQUALIFIED` or `FURTHER_RESEARCH`.                                                  |
| `icp_fit_tier`                | Enum         | Required after assessment: `EXCELLENT_FIT`, `REASONABLE_FIT` or `UNASSESSED`.                                 |
| `icp_rationale`               | String       | Required. Explains the qualification decision and fit tier.                                                   |
| `icp_evidence_urls`           | URL array    | Required. Sources supporting qualification decisions.                                                         |
| `workflow_status`             | Enum         | Required. Lifecycle status defined in Section 3.                                                              |
| `routing_outcome`             | Enum         | Required after routing. Must use Section 6 values.                                                            |
| `investigation_priority`      | Enum         | Required after routing: `HIGHEST`, `HIGH`, `MONITORING`, `RESEARCH` or `EXCLUDED`.                            |
| `detected_signal_combination` | Enum         | Required after both searches: `FINANCE_ONLY`, `EXPANSION_ONLY`, `BOTH`, `NEITHER` or `INSUFFICIENT_EVIDENCE`. |
| `commercial_angle`            | String/null  | Required for detected signal routes; nullable for monitoring and unresolved research.                         |
| `routing_rationale`           | String       | Required after routing. Explains the decision using recorded evidence.                                        |
| `recommended_next_action`     | String       | Required after routing.                                                                                       |
| `human_review_status`         | Enum         | Required before approval: `PENDING`, `APPROVED`, `REJECTED` or `MORE_RESEARCH_REQUIRED`.                      |
| `human_review_notes`          | String/null  | Required when a reviewer makes a decision.                                                                    |
| `crm_sync_status`             | Enum         | Required: `NOT_READY`, `READY`, `SYNCED` or `SYNC_FAILED`.                                                    |

### 7.2 Signal Search Record

| Field                   | Type          | Contract                                                                 |
| ----------------------- | ------------- | ------------------------------------------------------------------------ |
| `signal_search_id`      | String        | Required. Unique identifier for each search attempt.                     |
| `account_id`            | String        | Required. Parent account identifier.                                     |
| `signal_type`           | Enum          | Required: `FINANCE_RECRUITMENT` or `MULTI_BRANCH_EXPANSION`.             |
| `search_status`         | Enum          | Required. Values defined in Section 5.2.                                 |
| `signal_outcome`        | Enum          | Required when an outcome can be assigned. Values defined in Section 5.2. |
| `search_started_at`     | Datetime/null | Required once search begins.                                             |
| `search_completed_at`   | Datetime/null | Required when search reaches a terminal status.                          |
| `sources_checked`       | String array  | Required when research begins. Records actual sources checked.           |
| `search_coverage_notes` | String        | Required before a search can be marked sufficiently complete.            |
| `search_error`          | String/null   | Required when a search fails; otherwise null.                            |
| `attempt_number`        | Integer       | Required. Starts at 1 and increments for each retry.                     |
| `previous_search_id`    | String/null   | Null for first attempt; otherwise links to previous attempt.             |

### 7.3 Signal Evidence Record

| Field                    | Type               | Contract                                                                                                |
| ------------------------ | ------------------ | ------------------------------------------------------------------------------------------------------- |
| `signal_event_id`        | String             | Required. Unique event identifier.                                                                      |
| `signal_search_id`       | String             | Required. Links evidence to its search attempt.                                                         |
| `account_id`             | String             | Required. Parent account identifier.                                                                    |
| `signal_type`            | Enum               | Required. Finance recruitment or expansion.                                                             |
| `evidence_status`        | Enum               | Required: `CANDIDATE`, `VERIFIED`, `REJECTED` or `HISTORICAL`.                                          |
| `event_description`      | String             | Required. Describes the reported event.                                                                 |
| `source_name`            | String             | Required. Identifies the source.                                                                        |
| `source_url`             | URL                | Required. Direct source link.                                                                           |
| `published_at`           | Date/datetime/null | Publication date. Null if unavailable.                                                                  |
| `event_date`             | Date/datetime/null | Actual or expected event date. Null if unavailable.                                                     |
| `verified_at`            | Datetime/null      | Required when verified.                                                                                 |
| `evidence_excerpt`       | String/null        | Required for verified evidence; otherwise nullable.                                                     |
| `verification_notes`     | String/null        | Required when verified or when a candidate needs explanation.                                           |
| `rejection_reason`       | String/null        | Required when evidence is rejected.                                                                     |
| `job_title`              | String/null        | Finance recruitment only.                                                                               |
| `job_employer`           | String/null        | Finance recruitment only.                                                                               |
| `job_description_url`    | URL/null           | Finance recruitment only.                                                                               |
| `job_status`             | Enum/null          | Finance recruitment only: `OPEN`, `CLOSED`, `EXPIRED` or `UNKNOWN`.                                     |
| `job_function_relevance` | Enum/null          | Finance recruitment only: `RELEVANT`, `NOT_RELEVANT` or `UNKNOWN`.                                      |
| `expansion_type`         | Enum/null          | Expansion only: `NEW_OUTLET`, `NEW_DEPOT`, `NEW_WAREHOUSE`, `NEW_MARKET` or `OTHER_VERIFIED_EXPANSION`. |
| `expansion_location`     | String/null        | Expansion only. Verified location or market.                                                            |
| `expansion_event_status` | Enum/null          | Expansion only: `COMPLETED`, `ANNOUNCED`, `PLANNED` or `UNVERIFIED`.                                    |
| `new_locations_count`    | Integer/null       | Nullable. Record only when supported by evidence.                                                       |
| `recency_days`           | Integer/null       | Derived from the relevant event date or publication date, with the date basis recorded.                 |

### 7.4 Data Integrity and Ownership Rules

- Every material account fact and detected event must link to its source.
- Keep publication date, event date and verification date distinct.
- `VERIFIED` requires all evidence requirements for the relevant signal type.
- Retain rejected candidates and rejection reasons for auditability.
- Multiple vacancies or expansion events create separate evidence records.
- Deduplicate using verified domain where possible, supported by business name, location and entity checks.
- Do not merge similarly named businesses or distinct legal entities without evidence.
- Preserve conflicting sources and flag them for human resolution.
- AI interpretation must remain distinguishable from source facts.
- Discovery owns provisional account records; verification owns identity and firmographics; ICP screening owns qualification fields; signal research owns search and candidate records; evidence validation owns evidence status; routing owns route and angle; reviewers own approval; CRM preparation owns sync status.
- Downstream stages must not silently overwrite source facts, earlier search attempts or previous decisions.

## 8. Execution, Retry and Human Review

### 8.1 Execution Order

1. Discover a candidate business.
2. Create or retrieve its account record.
3. Verify identity and Nigerian operations.
4. Check for duplicates.
5. Evaluate all mandatory ICP conditions.
6. If disqualified, stop signal-led qualification and record the reason.
7. If ICP evidence is incomplete, route to `FURTHER_RESEARCH`.
8. If qualified, initiate finance recruitment and expansion searches independently.
9. Store candidate events and source evidence.
10. Validate event attribution, relevance and recency.
11. Determine each signal outcome using Section 5.
12. Apply the deterministic routing rules in Section 6.
13. Generate the segment-specific commercial angle and next action.
14. Submit the account for human review.
15. Prepare approved records for authorised CRM processing.

### 8.2 Retry and Recalculation

- Failed, incomplete and insufficient-coverage searches may be retried.
- Every retry creates a new search-attempt record.
- Retain previous timestamps, sources, outcomes, errors and evidence.
- A retry must not silently overwrite an earlier result.
- When a signal outcome changes, recalculate the signal combination, routing outcome, priority and commercial angle.
- Preserve previous routing decisions and the evidence on which they were based.
- Reassess recency when a record is refreshed.
- If a previously detected event becomes invalid or stale, update its evidence status and recalculate the account route.

### 8.3 Human Review

The reviewer must verify:

- Company identity and Nigerian operations.
- Approved segment and all mandatory ICP conditions.
- Fit tier and its supporting evidence.
- Search coverage and both signal outcomes.
- Event attribution, relevance and recency.
- Evidence URLs and source quality.
- Persona or role relevance.
- Commercial angle and recommended next action.
- Absence of unsupported claims about payment problems or purchase intent.

Review decisions:

- `APPROVED`
- `REJECTED`
- `MORE_RESEARCH_REQUIRED`

No account reaches `CRM_READY` without human approval and all required fields.

### 8.4 Acceptance Tests

- Both approved segments can qualify independently of signal detection.
- Fuel stations, unrelated SMEs and online-only retailers are excluded.
- A single-location high-volume supermarket is not automatically disqualified.
- Five or more locations improves prioritisation but is not a mandatory qualification threshold.
- An ICP failure stops signal-led qualification.
- Unknown ICP evidence produces `FURTHER_RESEARCH`, not `DISQUALIFIED`.
- Finance-only detection routes to `FINANCE_RECRUITMENT` with the correct segment angle.
- Expansion-only detection routes to `MULTI_BRANCH_EXPANSION` with the correct segment angle.
- Both detected signals route to `COMBINED_SIGNALS`.
- Two completed searches with sufficient coverage and no qualifying evidence route to `ICP_MONITORING`.
- An incomplete, failed or insufficient-coverage search cannot produce `NOT_DETECTED`.
- An unresolved candidate produces `UNVERIFIED`, not `NOT_DETECTED`.
- Closed or expired vacancies do not qualify as active recruitment.
- Announced expansion remains labelled `ANNOUNCED`, not operational.
- Warehouse or depot activity qualifies only when it represents a genuine distribution-footprint expansion.
- A verified signal is preserved when the other search remains unresolved.
- Duplicate accounts are not treated as new businesses.
- Retries preserve previous attempts and recalculate routing when outcomes change.
- No account reaches `CRM_READY` without human approval.

The workflow is implementation-ready when its states, qualification rules, evidence requirements, routing decisions, field contracts and acceptance tests can be implemented without inventing additional business rules. Clay providers, formulas, integrations and credit costs remain implementation decisions to test.

The existing Python research foundation, including DDGS discovery, Trafilatura extraction, Gemini-assisted research and JSON provenance, supports research activities. It does not establish that the Clay workflow has been built or is operational.

## 9. Design Principle

Prioritise evidence-backed commercial relevance over lead volume.

Every account must be traceable from verified identity through ICP qualification, independent signal research, evidence validation and deterministic routing. Every commercial angle must follow from the account's segment and verified signal evidence.

The workflow identifies businesses worth investigating. It does not manufacture buying intent.
