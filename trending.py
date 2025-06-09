#trending.py
from api_utils import *
from llm_utils import *




def generate_trending(keywords, extra_links=None, prompt_version="v01", **model_params):
    news = get_news(keywords, 3)


    prompt = build_prompt(prompt_type = 'trending',     
                          prompt_version = prompt_version,
                            keywords=keywords, news = news, 
                            article_text= '',
                            reference_url = '',
                            extra_links = extra_links)


    raw_response = get_llm_response(prompt)
    valid, parsed_json = verify_and_fix_json(raw_response)
    if valid:
        return parsed_json
    else:
        print("Could not parse/fix the JSON response.")
        return None



def validate_trending_output(output_json):
    """
    Validate that the trending JSON conforms to schema.
    Receives:
        - output_json: the JSON to validate
    """
    pass


def extract_text_from_trending_now_json(json_data):
    texts = []
    if not isinstance(json_data, dict): return ""
    texts.append(json_data.get("topic", ""))
    texts.append(json_data.get("category", ""))
    texts.append(json_data.get("subcategory", ""))
    texts.append(json_data.get("description", ""))
    if isinstance(json_data.get("why_is_it_trending"), list): texts.extend(json_data.get("why_is_it_trending"))
    if isinstance(json_data.get("key_points"), list): texts.extend(json_data.get("key_points"))
    if isinstance(json_data.get("overlook_what_might_happen_next"), list): texts.extend(json_data.get("overlook_what_might_happen_next"))
    return "\n".join(filter(None, texts)).strip()


