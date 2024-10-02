from pypdf import PdfReader
import re


def extract_incidents(file_path):
    # Load the PDF
    reader = PdfReader(file_path)

    # Extract text data from all pages
    text_data = []
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        # Extract text using layout mode to preserve text format
        text = page.extract_text(extraction_mode="layout")
        text_data.append(text)

    # Parse incidents using double spaces to separate columns
    incidents = []
    first_row = True  # Flag to track the first row
    for page_text in text_data:
        # Split the page text into lines
        lines = page_text.split('\n')
        for line in lines:
            # Use double spaces to split columns
            columns = re.split(r'\s{2,}', line.strip())

            # Ensure all columns exist to match the expected number of fields
            if len(columns) >= 5:
                # Skip the first row if it is the header
                if first_row:
                    first_row = False
                    continue

                # Assuming the order is:
                # Date / Time | Incident Number | Location | Nature | Incident ORI
                date_time = columns[0].strip()
                incident_number = columns[1].strip()
                location = columns[2].strip()
                nature = columns[3].strip()
                incident_ori = columns[4].strip()

                # Append incident data as a dictionary
                incidents.append({
                    'incident_time': date_time,
                    'incident_number': incident_number,
                    'incident_location': location,
                    'nature': nature,
                    'incident_ori': incident_ori
                })

    return incidents
