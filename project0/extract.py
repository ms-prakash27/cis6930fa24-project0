import re
from PyPDF2 import PdfReader
from typing import List, Dict, Tuple


def extract_incidents(pdf_file_path: str) -> List[Dict[str, str]]:
    """Extracts incident details from a PDF report and returns them as a list of dictionaries."""
    try:
        pdf_reader = PdfReader(pdf_file_path)
        raw_rows = extract_raw_rows_from_pdf(pdf_reader)
    except FileNotFoundError:
        print(f"File not found: {pdf_file_path}")
        return []
    except Exception as e:
        print(f"An error occurred while reading the PDF: {e}")
        return []

    # Clean and handle multiline locations
    cleaned_rows = combine_multiline_entries(raw_rows)

    # Extract incident data from cleaned rows
    return [parse_incident_row(row) for row in cleaned_rows]


def extract_raw_rows_from_pdf(pdf_reader) -> List[str]:
    """Extracts and cleans text rows from the PDF, skipping headers and irrelevant lines."""
    rows = []
    for page in pdf_reader.pages:
        text = page.extract_text()
        if text:
            # Clean the text and remove "NORMAN POLICE DEPARTMENT"
            cleaned_text = text.replace("NORMAN", "").replace("POLICE", "").replace("DEPARTMENT", "")

            # Split into lines and skip headers/irrelevant lines
            for line in cleaned_text.split('\n'):
                if any(header in line for header in ["Date / Time", "Daily Incident Summary (Public)"]):
                    continue  # Skip header lines
                rows.append(line.strip())

    return rows[1:-1]  # Optionally exclude first and last row if they contain irrelevant data


def combine_multiline_entries(raw_rows: List[str]) -> List[str]:
    """Combines multiline entries into single rows."""
    combined_rows = []
    i = 0
    while i < len(raw_rows):
        current_row = raw_rows[i].strip()

        # Check if the next row is a continuation (i.e., doesn't start with a date)
        if i + 1 < len(raw_rows) and not re.match(r"^\d{1,2}/\d{1,2}/\d{4}", raw_rows[i + 1]):
            current_row += " " + raw_rows[i + 1].strip()  # Combine current row with the next
            i += 2  # Skip the next row as it has been concatenated
        else:
            i += 1

        combined_rows.append(current_row)
    return combined_rows


def parse_incident_row(row: str) -> Dict[str, str]:
    """Parses a single incident row and returns a dictionary of structured data."""
    parts = row.strip().split(' ')
    if len(parts) < 5:  # Ensure there are enough parts
        return {"date_time": "", "incident_number": "", "location": "", "nature": "", "incident_ori": ""}

    incident_time = ' '.join(parts[:2])  # Time
    incident_number = parts[2]  # Incident number
    incident_ori = parts[-1]  # ORI code
    location_nature_part = ' '.join(parts[3:-1])  # Adjust index for correct slicing

    # Ensure the incident number is between 4-8 digits
    if not re.match(r"^\d{4,8}$", incident_number):
        incident_number = ""

    # Extract location and nature using regex
    incident_location, incident_nature = extract_location_and_nature(location_nature_part)

    return {
        "date_time": incident_time,
        "incident_number": incident_number,
        "location": incident_location,
        "nature": incident_nature,
        "incident_ori": incident_ori
    }


def extract_location_and_nature(location_nature_row: str) -> Tuple[str, str]:
    """Extracts the location and nature of the incident from the combined string."""
    terms_extra = '|'.join(['MVA', 'COP', 'DDACTS', 'EMS', '911'])
    location_nature_row = re.sub(rf'([a-zA-Z0-9])({terms_extra})', r'\1 \2', location_nature_row)
    location_nature_row = re.sub(r'([a-zA-Z0-9])([A-Z][a-z])', r'\1 \2', location_nature_row)

    # Find the start of nature
    pattern = rf'\b({terms_extra}|[A-Z][a-z]+)(?: [A-Z][a-z]+)*'
    match = re.search(pattern, location_nature_row)
    if match:
        inc_nature = location_nature_row[match.start():].strip()
        inc_location = location_nature_row[:match.start()].strip()
    else:
        inc_nature = ""
        inc_location = location_nature_row

    return inc_location, inc_nature








