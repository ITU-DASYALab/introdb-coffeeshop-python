Coffeeshop Web App in Python using DuckDB.

# Installation

Install Python if you have not done so already.

Personal recommendation is to use a venv or environment manager such as uv or poetry, 
but if you are ok with just using your global python installation that is up to you.


## Requirements

From the root directory run the following command to install the requirements:

```bash
pip install -r requirements.txt
```

## Create the database file

Create a `coffee.db` file and execute the statements in `init.sql` using DuckDB:

```bash
duckdb coffee.db < init.sql
```

# How to start the project

To run this application you need to start two terminals, one for the web frontend, and one for the python API server.

## Terminal 1: Web Frontend Server

Go to the web folder via a terminal and start the web server on port 8080 (If that one is in use by your system use another such as 5000, 5001, etc.)
```bash
cd web
python -m http.server 8080
```

This starts an HTTP server on http://localhost:8080. 
In other words the contents of the folder are accessible from that URL, and since there is an index.html inside the folder it dictates the web interface.


## Terminal 2: Python API Server



### Start the server
Now you can start the API server, which takes a database file as argument such as `coffee.db`.
```bash
python app.py <db-file>
```
It always starts the server on port 8000, if you want to change this do it in the function `run_server()` in `app.py`.


**Remember to restart the Python server after making changes in app.py.**
