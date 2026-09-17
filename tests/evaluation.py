from app.rag.retriever import RAGRetriever


retriever = RAGRetriever()

test_cases = [
    {
        "question": "What is the annual paid leave allowance?",
        "expected": ["24 days", "annual paid leave"]
    },
    {
        "question": "Who qualifies for service leave?",
        "expected": ["two years", "5 days", "service leave"]
    },
    {
        "question": "When can employees join technical training?",
        "expected": ["training", "employees"]
    },
    {
        "question": "What security requirements apply to passwords?",
        "expected": ["password", "security"]
    },
    {
        "question": "What technologies are used in machine learning projects?",
        "expected": ["Python", "TensorFlow", "PyTorch"]
    }
]


print("\n========== RAG EVALUATION ==========\n")

passed = 0

for i, test in enumerate(test_cases, start=1):

    print(f"Test {i}: {test['question']}")

    results = retriever.search(test["question"], k=3)

    combined_text = " ".join(
        result["document"]["text"]
        for result in results
    ).lower()

    matches = [
        keyword
        for keyword in test["expected"]
        if keyword.lower() in combined_text
    ]

    score = len(matches) / len(test["expected"])

    print(f"Expected keywords: {test['expected']}")
    print(f"Matched keywords: {matches}")
    print(f"Retrieval score: {score:.2f}")

    if score >= 0.5:
        print("STATUS: PASS")
        passed += 1
    else:
        print("STATUS: FAIL")

    print("-" * 50)

accuracy = passed / len(test_cases)

print("\n========== EVALUATION SUMMARY ==========")
print(f"Tests passed: {passed}/{len(test_cases)}")
print(f"Evaluation accuracy: {accuracy * 100:.1f}%")
print("========================================")