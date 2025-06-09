#update_me.py
from api_utils import *
from llm_utils import *
from config import * 



def generate_update_element(keywords, reference_url=None, prompt_version="v01", **model_params):
    """
    Generates a structured update element in JSON format using OpenAI's API and the tailored prompt.
    """
    news = get_news(keywords, 3)
    prompt = build_prompt(prompt_type = 'update_me', 
                          prompt_version = prompt_version,
                            keywords=keywords, news = news, 
                            article_text= "",
                            reference_url = reference_url)
    raw_response = get_llm_response(prompt)
    valid, parsed_json = verify_and_fix_json(raw_response)
    if valid:
        return parsed_json
    else:
        print("Could not parse/fix the JSON response.")
        return None




def validate_update_me_output(output_json):
    """
    Ensure the UpdateMe output JSON matches schema/constraints.
    Receives:
        - output_json: the JSON to validate
    """
    pass


def extract_text_from_update_element_json(json_data):
    texts = []
    if not isinstance(json_data, dict): return ""
    texts.append(json_data.get("category", ""))
    texts.append(json_data.get("subcategory", ""))
    texts.append(json_data.get("topic", ""))
    if isinstance(json_data.get("short_info"), list): texts.extend(json_data.get("short_info"))
    if isinstance(json_data.get("background_story"), dict):
        texts.append(json_data["background_story"].get("context_history", ""))
        texts.append(json_data["background_story"].get("current_developments", ""))
        texts.append(json_data["background_story"].get("relevance", ""))
    return "\n".join(filter(None, texts)).strip()




