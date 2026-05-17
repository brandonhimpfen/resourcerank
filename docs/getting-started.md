# Getting Started with ResourceRank

This guide walks you through installing ResourceRank, evaluating a resource, and interpreting the output.

## 1. Install ResourceRank

Clone or download the project, then open a terminal in the project folder.

```bash
python -m pip install -e .
```

Check that the command is available:

```bash
resourcerank --help
```

## 2. Choose a review profile

A review profile defines what matters for a specific curation context.

For an Awesome List, use:

```text
profiles/awesome-list.json
```

For a dataset catalog, use:

```text
profiles/dataset-catalog.json
```

For a newsletter source list, use:

```text
profiles/newsletter-source.json
```

## 3. Create a resource input file

Create a JSON file describing the resource.

```json
{
  "name": "Example Resource",
  "url": "https://github.com/example/project",
  "resource_type": "github_repository",
  "description": "A short description of the resource.",
  "topic": "open data",
  "section": "Open Data Tools",
  "stars": 75,
  "forks": 8,
  "last_commit_days": 45,
  "has_license": true,
  "license_name": "MIT",
  "has_readme": true,
  "readme_length_words": 850,
  "has_docs": true,
  "has_examples": true,
  "has_tests": false,
  "has_release": true,
  "has_website": true,
  "is_open_source": true,
  "commercial_model": "none",
  "submission_type": "pull_request",
  "self_submission": false,
  "promotional_language": "low",
  "relevance_notes": "The resource directly supports the collection and has enough documentation for users to understand it."
}
```

Save it as:

```text
my-resource.json
```

## 4. Run the evaluation

```bash
resourcerank evaluate --input my-resource.json --profile profiles/awesome-list.json
```

To save the review:

```bash
resourcerank evaluate \
  --input my-resource.json \
  --profile profiles/awesome-list.json \
  --output my-resource-review.json
```

## 5. Interpret the result

ResourceRank gives you a scorecard. The most important fields are:

### decision

The recommended review state.

- `accept`: the resource appears ready for inclusion
- `review`: the resource may be useful, but needs maintainer judgment
- `reject`: the resource does not currently meet the configured criteria

### score

The overall score from 0 to 100.

### confidence

How complete the input appears to be. A low confidence score usually means ResourceRank had too little information.

### signals

The individual category scores.

```json
"signals": {
  "relevance": 95,
  "documentation": 70,
  "maintenance": 85,
  "trust": 60,
  "openness": 95,
  "neutrality": 80
}
```

### concerns

Reasons to be careful before accepting the resource.

### strengths

Positive signals that support inclusion.

## 6. Make the final decision

ResourceRank is designed to support maintainers, not replace them.

A good review process is:

1. Run ResourceRank.
2. Read the output.
3. Check the resource manually.
4. Make the final decision.
5. Keep the JSON output as a review record if useful.
