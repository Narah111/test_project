# tests/integration/conftest.py

import pytest
import os
import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv

load_dotenv(".env.test")

print("[DEBUG] Loaded DB config:", {
    "DB_HOST": os.getenv("DB_HOST"),
    "DB_NAME": os.getenv("DB_NAME")
})

from main import app
from db import add_visit,get_visit_by_id

def ensure_test_db_exists():
    try:
        conn = psycopg2.connect(
            dbname="postgres",  
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM pg_database WHERE datname = 'test_db'")
        if not cur.fetchone():
            cur.execute("CREATE DATABASE test_db")
            print("[INFO] Created test_db")
        cur.close()
        conn.close()
    except OperationalError as e:
        raise RuntimeError(f"[ERROR] Could not connect to PostgreSQL. Check your .env.test settings.\nDetails:\n{e}")


def init_visits_table():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS visits (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP NOT NULL,
            ip TEXT NOT NULL,
            user_agent TEXT NOT NULL
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()


def truncate_visits_table():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()
    cur.execute("TRUNCATE visits RESTART IDENTITY;")
    conn.commit()
    cur.close()
    conn.close()


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    ensure_test_db_exists()
    init_visits_table()
    yield


@pytest.fixture(autouse=True)
def clean_visits():
    truncate_visits_table()


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def visits():
    truncate_visits_table()
    
    add_visit("172.18.0.1","Mozilla/5.0")
    add_visit("172.18.0.1","Mozilla/5.0")
    add_visit("172.18.0.1","Mozilla/5.0")

@pytest.fixture
def singel_visit_with_id():
    truncate_visits_table()
    
    ip="172.18.0.1"
    user_agent="Mozilla/5.0"
    new_visit = add_visit(ip, user_agent)
    return get_visit_by_id(new_visit["id"])   