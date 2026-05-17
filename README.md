# ResourceRank

[![Support Open Work](https://img.shields.io/badge/Support-Open%20Work-0A0A0A?style=flat&logo=github)](https://github.com/brandonhimpfen/support) 
[![DOI](https://zenodo.org/badge/1241152105.svg)](https://doi.org/10.5281/zenodo.20260625)

ResourceRank is a structured review tool for evaluating whether a submitted resource belongs in a curated collection.

It is designed for maintainers of Awesome Lists, resource directories, dataset catalogs, newsletters, knowledge bases, learning libraries, and other curated ecosystems.

ResourceRank does not replace human judgment. It turns review criteria into a consistent scorecard so maintainers can make better, faster, and more transparent decisions.

## What ResourceRank does

ResourceRank evaluates a resource using configurable review signals:

- Relevance
- Documentation
- Maintenance
- Trust
- Openness
- Neutrality

It returns a structured JSON review with:

- `decision`: `accept`, `review`, or `reject`
- `score`: overall score from 0 to 100
- `confidence`: how complete the input data appears to be
- `category_fit`: low, medium, or high
- `signals`: individual signal scores
- `concerns`: review concerns
- `strengths`: positive signals
- `summary`: plain-language review summary
- `suggested_action`: recommended maintainer action

## Who this is for

Use ResourceRank if you maintain:

- An Awesome List
- A GitHub-based directory
- A resource catalog
- A dataset catalog
- A research or learning library
- A newsletter source list
- A software/tools directory
- A knowledge base with submitted resources

## Install locally

From the project folder:

```bash
python -m pip install -e .
```

Confirm the CLI works:

```bash
resourcerank --help
```

## Evaluate your first resource

Run ResourceRank against the included example:

```bash
resourcerank evaluate \
  --input examples/freeeq8-review-input.json \
  --profile profiles/awesome-list.json
```

Save the output to a file:

```bash
resourcerank evaluate \
  --input examples/freeeq8-review-input.json \
  --profile profiles/awesome-list.json \
  --output review-output.json
```

## Example output

```json
{
  "decision": "review",
  "score": 61,
  "confidence": 92,
  "resource_type": "github_repository",
  "category_fit": "high",
  "recommended_section": "Recording, Mixing & Mastering Tools",
  "signals": {
    "relevance": 95,
    "documentation": 60,
    "maintenance": 85,
    "trust": 40,
    "openness": 95,
    "neutrality": 25
  },
  "concerns": [
    "Resource presentation appears highly promotional.",
    "Self-submission should receive extra maintainer review.",
    "Adoption signals are still early or limited."
  ],
  "strengths": [
    "Clear topical relevance or section fit is present.",
    "Documentation signals are adequate for review.",
    "Open-source or licensing signals are strong."
  ],
  "summary": "FreeEQ8 should receive maintainer review with a score of 61/100. Main issue: Resource presentation appears highly promotional.",
  "suggested_action": "Request clarification, stronger documentation, licensing details, or additional adoption evidence before accepting.",
  "profile": "awesome-list"
}
```

Actual scores may differ as the profile or scoring logic changes.

## Input format

Create a JSON file for the resource you want to review.

```json
{
  "name": "Example Resource",
  "url": "https://github.com/example/project",
  "resource_type": "github_repository",
  "description": "Short description of the resource.",
  "topic": "machine learning",
  "section": "Machine Learning Tools",
  "stars": 120,
  "forks": 12,
  "open_issues": 8,
  "last_commit_days": 30,
  "has_license": true,
  "license_name": "MIT",
  "has_readme": true,
  "readme_length_words": 900,
  "has_docs": true,
  "has_examples": true,
  "has_tests": true,
  "has_release": true,
  "has_website": true,
  "is_open_source": true,
  "commercial_model": "none",
  "submission_type": "pull_request",
  "self_submission": false,
  "promotional_language": "low",
  "relevance_notes": "The project directly fits the target collection."
}
```

You do not need every field, but the review confidence will be stronger when more fields are supplied.

## Review profiles

Profiles let you adapt ResourceRank to different types of curation.

Included profiles:

- `profiles/awesome-list.json`
- `profiles/newsletter-source.json`
- `profiles/dataset-catalog.json`

Show a profile:

```bash
resourcerank show-profile --profile profiles/awesome-list.json
```

Create your own profile by copying one of the included files and adjusting the weights.

```json
{
  "name": "my-directory",
  "description": "Review profile for my curated resource directory.",
  "weights": {
    "relevance": 35,
    "documentation": 20,
    "maintenance": 15,
    "trust": 15,
    "openness": 10,
    "neutrality": 5
  },
  "thresholds": {
    "accept": 80,
    "review": 55
  }
}
```

Weights do not need to add up to 100. ResourceRank normalizes them automatically.

## Decision meanings

### Accept

The resource appears strong enough for inclusion, assuming the maintainer agrees with the section placement and description.

### Review

The resource has enough value to consider, but one or more concerns require maintainer judgment.

### Reject

The resource does not currently meet the configured threshold or has concerns that make inclusion inappropriate.

## Suggested maintainer workflow

1. Create a resource input JSON file.
2. Choose a review profile.
3. Run ResourceRank.
4. Read the concerns and strengths.
5. Make a final human decision.
6. Save the output as part of your review record if useful.

## Important limitations

ResourceRank v1 is a rules-based scoring engine. It does not automatically crawl GitHub, websites, or APIs. This makes v1 predictable, transparent, and easy to run locally.

A future version can add:

- GitHub metadata fetching
- README analysis
- LLM-assisted qualitative review
- GitHub Action PR comments
- Dataset generation from maintainer decisions
- Trained classification models

## Why this approach

A strong curation system needs consistency before automation. ResourceRank v1 focuses on the schema, scoring philosophy, review profiles, and repeatable output format. Those pieces create the foundation for a future AI-assisted or trained model.
