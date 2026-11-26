import os
import re
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from google import genai
from dotenv import load_dotenv
from ddgs import DDGS
from trafilatura import fetch_url, extract


load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")

client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-3.1-flash-lite"

ROOT = Path.cwd()

RESEARCH_DIR = ROOT / "research" / "icp"
OUTPUT_DIR = ROOT / "icp"

SOURCE_REGISTER_PATH = RESEARCH_DIR / "source_register.json"
OUTPUT_PATH = OUTPUT_DIR / "icp.md"

MAX_RESULTS_PER_QUERY = 3
MAX_PAGE_CHARS = 3000
MAX_TOTAL_EVIDENCE_CHARS = 110000

REQUEST_TIMEOUT = 20

RESEARCH_TIMESTAMP = datetime.now(timezone.utc).isoformat()


# these are investigation categories, not predetermined icps
RESEARCH_AREAS = {
    "moniepoint_products": [
        "Moniepoint Nigeria official business banking products POS merchant payments business accounts settlements",
        "Moniepoint Nigeria official business banking collections transfers payment infrastructure enterprise products",
        "Moniepoint Nigeria business banking pricing merchant services official website",
    ],

    "restaurants_and_food_service": [
        "Nigeria restaurant groups multi outlet restaurant chains business operations payments POS",
        "Nigeria quick service restaurant chains franchise groups expansion outlets",
        "Nigeria restaurant hospitality industry supplier payments collections reconciliation operations",
    ],

    "supermarkets_and_grocery": [
        "Nigeria supermarket chains grocery retail groups multiple outlets expansion",
        "Nigeria independent supermarket operators grocery retail business payments",
        "Nigeria supermarket retail POS collections branch reconciliation supplier payments",
    ],

    "fmcg_distribution_and_wholesale": [
        "Nigeria FMCG distributors wholesalers distribution networks retailer collections payments",
        "Nigeria wholesale distribution companies FMCG supplier payments trade receivables",
        "Nigeria distributors depots warehouses multi location financial operations",
    ],

    "fuel_and_energy_retail": [
        "Nigeria petrol station networks filling station groups multiple locations payments",
        "Nigeria fuel retail station operators POS collections daily settlement operations",
    ],

    "pharmacy_and_health_retail": [
        "Nigeria pharmacy chains retail pharmacy groups multiple branches payments",
        "Nigeria pharmaceutical wholesalers distributors retailer collections operations",
    ],

    "hospitality_and_accommodation": [
        "Nigeria hotel groups hospitality chains multiple properties payment operations",
        "Nigeria hotels resorts accommodation businesses POS collections reconciliation",
    ],

    "healthcare_providers": [
        "Nigeria private hospital groups diagnostic centres clinic networks payments",
        "Nigeria healthcare providers multi location collections billing supplier payments",
    ],

    "education": [
        "Nigeria private school groups multi campus education operators fee collections",
        "Nigeria educational institutions payment collection reconciliation operations",
    ],

    "logistics_and_transport": [
        "Nigeria logistics companies transport operators distribution networks payment collections",
        "Nigeria haulage fleet companies multi location financial operations supplier payments",
    ],

    "building_materials_and_trade": [
        "Nigeria building materials distributors wholesalers construction supply businesses payments",
        "Nigeria cement steel hardware distribution companies dealer collections supplier payments",
    ],

    "electronics_and_appliances": [
        "Nigeria electronics retail chains appliance stores multiple branches POS payments",
        "Nigeria electronics distributors wholesale retailer collections operations",
    ],

    "fashion_and_specialty_retail": [
        "Nigeria fashion retail chains apparel stores multiple outlets payments",
        "Nigeria specialty retail chains multi branch collections supplier payments",
    ],

    "general_retail_and_commerce": [
        "Nigeria multi branch retail companies physical stores payment collection operations",
        "Nigeria wholesale retail trading companies multiple locations business payments",
    ],

    "cross_sector_financial_operations": [
        "Nigeria businesses multi branch POS reconciliation cash management supplier payments case study",
        "Nigeria business payment collection settlement reconciliation challenges retail distribution hospitality",
        "Nigeria finance treasury recruitment multi branch retail distribution hospitality companies",
        "Nigeria business expansion new outlets depots warehouses restaurant supermarket pharmacy retail",
    ],
}


