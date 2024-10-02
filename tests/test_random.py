import os
import sqlite3
import pytest
from project0 import db
from project0.extract import extract_incidents

dbname = "normanpd.db"
tablename = "incidents"


@pytest.fixture
def setup_database():
    conn = db.create_db()
    yield conn
    conn.close()
    #cleaning the database after testing
    db_path = os.path.join(os.getcwd(), 'resources', dbname)
    if os.path.exists(db_path):
        os.remove(db_path)


def test_createdb(setup_database):
    conn = setup_database

    #checking if the incidents table exists or not
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (tablename,))
    assert cursor.fetchone(), "The table incidents was not created."

    #checking if the table has exactly 5 columns or not
    cursor.execute(f'PRAGMA table_info({tablename})')
    columns = cursor.fetchall()
    assert len(columns) == 5, "The table incidents does not have the expected number of columns."


def test_populate_db(setup_database):
    conn = setup_database
    test_pdf_path = "tests/test_normanpd.pdf"
    extracted_data = extract_incidents(test_pdf_path)

    #populating the database with extracted data
    db.populate_db(conn, extracted_data)

    #checking if the table empty or not
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {tablename}")
    rows = cursor
