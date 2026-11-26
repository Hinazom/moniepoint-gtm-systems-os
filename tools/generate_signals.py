
import os
import json
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

from google import genai
from dotenv import load_dotenv
from ddgs import DDGS
from trafilatura import fetch_url, extract


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")

client = genai.Client(api_key=api_key)
model_name = "gemini-3.1-flash-lite"

root = Path.cwd()
icp_path = root / "icp" / "icp.md"
output_path = root / "icp" / "signals.md"
research_directory = root / "research" / "signals"

max_results_per_query = 5
max_page_chars = 4500
max_total_evidence_chars = 95000


# load the approved ICP.
if not icp_path.exists():
    raise FileNotFoundError(
        f"Could not find {icp_path}. Generate the ICP document first."
    )

icp_context = icp_path.read_text(encoding="utf-8")

if not icp_context.strip():
    raise ValueError("The ICP document is empty.")


# define research coverage across all approved ICP segments.
research_queries = [
    {
        "area": "moniepoint_products",
        "query": "Moniepoint Nigeria official business banking products business account POS payments collections settlement reconciliation"
    },
    {
        "area": "fmcg_distributors",
        "query": "Nigeria FMCG distributors wholesalers distribution depots warehouses expansion supplier payments trade receivables"
    },
    {
        "area": "fmcg_distributors",
        "query": "Nigeria FMCG distribution companies finance manager treasury controller accountant recruitment"
    },
    {
        "area": "fmcg_distributors",
        "query": "Nigeria FMCG distributors new distribution agreements regional expansion warehouse investment 2025 2026"
    },
    {
        "area": "petrol_station_networks",
        "query": "Nigeria petrol station networks new station openings acquisitions expansion 2025 2026"
    },
    {
        "area": "petrol_station_networks",
        "query": "Nigeria petrol stations digital payments POS settlement delays cash reconciliation working capital"
    },
    {
        "area": "petrol_station_networks",
        "query": "Nigeria fuel retail companies CNG EV infrastructure investment station expansion"
    },
    {
        "area": "petrol_station_networks",
        "query": "Nigeria petrol station companies finance manager treasury accountant recruitment"
    },
    {
        "area": "retail_chains_supermarkets",
        "query": "Nigeria supermarket chains retail groups new store openings geographic expansion 2025 2026"
    },
    {
        "area": "retail_chains_supermarkets",
        "query": "Nigeria supermarket retail chains finance manager treasury internal audit accountant recruitment"
    },
    {
        "area": "retail_chains_supermarkets",
        "query": "Nigeria supermarket chains POS payment infrastructure inventory financial management systems"
    },
    {
        "area": "retail_chains_supermarkets",
        "query": "Nigeria retail chains acquisitions franchise expansion new outlets"
    },
    {
        "area": "qsr_groups",
        "query": "Nigeria quick service restaurant groups restaurant chains new outlets franchise expansion 2025 2026"
    },
    {
        "area": "qsr_groups",
        "query": "Nigeria restaurant groups QSR finance manager accountant treasury recruitment"
    },
    {
        "area": "qsr_groups",
        "query": "Nigeria restaurant chains POS payment systems delivery operations reconciliation technology"
    },
    {
        "area": "pharmacy_chains",
        "query": "Nigeria pharmacy chains retail pharmacy groups new branches expansion acquisitions 2025 2026"
    },
    {
        "area": "pharmacy_chains",
        "query": "Nigeria pharmacy chains finance manager accountant treasury recruitment"
    },
    {
        "area": "pharmacy_chains",
        "query": "Nigeria pharmacy chains inventory POS payment technology supplier payments"
    },
    {
        "area": "logistics_haulage",
        "query": "Nigeria logistics haulage companies fleet expansion new depots contracts 2025 2026"
    },
    {
        "area": "logistics_haulage",
        "query": "Nigeria logistics haulage companies finance manager treasury accountant recruitment"
    },
    {
        "area": "logistics_haulage",
        "query": "Nigeria fleet operators driver payments fuel expenses supplier payments cash flow"
    },
    {
        "area": "healthcare_diagnostics",
        "query": "Nigeria diagnostic laboratory healthcare networks new branches facilities expansion 2025 2026"
    },
    {
        "area": "healthcare_diagnostics",
        "query": "Nigeria private healthcare diagnostic networks finance manager accountant treasury recruitment"
    },
    {
        "area": "healthcare_diagnostics",
        "query": "Nigeria diagnostic centres patient billing payment systems financial management reconciliation"
    },
    {
        "area": "cross_segment_signals",
        "query": "Nigeria companies finance controller treasury manager internal auditor accountant recruitment business expansion"
    },
    {
        "area": "cross_segment_signals",
        "query": "Nigeria businesses new branches acquisitions facility openings expansion announcements 2025 2026"
    },
    {
        "area": "cross_segment_signals",
        "query": "Nigeria businesses payment settlement delays POS reconciliation digital payment infrastructure challenges"
    },
    {
        "area": "cross_segment_signals",
        "query": "Nigeria companies payment provider migration POS deployment payment gateway adoption"
    },
    {
        "area": "cross_segment_signals",
        "query": "Nigeria businesses supplier agreements distribution contracts procurement partnerships expansion"
    },
]


