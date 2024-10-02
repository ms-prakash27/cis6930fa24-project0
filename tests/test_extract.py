import pytest
from project0.extract import extract_incidents


def test_extract_incidents():
    #local pdf  file form norman pd website to test the file
    test_pdf_path = "tests/test_normanpd.pdf"

    #extracting data from the local pdf file
    extracted_data = extract_incidents(test_pdf_path)

    #checking if the data extracted is in list form
    assert isinstance(extracted_data, list), "Extracted data should be a list."
    assert len(extracted_data) > 0, "No data was extracted from the PDF."


    #validateing the each entry is in its correct form or not
    expected_keys = {'incident_time', 'incident_number', 'incident_location', 'nature', 'incident_ori'}
    for incident in extracted_data:
        assert set(incident.keys()) == expected_keys, f"Extracted incident data structure is incorrect: {incident}"