def normalise_url(url):
    # remove fragments and common tracking parameters

    if not url:
        return None

    try:
        parts = urlsplit(url.strip())

        if parts.scheme not in ("http", "https"):
            return None

        if not parts.netloc:
            return None

        tracking_parameters = {
            "utm_source",
            "utm_medium",
            "utm_campaign",
            "utm_term",
            "utm_content",
            "fbclid",
            "gclid",
        }

        query_parts = []

        for item in parts.query.split("&"):
            if not item:
                continue

            key = item.split("=", 1)[0].lower()

            if key not in tracking_parameters:
                query_parts.append(item)

        return urlunsplit((
            parts.scheme.lower(),
            parts.netloc.lower(),
            parts.path.rstrip("/"),
            "&".join(query_parts),
            "",
        ))

    except Exception:
        return None


def make_source_id(index):
    return f"S{index:03d}"


print("\n========================================")
print("MONIEPOINT MARKET RESEARCH")
print("========================================")

print(f"Research areas: {len(RESEARCH_AREAS)}")
print(f"Maximum results per query: {MAX_RESULTS_PER_QUERY}")

search_sources = []
seen_urls = set()
search_failures = []

with DDGS() as ddgs:

    for area, queries in RESEARCH_AREAS.items():

        print(f"\n===== RESEARCH AREA: {area} =====")

        for query in queries:

            print(f"\nSearching: {query}")

            try:

                results = ddgs.text(
                    query,
                    max_results=MAX_RESULTS_PER_QUERY
                )

                result_count = 0

                for result in results:

                    raw_url = result.get("href")
                    url = normalise_url(raw_url)

                    if not url or url in seen_urls:
                        continue

                    seen_urls.add(url)

                    search_sources.append({
                        "title": result.get("title"),
                        "url": url,
                        "snippet": result.get("body") or "",
                        "query": query,
                        "research_area": area,
                    })

                    result_count += 1

                print(f"Unique results collected: {result_count}")

            except Exception as error:

                failure = {
                    "research_area": area,
                    "query": query,
                    "error": str(error),
                }

                search_failures.append(failure)

                print(f"Search failed: {error}")


print("\n========================================")
print("DISCOVERY RESULTS")
print("========================================")

print(f"Unique sources: {len(search_sources)}")
print(f"Search failures: {len(search_failures)}")

if not search_sources:
    raise RuntimeError(
        "No sources collected. "
        "Check DDGS availability and internet connectivity."
    )


evidence_trail = []

full_page_count = 0
snippet_count = 0
empty_source_count = 0

total_evidence_chars = 0

for index, source in enumerate(search_sources, 1):

    source_id = make_source_id(index)
    url = source["url"]

    print(f"\nExtracting [{source_id}]: {url}")

    extracted_text = None
    extraction_error = None

    try:

        downloaded = fetch_url(url)

        if downloaded:

            extracted_text = extract(
                downloaded,
                include_comments=False,
                include_tables=True,
            )

    except Exception as error:

        extraction_error = str(error)
        print(f"Extraction failed: {error}")

    if extracted_text and extracted_text.strip():

        evidence = extracted_text.strip()[:MAX_PAGE_CHARS]
        evidence_type = "FULL_PAGE_EXTRACTION"

        full_page_count += 1

    else:

        evidence = source["snippet"].strip()[:MAX_PAGE_CHARS]
        evidence_type = "SEARCH_SNIPPET_ONLY"

        if evidence:
            snippet_count += 1

    if not evidence:

        empty_source_count += 1

    # limit prompt evidence without deleting source metadata

    remaining_capacity = (
        MAX_TOTAL_EVIDENCE_CHARS - total_evidence_chars
    )

    if remaining_capacity <= 0:

        prompt_evidence = ""
        included_in_prompt = False

    else:

        prompt_evidence = evidence[:remaining_capacity]
        included_in_prompt = bool(prompt_evidence)

    total_evidence_chars += len(prompt_evidence)

    evidence_record = {
        "id": source_id,
        "title": source.get("title"),
        "url": url,
        "search_query": source["query"],
        "research_area": source["research_area"],
        "retrieved_at": RESEARCH_TIMESTAMP,
        "evidence_type": evidence_type,
        "extraction_error": extraction_error,
        "content": evidence,
        "included_in_gemini_prompt": included_in_prompt,
    }

    evidence_trail.append(evidence_record)