# standardise URLs to reduce duplicate search results.
def normalise_url(url):
    try:
        parsed = urlsplit(url)

        ignored_parameters = {
            "fbclid",
            "gclid",
            "ref",
            "source",
            "mc_cid",
            "mc_eid"
        }

        parameters = [
            (key, value)
            for key, value in parse_qsl(parsed.query)
            if not key.lower().startswith("utm_")
            and key.lower() not in ignored_parameters
        ]

        return urlunsplit((
            parsed.scheme.lower(),
            parsed.netloc.lower(),
            parsed.path.rstrip("/"),
            urlencode(parameters),
            ""
        ))

    except Exception:
        return url


# discover evidence for each research area.
print("\nStarting buying signals research...")

search_sources = []
seen_urls = set()
search_failures = []

with DDGS() as ddgs:
    for item in research_queries:
        query = item["query"]
        area = item["area"]

        print(f"\nSearching [{area}]: {query}")

        try:
            results = ddgs.text(
                query,
                max_results=max_results_per_query
            )

            for result in results:
                url = result.get("href")

                if not url:
                    continue

                normalized_url = normalise_url(url)

                if normalized_url in seen_urls:
                    continue

                seen_urls.add(normalized_url)

                search_sources.append({
                    "title": result.get("title"),
                    "url": url,
                    "normalized_url": normalized_url,
                    "snippet": result.get("body"),
                    "query": query,
                    "research_area": area
                })

        except Exception as e:
            search_failures.append({
                "query": query,
                "research_area": area,
                "error": str(e)
            })
            print(f"Search failed: {e}")


print(f"\nCollected {len(search_sources)} unique search results.")

if not search_sources:
    raise RuntimeError(
        "No search results were collected. "
        "Check your internet connection or DDGS availability."
    )


# extract webpage content and preserve search snippets as weaker evidence.
evidence_trail = []

full_page_count = 0
snippet_count = 0
unusable_count = 0

for idx, source in enumerate(search_sources, 1):
    source_id = f"S{idx:03d}"
    url = source["url"]

    print(f"\nExtracting [{source_id}]: {url}")

    extracted_text = None

    try:
        downloaded = fetch_url(url)

        if downloaded:
            extracted_text = extract(
                downloaded,
                include_comments=False,
                include_tables=True
            )

    except Exception as e:
        print(f"Extraction failed for {url}: {e}")

    if extracted_text and extracted_text.strip():
        evidence = extracted_text[:max_page_chars]
        evidence_type = "Full page extraction"
        full_page_count += 1

    else:
        evidence = source.get("snippet") or ""

        if evidence.strip():
            evidence_type = "Search snippet only"
            snippet_count += 1
        else:
            evidence_type = "No usable content"
            unusable_count += 1

    evidence_trail.append({
        "id": source_id,
        "title": source.get("title"),
        "url": url,
        "normalized_url": source.get("normalized_url"),
        "search_query": source.get("query"),
        "research_area": source.get("research_area"),
        "evidence_type": evidence_type,
        "content": evidence,
        "included_in_gemini_prompt": False
    })


