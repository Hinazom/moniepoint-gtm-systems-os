
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

# Load the ICP document so the signals research builds on the existing findings.
icp_path = "icp/icp.md"

if not os.path.exists(icp_path):
    raise FileNotFoundError(
        f"Could not find {icp_path}. Generate the ICP document first."
    )

with open(icp_path, "r", encoding="utf-8") as f:
    icp_context = f.read()

if not icp_context.strip():
    raise ValueError("The ICP document is empty.")

# Search for evidence across the main buying signal categories.
queries = [
    "Moniepoint official business banking products POS payments collections Nigeria",
    "Nigeria supermarket retail chains new branches expansion announcements 2025 2026",
    "Nigeria FMCG distributors wholesale distribution expansion warehouses recruitment",
    "Nigeria treasury manager finance manager accountant jobs retail distribution companies",
    "Nigeria business POS payment settlement complaints failed transactions reconciliation businesses",
    "Nigeria business payment technology adoption POS payment infrastructure retail distribution",
]

print("\nStarting buying signals research...")

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
unusable_count = 0

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
        evidence = extracted_text[:4000]
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
print(f"Sources without usable content: {unusable_count}")

if not scraped_evidence.strip():
    raise RuntimeError(
        "No usable evidence was collected. "
        "Gemini will not be called with an empty evidence set."
    )


# Save the collected sources so they can be reviewed later.
research_directory = "research/signals"

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


