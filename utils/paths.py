from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
AUDIO_DIR = DATA / "audio"
HISTORY_FILE = DATA / "history.json"

def ensure_dirs():
    DATA.mkdir(exist_ok=True)
    AUDIO_DIR.mkdir(exist_ok=True)
