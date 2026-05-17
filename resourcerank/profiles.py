from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

DEFAULT_PROFILE = {
    "name": "default",
    "description": "General resource review profile for curated collections.",
    "weights": {
        "relevance": 30,
        "documentation": 20,
        "maintenance": 15,
        "trust": 15,
        "openness": 10,
        "neutrality": 10
    },
    "thresholds": {
        "accept": 80,
        "review": 55
    },
    "rules": {
        "minimum_readme_words_for_full_docs": 500,
        "recent_commit_days": 180,
        "stale_commit_days": 730,
        "low_star_threshold": 25,
        "strong_star_threshold": 500
    }
}


def load_profile(path: str | None = None) -> Dict[str, Any]:
    if not path:
        return DEFAULT_PROFILE
    profile_path = Path(path)
    if not profile_path.exists():
        raise FileNotFoundError(f"Profile not found: {profile_path}")
    with profile_path.open("r", encoding="utf-8") as f:
        profile = json.load(f)
    return merge_profile(DEFAULT_PROFILE, profile)


def merge_profile(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            nested = dict(merged[key])
            nested.update(value)
            merged[key] = nested
        else:
            merged[key] = value
    return merged
