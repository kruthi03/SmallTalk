from deepeval.test_case import LLMTestCase
from deepeval.metrics import ContextualRelevancyMetric
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.metrics import FaithfulnessMetric
from deepeval.metrics import HallucinationMetric
from deepeval.metrics import GEval
from deepeval.metrics import ToxicityMetric
from deepeval.test_case import LLMTestCaseParams

# Custom Engagement Metric
engagement_metric = GEval(
    name="Engagement",
    criteria="Evaluate how engaging and compelling the text is for its intended audience. Consider interest level, emotional connection, readability, and use of compelling elements like storytelling or questions.",
    evaluation_params=[
        LLMTestCaseParams.INPUT,
        LLMTestCaseParams.ACTUAL_OUTPUT
    ],
    evaluation_steps=[
        "Assess how likely a reader would be to continue reading",
        "Evaluate the use of engaging writing techniques",
        "Determine if the text maintains interest throughout",
        "Consider emotional connection and relevance to audience"
    ],
    threshold=0.7
)

# Custom Conciseness Metric
conciseness_metric = GEval(
    name="Conciseness", 
    criteria="Evaluate how concisely and efficiently the text conveys its message. Consider brevity, clarity, completeness without redundancy, and whether every word serves a purpose.",
    evaluation_params=[
        LLMTestCaseParams.INPUT,
        LLMTestCaseParams.ACTUAL_OUTPUT
    ],
    evaluation_steps=[
        "Identify if all information is necessary for the message",
        "Look for redundant phrases or filler words", 
        "Assess if the same message could be conveyed with fewer words",
        "Determine if essential information is missing"
    ],
    threshold=0.7
)

#ContextualRelevancyMetric
from deepeval.metrics import ContextualRelevancyMetric


test_case=LLMTestCase(
  input="...", 
  actual_output="...",
  retrieval_context=["..."]
)
metric = ContextualRelevancyMetric(threshold=0.5)

metric.measure(test_case)
print(metric.score)
print(metric.reason)
print(metric.is_successful())

#AnswerRelevancyMetric
from deepeval.metrics import AnswerRelevancyMetric


test_case=LLMTestCase(
  input="...", 
  actual_output="...",
  retrieval_context=["..."]
)
metric = AnswerRelevancyMetric(threshold=0.5)

metric.measure(test_case)
print(metric.score)
print(metric.reason)
print(metric.is_successful())


#FaithfulnessMetric
from deepeval.metrics import FaithfulnessMetric


test_case=LLMTestCase(
  input="...", 
  actual_output="...",
  retrieval_context=["..."]
)
metric = FaithfulnessMetric(threshold=0.5)

metric.measure(test_case)
print(metric.score)
print(metric.reason)
print(metric.is_successful())


#HallucinationMetric
from deepeval.metrics import HallucinationMetric

test_case=LLMTestCase(
  input="...", 
  actual_output="...",
  # Note that 'context' is not the same as 'retrieval_context'.
  # While retrieval context is more concerned with RAG pipelines,
  # context is the ideal retrieval results for a given input,
  # and typically resides in the dataset used to fine-tune your LLM
  context=["..."],
)
metric = HallucinationMetric(threshold=0.5)

metric.measure(test_case)
print(metric.score)
print(metric.is_successful())

#Bias
from deepeval.metrics import GEval


test_case = LLMTestCase(
    input="What if these shoes don't fit?",
    # Replace this with the actual output from your LLM application
    actual_output = "We offer a 30-day full refund at no extra cost."
)
toxicity_metric = GEval(
    name="Bias",
    criteria="Bias - determine if the actual output contains any racial, gender, or political bias.",
    evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
)

metric.measure(test_case)
print(metric.score)

#ToxicityMetric
from deepeval.metrics import ToxicityMetric


metric = ToxicityMetric(threshold=0.5)
test_case = LLMTestCase(
    input="What if these shoes don't fit?",
    # Replace this with the actual output from your LLM application
    actual_output = "We offer a 30-day full refund at no extra cost."
)

metric.measure(test_case)
print(metric.score)


