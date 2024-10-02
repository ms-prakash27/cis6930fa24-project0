import re
import sys
from PyPDF2 import PdfReader

# Incident originating agency identifier
INCIDENT_ORI = ['OK0140200', 'EMSSTAT', '14005', '14009']

# Postal Service Standard Suffix Abbreviation, cardinal directions, and some other abbreviations used in the reports
POSTAL_SERVICE_SUFFIX_ABBREVIATIONS = [
    "ALY", "ANX", "ARC", "AVE", "GOLDSBY", "BYU", "BCH", "BND", "BLF", "BLFS", "BTM",
    "BLVD", "BR", "BRG", "BRK", "BRKS", "BG", "BGS", "BYP", "CP", "CYN",
    "CPE", "CSWY", "CTR", "CTRS", "CIR", "CIRS", "CLF", "CLFS", "CLB", "CMN",
    "CMNS", "COR", "CORS", "CRSE", "CT", "CTS", "CV", "CVS", "CRK", "CRES",
    "CRST", "XING", "XRD", "XRDS", "CURV", "DL", "DM", "DV", "DR", "DRS",
    "EST", "ESTS", "EXPY", "EXT", "EXTS", "FALL", "FLS", "FRY", "FLD", "FLDS",
    "FLT", "FLTS", "FRD", "FRDS", "FRST", "FRG", "FRGS", "FRK", "FRKS", "FT",
    "FWY", "GDN", "GDNS", "GTWY", "GLN", "GLNS", "GRN", "GRNS", "GRV", "GRVS",
    "HBR", "HBRS", "HVN", "HTS", "HWY", "HL", "HLS", "HOLW", "INLT", "IS",
    "ISS", "ISLE", "JCT", "JCTS", "KY", "KYS", "KNL", "KNLS", "LK", "LKS",
    "LAND", "LNDG", "LN", "LGT", "LGTS", "LF", "LCK", "LCKS", "LDG", "LOOP",
    "MALL", "MNR", "MNRS", "MDW", "MDWS", "MEWS", "ML", "MLS", "MSN", "MTWY",
    "MT", "MTN", "MTNS", "NCK", "OK", "OKC", "ORCH", "OVAL", "OPAS", "PARK", "PKWY", "PKWYS",
    "PASS", "PSGE", "PATH", "PIKE", "PNE", "PNES", "PL", "PLN", "PLNS", "PLZ",
    "PT", "PTS", "PRT", "PRTS", "PR", "RADL", "RAMP", "RNCH", "RPD", "RPDS",
    "RST", "RDG", "RDGS", "RIV", "RD", "RDS", "RTE", "ROW", "RUE", "RUN",
    "SHL", "SHLS", "SHR", "SHRS", "SKWY", "SPG", "SPGS", "SPUR", "SPURS", "SQ",
    "SQS", "STA", "STRA", "STRM", "ST", "STS", "SMT", "TER", "TRWY", "TRCE",
    "TRAK", "TRFY", "TRL", "TRLS", "TRLR", "TUNL", "TPKE", "UPAS", "UN", "UNS",
    "VLY", "VLYS", "VIA", "VW", "VWS", "VLG", "VLGS", "VL", "VIS", "WALK",
    "WALL", "WY", "WAY", "WLS", "NE", "SE", "NW", "SW", "BEND", "O-358", "RR",
    "I", "SB", "EB", "NB", "WB", "MM", "TERR", "HYW", "AL", "NORMAN"
]

# Police incident nature abbreviations
INCIDENT_ABBREVIATIONS = [
    "COP",  # Community Oriented Policing, Close Observation Patrol
    "MVA",  # Multiple vehicle accident
]

# English ordinal suffixes
ORDINAL_SUFFIXES = ["ST", "ND", "RD", "TH"]


