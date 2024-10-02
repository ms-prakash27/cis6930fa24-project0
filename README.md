# CIS6930FA24 -- PROJECT 0 -- README

This project processes the PDF incident reports that the Norman, Oklahoma police department provides. The system retrieves the PDF file from the specified URL, takes out the report's essential fields (date, incident number, location, nature, and officer; ORI), and stores the information in a SQLite database. After that, it prints the number of each type of incident to provide an overview of their nature. The project is modular, with distinct functions for database operations, extraction, fetching, and publishing status.

## Project Structure

- `main.py`: starting point of the application.
- `fetch.py`: handling downloading the incident PDF from a given URL.
- `extract.py`: extracting the incident data from the downloaded PDF.
- `db.py`: for managing the database operations (creation and population).
- `status.py`: generate and prints a summary of incidents.

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

For getting incidents in the form that has been asked in the project we have to run the following command at the project directory
```
pipenv run python project0/main.py --incidents <URL_TO_INCIDENT_PDF>
```
ex:
```
pipenv run python main.py --incidents "https://www.normanok.gov/sites/default/files/documents/2024-08/2024-08-01_daily_incident_summary.pdf"
```

### video 

https://drive.google.com/file/d/1o_u_aoD6EVa5TlknuncQxJ5FN12oEYuB/view?usp=sharing



## Functions 

### main.py

- The `main(url)` function uses the `fetch.py` module to download the incident data from a specified URL before orchestrating the whole incident data processing procedure. Following a successful PDF retrieval, the `extract.py` program organizes the important data fields for analysis by extracting pertinent incident information. The required structure to store the extracted data is then established by `main(url)`, which uses the `db.py` module to construct a new SQLite database. The method creates and publishes an incident summary as soon as the database is filled with incidents, giving users a concise rundown of the data that has been extracted. The smooth transition from data retrieval to summary presentation is guaranteed by this integrated technique.
- 
### fetch.py

- The fetch.py file is responsible for downloading incident reports in PDF format from a specified URL. Using urllib.request, the primary function fetch_incidents(url) sends an HTTP call to the specified URL and saves the PDF file to a temporary directory (/tmp/incidents.pdf). It provides the path to the saved PDF file for additional processing after a successful download. The function also offers error handling techniques, such as resolving URL-related errors and exceptions, ensuring handling of situations like missing files or failed requests.


### extract.py

- The extract_incidents function basically extracts incident data from PDF documents. It uses the PdfReader class from the pypdf package. This function is for documents containing tabular data separated by more than one space(here in this project). The method starts with loading the specified PDF file and extracting text from each page while maintaining the layout. The retrieved text is processed line by line, with regular expressions dividing each line into columns based on more than one space(for simplicity used double space as there no other double space). This ensures that data is correctly parsed, even if columns are not aligned. To properly manage headers, the function skips the first row of data on each page if it is recognized as a header, assuring only true incident data is processed.
- Each line of data is mapped to specific fields: date/time, incident number, location, nature, and incident ORI. These fields are combined into a dictionary that represents a single occurrence, and all incidents are grouped into a list of dictionaries for organized output. The function assumes that the PDF is formatted with more than one space(my obseravtion) between data fields; changes may be required for other formats. To use this function, pass the path to the PDF file and cycle through the resulting list of dictionaries to get detailed information about each incident.


### Database Development - db.py

- The SQLite database used to hold incident data is managed via the db.py file. It defines populate_db(conn, incidents) and create_db() as its two main functions. In order to establish a new SQLite database, the create_db() function first makes sure the resources directory is there and deletes any previous database files. After that, it makes a connection and produces a table called incidents, which is organized to hold information about the incident time,Incident number, location, nature, and incident_ori that is in charge. By repeatedly going through the incident data that has been provided and committing each item, the populate_db() function creates a list of incident entries in the database. The database is efficiently set up and populated thanks to this modular architecture, which also makes it simple to store and retrieve police incident reports.

### status.py

- An incident summary is retrieved and shown via the print_status(conn) function from the SQLite database's incidents table. It makes advantage of the supplied database connection (conn) to initiate a SQL query that groups incidents according to their type (kind of incident) and to establish a cursor. The query specifically chooses the type of incident and the number of occurrences for each type, then groups the results appropriately. Next, the outcomes are arranged alphabetically based on the types of incidences.
- once the data has been cursor-retrieved.The function fetchall() iterates through the rows and outputs, in the format nature|count, the count for each event type (nature). This feature aids in giving a brief summary of the quantity of incidents of each kind that are stored in the database.

## Testing

The project includes 3 test files:

### test_download.py

- The function test_fetch_incidents downloads a PDF file from the Norman Police Department in order to test the fetch.fetch_incidents method. It checks to make sure the file exists and is not empty and has a size larger than zero in order to confirm that the PDF file was downloaded successfully. To keep the testing environment organized, the method removes the downloaded file after making these assertions. This method assists in verifying that the incident summary was successfully downloaded and that the fetch module handled the file appropriately.

### test_extract.py
- Using data extracted from a local test PDF file (tests/test_normanpd.pdf), the test_extract_incidents function tests the extract_incidents method. It initially verifies the proper output format by ensuring that the extracted data is returned as a list. After that, the function checks to see if the list is empty to make sure that some incident data was successfully taken out of the PDF. The function loops over all entries and verifies that they contain the anticipated set of keys—incidence_time, incident_number, incident_location, nature, and incident_ori—in order to validate the structure of each incident. This guarantees that every occurrence that is extracted has the necessary characteristics and adheres to the right schema. These validations jointly indicate that extract_incidents correctly processes the PDF and delivers appropriately structured incident data.
### test_random.py

**setup_database**
- A temporary SQLite database connection is created for testing purposes via the setup_database method, which is a test fixture. After creating the database using the db.create_db() function, it returns the connection for usage in each test case. To keep the testing environment tidy, the function makes sure the database is correctly closed and erased after the tests are finished. The cleanup process is handled by checking if the database file exists and eliminating it, avoiding any leftover files from collecting.

**test_createdb**
- The purpose of the test_createdb function is to verify that the incidents table in the database was created and is organized correctly. In order to verify that the incidents table has been correctly created, it first queries the database. The table's schema information is then retrieved using a PRAGMA query, and it is claimed to have exactly 5 columns, in accordance with the expected structure. This guarantees that the table is correctly configured in accordance with the database module's specifications.

**test_populate_db**
- The primary goal of the test_populate_db function is to confirm that the database has been correctly populated with incident data. It simulates the process of parsing incident reports by extracting data using the extract_incidents function from a test PDF file (test_normanpd.pdf). After the data is extracted, db.populate_db(conn, extracted_data) is used to insert it into the incidents table. The function verifies that the data insertion procedure is successful by checking to see if the table is empty after the database has been filled.


To run the tests, use pytest:

```
pipenv run python -m pytest tests/

```

# Bugs and Assumptions

- Assumed that the provided URL is accessible and contains a valid PDF file
- Assumed that the PDF contains at least 5 columns: Date/Time, Incident Number, Location, Nature, and Incident ORI.
- Skipped the first row while extracting pdf becasue they contain headers which are disturbing the insertion to DB

