# Review Profiles

Review profiles let you adapt ResourceRank to different types of curated projects.

A profile controls:

- signal weights
- accept/review thresholds
- scoring rules

## Basic profile structure

```json
{
  "name": "awesome-list",
  "description": "Review profile for Awesome Lists and curated open resource collections.",
  "weights": {
    "relevance": 35,
    "documentation": 20,
    "maintenance": 15,
    "trust": 10,
    "openness": 15,
    "neutrality": 5
  },
  "thresholds": {
    "accept": 82,
    "review": 58
  }
}
```

## Signals

### relevance

How well the resource fits the collection, topic, and proposed section.

### documentation

How well the resource explains itself to users.

### maintenance

Whether the resource appears active, versioned, tested, or maintained.

### trust

Whether there are adoption signals, website signals, or other indicators that the resource is credible.

### openness

Whether the resource has clear licensing and reuse permissions.

### neutrality

Whether the resource appears informational and useful rather than overly promotional.

## Thresholds

Thresholds define the decision boundaries.

```json
"thresholds": {
  "accept": 80,
  "review": 55
}
```

This means:

- Score 80 or higher: `accept`
- Score 55 to 79: `review`
- Score below 55: `reject`

Some severe concerns, such as missing licensing or low relevance, may prevent automatic acceptance.

## Creating a custom profile

Copy an existing profile:

```bash
cp profiles/awesome-list.json profiles/my-project.json
```

Edit the weights and thresholds.

Then run:

```bash
resourcerank evaluate --input my-resource.json --profile profiles/my-project.json
```
