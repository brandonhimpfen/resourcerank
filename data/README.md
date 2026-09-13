# Evaluation Dataset

`evaluations.jsonl` contains historical ResourceRank evaluation cases derived from real Awesome List pull-request reviews. Each line is one independent submission context. The same underlying resource may therefore appear more than once when it was submitted to different lists or categories.

## Purpose

The dataset is intended for regression testing, calibration, scoring experiments, and analysis of ResourceRank decisions. It is not a blacklist or a permanent judgment about a resource. A rejection records the decision in the submission context and at the time reviewed.

## Format

Each line conforms to `schema/evaluation.schema.json`. Key groups are:

- `resource`: identity of the submitted resource.
- `submission`: list, category, contributor, affiliation, and cross-list context.
- `assessment`: category fit and normalized concern labels.
- `decision`: historical maintainer outcome and, where applicable, a recommended section.
- `provenance`: origin and review period.

## Important interpretation

Producer-side signals such as commit volume, feature count, package count, or technical scope should not be treated as substitutes for independent adoption, recognition, trust, or category fit. Affiliated submissions are not inherently disqualified.
