from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Resource:
    name: str
    url: str = ""
    resource_type: str = "unknown"
    description: str = ""
    topic: str = ""
    section: str = ""
    stars: Optional[int] = None
    forks: Optional[int] = None
    open_issues: Optional[int] = None
    last_commit_days: Optional[int] = None
    has_license: Optional[bool] = None
    license_name: str = ""
    has_readme: Optional[bool] = None
    readme_length_words: Optional[int] = None
    has_docs: Optional[bool] = None
    has_examples: Optional[bool] = None
    has_tests: Optional[bool] = None
    has_release: Optional[bool] = None
    has_website: Optional[bool] = None
    is_open_source: Optional[bool] = None
    commercial_model: str = "unknown"
    submission_type: str = "unknown"
    self_submission: Optional[bool] = None
    promotional_language: str = "unknown"
    relevance_notes: str = ""
    maintainer_notes: str = ""
    extra: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Resource":
        known = {field.name for field in cls.__dataclass_fields__.values()}
        kwargs = {k: v for k, v in data.items() if k in known}
        extra = {k: v for k, v in data.items() if k not in known}
        kwargs.setdefault("extra", extra)
        if "name" not in kwargs or not kwargs["name"]:
            raise ValueError("Resource input must include a non-empty 'name'.")
        return cls(**kwargs)


@dataclass
class ReviewResult:
    decision: str
    score: int
    confidence: int
    resource_type: str
    category_fit: str
    recommended_section: str
    signals: Dict[str, int]
    concerns: List[str]
    strengths: List[str]
    summary: str
    suggested_action: str
    profile: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "decision": self.decision,
            "score": self.score,
            "confidence": self.confidence,
            "resource_type": self.resource_type,
            "category_fit": self.category_fit,
            "recommended_section": self.recommended_section,
            "signals": self.signals,
            "concerns": self.concerns,
            "strengths": self.strengths,
            "summary": self.summary,
            "suggested_action": self.suggested_action,
            "profile": self.profile,
        }
