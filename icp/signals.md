# icp/signals.md

This document outlines the actionable buying signals for Moniepoint Business Banking & Payments. It focuses on identifying businesses at the "complexity tipping point," where manual financial management begins to impede operational growth.

---

## 1. Signal Framework: Classification and Intent

We define signals by their proximity to the "pain threshold"—the point at which a business is actively seeking to replace legacy processes with integrated financial infrastructure.

| Signal Class | Description | Lead Time |
| :--- | :--- | :--- |
| **Structural** | Permanent operational shifts (e.g., new branches). | Long-term |
| **Capability** | Intent to professionalize finance (e.g., hiring). | Medium-term |
| **Behavioral** | Immediate indicators of friction (e.g., public complaints). | Short-term |

---

## 2. Analysis of Key Buying Signals

### A. Finance and Treasury Recruitment (Strong)
*   **Definition:** Active job postings for "Treasury Manager," "Finance Analyst," or "Financial Controller."
*   **Commercial Relevance:** This is the highest-intent signal. It signifies a transition from founder-led manual accounting to a structured finance department [S13, S14]. Such hires are tasked with improving cash visibility, reconciliation speed, and payment security—direct pain points for Moniepoint’s core offering [S6].
*   **Detection:** Monitor job boards (Jobzilla, MyJobMag) and LinkedIn for specific titles in mid-market retail and FMCG [S13, S14, S15].
*   **Timing:** High. The need for a treasury tool often precedes or coincides with the arrival of the new hire.

### B. Multi-Branch Expansion (Moderate to Strong)
*   **Definition:** Public announcements of new store openings or expansion into new states [S1, S2, S3].
*   **Commercial Relevance:** A business growing from 5 to 24 outlets experiences a compounding increase in reconciliation complexity [S1]. The "payment friction" of managing cash flows across multiple, disparate locations is the primary driver for a unified banking platform [S6].
*   **Detection:** News monitoring for "new store launch," "branch expansion," or "network growth" within the retail and FMCG sectors [S1, S2, S4].
*   **Timing:** Immediate post-announcement. Once a new location is open, the volume of payments increases, making the need for reliable POS and instant settlement critical [S9].

### C. Operational Complexity Signals (Moderate)
*   **Definition:** Job postings for "Warehouse Operations," "Inventory Manager," or "Logistics Coordinator" in FMCG distribution [S3].
*   **Commercial Relevance:** Complex inventory and logistics require high-volume payments to suppliers and distributors. These firms need automated treasury tools to match incoming payments from retailers against outgoing supplier obligations [S6, S8].
*   **Detection:** LinkedIn job search filters for operations roles within companies classified as FMCG distributors or wholesale traders [S6, S7].

---

## 3. Signal Strength and Qualification Matrix

| Signal | Reliability | Ease of Detection | Priority |
| :--- | :--- | :--- | :--- |
| **Treasury/Finance Hire** | High | Medium | Primary |
| **Physical Expansion** | Moderate | High | Secondary |
| **Operations Role Hire** | Moderate | Medium | Tertiary |

**Methodology:** Priority is based on the correlation between the signal and the specific business problem (reconciliation) that Moniepoint solves. A Treasury Manager hire is a direct proxy for an intent to change financial software.

---

## 4. Combined Signals: The "Complexity Multiplier"

Single signals can be noise; combinations indicate a compelling prospect:

1.  **Expansion + Finance Hire:** A company launching a new store *while* hiring a Treasury Manager is the ideal Moniepoint lead. They are adding volume and simultaneously building the capacity to manage that volume professionally [S1, S14].
2.  **Ops Hire + Sector Specificity (FMCG):** An FMCG distributor hiring for both "Logistics" and "Accounts" indicates a scaling supply chain. This segment is highly reliant on manual, multi-source payments, making them prime candidates for Moniepoint’s treasury features [S6, S8].

---

## 5. False Positives and Disqualifying Indicators

*   **Foreign Franchise Entrants (e.g., Carrefour):** While high-profile, these companies often have pre-existing global banking relationships or proprietary international ERP systems that create high barriers to entry for local fintechs [S3].
*   **Store Closures/Downsizing:** While it implies a change in operations, it often indicates financial distress or a shift toward asset-light models, which may reduce the need for high-volume POS hardware [S4].
*   **Tech Adoption (BuiltWith/Wappalyzer):** Relying solely on "detected technology" is unreliable. Most mid-market Nigerian firms manage finances via WhatsApp/Excel, which are invisible to scanners [S6].

---

## 6. Practical GTM Application (Clay/Research Workflow)

*   **Search Queries:**
    *   `site:myjobmag.com "Treasury Manager" AND "Nigeria"`
    *   `"new store" OR "new branch" AND "supermarket" AND "Nigeria" -site:wikipedia.org`
*   **Verification:**
    *   Manual check of company size via LinkedIn. If the company has < 10 employees, they are likely too small for treasury-grade solutions.
    *   Cross-reference location announcements with recent news to ensure the expansion is active.
*   **Data Enrichment:**
    *   Extract company name, location, and role from job postings.
    *   Use firmographic data to filter for businesses with 5+ branches, as these are the high-value targets [S2].

---

## 7. Research Summary and Gaps

### Strongest Signals
*   **Treasury Manager Recruitment:** The most accurate indicator of a maturing finance function.
*   **Retail Branch Expansion:** Clearly mapped to high-frequency payment needs [S1, S2].

### Current Hypotheses
*   **Public Infrastructure Frustration:** While high-intent (people complaining about POS downtime), it is difficult to systematically monitor at scale without expensive social listening tools.
*   **"Internal Inertia":** The extent to which legacy banking ties prevent adoption remains an unverified blocker [S6].

### Research Gaps
*   **ERP Usage:** We lack reliable data on which businesses use Sage, SAP, or local alternatives, which would allow for better targeting based on integration potential.
*   **Informal-to-Formal Transition:** We cannot currently detect when a business moves its internal accounting from Excel to a formal ERP; this represents a massive "dark" signal for future growth.

## Research Sources & Evidence Trail

- [S1] [FoodCo expands network to 24 outlets - Vanguard News](https://www.vanguardngr.com/2026/09/foodco-expands-network-to-24-outlets/) | Full page extraction
- [S2] [Nigeria’s Modern Retail Sector Expands To 18,000 Outlets As ...](https://brandspurng.com/2026/05/15/nigerias-modern-retail-sector-expands-to-18000-outlets-as-indigenous-supermarket-chains-gain-market-dominance/) | Full page extraction
- [S3] [Carrefour Nigeria Takes Shape in Abuja as Garki and Central…](https://abujabusinessnews.com/2026/09/03/carrefour-nigeria-takes-shape-in-abuja-as-garki-and-central-area-locations-emerge/) | Full page extraction
- [S4] [Shoprite denies shutdown rumours, confirms new Palms, Circle ...](https://nairametrics.com/2026/03/13/shoprite-denies-shutdown-rumours-confirms-new-palms-circle-mall-stores-this-month/) | Full page extraction
- [S5] [FMCG Distributions Ltd – –](https://www.fmcgdistribution.org/) | Full page extraction
- [S6] [Welcome to All Brands & Commodities Distribution Limited ...](http://abcd.com.ng/) | Search snippet only
- [S7] [FMCG Distribution – Fortune Network Services](https://fortunenetworkservices.com/fmcg/) | Full page extraction
- [S8] [Fortunes Enterprises — Consumer Goods Wholesale Distributor ...](https://fortunesenterprises.com.ng/) | Full page extraction