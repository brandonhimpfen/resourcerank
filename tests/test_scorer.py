from resourcerank.profiles import DEFAULT_PROFILE
from resourcerank.schema import Resource
from resourcerank.scorer import ResourceScorer


def test_strong_resource_accepts_or_reviews_highly():
    resource = Resource.from_dict({
        "name": "Strong Tool",
        "description": "Useful open-source tool.",
        "topic": "developer tooling",
        "section": "Developer Tools",
        "stars": 1000,
        "forks": 120,
        "last_commit_days": 10,
        "has_license": True,
        "license_name": "MIT",
        "has_readme": True,
        "readme_length_words": 2000,
        "has_docs": True,
        "has_examples": True,
        "has_tests": True,
        "has_release": True,
        "has_website": True,
        "is_open_source": True,
        "commercial_model": "none",
        "self_submission": False,
        "promotional_language": "low",
        "relevance_notes": "Strong direct fit for the target collection with clear end-user value."
    })
    result = ResourceScorer(DEFAULT_PROFILE).evaluate(resource)
    assert result.score >= 80
    assert result.decision == "accept"


def test_weak_resource_rejects_or_reviews():
    resource = Resource.from_dict({
        "name": "Weak Tool",
        "description": "Small tool.",
        "stars": 2,
        "last_commit_days": 1200,
        "has_license": False,
        "has_readme": False,
        "has_docs": False,
        "is_open_source": False,
        "commercial_model": "unclear",
        "self_submission": True,
        "promotional_language": "high"
    })
    result = ResourceScorer(DEFAULT_PROFILE).evaluate(resource)
    assert result.score < 55
    assert result.decision == "reject"
