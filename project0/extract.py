# import re
# from pypdf import PdfReader
#
#
#
# def extract_incidents(incident_data):
#     incidents = []
#     try:
#         pdf_reader = PdfReader(incident_data)
#     except FileNotFoundError:
#         print(f"File not found: {incident_data}")
#         return incidents
#     except Exception as e:
#         print(f"An error occurred while reading the PDF: {e}")
#         return incidents
#     incident_pattern = re.compile(
#         r'(?P<date_time>\d+/\d+/\d+ \d+:\d+)\s+'
#         r'(?P<incident_number>\d{4}-\d{8})\s+'
#         r'(?P<location>(?:\d+\s+)?[A-Z0-9 /()~!_\-;.+:&,]+?)'
#         r'(?:\s+(?=911\s|999\s|112\s|\*\*\*|MVA|COP\s)|(?=\s[A-Z][a-z]))\s*'
#         r'(?P<nature>.+?)\s+'
#         r'(?P<incident_ori>(?:OK0140200|14005|EMSSTAT|14009))\s*$'
#     )
#
#     for page in pdf_reader.pages:
#         text = page.extract_text()
#         if not text:
#             continue
#         rows = text.split('\n')
#
#         for row in rows:
#             if row.startswith('Date / Time'):
#                 continue
#             match = incident_pattern.search(row.strip())
#             if match:
#                 incident = {
#                     "date_time": match.group("date_time"),
#                     "incident_number": match.group("incident_number"),
#                     "location": match.group("location").strip(),
#                     "nature": match.group("nature").strip(),
#                     "incident_ori": match.group("incident_ori")
#                 }
#
#                 incidents.append(incident)
#
#
#
#     return incidents

import re
from pypdf import PdfReader


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

    # Compile the pattern to match a complete incident line
    incident_pattern = re.compile(
        r'(?P<date_time>\d+/\d+/\d+ \d+:\d+)\s+'
        r'(?P<incident_number>\d{4}-\d{8})\s+'
        r'(?P<location>(?:\d+\s+)?[A-Z0-9 /()~!_\-;.+:&,\>\<]+?)'
        r'(?:\s+(?=911\s|999\s|112\s|\*\*\*|MVA|COP\s)|(?=\s[A-Z][a-z]))\s*'
        r'(?P<nature>.+?)\s+'
        r'(?P<incident_ori>(?:OK0140200|14005|EMSSTAT|14009|COMMAND))\s*'
    )

    buffer = ""
    for page in pdf_reader.pages:
        text = page.extract_text()
        if not text:
            continue
        rows = text.split('\n')

        for row in rows:
            row = row.strip()
            if row.startswith('Date / Time'):
                continue

            # Check if the row does not end with the expected ORI codes and accumulate in the buffer
            if row[0].isdigit() and not (row.endswith('EMSSTAT') or row.endswith('OK0140200') or row.endswith('14005') or row.endswith('14009') or row.endswith('COMMAND')):
                buffer = row  # Accumulate rows in buffer
                continue

            # If the buffer is not empty, prepend it to the current row
            row = buffer + " " + row
            # Reset buffer after appending to row
            row = re.sub(r'(\d{4}-\d{8})(?=\S)', r'\1 ', row)
            row = re.sub(r'(?<=[A-Z0-9])(?=[A-Z][a-z])', ' ', row)
            # Try to match the combined row
            match = incident_pattern.search(row.strip())
            if match:
                # Extract the data from the matched line
                incident = {
                    "date_time": match.group("date_time"),
                    "incident_number": match.group("incident_number"),
                    "location": match.group("location").strip(),
                    "nature": match.group("nature").strip(),
                    "incident_ori": match.group("incident_ori")
                }
                incidents.append(incident)

            buffer = ""




    return incidents