print("\n========================================")
print("EXTRACTION RESULTS")
print("========================================")

print(f"Full pages extracted: {full_page_count}")
print(f"Snippet fallbacks: {snippet_count}")
print(f"Empty sources: {empty_source_count}")
print(f"Characters sent to Gemini: {total_evidence_chars}")


coverage = {}

for area in RESEARCH_AREAS:

    area_sources = [
        source for source in evidence_trail
        if source["research_area"] == area
    ]

    usable_sources = [
        source for source in area_sources
        if source["content"].strip()
    ]

    full_pages = [
        source for source in usable_sources
        if source["evidence_type"] == "FULL_PAGE_EXTRACTION"
    ]

    coverage[area] = {
        "sources_found": len(area_sources),
        "usable_sources": len(usable_sources),
        "full_page_sources": len(full_pages),
        "snippet_only_sources": sum(
            source["evidence_type"] == "SEARCH_SNIPPET_ONLY"
            for source in usable_sources
        ),
    }


print("\n========================================")
print("RESEARCH COVERAGE BY AREA")
print("========================================")

for area, stats in coverage.items():

    print(
        f"{area}: "
        f"{stats['usable_sources']} usable sources, "
        f"{stats['full_page_sources']} full pages"
    )


if not any(item["usable_sources"] for item in coverage.values()):

    raise RuntimeError(
        "No usable evidence was extracted. "
        "Gemini will not be called."
    )


RESEARCH_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

source_register = {
    "research_timestamp": RESEARCH_TIMESTAMP,
    "model": MODEL_NAME,
    "research_areas": RESEARCH_AREAS,
    "coverage": coverage,
    "search_failures": search_failures,
    "sources": evidence_trail,
}

with open(SOURCE_REGISTER_PATH, "w", encoding="utf-8") as file:

    json.dump(
        source_register,
        file,
        indent=4,
        ensure_ascii=False,
    )

print(f"\nSource register saved: {SOURCE_REGISTER_PATH}")


scraped_evidence = ""

for source in evidence_trail:

    if not source["included_in_gemini_prompt"]:
        continue

    if not source["content"].strip():
        continue

    scraped_evidence += (
        f"\n\n--- SOURCE [{source['id']}] ---\n"
        f"Title: {source['title']}\n"
        f"URL: {source['url']}\n"
        f"Research area: {source['research_area']}\n"
        f"Search query: {source['search_query']}\n"
        f"Evidence type: {source['evidence_type']}\n"
        f"Content:\n{source['content']}"
    )


