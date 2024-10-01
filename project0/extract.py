import re
from PyPDF2 import PdfReader


def extract_incidents(incident_data):
    incidents = []
    try:
        pdf_reader = PdfReader(incident_data)
    except FileNotFoundError:
        print(f"File not found: {incident_data}")
        return incidents
    except Exception as e:
        print(f"An error occurred while reading the PDF: {e}")
        return incidents


    incident_pattern = re.compile(
        r'(?P<date_time>\d+/\d+/\d+ \d+:\d+)\s+'
        # r'^(?P<date_time>\d{1,2}/\d{1,2}/\d{4}\s\d{1,2}:\d{2})\s+'
        r'(?P<incident_number>\d{4}-\d{8})\s+'
        r'(?P<location>(?:\d+\s+)?[A-Z0-9 /()~!_\-;.+:&,]+?)'
        # r'(?:\s+(?=911\s)|(?=\s[A-Z][a-z]))\s*'
        r'(?:\s+(?=911\s|999\s|112\s|\*\*\*)|(?=\s[A-Z][a-z]))\s*'

        r'(?P<nature>.+?)\s+'
        r'(?P<incident_ori>[A-Z0-9]+)$'
    )


    for page in pdf_reader.pages:
        text = page.extract_text()
        if not text:
            continue
        rows = text.split('\n')

        for row in rows:
            if row.startswith('Date / Time'):
                continue
            match = incident_pattern.search(row.strip())
            if match:
                incident = {
                    "date_time": match.group("date_time"),
                    "incident_number": match.group("incident_number"),
                    "location": match.group("location").strip(),
                    "nature": match.group("nature").strip(),
                    "incident_ori": match.group("incident_ori")
                }
                incidents.append(incident)

    return incidents
