from openai import OpenAI
import json
from pathlib import Path
import os
import dotenv
dotenv.load_dotenv()

from data.schemas.session_schema import Session

def get_file_path(session: Session):
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content":
                (
                    """
                    Return only a string of the file path of where this session should be saved.
                    The root of the path should be notes/. Use forward slashes.
                    The path should be based on the content of the session.
                    Here is the current folder structure of notes/:
                    {folder_tree}
                    """
                ),
            },
            {
                "role": "user",
                "content": f"Please categorize the following text:\n\n{session.get_all()}",
            },
        ],
        temperature=0.0,
    )

    return response.choices[0].message.content.strip()

def get_folder_tree(root: str):
    root_path = Path(root)

    def build_tree(path: Path):
        return {
            "name": path.name,
            "path": path,
            "children": [
                build_tree(child)
                for child in sorted(path.iterdir())
                if child.is_dir()
            ]
        }

    return build_tree(root_path)
