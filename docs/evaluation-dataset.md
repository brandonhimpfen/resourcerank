# Historical Evaluation Dataset

ResourceRank includes a JSONL dataset of real curation decisions so changes to scoring logic can be tested against known maintainer outcomes.

The canonical file is `data/evaluations.jsonl`. One line represents one resource submission to one collection/category. This means a resource submitted to two Awesome Lists produces two evaluation cases because relevance and category fit are contextual.

The initial dataset contains both accepted and rejected cases. Positive controls are important so ResourceRank does not become a rejection detector.

Decisions are historical observations, not immutable labels. Resource maturity and adoption can change, and a future submission may receive a different result.
