# -*- coding: utf-8 -*-
import argparse
import fetch
import extract
import db
import status


def main(url):
    # Step 1: Downloading the data
    incident_data = fetch.fetch_incidents(url)

    # Step 2: Extracting the data
    incidents = extract.extract_incidents(incident_data)

    # Step 3: Creating a new database
    database = db.create_db()

    # Step 4: Inserting  data into the database
    db.populate_db(database, incidents)

    # Step 5: Printing incident counts
    status.print_status(database)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, help="Incident summary URL.")

    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)
