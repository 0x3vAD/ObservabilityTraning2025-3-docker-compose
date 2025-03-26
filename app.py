import fastapi
import os
import psycopg2
import subprocess
import traceback

from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

load_dotenv("sample-env")

DB_USER  = os.getenv('POSTGRES_USER')
DB_PASS = os.getenv('POSTGRES_PASSWORD')
DB_NAME = os.getenv('POSTGRES_DB')
DB_HOST = os.getenv('POSTGRES_HOST')

if not all([DB_USER, DB_PASS, DB_NAME, DB_HOST]):
    print("Missing environment variables for database connection.")
    exit(1)

class QuoteModel(BaseModel):
    quote: str
    author: str

app = fastapi.FastAPI()

def connect_to_db():
    global cur, conn
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        conn.autocommit = True
        print("Connected to PostgreSQL successfully!")
        return conn
    except KeyboardInterrupt:
        conn.close()
    except psycopg2.OperationalError as e:
        print(traceback.format_exc(e))

@app.get("/health")
def check_readiness():
    result = subprocess.run(["pg_isready", "-h", DB_HOST], stdout=subprocess.PIPE)
    response = result.stdout.decode().split("-")[1].strip()
    if response == "no response":
        conn.close()
        raise fastapi.HTTPException(status_code=404)
    elif response == "accepting connections" and conn.closed:
        connect_to_db()
    return response

@app.post("/add_quote")
async def add_quote(quote: QuoteModel):
    cur.execute("INSERT INTO quotes (quote, author) VALUES (%s, %s)", (quote.quote, quote.author))
    conn.commit()
    return {"message": "Quote added successfully"}

@app.get("/get_quote")
async def get_random_quote():
    cur.execute("SELECT quote, author FROM quotes ORDER BY RANDOM() LIMIT 1")
    return cur.fetchone()


if __name__ == "__main__":
    connect_to_db()