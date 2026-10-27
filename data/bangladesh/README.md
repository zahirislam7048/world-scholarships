# Bangladesh scholarships

`scholarships.csv` lists scholarships that are open, upcoming, or standing policies. Expired items are removed. A scheduled task updates it once a week.

Preview page: https://claude.ai/artifact/GHhrqtV9tbHzor4g3BAsZ5 (rebuilt with `python3 data/bangladesh/build_preview.py <out.html> [YYYY-MM-DD]`).

## How it is collected

The collecting session cannot open `.gov.bd` or university sites directly (network policy). So each record comes from a web search **restricted to that body's official domain** (e.g. `bracu.ac.bd`, `ugc.gov.bd`). Every `source_url` is on the official site, but the details come from search-result summaries. The pages were not read in full.

`verification_status = search-snippet` means: open `source_url` and confirm the amount, eligibility and deadline before using the record. After checking a record, change its status to `verified`.

## Keep / remove rule

- **Keep:** standing policies (`session_year` = ongoing), calls that are open, and calls announced for a future session.
- **Remove:** a record whose deadline has passed, or whose only evidence is a past session with no current call.

## Columns

| column | meaning |
|---|---|
| provider_type | `government`, `public`, `private`, `international` |
| coverage_amount | waiver % or stipend amount as stated by the source |
| session_year | academic/fiscal year or semester the source refers to |
| deadline | application deadline (YYYY-MM-DD) when the source gives one |
| collected_on | date the record was added or last changed |
| notes | conflicts between sources, outdated pages, etc. |
