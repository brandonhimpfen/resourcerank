# Resource Input Schema

ResourceRank accepts a JSON object describing one resource.

Only `name` is required. However, more complete inputs produce better reviews.

## Fields

### name

Required. The resource name.

```json
"name": "Example Tool"
```

### url

The main URL for the resource.

```json
"url": "https://github.com/example/tool"
```

### resource_type

The type of resource.

Examples:

- `github_repository`
- `website`
- `article`
- `dataset`
- `paper`
- `api`
- `tool`
- `newsletter_source`

### description

A short description of the resource.

### topic

The broad topic the resource belongs to.

### section

The section where the resource may be included.

### stars

GitHub stars or another adoption signal.

### forks

GitHub forks or another reuse signal.

### open_issues

Open issues. This is optional and should be interpreted carefully. Many open issues are not always bad, especially for large projects.

### last_commit_days

Number of days since the most recent commit or update.

### has_license

Whether the resource has a clear license.

### license_name

The license name, such as `MIT`, `Apache-2.0`, `GPL-3.0`, or `CC0-1.0`.

### has_readme

Whether the resource has a README or equivalent overview page.

### readme_length_words

Approximate README length in words.

### has_docs

Whether the resource has documentation beyond a basic README.

### has_examples

Whether the resource includes examples, demos, sample files, or usage instructions.

### has_tests

Whether the resource includes tests or validation workflows.

### has_release

Whether the resource has formal releases, versions, or changelogs.

### has_website

Whether the resource has a website, documentation site, demo page, or stable public homepage.

### is_open_source

Whether the resource is open source.

### commercial_model

Suggested values:

- `none`
- `open-core`
- `freemium`
- `paid-only`
- `closed`
- `unclear`

### submission_type

Suggested values:

- `pull_request`
- `issue`
- `manual_review`
- `newsletter_candidate`
- `dataset_submission`

### self_submission

Whether the resource was submitted by its creator, maintainer, company, or someone with a direct interest.

### promotional_language

Suggested values:

- `low`
- `medium`
- `high`
- `unknown`

Use `high` when the resource description or README feels more like advertising than documentation.

### relevance_notes

A short explanation of how the resource fits the collection.

### maintainer_notes

Optional notes from the reviewer or maintainer.
