# Base — Data Quality
[ID: base-data-quality]

Rules for projects where content or data accuracy matters as much as
code quality. Applies to lens databases, product catalogs, tutorial
content, wiki entries, and any project that declares data as a
first-class concern.

---

## Data sourcing
[ID: data-quality-sourcing]

- Every data point MUST trace to a named source (URL, publication,
  manufacturer spec sheet)
- Record the source alongside the data — not in a separate document
- Prefer primary sources (manufacturer, official docs) over aggregators
- When multiple sources conflict, document the conflict and the chosen
  value with rationale
- Never fabricate or estimate values without marking them as estimates

---

## Completeness tracking
[ID: data-quality-completeness]

- Define a completeness score for each entry: fields populated / total
  fields (e.g. `14/14`)
- Track completeness at the entry level, not just the collection level
- Incomplete entries MUST be queryable — add a `completeness` or
  `dataStatus` field
- Set a minimum completeness threshold for publishing (e.g. 80%)
- Entries below the threshold MAY exist in the database but MUST NOT
  appear in user-facing views

---

## Freshness
[ID: data-quality-freshness]

- Record when each entry was last verified: `lastVerified` date field
- Define a freshness window per collection (e.g. prices: 30 days,
  specs: 12 months)
- Entries beyond their freshness window SHOULD be flagged for review
- Price data MUST include a `priceDate` field — never show a price
  without indicating when it was captured
- Discontinued or unavailable items MUST be marked, not deleted

---

## Exact vs estimated values
[ID: data-quality-precision]

- Distinguish exact values (from specs or measurements) from estimates
  (derived, rounded, or interpolated)
- Use a naming convention or field suffix to mark estimates (e.g.
  `weightEstimated: true` or `~` prefix in display)
- Default to realistic/pessimistic estimates — never optimistic
- Document the estimation method when not obvious

---

## Scoring and derived fields
[ID: data-quality-scoring]

- Scoring formulas MUST be documented — not buried in code
- All inputs to a score MUST be traceable to source data
- Scores MUST be reproducible: same inputs always produce the same
  output
- Define the scoring scale once (e.g. 1–5, step 0.5) and use it
  consistently
- Features (boolean attributes like "weather sealed") are UI filter
  badges, not scoring inputs — keep them separate

---

## Data changelog
[ID: data-quality-changelog]

- Changes to source data MUST be committed with a message explaining
  what changed and why (e.g. "fix: update lens weight — manufacturer
  corrected spec sheet")
- When a scoring input changes, note that derived scores will change
- Do not batch unrelated data changes into a single commit — one
  entry or one field correction per commit
- For bulk imports or migrations, document the source and method in
  the commit message

---

## Identity and deduplication
[ID: data-quality-identity]

- Every entry MUST have a stable unique identifier that does not
  change when other fields are updated
- Define what makes two entries "the same" — document the identity
  key (e.g. manufacturer + model name + variant)
- Near-duplicates (regional names, revised versions, bundles) MUST
  be distinct entries with a relationship field linking them
- Never merge near-duplicates silently — flag for manual review
- Discontinued items that are replaced by a successor SHOULD link
  to the successor via a `replacedBy` field

---

## Validation
[ID: data-quality-validation]

- Validate data at ingest time — reject or flag entries that fail
  schema validation
- Use typed schemas (Zod, JSON Schema, TypeScript interfaces) for all
  data collections
- Range checks for numeric fields (e.g. weight > 0, price > 0)
- Enum checks for constrained fields (e.g. mount type, category)
- Build-time validation is acceptable for static sites — runtime
  validation for APIs
