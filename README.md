<p align="center">
  <img src="web/coffeeshop-logo.png" alt="Coffee Shop logo" width="200">
</p>

# Coffee Shop (Python)

A small web app for a coffee shop. It's used in ITU's *Introduction to Database Systems* course. Users can register, log in, browse products, buy drinks, and see the purchase history. The backend is a Python API built with [FastAPI](https://fastapi.tiangolo.com) that talks to a [DuckDB](https://duckdb.org) database. The frontend is a set of static HTML pages that call this API.

## Quick start

You need **Python 3.11+**, **Git**, and the **DuckDB CLI**. The commands below are for Linux, macOS, and the Windows Subsystem for Linux (WSL). If you use PowerShell or Command Prompt, please ask your teaching assistant.

```bash
git clone git@github.com:ITU-DASYALab/introdb-coffeeshop-python.git
cd introdb-coffeeshop-python
python3 -m venv .venv               # create a virtual environment
source .venv/bin/activate           # activate it (repeat in every new terminal)
pip install -r requirements.txt     # install the dependencies
duckdb coffee.db < init.sql         # create the database
```

The app has two parts, and each one needs its own terminal:

```bash
# Terminal 1: the API server on http://localhost:8000
source .venv/bin/activate
python app.py coffee.db

# Terminal 2: the web frontend on http://localhost:8080
cd web
python3 -m http.server 8080
```

Then open [http://localhost:8080](http://localhost:8080). You can log in as `Anna`, `Martin`, or `Omar`; all three have the password `test`.

If port 8080 is already in use, pick another port for the frontend, such as 5000. The API server always runs on port 8000, because the frontend expects it there (see `API_BASE` in `web/app.js`).

The API server doesn't reload by itself, so **restart it after every change to `app.py`**. To reset the database, run `duckdb coffee.db < init.sql` again. It drops and recreates all tables. While you have `coffee.db` open in the DuckDB CLI, the API server can't open it, so close the CLI (`.quit`) before you use the app.

<details>
<summary>Installing the prerequisites</summary>

```bash
sudo apt install python3 python3-venv git   # Python, venv, Git (Debian/Ubuntu/WSL)
curl https://install.duckdb.org | sh        # DuckDB CLI
```

</details>

## Your tasks

Three functions in `app.py` are left for you to implement. They are marked with `# TODO`:

| Function | Route | What it should do |
|---|---|---|
| `insert_user` | `POST /register` | Insert a newly registered user |
| `insert_purchase` | `POST /purchase` | Insert a purchase with the current timestamp |
| `get_user_purchases` | `GET /mypurchases` | Return one user's purchases, newest first |

Look at the functions that are already done, such as `login` and `get_all_purchases`, and follow the same pattern. Whenever a query includes user input, use `?` placeholders and pass the values as a list. Don't put the values into the SQL string yourself. The two insert functions change the database, so they can't open the connection with `read_only=True`.

## How the app works

The backend is in [`app.py`](app.py). Every endpoint opens its own connection to DuckDB, runs one query, and returns the result as JSON. `convert_rows_to_dicts` turns the result rows into a list of dictionaries, using the column names as keys. The request bodies are described by the Pydantic classes `Login`, `Registration`, and `PurchaseRequest` at the top of the file.

The frontend is in [`web/`](web). Each page uses `fetch` to call the API, with helper functions from [`web/app.js`](web/app.js). After login, the browser keeps the username in `sessionStorage` and sends it to the API whenever it's needed, for example when buying a product.

| Route | Description |
|---|---|
| `GET /products` | All products |
| `GET /purchases` | All purchases |
| `GET /mypurchases?username=...` | One user's purchases |
| `POST /login`, `POST /register` | Log in and register |
| `POST /purchase` | Buy a product |

While the API server is running, you can try every route in your browser at [http://localhost:8000/docs](http://localhost:8000/docs).

## Database

The schema and sample data are in [`init.sql`](init.sql):

```
user(username PK, email, password)
product(productname PK, price, description)
purchase(purchasetime, productname, username)   -- PK: all three columns
```
