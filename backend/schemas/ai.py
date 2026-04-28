from pydantic import BaseModel


class AIChatRequest(BaseModel):
    message: str


class AIChatResponse(BaseModel):
    answer: str
    tool_results: dict
