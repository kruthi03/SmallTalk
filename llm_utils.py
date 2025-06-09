#llm_utils.py

from openai import OpenAI
from config import OPENAI_API_KEY
import os
import json
import re

def get_llm_response(prompt):
    """
    Call the LLM (using OpenAI's API in this example) to generate a response.
    """

    client = OpenAI(api_key = OPENAI_API_KEY)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or another model if desired
            messages=[
                #{"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            #max_completion_tokens = 5000
        )
        llm_output = response.choices[0].message.content.strip()
        return llm_output
    except Exception as e:
        print("Error during LLM call:", e)
        return 

import os


def build_prompt(
    prompt_type,
    prompt_version,
    keywords=None,
    article_text=None,
    extra_links=None,
    news=None,
    reference_url=None,
    allow_options = False,
    template_dir="prompts"
):
    """
    Builds a prompt string by formatting a template file with provided arguments.
    Accepts all fields as strings or lists, regardless of whether the template uses them.
    This version assumes the caller always passes all known keyword arguments (even as None).

    Args:
        prompt_type (str): e.g., 'recommendation', 'trending', 'search_bar', 'update_me'
        prompt_version (str): e.g., 'v01'
        keywords (str or list): Keywords (always required)
        article_text (str): Summary or full article
        extra_links (list of str): Optional list of links
        news (list of dict or str): Optional news items
        reference_url (str or list): Optional reference URL(s)
        template_dir (str): Folder where templates are located

    Returns:
        str: Final prompt string with all placeholders substituted
    """

    # Normalize all fields
    keywords_str = ", ".join(keywords) if isinstance(keywords, list) else (keywords or "")

    article_text_str = article_text.strip() if article_text else ""

    extra_links_str = ""
    if extra_links:
        extra_links_str = "\n".join(f"- {link}" for link in extra_links)

    news_str = ""
    if news:
        for item in news:
            if isinstance(item, dict):
                line = f"- {item.get('title', '')}: {item.get('description', '')}".strip()
                if line and line != ":":
                    news_str += line + "\n"
            elif isinstance(item, str):
                news_str += f"- {item.strip()}\n"

    reference_url_str = ""
    if reference_url:
        if isinstance(reference_url, list):
            reference_url_str = "\n".join(f"- {url}" for url in reference_url)
        else:
            reference_url_str = reference_url.strip()

    # Load template
    template_filename = f"{prompt_type}_{prompt_version}.txt"
    template_path = os.path.join(template_dir, template_filename)

    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template not found: {template_path}")

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    # Format all known placeholders, regardless of usage
    prompt = template.format(
        keywords=keywords,
        articles=article_text_str,
        extra_links=extra_links_str,
        news=news_str.strip(),
        reference_url=reference_url_str,
        allow_options = allow_options
    )

    return prompt


def verify_and_fix_json(input_str):
    """Attempt to parse `input_str` as JSON. If it fails,
    apply a series of fixes, then re-parse. Return (parse_ok, final_json).
      parse_ok: bool - True if valid JSON was obtained (original or fixed).
      final_json: dict or list or None - The parsed JSON object, or None if fixes failed.
    """

    # Helper: Remove markdown code block markers (``` or ```json)
    def remove_markdown_code_block(s):
        lines = s.splitlines()
        # Remove starting ``` or ```json
        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]
        # Remove ending ```
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        return "\n".join(lines)

    # Helper: Remove literal newlines inside JSON string literals by replacing them with a space.
    # This function preserves double quotes around the string.
    def remove_newlines_in_strings(s):
        pattern = r'"((?:\\.|[^"\\])*)"'  # Regex to match string contents (handles escaped quotes too)

        def replacer(match):
            inner = match.group(1)
            # Replace literal newline characters with a space
            new_inner = inner.replace('\n', ' ')
            return '"' + new_inner + '"'

        return re.sub(pattern, replacer, s, flags=re.DOTALL)

    # STEP 1: Preprocess: remove markdown code fences & newlines in string literals
    preprocessed = remove_markdown_code_block(input_str)
    preprocessed = remove_newlines_in_strings(preprocessed)

    # Attempt to parse the preprocessed JSON
    try:
        parsed = json.loads(preprocessed)
        # If parsing works, return immediately
        return True, parsed
    except json.JSONDecodeError as error:
        # We'll attempt to fix the JSON below
        pass

    # STEP 2: Try to fix the JSON with heuristics
    try:
        fixed_string = preprocessed

        # 2a. Remove lingering triple backticks (edge case)
        fixed_string = re.sub(r'^```[a-zA-Z]*\s*', '', fixed_string)
        fixed_string = re.sub(r'\s*```$', '', fixed_string)

        # 2b. Fix missing commas between lines that appear to have valid JSON pairs
        lines = fixed_string.splitlines()
        for i in range(len(lines) - 1):
            current_line = lines[i].rstrip()
            next_line = lines[i + 1].lstrip()

            # If current line ends with a literal or true/false/null
            if (current_line.endswith('"') or 
                re.search(r'[0-9]$', current_line) or
                current_line.endswith('true') or 
                current_line.endswith('false') or
                current_line.endswith('null')):

                # And next line starts like a key or unquoted text that might be a key
                if (next_line.startswith('"') or re.match(r'^[a-zA-Z_]', next_line)):
                    # If there's no trailing comma, add it
                    if not current_line.endswith(','):
                        lines[i] = current_line + ','

        fixed_string = "\n".join(lines)

        # 2c. Add missing quotes around keys: from { key: "value" } to { "key": "value" }
        fixed_string = re.sub(r'([{,]\s*)([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'\1"\2":', fixed_string)

        # 2d. Remove trailing commas before closing braces/brackets
        fixed_string = re.sub(r',\s*([}\]])', r'\1', fixed_string)

        # 2e. Fix missing quotes around string values (somewhat simplistic)
        # e.g. : key -> : "key"
        fixed_string = re.sub(r':\s*([a-zA-Z0-9_][^{}\[\]"\',:}\]]*[a-zA-Z0-9_])', r': "\1"', fixed_string)

        # 2f. Replace undefined or NaN with null
        fixed_string = re.sub(r':\s*undefined', r': null', fixed_string)
        fixed_string = re.sub(r':\s*NaN', r': null', fixed_string)

        # 2g. Remove newlines inside string literals again
        fixed_string = remove_newlines_in_strings(fixed_string)

        # 2h. Balance braces/brackets if needed
        open_braces = fixed_string.count('{')
        close_braces = fixed_string.count('}')
        open_brackets = fixed_string.count('[')
        close_brackets = fixed_string.count(']')

        if open_braces > close_braces:
            fixed_string += '}' * (open_braces - close_braces)
        if open_brackets > close_brackets:
            fixed_string += ']' * (open_brackets - close_brackets)

        # Final attempt to parse
        parsed_fixed = json.loads(fixed_string)
        return True, parsed_fixed

    except Exception:
        # If we still fail, return parse_ok=False with no JSON
        return False, None


