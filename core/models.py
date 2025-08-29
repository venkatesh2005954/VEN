from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class HistoryItem(BaseModel):
    id: str
    text_input: str  # original text
    text_styled: str  # transformed text (or same as input)
    voice: str
    tone: str
    style: str
    audio_path: str
    created_at: datetime
