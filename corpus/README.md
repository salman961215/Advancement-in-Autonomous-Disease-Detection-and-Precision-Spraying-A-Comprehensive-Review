# Corpus

`corpus_130.csv` is the machine-readable corpus of all 130 reviewed papers.

Columns:
- `bibkey` — citation key, matches `../references.bib`
- `reference` — author/year short form
- `year` — publication year (2020–2026)
- `section` — Detection, Spraying, or Closed-loop
- `subtheme` — finer grouping (e.g. Visual-VLM, Spectral-HSI, EndToEnd, DecisionIntelligence, SensorFusion)
- `crop`, `technique`, `key_result`
- `also_in_section` — set only for Baltazar et al. (2021), which spans Spraying and Closed-loop

The file holds one row per unique paper (129 rows). The deduplicated corpus is 130
because Baltazar et al. (2021) is a member of two sections; it is counted once in the
total and flagged via `also_in_section`.
