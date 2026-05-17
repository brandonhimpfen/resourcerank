# Dataset Roadmap

ResourceRank can become stronger over time by collecting structured review examples.

The goal is to build a dataset of resource submissions and maintainer decisions.

## Recommended dataset format

Use JSONL, with one reviewed resource per line.

```json
{"input":{"name":"Example Tool","resource_type":"github_repository"},"output":{"decision":"review","score":64,"reasons":["Limited documentation"]}}
```

## Useful labels

For each example, store:

- resource name
- resource URL
- resource type
- topic
- proposed section
- metadata signals
- maintainer decision
- score
- concerns
- strengths
- final rationale

## Suggested decision labels

Use three labels at first:

- `accept`
- `review`
- `reject`

Avoid adding too many labels early. A small, consistent dataset is more useful than a large, messy one.

## How many examples are useful

A practical starting point:

- 50 examples: enough to test the schema
- 100 to 300 examples: enough to see patterns
- 500 to 1,000 examples: enough to consider model-assisted classification
- 2,000+ examples: enough to begin serious fine-tuning experiments

## What to collect first

Start with past maintainer decisions:

- accepted Awesome List entries
- rejected submissions
- “needs review” cases
- self-submissions
- early-stage projects
- highly mature projects
- unclear licensing cases
- overly promotional resources

## Why this matters

The dataset should not only teach whether a resource is “good.” It should teach whether a resource is appropriate for structured inclusion in a curated ecosystem.
