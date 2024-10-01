import os
import sqlite3
import pytest
from project0.db import create_db, populate_db


@pytest.fixture
def db_connection():
    # Create a test database connection
    conn = create_db()
    yield conn
    # Cleanup after the test
    conn.close()


def test_create_db(db_connection):
    cursor = db_connection.cursor()

    # Check if the table was created
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='incidents';")
    table = cursor.fetchone()

    assert table is not None, "Incidents table should exist."


def test_populate_db(db_connection):
    # Example incident data
    incidents_data = [
        {
            'date_time': '2024-01-01 12:00:00',
            'incident_number': '001',
            'location': 'Location A',
            'nature': 'Theft',
            'incident_ori': 'Officer 1'
        },
        {
            'date_time': '2024-01-02 13:30:00',
            'incident_number': '002',
            'location': 'Location B',
            'nature': 'Assault',
            'incident_ori': 'Officer 2'
        }
    ]

    # Populate the database with test data
    populate_db(db_connection, incidents_data)

    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM incidents;")
    rows = cursor.fetchall()

    assert len(rows) == 2, "There should be 2 rows in the database."
    assert rows[0][1] == '001', "First incident number should be '001'."
    assert rows[1][2] == 'Location B', "Second incident location should be 'Location B'."

    # Optionally, check other fields


def test_cleanup():
    db_path = '../resources/normanpd.db'
    if os.path.exists(db_path):
        os.remove(db_path)
