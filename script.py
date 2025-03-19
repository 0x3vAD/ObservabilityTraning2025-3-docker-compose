import argparse
import os
import psycopg2
import traceback

from dotenv import load_dotenv

load_dotenv("sample-env")

DB_USER  = os.getenv('POSTGRES_USER')
DB_PASS = os.getenv('POSTGRES_PASSWORD')
DB_NAME = os.getenv('POSTGRES_DB')
DB_HOST = os.getenv('POSTGRES_HOST')

if not all([DB_USER, DB_PASS, DB_NAME]):
    print("Missing environment variables for database connection.")
    exit(1)

def check_readiness():
    os.system(f"pg_isready -h {DB_HOST}")

def add_quote(cur, author, quote):
    cur.execute("INSERT INTO quotes (quote, author) VALUES (%s, %s)", (quote, author))
    print("Quote added successfully")

def get_random_quote(cur):
    cur.execute("SELECT quote, author FROM quotes ORDER BY RANDOM() LIMIT 1")
    quote, author = cur.fetchone()
    print("Random quote: %s - %s" % (quote, author))

    

try:
    check_readiness()
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cur = conn.cursor()

    parser = argparse.ArgumentParser(description="Quotes Database CLI")
    parser.add_argument("action", choices=["add", "random"], help="Action to perform: add or random")
    parser.add_argument("--author", help="Author of the quote")
    parser.add_argument("--quote", help="Quote to add")

    args = parser.parse_args()


    if args.action == "add":
        if not args.author or not args.quote:
            print("Author and quote are required for adding a quote")
        add_quote(cur, args.author, (args.quote,))

    elif args.action == "random":
        get_random_quote(cur)

    conn.commit()
    cur.close() 
    conn.close()

except Exception as e:
    print(traceback.format_exc(e))
    print("Unable to connect to the database")
