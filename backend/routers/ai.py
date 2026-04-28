from pathlib import Path

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from core.deps import get_current_user
from db.session import get_db
from schemas.ai import AIChatRequest, AIChatResponse
from schemas.ocr import InvoiceParseResponse
from services.ai_service import run_ai_chat
from services.ocr_service import parse_invoice_with_fallback

router = APIRouter()


@router.post("/chat", response_model=AIChatResponse)
def ai_chat(payload: AIChatRequest, db: Session = Depends(get_db), _=Depends(get_current_user)):
    answer, tool_results = run_ai_chat(db, payload.message)
    return AIChatResponse(answer=answer, tool_results=tool_results)


@router.post("/invoice/parse", response_model=InvoiceParseResponse)
async def parse_invoice(file: UploadFile = File(...), _=Depends(get_current_user)):
    file_path = Path("backend/uploads") / file.filename
    file_path.write_bytes(await file.read())
    data = parse_invoice_with_fallback(file_path)
    return data