prompt = f"""
# COMPREHENSIVE MARKET AND IDEAL CUSTOMER PROFILE RESEARCH

## Company and Market

Company: Moniepoint
Market: Nigeria
Product category: Business banking, merchant payments,
collections, settlements and related financial services.

## Research Objective

Identify the Nigerian business segments with the strongest
evidence-backed commercial potential for Moniepoint.

The objective is to identify genuine commercial opportunities,
not merely to produce a narrow list of familiar industries.

A missed viable segment could mean lost revenue for Moniepoint.
A false-positive segment could waste sales resources.

Therefore, the analysis must minimise both:

1. False exclusions of commercially attractive businesses.
2. False inclusions of businesses with weak or unsupported fit.

Do not sacrifice commercial opportunity for superficial
simplicity or convenient classification.

## Critical Research Principle

The sectors supplied in the evidence collection plan are
research categories, not predetermined ICP decisions.

Do not assume that supermarkets and FMCG distributors
must be the best segments.

Do not assume that restaurants, hotels, pharmacies,
fuel stations, healthcare providers, schools, logistics
companies or other sectors are inferior.

Evaluate each segment on its actual business model,
transaction characteristics, financial workflows and
verified Moniepoint product fit.

A sector must not be rejected merely because public
information about it is less accessible.

## Research Evidence

The following evidence was retrieved from web searches
and webpage extraction.

{scraped_evidence}

## Source Coverage Information

The following table describes how much evidence was
collected for each research area:

{json.dumps(coverage, indent=2)}

Search failures:

{json.dumps(search_failures, indent=2)}

Coverage limitations must influence confidence.

A segment with weak evidence coverage must not be
declared commercially unattractive merely because
the research process did not retrieve enough information.

## Stage 1: Broad Market Discovery

Identify and evaluate relevant Nigerian business segments.

At a minimum, investigate:

- Restaurants and quick-service restaurant groups.
- Supermarkets and grocery retailers.
- FMCG distributors and wholesalers.
- Fuel stations and energy retail networks.
- Pharmacies and pharmaceutical distribution.
- Hotels and hospitality groups.
- Private hospitals, clinics and diagnostic networks.
- Private schools and education groups.
- Logistics, transport and haulage businesses.
- Building materials and construction supply distributors.
- Electronics and appliance retailers and distributors.
- Fashion and specialty retail chains.
- General multi-location physical retailers.
- Other commercially relevant sectors identified by the evidence.

Do not treat this list as exhaustive.

Identify additional segments where the evidence indicates
a meaningful business banking or merchant payments opportunity.

Separate broad industries from commercially meaningful
subsegments.

For example, distinguish a single independent restaurant
from a restaurant group operating multiple locations.

## Stage 2: Analyse Actual Payment and Financial Workflows

For each relevant segment, investigate:

1. How the business receives customer payments.
2. Whether transactions are predominantly in-person,
   online, B2B, B2C or mixed.
3. Whether it operates POS terminals, bank transfers,
   payment gateways, cash or other payment methods.
4. How funds are collected and settled.
5. Whether multiple locations create reconciliation
   or financial-control requirements.
6. How the business pays suppliers and employees.
7. Whether it manages collections from multiple customers,
   dealers, retailers or branches.
8. Whether payment workflows are centralised or decentralised.
9. Whether transaction frequency and value create a
   meaningful banking or payments use case.
10. What operational or financial complexity is actually
    supported by evidence.

Do not assume that every multi-branch business has
complex reconciliation problems.

Do not assume that every high-volume business has
poor banking infrastructure.

Do not present a common industry problem as a verified
problem experienced by a specific company.

## Stage 3: Moniepoint Product Fit

Establish Moniepoint's actual product capabilities
using reliable evidence, preferably official sources.

For each capability:

- Identify the product or service.
- Explain the relevant customer workflow.
- Identify the business segments that could benefit.
- Distinguish directly supported use cases from speculative ones.
- Identify product limitations and missing evidence.

Do not invent products, integrations, settlement speeds,
pricing, service guarantees or technical capabilities.

Do not assume that a general POS proposition automatically
solves complex treasury, ERP or enterprise reconciliation needs.

Evaluate product fit separately for:

- Merchant collections.
- POS and in-person payments.
- Business accounts and banking.
- Transfers and settlements.
- Supplier payments.
- Multi-location financial management.
- Business payment collection.
- Other verified capabilities found in the evidence.

If the evidence does not establish a product capability,
mark it as requiring verification.

## Stage 4: Comparative Segment Assessment

Build a comparative table for the identified segments.

Assess:

- Payment frequency.
- Typical transaction characteristics.
- Physical operating footprint.
- Number and distribution of locations.
- Collection complexity.
- Supplier-payment requirements.
- Reconciliation requirements.
- Financial management maturity.
- Potential Moniepoint product fit.
- Addressable business population.
- Evidence of Nigerian market activity.
- Competitive intensity.
- Likely economic buyer.
- Sales accessibility.
- Implementation complexity.
- Potential commercial value.
- Confidence in the assessment.

Use evidence wherever possible.

Do not invent transaction volumes, turnover, market size,
branch counts or conversion rates.

Where reliable numerical data is unavailable, use
transparent qualitative assessments and explain the basis.

Do not give every segment an artificially precise numerical
score. If a scoring framework is used, define its criteria,
weights and evidence limitations.

Distinguish the following:

- Commercial attractiveness.
- Product fit.
- Operational need.
- Addressability.
- Evidence confidence.

These are different dimensions and must not be collapsed
into one unsupported score.

## Stage 5: Firmographic and Operational Qualification

Investigate characteristics that help identify commercially
attractive companies within each segment.

Consider:

- Nigerian operating presence.
- Business identity and legal or trading structure.
- Active commercial operations.
- Physical locations, outlets, branches, depots or facilities.
- Employee count and organisational maturity.
- Revenue and turnover where credible evidence exists.
- Geographic coverage.
- Business model.
- Payment and collection relevance.
- Finance and treasury function maturity.

Do not invent universal minimum revenue, headcount,
transaction volume or branch-count thresholds.

Distinguish mandatory qualification conditions from
prioritisation heuristics.

A single-location business must not automatically be
excluded if its actual operating model and payment activity
indicate strong fit.

A large company must not automatically qualify merely
because it is large.

## Stage 6: Buying Committee

For each attractive segment, identify:

- Economic buyer.
- Business owner or founder.
- Managing director or chief executive.
- Chief financial officer.
- Finance director.
- Head of Finance.
- Treasury manager.
- Financial controller.
- Operations director.
- Relevant payments or technology stakeholders.
- Procurement or compliance blockers.

Explain how buying authority changes with business size,
ownership and organisational maturity.

Do not assume that the person with the most relevant job
title is necessarily the final decision-maker.

## Stage 7: Observable Buying Signals

Distinguish between:

A. ICP characteristics.
B. Operational indicators.
C. Genuine observable buying signals.
D. Evidence of explicit purchase intent.

Investigate signals such as:

- New branches, outlets, depots or geographic expansion.
- Finance, treasury or financial-control recruitment.
- New distribution relationships.
- Business acquisitions or consolidation.
- New payment infrastructure or technology deployments.
- Publicly announced banking or payment partnerships.
- Other verifiable developments relevant to financial operations.

Assess the relevance, recency, reliability and attribution
of each signal.

Do not claim that a business intends to switch providers
merely because it is expanding or recruiting.

## Stage 8: Anti-ICP and Exclusion Logic

Identify genuinely unsuitable businesses and explain why.

Distinguish:

- Definitively unsuitable businesses.
- Businesses outside the selected campaign scope.
- Businesses with insufficient public evidence.
- Businesses requiring further investigation.
- Businesses with strong potential but uncertain product fit.

Do not confuse an unverified business with a bad prospect.

Do not classify a business as disqualified solely because
its website is poor, its turnover is unavailable or its
branch count cannot be established.

## Stage 9: Market Opportunity and Missed-Revenue Audit

This section is mandatory.

Identify sectors or subsegments that could be commercially
valuable but might be missed by a narrow ICP.

Specifically investigate whether excluding restaurants,
hospitality, pharmacies, fuel stations, healthcare,
education or other sectors could create material
opportunity costs.

For each potentially missed segment, explain:

- Why it could be commercially attractive.
- Which Moniepoint capabilities could be relevant.
- What evidence supports the opportunity.
- What evidence is missing.
- What additional research would validate or reject it.
- Whether it merits a separate campaign or further testing.

Do not recommend adding a segment simply to make the ICP broad.

Recommend inclusion only where commercial logic and
evidence justify it.

## Stage 10: Final ICP Architecture

Produce three distinct outputs.

### A. Market-Level ICP Recommendation

Identify the strongest potential customer segments
for Moniepoint across the Nigerian market.

Classify them as:

- PRIMARY OPPORTUNITY.
- SECONDARY OPPORTUNITY.
- EMERGING OR UNDER-RESEARCHED OPPORTUNITY.
- LOW PRIORITY OR POOR FIT.

Explain the reasoning and confidence behind each classification.

Do not force a segment into a category if the evidence
is insufficient.

### B. Segment-Specific ICP Definitions

For each recommended segment, define:

- Business model.
- Ideal operating characteristics.
- Payment and financial workflows.
- Mandatory qualification criteria.
- Prioritisation criteria.
- Economic buyer.
- Relevant buying signals.
- Moniepoint product fit.
- Exclusion criteria.
- Evidence requirements.

### C. Campaign-Specific ICP Recommendation

Recommend which segments should be included in a
practical prospecting campaign.

Explain whether the existing focus on:

- RETAIL_SUPERMARKET
- FMCG_DISTRIBUTOR

is commercially justified, too narrow or should be expanded.

Do not silently change an existing campaign's approved
scope. Present any proposed expansion explicitly.

## Evidence and Reasoning Standards

1. Cite claims using the supplied source IDs, such as [S001].

2. Never invent source IDs, sources, statistics or company facts.

3. Every material factual claim must be supported by evidence
   where available.

4. Distinguish:
   - Verified facts.
   - Reasonable inferences.
   - Estimates.
   - Unvalidated hypotheses.
   - Unknown information.

5. A search snippet is weaker evidence than an extracted
   source page.

6. A source's existence does not establish that it supports
   the associated claim. Check its actual content.

7. Prefer official company sources, regulatory publications,
   credible industry research and reputable Nigerian
   business publications.

8. Identify conflicting evidence rather than silently
   selecting whichever source supports the conclusion.

9. Do not treat the absence of public evidence as evidence
   that a business lacks a particular capability or need.

10. Do not infer financial distress, dissatisfaction with
    a bank, payment failure or switching intent without
    direct evidence.

11. Do not invent numerical qualification thresholds.

12. Never use an em dash.

13. Use precise, commercially useful language.

14. Avoid generic statements that could apply to any business.

15. Do not force a conclusion where the evidence is inadequate.

## Final Evidence Assessment

Conclude with:

1. Strongest evidence-backed market opportunities.
2. Segments that warrant additional investigation.
3. Segments that appear less attractive and why.
4. Potential revenue opportunities that a narrow ICP could miss.
5. Important assumptions that remain unverified.
6. Research gaps and the specific evidence needed to resolve them.
7. Recommended campaign segments.
8. Confidence levels and limitations.
9. Claims that must not yet be used in prospect qualification.

The final recommendation must reflect the available evidence,
not the initial assumptions or convenience of the research process.
"""


