# utils/classifier_llm.py
import json
from utils.llm import run_llm
from utils.prompts import CLASSIFY_PROMPT
from utils.data_formats import ClassificationResult
from utils.json_manager import load_index, iter_folders
from utils.embedding import FolderRetriever

def build_folder_retriever(index):
    pairs = list(iter_folders(index))
    retriever = FolderRetriever()
    retriever.build(pairs)
    return retriever, pairs

def select_candidate_folders(retriever, query, pairs, k=5):
    top = retriever.top_k(query, k=k)
    path_to_summary = {fp: summ for fp, summ in pairs}
    lines = []
    for path, score in top:
        summ = path_to_summary.get(path, "")
        lines.append(f"- {path}: \"{summ}\"")
    return "\n".join(lines)

def classify_with_llm(note_text: str):
    index = load_index()
    retriever, pairs = build_folder_retriever(index)

    candidates = select_candidate_folders(retriever, note_text, pairs, k=5)
    prompt = CLASSIFY_PROMPT.format(candidates=candidates, note_text=note_text)

    raw = run_llm(prompt)
    # try to find the JSON in the response
    try:
        start = raw.find("{")
        end = raw.rfind("}") + 1
        data = json.loads(raw[start:end])
        return ClassificationResult(**data)
    except Exception as e:
        # Fallback to misc
        return ClassificationResult(folder_path="Misc", tags=["unclassified"])