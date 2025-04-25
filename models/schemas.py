from pydantic import BaseModel

class TextInput(BaseModel):
    text: str
    summary_type: str
    groq_api_key: str

class SummaryResponse(BaseModel):
    summary: str
    summary_id: str