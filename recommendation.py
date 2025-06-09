#recommendations.py

from api_utils import *
from llm_utils import *




def generate_recommendation(keywords, prompt_version="v01", region = "us", num_results=15, lang="en", **model_params):   
    urls = get_urls_from_google(keywords, region = region, num_results=num_results, lang=lang)
    articles = get_articles(urls)
    print(len(" ".join(articles)))
    articles = " ".join(articles)[0:21000]

    prompt = build_prompt(prompt_type = 'recommendation', 
                          prompt_version = prompt_version,
                            keywords=keywords, news = '', 
                            article_text= articles,
                            reference_url = '')
    response = get_llm_response(prompt)
    valid, fixed_json = verify_and_fix_json(response)
    if valid:
        return fixed_json
    else:
        print("The Error is not fixed")




#TODO: Implement the build_prompt_recommendations function
def validate_recommendation_output(output_json):
    """
    Validate that the recommendation JSON conforms to schema.
    Receives:
        - output_json: the JSON to validate
    """
    pass


def extract_text_from_recommendations_json(json_data):
    texts = []
    if not isinstance(json_data, dict): return ""
    texts.append(json_data.get("introduction", ""))
    key_tips = json_data.get("key_tips_and_takeaways", {})
    if isinstance(key_tips, dict):
        for _, tips_list in key_tips.items():
            if isinstance(tips_list, list): texts.extend(str(tip) for tip in tips_list)
    fun_facts = json_data.get("fun_facts", [])
    if isinstance(fun_facts, list): texts.extend(str(fact) for fact in fun_facts)
    texts.append(json_data.get("conclusion", ""))
    return "\n".join(filter(None, texts)).strip()