# Give Gemini the existing ICP, retrieved evidence and buying signals requirements.
prompt = f"""
# MONIEPOINT BUYING SIGNALS RESEARCH

## Existing ICP Context

The following document contains the current preliminary
Ideal Customer Profile research for Moniepoint Business
Banking & Payments.

Use it as working context for this investigation.

Do not automatically accept its conclusions as verified
facts. Its segment priorities and assumptions may require
further validation.

{icp_context}


## Research Evidence

The following evidence was retrieved programmatically
from web search results and webpage extraction.

{scraped_evidence}


## Research Objective

Develop a comprehensive, research-backed document at
icp/signals.md identifying and analysing the buying signals
that indicate a Nigerian business may have a genuine need
or propensity to adopt Moniepoint Business Banking
& Payments.

Identify observable events, business developments,
operational changes, technology adoption patterns and
behavioural indicators that can help identify businesses
with an increased likelihood of purchasing Moniepoint's
products and services.

The objective is not simply to list characteristics of
companies that fit the ICP.

Determine what happens within or around a business that
creates a potential purchasing opportunity, why that
event matters, what underlying need it may indicate and
how it can be detected before or during the buying process.


## Initial Hypotheses

Investigate the following as potential buying signals:

1. High-volume POS and transaction growth:
Increasing checkout activity, additional POS terminals,
growing payment volumes or other indicators of expanding
payment operations.

2. Geographic and multi-branch expansion:
New retail outlets, branches, warehouses, distribution
facilities or geographical expansion.

3. Finance and treasury hiring:
Recruitment for finance managers, treasury personnel,
internal auditors, accountants and other roles associated
with increasing financial or operational complexity.

4. Public infrastructure frustration:
Public complaints, discussions or other evidence of
dissatisfaction with banking services, POS reliability,
payment failures, reconciliation or settlement delays.

These are starting hypotheses, not an exhaustive list
or predetermined conclusions.

Investigate additional signals that may be more predictive,
commercially relevant or easier to identify.


## Research and Analysis

For every identified buying signal, investigate:

### 1. Signal Definition

- What exactly constitutes the signal?
- What business event or change does it represent?
- Why might it indicate a need for Moniepoint?
- Which customer segments are most likely to exhibit it?
- What underlying commercial or operational problem
  might it reveal?

### 2. Commercial Relevance

- What purchasing need could the signal indicate?
- Which verified Moniepoint products or capabilities
  might be relevant?
- What circumstances would make the opportunity
  more compelling?
- What alternative explanations could account for the signal?
- How likely is the signal to indicate actual purchasing intent?

### 3. Detectability and Data Sources

Determine how the signal could realistically be identified.

Investigate potential sources such as:

- Company websites and announcements.
- Job postings and recruitment platforms.
- News publications and business directories.
- LinkedIn company updates and employee activity.
- Social media discussions and customer complaints.
- Technology detection platforms such as BuiltWith
  and Wappalyzer.
- Business databases and company intelligence platforms.
- Public regulatory filings and business records,
  where relevant.

Distinguish between directly observable signals,
indirect indicators and information that would require
manual research or direct engagement.

Do not assume that a signal is publicly detectable
simply because it exists within a business.

### 4. Timing and Signal Persistence

Investigate:

- When the signal is most commercially relevant.
- How long after the event the opportunity may remain actionable.
- Whether the signal is temporary, recurring or persistent.
- Whether multiple signals occurring together indicate
  greater purchasing propensity.
- Whether the signal suggests immediate buying intent
  or merely future potential.

### 5. Signal Strength and Qualification

Develop a defensible framework for distinguishing
strong, moderate and weak signals.

Assess signals based on:

- Relevance to Moniepoint's verified product capabilities.
- Evidence of an actual business need.
- Commercial significance.
- Reliability of available evidence.
- Ease of detection.
- Recency.
- Likelihood of indicating a purchasing opportunity.

Explain the reasoning behind each assessment.

Do not assign arbitrary numerical scores without
a defensible methodology.

### 6. Combined Signals and Buying Intent

Investigate how individual signals interact.

Identify combinations that may indicate a stronger
opportunity than any individual signal alone.

For example, investigate whether branch expansion
combined with finance hiring, increased payment complexity
or technology migration provides stronger evidence
of potential demand.

Do not assume that combining more signals automatically
produces a better prospect.

Explain which combinations are meaningful and why.

### 7. False Positives and Disqualifying Indicators

Identify events that might appear commercially significant
but do not necessarily indicate a need for Moniepoint.

Explain how to distinguish genuine buying opportunities
from ordinary business activity, weak proxies,
outdated information and misleading signals.


## Practical GTM Application

The findings should be usable in subsequent
GTM engineering workflows.

For each signal, establish:

- What to search for.
- Where to find the information.
- What evidence to capture.
- How to determine whether the signal is current.
- How to associate the signal with the correct company.
- What information may be extracted or enriched automatically.
- What requires human verification.
- How the signal could be used to prioritise an account.
- What additional information would be needed before
  initiating outreach.

Where appropriate, suggest practical search queries,
keywords, job-title patterns, technology indicators
and other observable data points.

Do not invent Clay integrations, data providers,
platform capabilities or detection methods.


## Research Standards

1. Conduct research rather than simply elaborating
   on the initial four hypotheses.

2. Prioritise signals that have a credible connection
   to a purchasing need.

3. Use reliable sources and cite material factual claims
   using the supplied source IDs, for example [S1] or [S3].

4. Never invent source IDs or citations.

5. Distinguish verified observations, evidence-supported
   inferences and hypotheses.

6. Search snippets are weaker evidence than extracted
   webpage content. Identify claims that rely only on snippets.

7. Do not treat a source as proof of a claim unless its
   actual content supports that claim.

8. Do not fabricate buying behaviour, market statistics
   or purchasing triggers.

9. Challenge weak or misleading signals.

10. Consider differences between customer segments
    identified in the existing ICP document.

11. Prioritise practical detectability and commercial
    relevance over theoretical possibilities.

12. Do not confuse company growth with buying intent.

13. Explain limitations and research gaps where evidence
    is unavailable.

14. Do not claim that Moniepoint offers a capability
    unless the supplied evidence supports it.

15. Never use em dashes anywhere in the document.


## Deliverable

Produce a comprehensive Markdown document at
icp/signals.md.

Organise the findings logically. Use comparison tables
where useful.

The document should provide a practical foundation for
account research, signal monitoring, prospect qualification,
prioritisation and subsequent Clay-based GTM workflows.

Conclude with:

- The strongest evidence-supported buying signals.
- Signals that remain hypotheses.
- The most useful combinations of signals.
- Important false positives.
- Research gaps requiring further investigation.

Use clean Markdown headings and practical examples.
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


# Save the generated buying signals document.
output_path = "icp/signals.md"

os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    f.write(final_output)

print(f"\nBuying signals successfully saved to {output_path}")


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
    f"Generated Moniepoint buying signals research using "
    f"DDGS, Trafilatura and Gemini 3.1 Flash Lite. "
    f"Collected {len(search_sources)} search results, "
    f"extracted {full_page_count} full pages, used "
    f"{snippet_count} search snippets and recorded "
    f"{unusable_count} sources without usable content. "
    f"Used the existing ICP document as research context. "
    f"Saved signals to `{output_path}` and the source "
    f"register to `{source_register_path}`."
)

with open(work_log_path, "a", encoding="utf-8") as log_file:
    log_file.write(log_entry)

print(f"Work log updated at {work_log_path}")


print("\n========================================")
print("MONIEPOINT BUYING SIGNALS RESEARCH COMPLETED")
print("========================================")
print(f"Search results: {len(search_sources)}")
print(f"Full pages extracted: {full_page_count}")
print(f"Snippet fallbacks: {snippet_count}")
print(f"Sources without usable content: {unusable_count}")
print(f"Signals document: {output_path}")
print(f"Source register: {source_register_path}")
print(f"Work log: {work_log_path}")
print("========================================")
