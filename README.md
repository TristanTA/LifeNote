# LifeNote

Local-first note capture + lightweight organization.

## What this repo contains
- `main.py`: Streamlit entrypoint (calls the UI)
- `app/ui/`: Streamlit UI components
- `data/`: local data + schemas/managers
- `models/`: NLP/ASR helpers (Whisper/BERT/etc.)

## Requirements
- Python 3.10+ recommended

## Setup
```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## Run
```bash
streamlit run main.py
# or
python run_app.py
```

## Notes on data
This project stores local data under `data/` (including a sqlite DB). If you intend to keep your personal data out of git, consider adding additional ignore rules and/or moving the DB outside the repo.

## License
No license file is currently included. If you want this to be open source, add a `LICENSE` (MIT/Apache-2.0/etc.).
