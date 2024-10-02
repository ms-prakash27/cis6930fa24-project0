# -*- coding: utf-8 -*-
import argparse
import fetch
import extract
import db
import status


def main(url):
    #Downloading the data
    incident_data = fetch.fetch_incidents(url)

    #Extracting the data
    incidents = extract.extract_incidents(incident_data)

    #Creating a new database
    database = db.create_db()

    #Inserting  data into the database
    db.populate_db(database, incidents)

    #Printing the counts of incidents
    status.print_status(database)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, help="Incident summary URL.")

    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)
