def print_status(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT nature, COUNT(*) FROM incidents GROUP BY nature ORDER BY nature ASC')

    rows = cursor.fetchall()
    for row in rows:
        print(f"{row[0]}|{row[1]}")
