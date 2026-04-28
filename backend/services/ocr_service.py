import json
from pathlib import Path


def parse_invoice_with_fallback(file_path: Path) -> dict:
    # Production systems should use OCR engines (Textract/Vision/Tesseract).
    # For demo: parse JSON-like text when available.
    content = file_path.read_text(errors="ignore")
    try:
        data = json.loads(content)
        return {
            "supplier": data.get("supplier", "Unknown Supplier"),
            "items": data.get("items", []),
            "total": float(data.get("total", 0)),
        }
    except json.JSONDecodeError:
        return {
            "supplier": "Unknown Supplier",
            "items": [{"name": "Unparsed Item", "quantity": 1, "unit_price": 0.0}],
            "total": 0.0,
        }
