from openai import OpenAI
import json
import os
import dotenv
dotenv.load_dotenv()

from data.schemas.text_schema import Text

def extract_json(raw: str) -> str:
    """Extract first valid JSON object from a raw LLM response."""
    start = raw.find("{")
    end = raw.rfind("}")
    if start == -1 or end == -1:
        raise ValueError(f"Model did not return JSON:\n{raw}")
    return raw[start:end+1]

def categorize_text(text: Text):
    package_raw = get_category(text)

    # sanitize & load JSON
    try:
        json_str = extract_json(package_raw)
        package = json.loads(json_str)
    except Exception as e:
        raise ValueError(f"Failed to parse categorizer JSON:\n{package_raw}") from e

    text.tags = package.get("tags", [])
    text.title = package.get("title", "")
    return text

def get_category(text: Text):
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content":
                (
                    "Respond ONLY with valid JSON. No markdown, no explanation.\n"
                    "{\n"
                    "  \"tags\": [\"tag1\", \"tag2\"],\n"
                    "  \"title\": \"A concise title summarizing the text\"\n"
                    "}"
                ),
            },
            {
                "role": "user",
                "content": f"Please categorize the following text:\n\n{text.content}",
            },
        ],
        temperature=0.0,
    )

    return response.choices[0].message.content.strip()