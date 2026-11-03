# IOC Watchlist — Backend

FastAPI backend to ingest, normalize, tag, and query Indicators of Compromise.

---

## Folder Structure

```
backend/
├── run.py                        # Entry point — uvicorn run:app --reload - create_app(): function
├── requirements.txt
├── .env                          # Local config (gitignored)
├── .env.example                  # Template — copy to .env and fill in values
│
└── app/
    ├── constants.py              # All enums: IOCType, TableName, APIPrefix, ErrorCode, Env, EnvFilePath
    │
    ├── connections/
    │   ├── env_config.py         # Loads .env → exposes DATABASE_URL, HOST, PORT, IS_PROD, etc.
    │   └── database.py           # SQLAlchemy engine, Base, get_db
    │
    │
    ├── schemas/                  # Pydantic I/O contracts
    │   ├── ioc.py
    │   └── response.py
    │
    ├── repositories/             # Raw DB queries — no business logic
    │   ├── ioc_repository.py
    │   └── tag_repository.py
    │
    ├── services/                 # Business logic
    │   ├── ioc_service.py
    │   └── tag_service.py
    │
    ├── controllers/              # FastAPI routers — HTTP layer
    │   ├── health_controller.py  # GET /healthz
    │   ├── ioc_controller.py     # POST · GET · DELETE /api/v1/iocs
    │   └── tag_controller.py     # GET /api/v1/tags
    │
    ├── exceptions/
    │   ├── custom_exceptions.py  # CustomAPIException(message, error_code, status_code)
    │   └── handlers.py           # api_exception_handler — single handler for all errors
    │
    └── utils/
        ├── logger.py             # Loguru logger — import everywhere: from app.utils.logger import logger
        └── ioc_engine/           # Pure IOC normalization logic (no DB)
            └── defang.py         # defang input
            └── detectors.py      # detect_type
            └── engine.py         # canonicalize · normalize_and_detect
```

---

## Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
cp .env.example .env
```

---

## Run

```bash
uvicorn run:app --reload      # development
python run.py                  # reads HOST / PORT / ENV from .env
uvicorn run:app --host 0.0.0.0 --port 8000 --workers 4  # production (not SQLite)
```

Docs: `http://localhost:8000/docs`

---

## API

| Method   | Path                  | Description              |
|----------|-----------------------|--------------------------|
| `GET`    | `/healthz`            | Health check             |
| `POST`   | `/api/v1/iocs`        | Ingest an IOC            |
| `GET`    | `/api/v1/iocs`        | List / filter IOCs       |
| `DELETE` | `/api/v1/iocs/{id}`   | Delete an IOC            |
| `GET`    | `/api/v1/tags`        | List all tags            |

Query params for `GET /api/v1/iocs`: `type`, `tag`, `page`, `size` (max 200).

---

## IOC Types

`md5` · `sha1` · `sha256` · `ipv4` · `domain` · `url`

Defanged formats are normalized on ingest — `hxxps://evil[.]com` → `https://evil.com`.
