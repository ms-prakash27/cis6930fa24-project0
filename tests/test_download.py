import os
import pytest
from project0.fetch import fetch_incidents
from urllib.error import URLError


def test_fetch_incidents_valid_url():
    # Use a locally stored file to simulate a valid fetch.
    url = "https://www.normanok.gov/sites/default/files/documents/2024-08/2024-08-01_daily_incident_summary.pdf"
    pdf_file_path = fetch_incidents(url)

    assert pdf_file_path is not None, "The PDF file path should not be None."
    assert os.path.exists(pdf_file_path), "The PDF file should be downloaded and exist."

    # Cleanup
    if os.path.exists(pdf_file_path):
        os.remove(pdf_file_path)



