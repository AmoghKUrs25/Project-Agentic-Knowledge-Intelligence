def evaluate_context(results):
    """
    Check whether vector retrieval produced sufficiently
    relevant evidence.

    Returns:
        True  -> evidence is good enough
        False -> retrieval should be retried
    """

    if not results:
        return False

    best_score = max(
        result.get("score", 0.0)
        for result in results
    )

    print(f"Retrieval quality score: {best_score:.3f}")

    return best_score >= 0.35