import json
from datetime import datetime
from typing import List
from .models import HistoryItem
from utils.paths import HISTORY_FILE, ensure_dirs


class HistoryRepo:
    def __init__(self):
        ensure_dirs()
        if not HISTORY_FILE.exists():
            HISTORY_FILE.write_text("[]", encoding="utf-8")

    def load(self) -> List[HistoryItem]:
        try:
            content = HISTORY_FILE.read_text(encoding="utf-8").strip()
            if not content:  # empty file
                return []
            data = json.loads(content)
            return [HistoryItem(**item) for item in data]
        except (json.JSONDecodeError, OSError):
            # Reset corrupted file
            HISTORY_FILE.write_text("[]", encoding="utf-8")
            return []

    def save_all(self, items: List[HistoryItem]) -> None:
        serial = [
            i.model_dump() | {"created_at": i.created_at.isoformat()} for i in items
        ]
        HISTORY_FILE.write_text(json.dumps(serial, indent=2), encoding="utf-8")

    def insert_top(self, item: HistoryItem) -> List[HistoryItem]:
        items = self.load()
        items.insert(0, item)
        self.save_all(items)
        return items

    def clear(self):
        self.save_all([])
