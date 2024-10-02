from pypdf import PdfReader
import re


def extract_incidents(file_path):
    #PDF Loading
    reader = PdfReader(file_path)


    # extracting text data from all pages
    text_data = [page.extract_text(extraction_mode="layout") for page in reader.pages]


    #parisng all the incident using doubles spaces to seperate columns
    incidents = []
    #variable to track if the header is skipped or not
    header_skipped = False

    for page_text in text_data:
        #spliting the page text into lines
        lines = page_text.split('\n')
        for line in lines:
            #using double spaces for splitting of columns
            columns = re.split(r'\s{2,}', line.strip())

            #ensuring that all columns and exist to match the expected number of fields
            if len(columns) >= 5:
                # Skip the first row if it is the header
                if not header_skipped:
                    header_skipped = True
                    continue

                #opening the columns in the following order:
                # Date / Time | Incident Number | Location | Nature | Incident ORI
                date_time, incident_number, location, nature, incident_ori = map(str.strip, columns[:5])

                #appending incident data as a dictionary
                incidents.append({
                    'incident_time': date_time,
                    'incident_number': incident_number,
                    'incident_location': location,
                    'nature': nature,
                    'incident_ori': incident_ori
                })

    return incidents
