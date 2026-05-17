from __future__ import annotations

from typing import Dict, List, Tuple

from .schema import Resource, ReviewResult


def clamp(value: int, minimum: int = 0, maximum: int = 100) -> int:
    return max(minimum, min(maximum, int(round(value))))


class ResourceScorer:
    def __init__(self, profile: Dict):
        self.profile = profile
        self.weights = profile.get("weights", {})
        self.rules = profile.get("rules", {})
        self.thresholds = profile.get("thresholds", {"accept": 80, "review": 55})

    def evaluate(self, resource: Resource) -> ReviewResult:
        raw_signals = {
            "relevance": self.score_relevance(resource),
            "documentation": self.score_documentation(resource),
            "maintenance": self.score_maintenance(resource),
            "trust": self.score_trust(resource),
            "openness": self.score_openness(resource),
            "neutrality": self.score_neutrality(resource),
        }
        score = self.weighted_score(raw_signals)
        concerns, strengths = self.build_findings(resource, raw_signals)
        decision = self.decision(score, concerns)
        category_fit = self.category_fit(raw_signals["relevance"])
        confidence = self.confidence(resource)
        summary = self.summary(resource, score, decision, concerns, strengths)
        suggested_action = self.suggested_action(decision, concerns)

        return ReviewResult(
            decision=decision,
            score=score,
            confidence=confidence,
            resource_type=resource.resource_type,
            category_fit=category_fit,
            recommended_section=resource.section or "manual_review_required",
            signals=raw_signals,
            concerns=concerns,
            strengths=strengths,
            summary=summary,
            suggested_action=suggested_action,
            profile=self.profile.get("name", "default"),
        )

    def weighted_score(self, signals: Dict[str, int]) -> int:
        total_weight = sum(self.weights.get(k, 0) for k in signals)
        if total_weight <= 0:
            return clamp(sum(signals.values()) / len(signals))
        weighted = sum(signals[k] * self.weights.get(k, 0) for k in signals) / total_weight
        return clamp(weighted)

    def score_relevance(self, r: Resource) -> int:
        score = 50
        if r.topic:
            score += 15
        if r.section:
            score += 15
        if r.relevance_notes and len(r.relevance_notes.split()) >= 12:
            score += 15
        if not r.description:
            score -= 10
        return clamp(score)

    def score_documentation(self, r: Resource) -> int:
        score = 35
        if r.has_readme:
            score += 15
        words = r.readme_length_words or 0
        if words >= self.rules.get("minimum_readme_words_for_full_docs", 500):
            score += 20
        elif words >= 150:
            score += 10
        if r.has_docs:
            score += 15
        if r.has_examples:
            score += 10
        if not r.has_readme and not r.has_docs:
            score -= 20
        return clamp(score)

    def score_maintenance(self, r: Resource) -> int:
        score = 50
        days = r.last_commit_days
        if days is None:
            score -= 10
        elif days <= self.rules.get("recent_commit_days", 180):
            score += 25
        elif days >= self.rules.get("stale_commit_days", 730):
            score -= 25
        if r.has_release:
            score += 10
        if r.has_tests:
            score += 10
        return clamp(score)

    def score_trust(self, r: Resource) -> int:
        score = 45
        stars = r.stars
        if stars is not None:
            if stars >= self.rules.get("strong_star_threshold", 500):
                score += 25
            elif stars >= self.rules.get("low_star_threshold", 25):
                score += 10
            else:
                score -= 5
        if r.forks is not None and r.forks >= 10:
            score += 10
        if r.has_website:
            score += 10
        if r.open_issues is not None and r.open_issues > 250:
            score -= 10
        return clamp(score)

    def score_openness(self, r: Resource) -> int:
        score = 50
        if r.is_open_source:
            score += 20
        if r.has_license:
            score += 20
        if r.license_name:
            score += 5
        if r.commercial_model.lower() in {"closed", "paid-only", "unclear"}:
            score -= 15
        return clamp(score)

    def score_neutrality(self, r: Resource) -> int:
        score = 70
        promo = r.promotional_language.lower()
        if promo == "high":
            score -= 35
        elif promo == "medium":
            score -= 15
        if r.self_submission:
            score -= 10
        if r.commercial_model.lower() in {"freemium", "paid-only"}:
            score -= 10
        return clamp(score)

    def decision(self, score: int, concerns: List[str]) -> str:
        accept = self.thresholds.get("accept", 80)
        review = self.thresholds.get("review", 55)
        severe = any("missing license" in c.lower() or "low relevance" in c.lower() for c in concerns)
        if score >= accept and not severe:
            return "accept"
        if score >= review:
            return "review"
        return "reject"

    def category_fit(self, relevance_score: int) -> str:
        if relevance_score >= 80:
            return "high"
        if relevance_score >= 60:
            return "medium"
        return "low"

    def confidence(self, r: Resource) -> int:
        known_fields = 0
        total = 13
        for value in [r.description, r.topic, r.section, r.stars, r.last_commit_days, r.has_license,
                      r.has_readme, r.readme_length_words, r.has_docs, r.has_examples, r.has_release,
                      r.has_website, r.promotional_language != "unknown"]:
            if value not in (None, "", False):
                known_fields += 1
        return clamp((known_fields / total) * 100)

    def build_findings(self, r: Resource, signals: Dict[str, int]) -> Tuple[List[str], List[str]]:
        concerns: List[str] = []
        strengths: List[str] = []

        if signals["relevance"] < 60:
            concerns.append("Low relevance evidence for the requested collection or section.")
        else:
            strengths.append("Clear topical relevance or section fit is present.")
        if signals["documentation"] < 55:
            concerns.append("Documentation appears limited or incomplete.")
        else:
            strengths.append("Documentation signals are adequate for review.")
        if signals["maintenance"] < 50:
            concerns.append("Maintenance activity is weak, stale, or unclear.")
        if r.has_license is False:
            concerns.append("Missing license or unclear reuse permissions.")
        if signals["openness"] >= 70:
            strengths.append("Open-source or licensing signals are strong.")
        if r.promotional_language.lower() == "high":
            concerns.append("Resource presentation appears highly promotional.")
        if r.self_submission:
            concerns.append("Self-submission should receive extra maintainer review.")
        if r.stars is not None and r.stars < self.rules.get("low_star_threshold", 25):
            concerns.append("Adoption signals are still early or limited.")
        if r.has_examples:
            strengths.append("Examples are available for end-user evaluation.")
        if r.has_tests:
            strengths.append("Testing signals improve implementation confidence.")
        return concerns, strengths

    def summary(self, r: Resource, score: int, decision: str, concerns: List[str], strengths: List[str]) -> str:
        name = r.name
        if decision == "accept":
            return f"{name} appears suitable for inclusion with a score of {score}/100. The resource shows enough quality, relevance, and trust signals for acceptance."
        if decision == "review":
            issue = concerns[0] if concerns else "Some review signals require maintainer judgment."
            return f"{name} should receive maintainer review with a score of {score}/100. Main issue: {issue}"
        issue = concerns[0] if concerns else "The resource does not meet the configured review threshold."
        return f"{name} is not currently recommended for inclusion with a score of {score}/100. Main issue: {issue}"

    def suggested_action(self, decision: str, concerns: List[str]) -> str:
        if decision == "accept":
            return "Accept if the maintainer agrees with the section placement and description."
        if decision == "review":
            return "Request clarification, stronger documentation, licensing details, or additional adoption evidence before accepting."
        return "Reject for now or invite a revised submission after the concerns are addressed."
