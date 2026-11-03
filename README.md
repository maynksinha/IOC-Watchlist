# IOC Watchlist

A web application for security analysts to maintain a watchlist of **Indicators of Compromise (IOCs)**. Supports defanged input, automatic type detection, deduplication, tagging, and filtering.

Built with **FastAPI + SQLite** (backend) and **React 18 + Redux Toolkit** (frontend).

---

## Features

- Add IOCs — URLs, IPs, domains, MD5/SHA1/SHA256 hashes
- Automatic **type detection** and **defanging** (`hxxps://`, `[.]`, `[dot]`, etc.)
- **Deduplication** — same canonical form is rejected with a 409 and a reference to the original
- **Tags** — chip input, stored lowercase, filterable
- **Filter** by type and tag — table updates instantly via RTK Query cache invalidation
- **Delete** with confirmation
- REST API with OpenAPI docs at `/docs`
- SQLite persistence — zero setup, WAL mode

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12, FastAPI, SQLAlchemy 2 async, aiosqlite |
| Database | SQLite (WAL mode via aiosqlite) |
| Frontend | React 18, Vite, Redux Toolkit, Tailwind CSS |

---

## Local Development Setup

### Prerequisites

- Python 3.12+
- Node.js 20+
- Git

### 1 — Clone and enter the project

```bash
git clone <repo-url>
cd ioc-watchlist
```

### 2 — Backend setup

```bash
cd backend

# Create and activate virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
```

The default `.env` is ready to go for local dev — no changes needed.

### 3 — Start the backend

```bash
# From backend/ directory, with .venv active
uvicorn app.main:app --reload --port 8000
```

The database file (`data/ioc_watchlist.db`) is created automatically on first start via the lifespan hook — **no migration step required** for local dev.

Visit **http://localhost:8000/docs** for the interactive OpenAPI docs.

### 4 — Frontend setup

```bash
# In a separate terminal
cd frontend
npm install
npm run dev
```

Visit **http://localhost:5173** — the Vite dev server proxies `/api/*` requests to the backend automatically.


## API Reference

Base URL: `http://localhost:8000/api/v1`

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/iocs` | Create IOC |
| `GET` | `/iocs` | List IOCs (filterable, paginated) |
| `DELETE` | `/iocs/{id}` | Delete IOC |
| `GET` | `/tags` | List all tag names |
| `GET` | `/healthz` | Health check |

Full interactive docs: **http://localhost:8000/docs**

### POST /api/v1/iocs

```json
{
  "value": "hxxps://evil[.]com/login",
  "note": "seen in phishing email",
  "tags": ["phishing", "c2"]
}
```

Responses: `201` created · `400` invalid IOC · `409` duplicate · `422` validation error

### GET /api/v1/iocs

Query params: `type`, `tag`, `page` (default 1), `size` (default 50, max 200)

```
GET /api/v1/iocs?type=url&tag=phishing&page=1&size=20
```

---

### Data persistence

The SQLite database is stored at `./data/ioc_watchlist.db` on your host machine (mounted into the container). It survives container restarts. Delete the `data/` folder to reset.

---

## Environment Variables

### Backend (`backend/.env`)

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `sqlite+aiosqlite:///./data/ioc_watchlist.db` | Database connection string |
| `APP_ENV` | `development` | `development` or `production` |
| `CORS_ORIGINS` | `http://localhost:5173` | Comma-separated allowed origins |

To switch to Postgres: `DATABASE_URL=postgresql+asyncpg://user:pass@host/dbname`

### Frontend (`frontend/.env`)

| Variable | Default | Description |
|---|---|---|
| `VITE_API_BASE_URL` | `` (empty) | API base URL — empty means same-origin (production). Set to `http://localhost:8000` only for standalone frontend dev without the Vite proxy. |

---

## IOC Engine

### Defanging (input normalization)

Defanged IOCs are automatically refanged before processing:

| Input | Output |
|---|---|
| `hxxps://evil.com` | `https://evil.com` |
| `evil[.]com` | `evil.com` |
| `evil[dot]com` | `evil.com` |
| `http[s]://evil.com` | `https://evil.com` |
| `user[@]evil.com` | `user@evil.com` |

### Type detection (priority order)

1. `md5` — exactly 32 hex chars
2. `sha1` — exactly 40 hex chars
3. `sha256` — exactly 64 hex chars
4. `ipv4` — 4 octets 0–255, no leading zeros
5. `url` — starts with `http://`, `https://`, or `ftp://`
6. `domain` — labels separated by dots, valid TLD

Unrecognized input → `400 INVALID_IOC`

### Deduplication

IOCs are deduplicated by their **canonical form**:
- URL: lowercase scheme+host, path case preserved, fragment stripped, trailing root slash stripped
- Domain: lowercase, trailing dot stripped
- IPv4: trailing dot stripped
- Hashes: lowercase

---