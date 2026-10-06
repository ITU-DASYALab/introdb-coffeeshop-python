from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
from urllib3 import HTTPResponse
import duckdb
import click
import uvicorn
from datetime import datetime

class Login(BaseModel):
    username: str
    password: str

class Registration(BaseModel):
    username: str
    password: str
    email: str

class PurchaseRequest(BaseModel):
    username: str
    productname: str

origins = ["*"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

CONNECTION = ""

def convert_rows_to_dicts(rows, columns):
    data = []
    for row in rows:
        instance = {}
        for i, column in enumerate(columns):
            instance[column] = row[i]
        data.append(instance)
    return data 
    # Shorter and faster version:
    # return [dict(zip(columns,row)) for row in rows]

@app.post("/login")
def login(info: Login):
    """
    Returns a token if the user exists in the database
    ### Parameters
    login: Login
        The login information
    ### Returns
    dict:
        A dictionary with the access token and token type if the user exists, otherwise an empty dictionary
    """
    conn = None
    try:
        conn = duckdb.connect(CONNECTION, read_only=True)
        conn.execute(
            "select * from user where username = ? and password = ?",
            [info.username, info.password]
        )
        if conn.fetchone() is not None:
            return {'access_token': info.username, 'token_type': 'bearer'}
        else:
            return {}
    except duckdb.Error as e:
        print(e)
        return HTTPException(400, detail=e)
    finally:
        if conn is not None:
            conn.close()


@app.get("/products")
def get_products():
    """
    Returns all products in the database
    ### Returns
    list:
        A list of dictionaries with the product information
    """
    try:
        with duckdb.connect(CONNECTION, read_only=True) as conn:
            rows = conn.execute(
                "select productname as name, price, description from product"
            ).fetchall()
            columns = [desc[0] for desc in conn.description]
            return convert_rows_to_dicts(rows, columns)
    except duckdb.Error as e:
        print(e)
        return HTTPException(400, detail=e)


@app.post("/register")
def insert_user(new_user: Registration):
    """
    Inserts a new user into the database
    ### Parameters
    new_user: Registration
        The new user information
    ### Returns
    HTTPResponse:
        A HTTP response with status code 200 if the user was inserted successfully,
        otherwise a HTTP exception with status code 400
    """
    try:
        # TODO: insert the new user into the database
        return HTTPResponse(status=200)
    except duckdb.DataError as e:
        print(e)
        return HTTPException(400, detail=e)


@app.get("/purchases")
def get_all_purchases():
    """
    Returns all purchases for a given user
    ### Parameters
    session: str
        The username of the user
    ### Returns
    list:
        A list of dictionaries with the purchase information
    """
    try:
        with duckdb.connect(CONNECTION, read_only=True) as conn:
            rows = conn.execute(
                "select * from purchase", 
            ).fetchall()
            columns = [desc[0] for desc in conn.description]
            return convert_rows_to_dicts(rows, columns)
    except duckdb.Error as e:
        print(e)
        return HTTPException(400, detail=e)


@app.get("/mypurchases")
def get_user_purchases(username: str):
    """
    Returns all purchases for a given user
    ### Parameters
    session: str
        The username of the user
    ### Returns
    list:
        A list of dictionaries with the purchase information 
        (You can use convert_rows_to_dicts to do this. See get_all_purchases for an example)
    """
    try:
        # TODO: query the database for purchases by this user ordered by time descending,
        # and populate the purchases list
        return []
    except duckdb.Error as e:
        print(e)
        return HTTPException(400, detail=e)


@app.post("/purchase")
def insert_purchase(purchase: PurchaseRequest):
    """
    Inserts a new purchase into the database
    ### Parameters
    purchase: PurchaseRequest
        The purchase information
    ### Returns
    HTTPResponse:
        A HTTP response with status code 200 if the purchase was inserted successfully,
        otherwise a HTTP exception with status code 400
    """
    try:
        # TODO: insert the new purchase into the database
        return HTTPResponse(status=200)
    except duckdb.Error as e:
        print(e)
        return HTTPException(400, detail=e)


@click.command()
@click.argument('db_file', type=Path)
def run_server(db_file):
    """
    Starts the server on localhost port 8000
    ### Parameters:
    db_file: str
        The database config file
    """
    global CONNECTION
    CONNECTION = db_file
    uvicorn.run(app, host="localhost", port=8000)


if __name__ == "__main__":
    run_server()
