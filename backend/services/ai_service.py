import json

from sqlalchemy.orm import Session

from core.config import settings
from models.product import Product
from services.purchase_order_service import list_po_history
from services.product_service import get_low_stock_products, get_product_or_404


def _tool_get_low_stock_products(db: Session):
    rows = get_low_stock_products(db)
    return [{"id": p.id, "name": p.name, "sku": p.sku, "stock": p.stock, "threshold": p.threshold} for p in rows]


def _tool_get_product_detail(db: Session, product_id: int):
    product = get_product_or_404(db, product_id)
    return {"id": product.id, "name": product.name, "sku": product.sku, "stock": product.stock, "price": product.price}


def _tool_get_po_history(db: Session, product_id: int):
    history = list_po_history(db, product_id)
    return [
        {
            "po_id": po.id,
            "status": po.status.value,
            "total_amount": po.total_amount,
            "items": [{"product_id": i.product_id, "quantity": i.quantity} for i in po.items],
        }
        for po in history
    ]


def run_ai_chat(db: Session, message: str):
    tools = {
        "get_low_stock_products": lambda args: _tool_get_low_stock_products(db),
        "get_product_detail": lambda args: _tool_get_product_detail(db, int(args["product_id"])),
        "get_po_history": lambda args: _tool_get_po_history(db, int(args["product_id"])),
    }

    if not settings.openai_api_key:
        # Deterministic local fallback demonstrating tool routing
        lower = message.lower()
        if "low stock" in lower:
            result = tools["get_low_stock_products"]({})
            return "Fetched low-stock products from database.", {"get_low_stock_products": result}
        if "detail" in lower:
            product = db.query(Product).first()
            if not product:
                return "No products available.", {}
            result = tools["get_product_detail"]({"product_id": product.id})
            return "Fetched product detail from database.", {"get_product_detail": result}
        return "OpenAI key missing. Configure OPENAI_API_KEY for live tool-calling.", {}

    from openai import OpenAI

    client = OpenAI(api_key=settings.openai_api_key)
    tool_schema = [
        {
            "type": "function",
            "function": {
                "name": "get_low_stock_products",
                "description": "Return products at or below threshold",
                "parameters": {"type": "object", "properties": {}},
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_product_detail",
                "description": "Get product details by product_id",
                "parameters": {"type": "object", "properties": {"product_id": {"type": "integer"}}, "required": ["product_id"]},
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_po_history",
                "description": "Get PO history by product_id",
                "parameters": {"type": "object", "properties": {"product_id": {"type": "integer"}}, "required": ["product_id"]},
            },
        },
    ]

    first = client.chat.completions.create(
        model=settings.openai_model,
        messages=[{"role": "user", "content": message}],
        tools=tool_schema,
        tool_choice="auto",
    )

    tool_results = {}
    msg = first.choices[0].message
    messages = [{"role": "user", "content": message}, msg]
    for call in msg.tool_calls or []:
        args = json.loads(call.function.arguments or "{}")
        result = tools[call.function.name](args)
        tool_results[call.function.name] = result
        messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})

    second = client.chat.completions.create(model=settings.openai_model, messages=messages)
    return second.choices[0].message.content, tool_results
