
import os
import json
from datetime import datetime

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


# Search for relevant information across different research areas.
queries = [
    "Moniepoint business banking official products POS business Nigeria",
    "Nigeria retail chains supermarket groups business expansion",
    "Nigeria FMCG distributors wholesale payment collection operations",
    "Nigeria business banking POS settlement competitors fintech",
    "Nigeria finance treasury manager recruitment retail distribution",
]

print("\nStarting web research...")

search_sources = []
seen_urls = set()

with DDGS() as ddgs:
    for query in queries:
        print(f"\nSearching: {query}")

        try:
            results = ddgs.text(query, max_results=4)

            for result in results:
                url = result.get("href")

                if not url or url in seen_urls:
                    continue

                seen_urls.add(url)

                search_sources.append({
                    "title": result.get("title"),
                    "url": url,
                    "snippet": result.get("body"),
                    "query": query
                })

        except Exception as e:
            print(f"Search failed for '{query}': {e}")


print(f"\nCollected {len(search_sources)} unique search results.")

if not search_sources:
    raise RuntimeError(
        "No search results were collected. "
        "Check your internet connection or DDGS availability."
    )


# Extract webpage content and retain search snippets when extraction fails.
scraped_evidence = ""
evidence_trail = []

full_page_count = 0
snippet_count = 0

for idx, source in enumerate(search_sources, 1):
    source_id = f"S{idx}"
    url = source["url"]

    print(f"\nExtracting [{source_id}]: {url}")

    extracted_text = None

    try:
        downloaded = fetch_url(url)

        if downloaded:
            extracted_text = extract(
                downloaded,
                include_comments=False,
                include_tables=False
            )

    except Exception as e:
        print(f"Extraction failed for {url}: {e}")

    if extracted_text and extracted_text.strip():
        evidence = extracted_text[:5000]
        evidence_type = "Full page extraction"
        full_page_count += 1

    else:
        evidence = source.get("snippet") or ""
        evidence_type = "Search snippet only"

        if evidence.strip():
            snippet_count += 1

    # Keep the source details alongside the extracted evidence.
    evidence_record = {
        "id": source_id,
        "title": source.get("title"),
        "url": url,
        "search_query": source.get("query"),
        "evidence_type": evidence_type,
        "content": evidence
    }

    evidence_trail.append(evidence_record)

    if evidence.strip():
        scraped_evidence += (
            f"\n\n--- SOURCE [{source_id}] ---\n"
            f"Title: {source.get('title')}\n"
            f"URL: {url}\n"
            f"Search query: {source.get('query')}\n"
            f"Evidence type: {evidence_type}\n"
            f"Content:\n{evidence}"
        )


print("\nEvidence collection completed.")
print(f"Full pages extracted: {full_page_count}")
print(f"Search snippets used: {snippet_count}")

if not scraped_evidence.strip():
    raise RuntimeError(
        "No usable evidence was collected. "
        "Gemini will not be called with an empty evidence set."
    )


# Save the collected sources so they can be reviewed later.
research_directory = "research/icp"

os.makedirs(research_directory, exist_ok=True)

source_register_path = os.path.join(
    research_directory,
    "source_register.json"
)

with open(source_register_path, "w", encoding="utf-8") as f:
    json.dump(
        evidence_trail,
        f,
        indent=4,
        ensure_ascii=False
    )

print(f"\nSource register saved to {source_register_path}")


