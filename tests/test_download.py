from project0 import fetch
from project0 import db
import os

def test_fetch_incidents():
    #url from NormanPD department
    test_url = "https://www.normanok.gov/sites/default/files/documents/2024-08/2024-08-01_daily_incident_summary.pdf"

    #fetching the incidents PDF
    pdf_file_path = fetch.fetch_incidents(test_url)

    #asserting that the file exists and is not empty
    assert os.path.exists(pdf_file_path)
    assert os.path.getsize(pdf_file_path) > 0

    #cleaning after ther test
    os.remove(pdf_file_path)
