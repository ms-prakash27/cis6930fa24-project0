import sqlite3
import os

def create_db():
    db_path = os.path.join(os.getcwd(), 'resources', 'normanpd.db')

    # Ensure the resources directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Delete the database file if it exists
    if os.path.exists(db_path):
        os.remove(db_path)

    # Create a new database connection
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create incidents table
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
    print(f"Database created at: {os.path.abspath(db_path)}")  # Print the full path for debugging
    return conn


def populate_db(conn, incidents):
    cursor = conn.cursor()
    for incident in incidents:
        cursor.execute('''
            INSERT INTO incidents (incident_time, incident_number, incident_location, nature, incident_ori)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            incident['date_time'],
            incident['incident_number'],
            incident['location'],
            incident['nature'],
            incident['incident_ori']
        ))
    conn.commit()
    print('Populated the database with incidents.')


# Example usage:
if __name__ == "__main__":
    conn = create_db()
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
    populate_db(conn, incidents_data)
    conn.close()