print("\n========================================")
print("REQUESTING GEMINI MARKET ANALYSIS")
print("========================================")

response = client.models.generate_content(
    model=MODEL_NAME,
    contents=prompt,
)

content = response.text

if not content or not content.strip():

    raise ValueError(
        "Gemini returned an empty response. "
        "The existing ICP file will not be overwritten."
    )


evidence_markdown = """

## Research Sources and Evidence Trail

"""

for source in evidence_trail:

    evidence_markdown += (
        f"\n- [{source['id']}] "
        f"[{source['title'] or 'Untitled source'}]"
        f"({source['url']})"
        f" | Area: {source['research_area']}"
        f" | Evidence: {source['evidence_type']}"
    )


coverage_markdown = """

## Research Coverage Audit

"""

for area, stats in coverage.items():

    coverage_markdown += (
        f"\n- **{area}:** "
        f"{stats['usable_sources']} usable sources; "
        f"{stats['full_page_sources']} full-page extractions; "
        f"{stats['snippet_only_sources']} snippet-only sources."
    )


final_output = (
    content
    + evidence_markdown
    + coverage_markdown
)


OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

temporary_output = OUTPUT_PATH.with_suffix(".md.tmp")

with open(temporary_output, "w", encoding="utf-8") as file:
    file.write(final_output)

