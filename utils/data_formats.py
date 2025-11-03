from pydantic import BaseModel, Field
from typing import List

class ClassificationResult(BaseModel):
    folder_path: str
    new_folders: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)