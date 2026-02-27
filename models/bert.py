from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class Summarizer:
    """DistilBART-based text summarizer with simple token chunking."""

    def __init__(self, debug: bool = False):
        """Initialize tokenizer + model.

        Args:
            debug: If True, prints minimal debug logs.
        """
        self.debug = debug
        model_name = "sshleifer/distilbart-cnn-12-6"

        if self.debug:
            print(f"[DEBUG] Initializing summarizer model={model_name}")

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

        if self.debug:
            print("[DEBUG] Summarizer initialized")

    def summarize(self, input_text: str, token_limit: int = 1024) -> str:
        """Summarize input_text into concise bullet points.

        If the input exceeds token_limit, it is chunked and summarized chunk-by-chunk,
        then the merged summaries are summarized again.

        Args:
            input_text: Text to summarize.
            token_limit: Max input tokens allowed before chunking.

        Returns:
            Summary text.
        """
        token_count = self._token_count(input_text)

        if self.debug:
            print(f"[DEBUG] summarize(): token_count={token_count}, token_limit={token_limit}")

        if token_count > token_limit:
            if self.debug:
                print("[DEBUG] summarize(): over limit -> chunking")

            chunks = self.chunk(input_text)

            summaries = []
            for i, chunk in enumerate(chunks):
                if self.debug:
                    print(f"[DEBUG] summarize(): summarizing chunk {i + 1}/{len(chunks)}")
                summaries.append(self.summarize(chunk))

            merged = "\n".join(summaries)
            return self.summarize(merged)

        # Simple prompt steering: keep output as bullet points for note storage.
        bulleted_input = "Summarize into concise bullet points:\n" + input_text
        inputs = self.tokenizer(bulleted_input, return_tensors="pt", truncation=True)
        summary_ids = self.model.generate(**inputs)
        summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        return summary
    
    def _token_count(self, text: str) -> int:
        """Return number of tokens without truncation."""
        return len(self.tokenizer.encode(text, add_special_tokens=False))

    def chunk(self, input_text: str, max_tokens: int = 900, overlap: int = 100):
        """Split text into overlapping token chunks.

        Args:
            input_text: Text to split.
            max_tokens: Tokens per chunk.
            overlap: Tokens overlapped between adjacent chunks.

        Returns:
            List of decoded text chunks.
        """
        tokens = self.tokenizer(input_text, return_tensors="pt", truncation=False)["input_ids"][0]

        chunks = []
        start = 0
        total_tokens = len(tokens)

        if self.debug:
            print(f"[DEBUG] chunk(): total_tokens={total_tokens}, max_tokens={max_tokens}, overlap={overlap}")

        while start < total_tokens:
            end = min(start + max_tokens, total_tokens)
            chunk_tokens = tokens[start:end]
            chunk_text = self.tokenizer.decode(chunk_tokens, skip_special_tokens=True)
            chunks.append(chunk_text)

            if end == total_tokens:
                break

            # Sliding window overlap to reduce boundary loss.
            start = end - overlap

        if self.debug:
            print(f"[DEBUG] chunk(): produced_chunks={len(chunks)}")

        return chunks