# CIS6930FA24 -- PROJECT 0 -- README

This project processes the PDF incident reports that the Norman, Oklahoma police department provides. The system retrieves the PDF file from the specified URL, takes out the report's essential fields (date, incident number, location, nature, and officer; ORI), and stores the information in a SQLite database. After that, it prints the number of each type of incident to provide an overview of their nature. The project is modular, with distinct functions for database operations, extraction, fetching, and publishing status.

## Project Structure

- `main.py`: The entry point of the application.
- `fetch.py`: Handles downloading the incident PDF from a given URL.
- `extract.py`: Extracts incident data from the downloaded PDF.
- `db.py`: Manages database operations (creation and population).
- `status.py`: Generates and prints a summary of incidents.

## How to Install



This project requires python, preferable version 3.12 and pipenv should be installed

for installing dependenices use
```
pipenv install
```
For initializing a virtual emvironment use
```
pipenv shell
```

## How to run

```
pipenv run python project0/main.py --incidents <URL_TO_INCIDENT_PDF>
```
ex:
```
pipenv run python main.py --incidents "https://www.normanok.gov/sites/default/files/documents/2024-08/2024-08-01_daily_incident_summary.pdf"
```




## Functions 

### main.py

- `main(url)`: Orchestrates the entire process:
  1. Downloads the incident data
  2. Extracts incidents from the PDF
  3. Creates a new database
  4. Populates the database with extracted incidents
  5. Prints the incident summary

### fetch.py

- The fetch.py file is responsible for downloading incident reports in PDF format from a specified URL. Using urllib.request, the primary function fetch_incidents(url) sends an HTTP call to the specified URL and saves the PDF file to a temporary directory (/tmp/incidents.pdf). It provides the path to the saved PDF file for additional processing after a successful download. The function also offers error handling techniques, such as resolving URL-related errors and exceptions, ensuring robust handling of situations like missing files or failed requests.


### extract.py

- The extract.py file uses the PyPDF2 library and regular expressions to extract incident data from the downloaded PDF. The PdfReader from PyPDF2 is used by the main method, extract_incidents(incident_data), to load and parse the PDF. Every page of the document is iterated through, with the text extracted and regex patterns applied to identify important fields like Date/Time, Incident Number, Location, Nature, and Incident ORI. After that, each instance that matches is added to a list for later use. In order to handle situations such as missing files or problems with text extraction, the function also has error handling.

#### regex used

        r'(?P<date_time>\d+/\d+/\d+ \d+:\d+)\s+'
        r'(?P<incident_number>\d{4}-\d{8})\s+'
        r'(?P<location>(?:\d+\s+)?[A-Z0-9 /()~!_\-;.+:&,]+?)'
        r'(?:\s+(?=911\s|999\s|112\s|\*\*\*)|(?=\s[A-Z][a-z]))\s*'
        r'(?P<nature>.+?)\s+'
        r'(?P<incident_ori>[A-Z0-9]+)$'

- **DateTime**
   - r'(?P<date_time>\d+/\d+/\d+ \d+:\d+)\s+' - (?P<date_time>...) is a named group called "date_time," which makes it simple to refer to this portion of the match. 
   - A date format is represented as \d+/\d+/\d+, where \d+ denotes one or more digits separated by /, such as "09/30/2024."
   - "A space followed by \d+:\d+ matches the time portion in hh:mm format, e.g.," 11:44.
   - \s+ guarantees that the date and time are followed by one or more spaces.
   - we may also use r'^(?P<date_time>\d{1,2}/\d{1,2}/\d{4}\s\d{1,2}:\d{2})\s+'. It offers a fixed length of month, date, and year.
- **Incident_Number**
  -r'(?P<incident_number>\d{4}-\d{8})\s+'
  - An incident number with four digits, a hyphen, and eight digits is matched by this regex pattern. The \s+ makes sure that the incident number is followed by one or more spaces. In a named group called incident_number, the pattern records the incident number.