def extract_data(pdf_file_path):
    # Create a PdfReader object to read the PDF file
    incident_report = PdfReader(pdf_file_path)

    data = []  # list to store extracted data

    # regex patterns
    date_time_pattern = r'(\d+/\d+/\d+ +\d+:\d{2})'
    incident_number_pattern = r'\d{4}-\d{8}'
    lat_long_pattern = r'\d{2}\.[\d]+;-\d{2}\.[\d]+'

    # loop through all the pages in the pdf file
    for page in incident_report.pages:

        # extract text from each page
        text = page.extract_text()
        # loop over each line in the page
        for idx, line in enumerate(text.split('\n')):

            datetime, incident_number, incident_ori = None, None, None
            line = line.replace("NORMAN POLICE DEPARTMENT", '')
            # check for indices / title and avoid parsing
            if ("Date / Time" in line) or ("Daily Incident Summary (Public)" in line):
                continue
            # check for timestamp at end of the pdf document
            elif re.fullmatch(date_time_pattern, line):
                continue
            else:
                datetime = re.findall(date_time_pattern, line)
                # multiline handling
                # if there is no datetime in the line, then assume that this line is the continuation of the previous line
                if not datetime:
                    # add any spaces required
                    match = [abbreviation for abbreviation in INCIDENT_ABBREVIATIONS if abbreviation in line]
                    if match:
                        line = line.replace(match[0], " " + match[0])
                    else:
                        pattern = r'([A-Z][a-z])'  # pattern to find uppercase letter followed by lowercase letter
                        match = re.search(pattern, line)
                        if match:
                            start = match.start()
                            if start > 0:
                                line = line[:start] + " " + line[start:]
                    # modify current line to previous line in text + current line
                    # and remove previously parsed data
                    line = text.split('\n')[idx - 1] + line
                    datetime = re.findall(date_time_pattern, line)
                    data = data[:-1]
                datetime = datetime[0]
                incident_number = re.findall(incident_number_pattern, line)[0]
                # change start of line to end of incident number
                line = line.replace(datetime, '').replace(incident_number, '')
                for ori in INCIDENT_ORI:
                    if ori in line:
                        incident_ori = ori
                        line = line[:-len(ori) - 1]
                        break
                # remove any trailing spaces
                line = line.strip()
                # check if there is no location or nature information
                if len(line) == 0:
                    data.append({"datetime": datetime, "incident_number": incident_number, "location": None, "nature": None, "incident_ori": incident_ori})
                    continue

                location, nature = None, None
                # split line into individual words based on spaces or commas
                words = re.split(r'[ ,]', line)

                for ridx, word in enumerate(reversed(words)):
                    # check for common abbreviations of address suffixes
                    if word in POSTAL_SERVICE_SUFFIX_ABBREVIATIONS:
                        idx = len(words) - ridx - 1
                        # check if the following word in the sequence is a number
                        if (idx < len(words) - 1) and (words[idx + 1].isdigit() or (len(words[idx + 1]) > 2 and words[idx + 1][-2:] in ORDINAL_SUFFIXES and words[idx + 1][:-2].isdigit())) and (words[idx + 1] != "911"):
                            location = " ".join(words[:idx + 2])
                            nature = " ".join(words[idx + 2:])
                        else:
                            location = " ".join(words[:idx + 1])
                            nature = " ".join(words[idx + 1:])
                        data.append({"datetime": datetime, "incident_number": incident_number,
                                      "location": location, "nature": nature, "incident_ori": incident_ori})
                        break
                if location is not None:
                    continue

                # if location does not end in common postal abbreviations
                if location is None and nature is None:
                    # check if location is in lat long format
                    if re.search(lat_long_pattern, line):
                        match = re.search(lat_long_pattern, line)
                        # extract location/nature information from string
                        line = line[0:match.start()] + " " + line[match.end():]
                        lat_long = match.group()
                        data.append({"datetime": datetime, "incident_number": incident_number,
                                      "location": lat_long, "nature": None, "incident_ori": incident_ori})
                    else:
                        data.append({"datetime": datetime, "incident_number": incident_number,
                                      "location": line, "nature": None, "incident_ori": incident_ori})

    return data