print("\nEvidence collection completed.")
print(f"Full pages extracted: {full_page_count}")
print(f"Search snippets used: {snippet_count}")
print(f"Sources without usable content: {unusable_count}")

usable_sources = [
    source for source in evidence_trail
    if source["content"].strip()
]

if not usable_sources:
    raise RuntimeError(
        "No usable evidence was collected. "
        "Gemini will not be called with an empty evidence set."
    )


# save the complete evidence register.
research_directory.mkdir(parents=True, exist_ok=True)

source_register_path = research_directory / "source_register.json"

def save_source_register():
    with open(source_register_path, "w", encoding="utf-8") as f:
        json.dump(
            evidence_trail,
            f,
            indent=4,
            ensure_ascii=False
        )

save_source_register()


# prepare evidence without exceeding the configured prompt limit.
prompt_evidence_parts = []
total_evidence_chars = 0
included_source_count = 0

for source in usable_sources:
    header = (
        f"\n\n--- SOURCE [{source['id']}] ---\n"
        f"Title: {source['title']}\n"
        f"URL: {source['url']}\n"
        f"Research area: {source['research_area']}\n"
        f"Search query: {source['search_query']}\n"
        f"Evidence type: {source['evidence_type']}\n"
        f"Content:\n"
    )

    remaining_chars = (
        max_total_evidence_chars
        - total_evidence_chars
        - len(header)
    )

    if remaining_chars <= 0:
        break

    prompt_content = source["content"][:remaining_chars]

    prompt_evidence_parts.append(header + prompt_content)

    source["included_in_gemini_prompt"] = True
    source["prompt_content_length"] = len(prompt_content)
    source["prompt_content_truncated"] = (
        len(prompt_content) < len(source["content"])
    )

    total_evidence_chars += len(header) + len(prompt_content)
    included_source_count += 1

scraped_evidence = "".join(prompt_evidence_parts)

if not scraped_evidence.strip():
    raise RuntimeError("The evidence prepared for Gemini is empty.")

save_source_register()

print(f"\nSources included in Gemini prompt: {included_source_count}")
print(f"Evidence characters: {total_evidence_chars}")


