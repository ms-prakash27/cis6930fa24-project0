import sqlite3
import os


def create_db():
    db_path = os.path.join(os.getcwd(), 'resources', 'normanpd.db')

    #Ensuring that the resources directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    #Deleting the database file if it exists
    if os.path.exists(db_path):
        os.remove(db_path)

    #Creating a new database connection
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    #Creating the incidents table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS incidents (
            incident_time TEXT,
            incident_number TEXT,
            incident_location TEXT,
            nature TEXT,
            incident_ori TEXT
        )
    ''')
    conn.commit()

    return conn


def populate_db(conn, incidents):
    cursor = conn.cursor()

    for incident in incidents:
        #Making sure the incident dictionary contains all necessary fields and handling missing data
        incident_time = incident.get('date_time', 'Unknown')
        incident_number = incident.get('incident_number', 'Unknown')
        location = incident.get('location', 'Unknown')
        nature = incident.get('nature', 'Unknown')
        incident_ori = incident.get('incident_ori', 'Unknown')

        cursor.execute('''
            INSERT INTO incidents (incident_time, incident_number, incident_location, nature, incident_ori)
            VALUES (?, ?, ?, ?, ?)
        ''', (incident_time, incident_number, location, nature, incident_ori))

    conn.commit()


