from pydantic import BaseModel
from typing import Optional, List

class TextInput(BaseModel):
    text: str
    summary_type: str
    groq_api_key: str

class SummaryResponse(BaseModel):
    summary: str
    summary_id: str

class SummaryItem(BaseModel):
    id: str
    type: str
    title: str
    created_at: str

class UserSummariesResponse(BaseModel):
    summaries: List[SummaryItem]