# replace the existing report only after the new report is written successfully

os.replace(temporary_output, OUTPUT_PATH)

print(f"\nICP report saved: {OUTPUT_PATH}")


now = datetime.now()
iso_calendar = now.isocalendar()

work_log_path = (
    ROOT
    / "work-log"
    / f"{iso_calendar.year}-W{iso_calendar.week:02d}.md"
)

work_log_path.parent.mkdir(parents=True, exist_ok=True)

timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

log_entry = (
    f"\n- [{timestamp}] "
    f"Completed broad Moniepoint market and ICP research "
    f"using DDGS, Trafilatura and Gemini {MODEL_NAME}. "
    f"Investigated {len(RESEARCH_AREAS)} market research areas. "
    f"Collected {len(search_sources)} unique sources. "
    f"Extracted {full_page_count} full pages and used "
    f"{snippet_count} search snippets. "
    f"Search failures: {len(search_failures)}. "
    f"Saved report to `{OUTPUT_PATH.relative_to(ROOT)}` "
    f"and source register to "
    f"`{SOURCE_REGISTER_PATH.relative_to(ROOT)}`."
)

with open(work_log_path, "a", encoding="utf-8") as file:
    file.write(log_entry)


print("\n========================================")
print("MONIEPOINT MARKET RESEARCH COMPLETED")
print("========================================")

print(f"Research areas: {len(RESEARCH_AREAS)}")
print(f"Search results: {len(search_sources)}")
print(f"Full pages extracted: {full_page_count}")
print(f"Snippet fallbacks: {snippet_count}")
print(f"Empty sources: {empty_source_count}")
print(f"Search failures: {len(search_failures)}")
print(f"Evidence characters: {total_evidence_chars}")

print(f"\nICP report: {OUTPUT_PATH}")
print(f"Source register: {SOURCE_REGISTER_PATH}")
print(f"Work log: {work_log_path}")

print("========================================")