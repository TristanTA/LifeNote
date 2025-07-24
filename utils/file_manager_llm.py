from llama_cpp import Llama

LLM_PATH = "models/TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf"
llm = Llama(model_path=LLM_PATH, n_threads=8, n_ctx=4096)

def run_llm(prompt: str) -> str:
    out = llm(prompt, max_tokens=512, stop=["</s>"])
    return out["choices"][0]["text"].strip()