- **Location** 
  r'(?P<location>(?:\d+\s+)?[A-Z0-9 /()~!_\-;.+:&,]+?)'
        r'(?:\s+(?=911\s|999\s|112\s|\*\*\*)|(?=\s[A-Z][a-z]))\s*'
  - This regex pattern corresponds to an incident's location. The first portion, (?:\d+\s+)?, allows for places that begin with numbers (e.g., street addresses) by optionally capturing one or more digits followed by spaces. The primary section, [A-Z0-9 /()~!_\-;.+:&,]+?, corresponds to a series of alphanumeric characters and frequently used address symbols. The second part, (?:\s+(?=911\s|999\s|112\s|\*\*\*)|(?=\s[A-Z][a-z])), ensures that the match is followed by particular emergency numbers (such 911, 999, 112, or "***") or a capital letter followed by lowercase letters, which helps identify where the location ends and other fields (like nature) begin.
-  **Nature**
   -  r'(?P<nature>.+?)\s+' 
   - The context of the incident is captured by this regex pattern. In order to capture the shortest text before coming across a space, the expression (?P<nature>.+?) employs the.+? to match any character (apart from newlines) in a non-greedy manner. By indicating that this field ends before the next, the \s+ makes sure that there are one or more spaces after the matching nature text. we can simple regex for this.
-  **Incident_ORI**
  - The incident ORI field is composed of uppercase letters (A-Z) and digits (0-9), which are captured by this regex pattern. One or more instances of capital letters or numbers are matched by the pattern (?P<incident_ori>[A-Z0-9]+), and the $ makes sure that this field is at the end of the line. It stands in for the officer or organization that caused the incident.



### db.py

- The SQLite database used to hold incident data is managed via the db.py file. It defines populate_db(conn, incidents) and create_db() as its two main functions. In order to establish a new SQLite database, the create_db() function first makes sure the resources directory is there and deletes any previous database files. After that, it makes a connection and produces a table called incidents, which is organized to hold information about the incident time,Incident number, location, nature, and incident_ori that is in charge. By repeatedly going through the incident data that has been provided and committing each item, the populate_db() function creates a list of incident entries in the database. The database is efficiently set up and populated thanks to this modular architecture, which also makes it simple to store and retrieve police incident reports.

### status.py

- An incident summary is retrieved and shown via the print_status(conn) function from the SQLite database's incidents table. It makes advantage of the supplied database connection (conn) to initiate a SQL query that groups incidents according to their type (kind of incident) and to establish a cursor. The query specifically chooses the type of incident and the number of occurrences for each type, then groups the results appropriately. Next, the outcomes are arranged alphabetically based on the types of incidences.
- once the data has been cursor-retrieved.The function fetchall() iterates through the rows and outputs, in the format nature|count, the count for each event type (nature). This feature aids in giving a brief summary of the quantity of incidents of each kind that are stored in the database.

## Testing

The project includes several test files:

### test_download.py

-To test the fetch_incidents function, which downloads a PDF file from a given URL, use the test_fetch_incidents_valid_url function. This test simulates the fetch process using a working URL that points to a PDF daily incident summary from the City of Norman, Oklahoma. The test uses os.path.exists to confirm that the file actually exists on the local filesystem and that the supplied file path is not None in order to determine whether the fetch_incidents method properly downloaded the PDF. The test does cleanup by erasing the file after verifying that it has been downloaded in order to prevent leaving needless artifacts. This guarantees that the function downloads and stores the PDF file locally in the expected manner.

### test_random.py

**test_create_db**
This test verifies that the necessary structure and database have been established successfully. The test confirms that the create_db function generates an incident table by using a fixture db_connection, which offers a temporary database connection. It accomplishes this by running a query against the SQLite system tables to see if the incidents table is there. The test passes if the table is there; if not, an assertion error is raised.

**test_populate_db**
The populate_db function, which adds data to the incidents database, is tested to ensure it operates as intended. In order to insert the sample incident data (two records) into the database, populate_db is called first. The test retrieves every record from the incidents database post insertion and makes the following assertion

**test_cleanup**
After the tests have completed, this test is in charge of clearing the database file. It deletes the database file normanpd.db if it is detected in the../resources/ directory after verifying that it is there. By performing this cleanup, you can lessen the likelihood that lingering test artifacts will interfere with future tests or clog the file system.


To run the tests, use pytest:

```
pipenv run python -m pytest tests/

```

## Notes

- The project uses a SQLite database stored in `../resources/normanpd.db`.
- Ensure you have the necessary permissions to write to the `/tmp/` directory and the `resources` folder.
- The project includes error handling for various scenarios, such as network issues or file not found errors.