# Give Gemini the retrieved evidence and the ICP research requirements.
prompt = f"""
# IDEAL CUSTOMER PROFILE RESEARCH
## Moniepoint Business Banking & Payments

## Research Evidence

The following evidence was retrieved programmatically
from web search results and webpage extraction.

{scraped_evidence}


## Research Objective

Develop a comprehensive, research-backed Ideal Customer
Profile (ICP) for Moniepoint Business Banking & Payments.

Identify, investigate, evaluate and prioritise the Nigerian
business segments with the strongest potential commercial
fit.

Do not simply validate predetermined customer categories.
Challenge the initial hypotheses and allow the evidence
to influence your conclusions.


## Initial Market Hypotheses

Treat these as starting points for investigation, not fixed
targeting requirements:

- High-growth Nigerian retail businesses and multi-location
  operators.
- Supermarket groups, retail chains and fuel station networks.
- Commercial distributors, wholesalers and businesses with
  complex payment and collection operations.
- Businesses operating across multiple branches, locations
  or sales channels.
- Companies with substantial transaction volumes,
  operational complexity or growing financial management
  requirements.
- Lagos, Abuja and Port Harcourt as initial geographic areas
  of interest. Investigate other Nigerian commercial clusters.
- Consider different revenue levels, employee counts and
  stages of growth. Do not assume that size alone indicates
  strong product fit.


## Research and Analysis

Investigate and compare the market across these dimensions:

### 1. Market and Segment Analysis

Identify relevant Nigerian business segments and subsegments.

Examine business models, revenue mechanisms, operating
structures, transaction volumes, locations, payment
dependencies and commercial attractiveness.

Compare and prioritise the segments.


### 2. Firmographic and Operational Characteristics

Investigate company size, annual turnover, employee count,
physical footprint, maturity, ownership structure,
geographical presence and operational complexity.


### 3. Technographic and Financial Infrastructure

Investigate banking platforms, POS terminals, acquiring
infrastructure, ERP platforms, e-commerce checkouts and
reconciliation tools.

Identify which technologies can actually be detected
through tools such as BuiltWith or Wappalyzer.

Explain detection limitations.


### 4. Buying Committee and Decision-Making Dynamics

Identify economic buyers, decision-makers, technical
evaluators, operational stakeholders and potential blockers.

Distinguish between founder-led and professionally
managed businesses.


### 5. Existing Solutions, Customer Problems and Unmet Needs

Investigate actual workflows, alternatives, workarounds,
reconciliation problems, delayed access to funds and
operational bottlenecks.


### 6. Moniepoint Product Fit and Competitive Positioning

Evaluate verified Moniepoint capabilities against the
problems identified.

Compare relevant alternatives, including traditional banks
and competing fintech providers.

Do not assume that a product capability exists unless
the supplied evidence supports it.


### 7. Buying Signals and Prospect Identification

Identify observable events and behavioural indicators
that could signal readiness to adopt or switch.

Distinguish between general ICP characteristics and
genuine buying signals.


### 8. Customer Qualification, Prioritisation and Anti-ICP

Develop excellent-fit, reasonable-fit and poor-fit criteria.

Explain exclusion criteria and their commercial rationale.


### 9. Strategic Recommendations

Identify primary ICPs, secondary ICPs, geographic
concentrations, qualification criteria and strategic priorities.


## Research Standards and Guardrails

1. Cite retrieved evidence using its source ID, for example
   [S1] or [S3].

2. Every material factual claim should have a supporting
   source ID where available.

3. Never invent source IDs, citations, market statistics,
   company characteristics or technology detection markers.

4. Distinguish clearly between:
   - Verified facts
   - Reasonable inferences
   - Estimates
   - Unvalidated hypotheses

5. Search snippets are weaker evidence than extracted
   webpage content. Identify claims that rely only on snippets.

6. Do not treat a source as proof of a claim unless its
   actual content supports that claim.

7. Where evidence is missing, explain the uncertainty.
   Do not fill research gaps with invented information.

8. Challenge initial assumptions wherever the evidence
   warrants it.

9. Make the analysis commercially specific to Nigerian
   businesses and their operating environments.

10. Emphasise analytical depth, useful distinctions and
    actionable insights.

11. Never use em dashes anywhere in the document.

12. Use clean Markdown headings and comparative tables
    where appropriate.


## Final Evidence Assessment

Conclude with:

- The strongest evidence-backed ICP conclusions.
- Important assumptions that remain unverified.
- Research gaps that require additional investigation.
- Claims that should not yet be used in prospect targeting.

"""


print("\nRequesting ICP analysis from Gemini...")

response = client.models.generate_content(
    model=model_name,
    contents=prompt
)

content = response.text

if not content or not content.strip():
    raise ValueError(
        "Gemini returned an empty response. "
        "The existing ICP file will not be overwritten."
    )


# Add the source links to the end of the generated document.
evidence_markdown = (
    "\n\n## Research Sources & Evidence Trail\n"
)

for source in evidence_trail:
    evidence_markdown += (
        f"\n- [{source['id']}] "
        f"[{source['title'] or 'Untitled source'}]"
        f"({source['url']})"
        f" | {source['evidence_type']}"
    )

final_output = content + evidence_markdown


# Save the generated ICP document.
output_path = "icp/icp.md"

os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    f.write(final_output)

print(f"\nICP successfully saved to {output_path}")


# Record the research activity in the current week's work log.
now = datetime.now()
iso_calendar = now.isocalendar()

work_log_path = (
    f"work-log/{iso_calendar.year}-W{iso_calendar.week:02d}.md"
)

os.makedirs(os.path.dirname(work_log_path), exist_ok=True)

timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

log_entry = (
    f"\n- [{timestamp}] "
    f"Generated Moniepoint Business Banking ICP using "
    f"DDGS, Trafilatura and Gemini 3.1 Flash Lite. "
    f"Collected {len(search_sources)} search results, "
    f"extracted {full_page_count} full pages and used "
    f"{snippet_count} search snippets. "
    f"Saved ICP to `{output_path}` and source register to "
    f"`{source_register_path}`."
)

with open(work_log_path, "a", encoding="utf-8") as log_file:
    log_file.write(log_entry)

print(f"Work log updated at {work_log_path}")


print("\n========================================")
print("MONIEPOINT ICP RESEARCH COMPLETED")
print("========================================")
print(f"Search results: {len(search_sources)}")
print(f"Full pages extracted: {full_page_count}")
print(f"Snippet fallbacks: {snippet_count}")
print(f"ICP document: {output_path}")
print(f"Source register: {source_register_path}")
print(f"Work log: {work_log_path}")
print("========================================")