from gpt4all import GPT4All

model_path = "models/TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf"
llm = GPT4All(model_path)

def run_llm(prompt: str):
    return llm.generate(prompt, max_tokens=512)
