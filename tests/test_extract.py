import pytest
from project0.extract import extract_incidents


def test_extract_incidents():
    # Path to the local PDF file in the resources directory
    test_pdf_path = "tests/test_incidents.pdf"

    # Extract data from the local test PDF
    extracted_data = extract_incidents(test_pdf_path)

    # Check that data is extracted and is in list form
    assert isinstance(extracted_data, list), "Extracted data should be a list."
    assert len(extracted_data) > 0, "No data was extracted from the PDF."

    # Validate that each entry has the expected keys
    expected_keys = {'incident_time', 'incident_number', 'incident_location', 'nature', 'incident_ori'}
    for incident in extracted_data:
        assert set(incident.keys()) == expected_keys, f"Extracted incident data structure is incorrect: {incident}"
