# GitHub Action Usage

ResourceRank v1 includes an example GitHub Actions workflow. It is intentionally conservative and file-based.

The workflow evaluates JSON files placed in a `reviews/input/` folder and writes outputs to `reviews/output/`.

## Example folder structure

```text
reviews/
  input/
    submitted-resource.json
  output/
```

## Example workflow

See:

```text
.github/workflows/resourcerank-example.yml
```

## How to use it

1. Add ResourceRank to your repository.
2. Add one or more resource input JSON files to `reviews/input/`.
3. Run the workflow manually or on pull requests.
4. Review the generated JSON outputs.

## Important note

The included workflow is a starter. It does not automatically comment on pull requests yet. That is intentional for v1, because maintainers should first confirm that the scoring profile matches their project.

Future versions can add:

- PR comments
- changed-file detection
- automatic GitHub metadata collection
- README parsing
- score badges
- maintainer override records
