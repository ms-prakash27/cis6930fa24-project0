from pypdf import PdfReader
import re

def extract_incidents(file_path):
    # Load the PDF
    reader = PdfReader(file_path)

    # Extract text data from all pages
    text_data = [page.extract_text(extraction_mode="layout") for page in reader.pages]

    # Parse incidents using double spaces to separate columns
    incidents = []
    header_skipped = False  # Flag to track if the header is skipped

    for page_text in text_data:
        # Split the page text into lines
        lines = page_text.split('\n')
        for line in lines:
            # Use double spaces to split columns
            columns = re.split(r'\s{2,}', line.strip())

            # Ensure all columns exist to match the expected number of fields
            if len(columns) >= 5:
                # Skip the first row if it is the header
                if not header_skipped:
                    header_skipped = True
                    continue

                # Unpack columns assuming the order:
                # Date / Time | Incident Number | Location | Nature | Incident ORI
                date_time, incident_number, location, nature, incident_ori = map(str.strip, columns[:5])

                # Append incident data as a dictionary
                incidents.append({
                    'incident_time': date_time,
                    'incident_number': incident_number,
                    'incident_location': location,
                    'nature': nature,
                    'incident_ori': incident_ori
                })

    return incidents