# analyse buying signals without changing the approved ICP.
prompt = f"""
# MONIEPOINT BUYING SIGNALS RESEARCH

## 1. Authoritative ICP

The following ICP document is the approved campaign definition.

Treat it as authoritative.

Preserve its approved customer segments, priority classifications,
mandatory qualification criteria, commercial focus and product proposition.

Do not rewrite, broaden, replace or independently reconsider the ICP.

Do not introduce additional target segments.

Do not demote or remove any approved segment.

Do not invent mandatory qualification thresholds.

Your task is to identify buying signals that help identify businesses
within this existing ICP that may have a genuine purchasing opportunity.

{icp_context}


## 2. Approved Segment Structure

Preserve these classifications throughout the report.

Primary:
- FMCG distributors and wholesalers.
- Petrol station networks.
- Retail chains and supermarkets.

Secondary:
- Quick-service restaurant groups.
- Pharmacy chains.

Emerging:
- Logistics and haulage businesses.
- Specialised healthcare and diagnostic networks.

Research all seven segments.

Do not assume that every company within a segment is qualified.


## 3. Research Evidence

The following evidence was collected through web searches and webpage extraction.

Use only the supplied source IDs when citing evidence.

{scraped_evidence}


## 4. Research Objective

Identify observable business events, operational changes, financial developments
and commercial activities that may indicate a genuine need for Moniepoint
Business Banking and Payments.

For every proposed signal, explain:

- What happened.
- Which business it happened to.
- Which approved segment it relates to.
- Why it may indicate a purchasing need.
- Which documented Moniepoint capability may be relevant.
- How the event can be detected.
- What evidence is needed to verify it.
- How recently it must have occurred.
- What alternative explanations may exist.

Distinguish a company characteristic from a buying signal.

For example, operating several branches may indicate ICP fit.
Opening new branches is a potential buying signal.


## 5. Segment-Specific Research

Investigate the following signals separately.

### FMCG distributors and wholesalers

- New warehouses and distribution depots.
- Geographic distribution expansion.
- New supplier and distribution agreements.
- Changes in trade receivables and credit-based sales.
- Finance, treasury and accounting recruitment.
- Increased supplier-payment complexity.
- Inventory and working-capital changes.
- Payment and reconciliation challenges.

### Petrol station networks

- New station openings.
- Station acquisitions and network expansion.
- CNG, EV and diversified retail investments.
- Digital payment and POS adoption.
- Settlement and reconciliation problems.
- Changes in cash-management operations.
- Finance and treasury recruitment.
- Fuel restocking and working-capital pressures.

### Retail chains and supermarkets

- New store openings and geographic expansion.
- Acquisitions and outlet consolidation.
- Changes in transaction and payment complexity.
- POS and payment infrastructure deployments.
- Inventory and financial-management system changes.
- Finance, treasury and internal audit recruitment.
- Reconciliation challenges across outlets.
- Changes in supplier-payment operations.

### Quick-service restaurant groups

- New restaurant outlets and franchise expansion.
- Geographic expansion and acquisitions.
- Payment-channel changes.
- POS and restaurant-management technology deployments.
- Finance and accounting recruitment.
- Delivery and collection payment changes.
- Reconciliation across multiple locations.

### Pharmacy chains

- New pharmacy outlets and acquisitions.
- Geographic expansion.
- Inventory, POS and management-system changes.
- Finance and accounting recruitment.
- Supplier-payment changes.
- Payment and reconciliation challenges.
- Expansion into new retail and healthcare services.

### Logistics and haulage businesses

- Fleet expansion and depot openings.
- New contracts and commercial partnerships.
- Geographic expansion.
- Finance and treasury recruitment.
- Driver payments and fleet expenses.
- Supplier and maintenance-payment complexity.
- Cash-flow and reconciliation challenges.

### Specialised healthcare and diagnostic networks

- New diagnostic centres and facilities.
- Geographic and multi-branch expansion.
- Corporate and institutional partnerships.
- Billing and payment infrastructure changes.
- Finance, accounting and treasury recruitment.
- Payment and reconciliation complexity.

These are research hypotheses, not predetermined findings.
Do not present them as established buying signals without evidence.


## 6. Cross-Segment Signals

Investigate signals that may apply across multiple segments:

- Finance and treasury recruitment.
- New branches, depots, stations and facilities.
- Acquisitions and ownership changes.
- Supplier and distribution agreements.
- Payment infrastructure deployments.
- Payment-provider migrations.
- Settlement and reconciliation problems.
- Financial management system changes.
- Expansion-related increases in payment complexity.
- New contracts that materially increase transaction volumes.

Explain differences in relevance between segments.


## 7. Commercial Signal Categories

Organise the findings into five categories:

1. Financial complexity.
2. Operational expansion.
3. Payment infrastructure changes.
4. Working-capital pressure.
5. Commercial and organisational change.

For each signal, explain the relationship between the observed event
and the underlying financial or operational problem.

Do not assume that every signal creates an immediate purchasing opportunity.


## 8. Signal Strength and Evidence Assessment

Classify each signal as:

- Strong.
- Moderate.
- Weak.
- Unvalidated hypothesis.

Assess each signal using:

- Directness of evidence.
- Reliability of the source.
- Relevance to Moniepoint's documented capabilities.
- Commercial significance.
- Recency.
- Detectability.
- Likelihood of indicating a genuine purchasing need.

Explain the classification.

Do not invent numerical scores or arbitrary thresholds.

A signal must not be classified as strong simply because it sounds commercially attractive.


## 9. Evidence Validation

For every important signal and associated claim:

- Identify the source ID.
- Explain precisely what the source establishes.
- Distinguish company-specific evidence from general market evidence.
- Distinguish direct observations from inference.
- Identify whether evidence comes from a full-page extraction or search snippet.
- Identify duplicate or syndicated reporting where apparent.
- Identify sources that are promotional, commercial or otherwise potentially biased.
- State when a source does not establish the claimed purchasing need.

Never use a source merely because its title appears relevant.

Never invent citations.

Never cite a source that does not support the accompanying claim.

Do not treat multiple reports about the same underlying announcement as independent corroboration.


## 10. Signal Combinations

Investigate combinations such as:

- Branch expansion plus finance recruitment.
- New depots plus supplier-payment complexity.
- Petrol station expansion plus payment infrastructure changes.
- Retail expansion plus reconciliation-related recruitment.
- New healthcare facilities plus financial-system changes.
- Fleet expansion plus driver and supplier payment complexity.

For each combination, explain:

- Why the signals may reinforce each other.
- Which segments are relevant.
- What additional evidence would strengthen the inference.
- What alternative explanations remain possible.

Do not claim that a combination establishes an imminent provider switch without direct evidence.


## 11. False Positives and Qualification Safeguards

Investigate misleading indicators such as:

- Routine replacement recruitment.
- General hiring unrelated to financial complexity.
- Announced expansion that has not occurred.
- Franchise outlets incorrectly attributed to the parent company.
- Old vacancies.
- Generic POS adoption without evidence of a wider financial need.
- General market statistics attributed to an individual company.
- Acquisitions incorrectly attributed to subsidiaries.
- Ownership changes without evidence of operational or financial changes.

Keep these stages separate:

1. ICP qualification.
2. Buying signal detection.
3. Account prioritisation.
4. Contact readiness.

A missing public buying signal must not automatically disqualify an otherwise qualified ICP account.

Absence of public evidence is not proof that a business lacks the underlying need.

Use:
- DETECTED.
- NOT DETECTED.
- UNRESOLVED.
- RESEARCH REQUIRED.

Do not convert insufficient evidence into a negative qualification decision.


## 12. Practical Detection Framework

For each signal, specify:

- Signal name.
- Description.
- Applicable segments.
- Segment priority.
- Search keywords.
- Likely public sources.
- Evidence to capture.
- Recency information.
- Verification method.
- False-positive risks.
- Recommended status.
- Human-review requirements.

Distinguish what can be automated from what requires manual verification.

Do not invent Clay integrations or provider capabilities.

Explain how to associate the evidence with the correct company, parent,
subsidiary, brand or operating entity.


## 13. Recommended Clay Fields

Recommend practical fields that support subsequent account research.

Consider:

- signal_type
- signal_detected
- signal_status
- signal_date
- signal_source_url
- signal_evidence
- signal_confidence
- signal_relevance
- applicable_segment
- finance_role_relevance
- expansion_type
- ownership_model
- confirmed_location_count
- signal_verification_status

Recommend suitable data types and explain their purpose.

Do not make an unsupported signal a mandatory qualification condition.

Do not make a buying signal a substitute for the ICP's mandatory criteria.


## 14. Research Standards

1. Preserve the approved ICP exactly as the campaign definition.
2. Research all seven approved segments.
3. Do not introduce new segments.
4. Do not change mandatory qualification requirements.
5. Do not invent segment thresholds.
6. Use supplied source IDs only.
7. Validate citations against the actual evidence.
8. Distinguish facts, inferences and hypotheses.
9. Treat snippets as weaker evidence than extracted content.
10. Identify duplicates and syndicated reporting.
11. Distinguish company-specific evidence from market-wide observations.
12. Do not fabricate market statistics or purchasing behaviour.
13. Do not assume company growth equals buying intent.
14. Do not assume that public evidence represents all company operations.
15. Do not claim an imminent purchasing decision without direct evidence.
16. Explain research limitations.
17. Do not claim Moniepoint offers undocumented capabilities.
18. Never use em dashes.
19. Use clean Markdown without escaped table delimiters, HTML entities
    or unnecessary bold formatting.


## 15. Required Deliverable

Produce a comprehensive Markdown document at:

icp/signals.md

Use this structure:

1. Research scope and methodology.
2. Approved ICP segments and priority classifications.
3. Executive summary.
4. Segment-specific buying signals.
5. Cross-segment buying signals.
6. Commercial signal categories.
7. Signal strength and evidence assessment.
8. High-value signal combinations.
9. False positives and qualification safeguards.
10. Practical detection and verification framework.
11. Recommended Clay fields and logic.
12. Research gaps and unvalidated hypotheses.
13. Final buying signals recommendations.
14. Research sources and evidence trail.

Conclude with:

- Strongest evidence-supported signals for each segment.
- Signals that remain hypotheses.
- Most useful combinations.
- Important false positives.
- Signals suitable for automated detection.
- Signals requiring human verification.
- Research gaps.

The final document must support the existing ICP.
It must not replace or rewrite it.
"""


