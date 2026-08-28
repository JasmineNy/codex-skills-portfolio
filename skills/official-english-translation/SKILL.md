---
name: official-english-translation
description: Official English translation and localization workflow for company brochures, sales leaflets, PowerPoint decks, case studies, website-ready marketing copy, and other externally published promotional materials. Use when Codex needs to translate Chinese company materials into polished official English, preserve brand voice, adapt copy for international audiences, or enforce a company-specific terminology knowledge base instead of directly translating proprietary names, product names, service names, slogans, solution names, certifications, awards, customer labels, and industry-specific terms.
---

# Official English Translation

## Operating Principle

Produce publication-ready English, not literal translation. Treat the company terminology knowledge base as authoritative: when a source term appears in the material, use the approved English term from `references/company-terminology.tsv`. Do not invent, paraphrase, or directly translate proprietary names when an approved term exists.

Use the historical translation assets as the style baseline. The terminology in `company-terminology.tsv` is sourced from `具身智能英文版定稿.docx`; the style samples in `official-translation-style-samples.md` are sourced from prior finalized case-study and subtitle edits. If the user's current instructions conflict with the historical style, follow the user's current instructions and note the exception.

If the glossary is incomplete, pause only for critical brand terms. For ordinary gaps, translate with a clear candidate term and add the item to a "Terminology updates needed" section in the deliverable or handoff notes.

## Required References

Load only what is needed:

- `references/company-profile.md`: read before translation when the company, industry, audience, or offer is unclear.
- `references/company-terminology.tsv`: read before every translation task; it is the official terminology source.
- `references/official-english-style.md`: read for tone, capitalization, punctuation, and localization rules.
- `references/official-translation-style-samples.md`: read for brochures, PPTs, case studies, video subtitles, headlines, scenario descriptions, and any task where the output should resemble past official translations.
- `references/translation-qa-checklist.md`: read before final QA.

## Workflow

1. Identify the artifact type: brochure, flyer, PPT, case study, web copy, subtitle/script, or mixed package.
2. Extract source text while preserving structure, slide order, headings, captions, tables, figures, legal text, and call-to-action copy.
3. Load the terminology TSV and map all proprietary or industry-specific terms before drafting.
4. Load the style samples when the artifact is a brochure, PPT, case study, or subtitle/script, then mirror the closest relevant sample's level of concision, title style, and rhetorical structure.
5. Translate in official English:
   - Lead with meaning and market impact.
   - Keep claims accurate and verifiable.
   - Preserve numbers, dates, product specs, certification names, customer names, and case metrics.
   - Adapt Chinese rhetorical phrasing into concise English marketing language.
6. Apply company voice and formatting rules from `official-english-style.md`.
7. Check terminology compliance. For plain text, run `scripts/glossary_check.py`; for PPT/DOCX/PDF, extract text first or perform a manual glossary pass.
8. Finalize with a short QA note that lists resolved terminology choices, historical style samples used, and any unresolved terms needing approval.

## File-Specific Handling

For PowerPoint decks, preserve slide intent and hierarchy. Translate speaker notes if requested. Keep titles short enough for slide layouts, and verify after editing that text boxes do not overflow. When available, use the Presentations workflow to render and visually inspect slides.

For company brochures and sales leaflets, preserve layout sections and image captions. Prefer crisp benefit-led English over sentence-by-sentence mirroring. Keep headlines, subheads, and CTA lines punchy.

For case studies, keep the standard structure: Client / Challenge / Solution / Results. Preserve quantitative outcomes exactly unless the source is ambiguous. Avoid overstating customer endorsement.

For video subtitles, keep lines short, natural, and on-screen friendly. Prefer the corrected subtitle style in `official-translation-style-samples.md` over literal word order.

For legal, compliance, awards, certifications, technical specs, and partner/customer names, translate conservatively. Do not localize official organization names unless the glossary or source provides the official English form.

## Terminology Rules

Use `company-terminology.tsv` as the source of truth. Each row should capture:

- `source_term`: Chinese term or original brand term found in source materials.
- `approved_english`: required official English term.
- `term_type`: company, product, solution, service, slogan, certification, industry, customer_segment, award, metric, other.
- `forbidden_translations`: direct translations or legacy variants to avoid, separated by `|`.
- `notes`: context, capitalization, article use, or approval status.

When updating the glossary:

- Add only terms that are company-specific, externally visible, strategically important, or repeatedly mistranslated.
- Prefer the user's approved wording over model judgment.
- Mark uncertain candidates in `notes` as `needs approval`.
- Keep one canonical English term per source term unless the context truly requires variants.

Terminology and style priority:

1. Explicit user instructions in the current task.
2. `company-terminology.tsv` for approved terms and forbidden translations.
3. `official-translation-style-samples.md` for historical case-study, PPT, brochure, and subtitle style.
4. General translation judgment.

## Quality Bar

Before delivery, confirm:

- Approved terminology is used wherever source terms appear.
- Headlines sound natural in English and fit their medium.
- The translation is suitable for official external publication.
- Numbers, names, dates, certifications, awards, and customer facts match the source.
- No machine-translation artifacts remain, such as stiff word order, duplicated modifiers, or literal idioms.
- Any unresolved terminology is clearly listed for user approval.
