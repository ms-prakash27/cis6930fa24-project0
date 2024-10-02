import os
import sqlite3
import pytest
from project0 import db  # Import the db module directly instead of specific functions
from project0.extract import extract_incidents

dbname = "normanpd.db"
tablename = "incidents"


@pytest.fixture
def setup_database():
    """Fixture to create a database and return its connection."""
    conn = db.create_db()  # Access the function through the module
    yield conn
    conn.close()
    # Clean up database after test
    db_path = os.path.join(os.getcwd(), 'resources', dbname)
    if os.path.exists(db_path):
        os.remove(db_path)


def test_createdb(setup_database):
    conn = setup_database

    # Check if the incidents table exists
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (tablename,))
    assert cursor.fetchone(), "The incidents table was not created."

    # Check if the table has exactly 5 columns
    cursor.execute(f'PRAGMA table_info({tablename})')
    columns = cursor.fetchall()
    assert len(columns) == 5, "The incidents table does not have the expected number of columns."


def test_populate_db(setup_database):
    conn = setup_database

    # Path to the local PDF file in the resources directory
    test_pdf_path = "tests/test_incidents.pdf"

    # Extract data from the local test PDF
    extracted_data = extract_incidents(test_pdf_path)

    # Populate the database with extracted data
    db.populate_db(conn, extracted_data)  # Access the function through the module

    # Check if table is not empty
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {tablename}")
    rows = cursor
