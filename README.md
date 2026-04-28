# SmartStore AI — Intelligent Inventory & Vendor Management System

Production-oriented full-stack project with AI-assisted inventory and vendor workflows.

## 1) Folder Structure

```text
smartAi/
├── backend/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   ├── uploads/
│   ├── main.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── pages/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── store/
│   │   └── utils/
│   ├── package.json
│   └── .env.example
└── README.md
```

## 2) Backend (FastAPI + SQLAlchemy + JWT)

### Features
- RESTful routers for auth, products, suppliers, purchase orders, AI, and health.
- Pydantic v2 request/response schema separation.
- SQLAlchemy ORM relationships for product/supplier/PO domain.
- JWT access token auth + refresh endpoint.
- Role model (`Admin`, `Staff`) in user entity.
- Global error handlers for validation and unexpected exceptions.

### Key Endpoints
- `POST /auth/register`, `POST /auth/login`, `POST /auth/refresh`
- `GET|POST|PUT|DELETE /products`
- `GET /products/{id}/forecast` (moving average)
- `GET|POST|PUT|DELETE /suppliers`
- `POST /purchase-orders`, `GET /purchase-orders`, `PATCH /purchase-orders/{id}/status`
- `POST /ai/chat` (LLM tool-calling)
- `POST /ai/invoice/parse` (OCR parser demo)

## 3) Frontend (React + Zustand + Tailwind)

### Features
- Route protection with redirect to `/login` for unauthenticated users.
- Zustand auth store to avoid prop drilling.
- API services using Axios with auth interceptor.
- Reusable components (`Layout`, `ApiState`, `ProductForm`).
- Client-side validation for login/product forms.
- Responsive layout for tablet/desktop targets (768px and 1440px containers).

## 4) AI Integration (Tool/Function Calling)

`/ai/chat` supports these tools:
- `get_low_stock_products`
- `get_product_detail`
- `get_po_history`

Behavior:
- Tool functions query **real DB data**.
- If `OPENAI_API_KEY` is configured, endpoint executes OpenAI function-calling workflow.
- Without key, it uses deterministic fallback that still routes through DB tool handlers.

## 5) Automation (APScheduler)

Background daily cron job:
- checks low-stock products
- creates draft purchase orders using default supplier
- writes automation logs (`automation_logs` table)

Configured in `services/scheduler_service.py` and started from app lifespan.

## 6) Run Locally

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

## Production Notes
- Replace SQLite with PostgreSQL by setting `DATABASE_URL`.
- Add Alembic migrations for versioned schema changes.
- Enforce stricter RBAC in routers using `require_admin` dependency.
- Integrate real OCR provider for invoices.
- Store refresh tokens in DB/redis with rotation and revocation.
