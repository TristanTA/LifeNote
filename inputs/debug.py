import random

SAMPLE_NOTES = [
    "Meeting notes: Discussed LifeNotes architecture. Need SQLite schema for notes, resources, and user preferences.",
    "Idea: Add semantic search so old notes surface automatically when related topics appear.",
    "Reminder: Buy groceries after class. Eggs, spinach, gluten-free bread.",
    "Project thought: Could use Whisper for transcription and DistilBART for summarization.",
    "Observation: Productivity improves when tasks are written as small actionable steps.",
    "Research note: Retrieval-augmented generation improves factual consistency of LLM outputs.",
    "Daily log: Worked on LifeNotes UI and tested note recording pipeline.",
    "Concept: Link audio notes to text summaries and allow playback from the search results.",
    "Todo: Review API token usage and optimize model calls.",
    "Random idea: Notes system could track themes in thinking over time."
]


def get_debug_note():
    """Return a random sample note."""
    return random.choice(SAMPLE_NOTES)