from deepeval.test_case import LLMTestCase

# Create test case with keywords, JSON output, and retrieval context
test_case = LLMTestCase(
    input="machine learning neural networks",  # keywords
    actual_output='''{
        "title": "Neural Network Fundamentals",
        "inventor": "Geoffrey Hinton", 
        "year_invented": "1943",
        "applications": ["pattern recognition", "data analysis"],
        "accuracy": "99.9%",
        "category": "machine learning"
    }''',  # JSON output with potential hallucinations
    retrieval_context=[
        "Neural networks are a type of machine learning algorithm.",
        "They are used for pattern recognition and data analysis.",
        "Neural networks have become popular in recent decades."
    ]
)

# Initialize and measure hallucination
metric = KeywordJSONHallucinationMetric(threshold=0.7, strict_mode=False)
score = metric.measure(test_case)

print(f"Hallucination Score: {score:.2f}")
print(f"Success: {metric.is_successful()}")
print(f"Detailed Reason: {metric.reason}")
