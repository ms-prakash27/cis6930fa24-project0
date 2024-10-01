import urllib.request
import urllib.error

def fetch_incidents(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'
    }
    request = urllib.request.Request(url, headers=headers)

    try:
        # Fetch the PDF data
        with urllib.request.urlopen(request) as response:
            data = response.read()

        # Save the PDF to a temporary file
        pdf_file = "/tmp/incidents.pdf"
        with open(pdf_file, "wb") as f:
            f.write(data)

        return pdf_file
    except urllib.error.URLError as e:
        raise Exception(f"Failed to fetch incidents due to a URL error: {e}")
    except Exception as e:
        raise Exception(f"Failed to fetch incidents: {e}")