print("\nRequesting buying signals analysis from Gemini...")

response = client.models.generate_content(
    model=model_name,
    contents=prompt
)

content = response.text

if not content or not content.strip():
    raise ValueError(
        "Gemini returned an empty response. "
        "The existing signals file will not be overwritten."
    )


# append the complete source register to the report.
evidence_markdown = "\n\n## Research Sources and Evidence Trail\n"

for source in evidence_trail:
    evidence_markdown += (
        f"\n- [{source['id']}] "
        f"[{source['title'] or 'Untitled source'}]"
        f"({source['url']})"
        f" | Research area: {source['research_area']}"
        f" | Evidence: {source['evidence_type']}"
    )

final_output = content.strip() + evidence_markdown


# save the report using a temporary file to protect the previous version.
output_path.parent.mkdir(parents=True, exist_ok=True)

temporary_output_path = output_path.with_suffix(".tmp")

temporary_output_path.write_text(
    final_output,
    encoding="utf-8"
)

temporary_output_path.replace(output_path)


# record the research activity in the weekly work log.
now = datetime.now()
iso_calendar = now.isocalendar()

work_log_path = (
    root
    / "work-log"
    / f"{iso_calendar.year}-W{iso_calendar.week:02d}.md"
)

work_log_path.parent.mkdir(parents=True, exist_ok=True)

timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

log_entry = (
    f"\n- [{timestamp}] "
    f"Generated Moniepoint buying signals research using "
    f"DDGS, Trafilatura and Gemini 3.1 Flash Lite. "
    f"Collected {len(search_sources)} unique search results, "
    f"extracted {full_page_count} full pages, used "
    f"{snippet_count} search snippets and recorded "
    f"{unusable_count} sources without usable content. "
    f"Included {included_source_count} sources in the Gemini prompt. "
    f"Researched all seven approved ICP segments while preserving "
    f"the existing ICP as the authoritative campaign definition. "
    f"Saved signals to `{output_path}` and the source "
    f"register to `{source_register_path}`."
)

with open(work_log_path, "a", encoding="utf-8") as log_file:
    log_file.write(log_entry)


print("\n========================================")
print("MONIEPOINT BUYING SIGNALS RESEARCH COMPLETED")
print("========================================")
print(f"Search results: {len(search_sources)}")
print(f"Full pages extracted: {full_page_count}")
print(f"Snippet fallbacks: {snippet_count}")
print(f"Sources without usable content: {unusable_count}")
print(f"Search failures: {len(search_failures)}")
print(f"Sources included in Gemini prompt: {included_source_count}")
print(f"Evidence characters: {total_evidence_chars}")
print(f"Signals document: {output_path}")
print(f"Source register: {source_register_path}")
print(f"Work log: {work_log_path}")
print("========================================")
