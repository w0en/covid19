import gspread
from google.oauth2 import service_account
import PyPDF2
from datetime import datetime
from pprint import pprint as pp
import words2num


DATE_STRING = datetime.today().strftime('%d %b %Y')
PDF_PATH = 'downloaded_pdfs/%s.pdf' % DATE_STRING
DELIMITER = '\n'
cases_today = {}

"""
# setup
credentials = service_account.Credentials.from_service_account_file("credentials.json")
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
scoped_credentials = credentials.with_scopes(scope)
client = gspread.authorize(scoped_credentials)
url = "https://docs.google.com/spreadsheets/d/1UFWHuTJiDdJhtgygfqX9GRIGLqFIjQuI88cN-S8PhL0"
"""


def clean_list(page):
    paragraphs = list(filter(lambda x: not (x.isspace()), page.extractText().split(DELIMITER)))
    pp(paragraphs)
    concatenated = []
    for e in paragraphs:
        if not e.endswith("now."):
            concatenated[-1] += " " + e
        else:
            concatenated.append(e)

    print("NEW: " + str(concatenated))
    return None


pdf = open(PDF_PATH, 'rb')
pdf_reader = PyPDF2.PdfFileReader(pdf)
for i in range(pdf_reader.numPages):
    print("PAGE " + str(i + 1) + " OF " + str(pdf_reader.numPages))
    clean_list(pdf_reader.getPage(i))
print("FINISHED PRINTING")
