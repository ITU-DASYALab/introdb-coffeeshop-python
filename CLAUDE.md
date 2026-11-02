# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project purpose

A teaching project for an intro-to-databases course: a small coffee shop web app with a FastAPI + DuckDB backend and a static HTML/JS frontend. Several endpoints in `app.py` are intentionally left as `# TODO` stubs (`/register`, `/mypurchases`, `/purchase`) for students to implement with SQL. Don't fill them in unless asked to.

The app is intentionally simplistic about security, since the course is about SQL, not auth: passwords are stored in plaintext, the "access token" is just the username, and some pages render API data via `innerHTML` (the escaped version is left commented out next to it). Don't treat these as bugs to fix unless the task is about them.

## Commands

```bash
pip install -r requirements.txt          # pinned deps: fastapi, duckdb, uvicorn, click, pydantic, urllib3
duckdb coffee.db < init.sql              # (re)create the database; init.sql drops and recreates all tables with seed data
python app.py coffee.db                  # API server on http://localhost:8000 (no auto-reload; restart after editing app.py)
cd web && python -m http.server 8080     # frontend on http://localhost:8080
```

Both servers must run at the same time. There are no tests, linter, or build step.

## Architecture

- **Backend (`app.py`)**: one FastAPI module. `run_server` is a `click` command that stores the DB path in the module-level `CONNECTION` global and starts uvicorn on a hardcoded `localhost:8000`. Each endpoint opens its own short-lived `duckdb.connect(CONNECTION, ...)` (`read_only=True` for queries), runs parameterized SQL (`?` placeholders), and converts results with `convert_rows_to_dicts(rows, columns)` using column names from `conn.description`. Write endpoints need a non-read-only connection. CORS allows all origins.
- **Schema (`init.sql`)**: three tables: `user(username PK, email, password)`, `product(productname PK, price, description)`, `purchase(purchasetime, productname, username)` with a composite PK. Note `/products` aliases `productname` as `name` because the frontend expects that.
- **Frontend (`web/`)**: plain HTML pages with inline `<script>` blocks, sharing helpers from `web/app.js`. `API_BASE` is hardcoded to `http://localhost:8000`. After login, the token (the username) lives in `sessionStorage`, and pages send it as the `username` field or query param (e.g. `/mypurchases?username=<token>`, `POST /purchase {username, productname}`). Elements marked `data-authed` / `data-guest` are toggled by `setAuthUI()`. The purchase tables accept several field-name variants (`username ?? user`, `purchasetime ?? timestamp`), but the backend should return the schema's column names.
