# tests/integration/conftest.py

import pytest
import os
import psycopg2
from dotenv import load_dotenv


load_dotenv(".env.test")


from main import app


def ensure_test_db_exists():

    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
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


