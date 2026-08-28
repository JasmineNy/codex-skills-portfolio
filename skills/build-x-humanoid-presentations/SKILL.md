---
name: build-x-humanoid-presentations
description: Create branded X-Humanoid PowerPoint presentations from source notes, reports, spreadsheets, or rough outlines. Use for internal reporting, quarterly or annual reviews, project retrospectives, management updates, external speeches, customer presentations, and requests mentioning “内部述职”, “季度复盘”, “年度汇报”, “项目复盘”, “外部演讲”, “客户汇报”, “模板01”, or “模板02”. Select the company template, validate data logic and confidentiality, adapt sparse data to suitable layouts, and use the bundled data-expression library only as an analysis-pattern reference.
---

# Build X-Humanoid Presentations

Create a final `.pptx` only when the user asks for one. Treat the bundled files as immutable source assets; never overwrite them.

## Load the required guidance

1. Read `references/reporting-rules.md` before outlining or editing slides.
2. Read or query `references/data-expression-index.json` only when the request contains quantitative analysis, charts, comparisons, forecasts, portfolios, or risk matrices.
3. Load and follow the installed Presentations skill for PowerPoint authoring, template inheritance, artifact-tool use, rendering, and QA.

## Resolve the presentation route

Apply this precedence:

1. If the user explicitly says `模板01` or `模板02`, use that template.
2. Otherwise map internal reports, reviews, and retrospectives to `assets/ppt模版01.pptx`.
3. Otherwise map external speeches, customer presentations, and public-facing decks to `assets/ppt模版02.pptx`.
4. If neither a template number nor an audience is clear, ask whether the deck is internal or external before authoring.

An explicit template number controls visual selection but does not disable the external confidentiality gate.

## Intake and content planning

Collect or derive the audience, purpose, reporting period, presenter, source materials, decision or action requested, and desired output path. Ask only for missing information that materially changes the deck.

Convert source material into a conclusion-led narrative. Preserve names, dates, units, definitions, status, risks, dependencies, and evidence. Do not invent facts, targets, causal explanations, sample sizes, benchmarks, or forecasts.

Before selecting layouts, create a data inventory with:

- metric name and business meaning;
- value, unit, period, and comparison base;
- numerator and denominator for rates;
- actual, target, forecast, or estimate status;
- source, sample size, and material exclusions;
- uncertainty, missing values, and assumptions.

## Select analysis patterns

Search `references/data-expression-index.json` by `analysisPatterns`, `chartTypes`, `recommendedDataVolume`, or slide title. Use the indexed slide number to inspect the corresponding page in `assets/data-analysis-reference.pptx`.

Use the reference library only for analysis logic and chart structure. Keep the selected company template as the final deck's visual source. Never carry the reference library's logo, footer, font, colors, sample copy, or example data into an X-Humanoid deck.

Reuse a chart structure only when the index marks the page `chart-structure-reusable`. Replace every series, category, title, annotation, unit, source, and forecast marker with validated current information, then restyle it to the company template. For `logic-reference-only` pages, recreate the analytical logic instead of copying objects.

When the available data is smaller than the reference layout expects, remove panels and reflow the remaining content. Never leave empty charts or fabricate data to fill a template.

## Apply approval gates

For all decks, verify data logic against `references/reporting-rules.md` before authoring charts.

For external decks, stop before final authoring when the material contains potentially non-public customer names, pricing, product roadmaps, unpublished performance data, personal contact details, confidential partnerships, or unsupported external claims. List the affected items and request confirmation, redaction, or a public-source replacement.

## Author and verify

Use the Presentations skill's exact template-following workflow with the selected company template. Preserve typography, palette, spacing, logo, footer, page markers, and brand chrome. Map each output slide to an inherited source slide and make only validated edits or bounded insertions.

Render and inspect every final slide. Fix unintended overlap, clipping, title wrapping, unresolved placeholders, inconsistent footers, incorrect chart labels, mismatched units, missing sources, and data-to-conclusion contradictions. Inspect the exported PPTX XML for empty structural placeholders as required by the Presentations skill.

Return only the finished deck and concise source notes unless the user requests intermediate material.

## Refresh the reference index

When `assets/data-analysis-reference.pptx` is replaced with an updated version, run:

```bash
node scripts/rebuild-data-expression-index.mjs
```

The script performs a resilient OOXML scan, records EMF/WMF media and pattern-fill risks as logic-only compatibility issues, and continues indexing the remaining pages.
