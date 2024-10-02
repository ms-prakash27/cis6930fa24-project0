from project0 import db
import os
import sqlite3

def test_create_db():
    #Creating a new database
    conn = db.create_db()

    #Checking if the database file is created
    db_path = os.path.join(os.getcwd(), 'resources', 'normanpd.db')
    assert os.path.exists(db_path)

    #Verifying that the table is correctly created
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='incidents';")
    table = cursor.fetchone()
    assert table is not None

    #Cleaning up
    conn.close()
    os.remove(db_path)

def test_populate_db():
    #Creating a database connection
    conn = db.create_db()

    # Sample incidents data
    sample_incidents = [
        {
            "date_time": "01/01/2024 08:00",
            "incident_number": "2024-00000001",
            "location": "123 Main St",
            "nature": "Alarm",
            "incident_ori": "OK0140200"
        }
    ]

    #Populate the database with sample data
    db.populate_db(conn, sample_incidents)

    # Query the database to ensure data is inserted
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM incidents")
    rows = cursor.fetchall()

    assert len(rows) == 1
    assert rows[0][0] == "01/01/2024 08:00"
    assert rows[0][1] == "2024-00000001"
    assert rows[0][2] == "123 Main St"
    assert rows[0][3] == "Alarm"
    assert rows[0][4] == "OK0140200"

    # Clean up
    conn.close()
    os.remove(os.path.join(os.getcwd(), 'resources', 'normanpd.db'))
