import gspread
from google.oauth2 import service_account
import PyPDF2
from datetime import datetime
from pprint import pprint as pp
import words2num

DATE_STRING = datetime.today().strftime('%d %b %Y')
PDF_PATH = 'downloaded_pdfs/%s.pdf' % DATE_STRING
DELIMITER = '\n\n'
cases_today = {}

"""
# setup
credentials = service_account.Credentials.from_service_account_file("credentials.json")
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
scoped_credentials = credentials.with_scopes(scope)
client = gspread.authorize(scoped_credentials)
url = "https://docs.google.com/spreadsheets/d/1UFWHuTJiDdJhtgygfqX9GRIGLqFIjQuI88cN-S8PhL0"
"""


def find_address(paragraph):
    return None


pdf = open(PDF_PATH, 'rb')
pdf_reader = PyPDF2.PdfFileReader(pdf)
for i in range(pdf_reader.numPages):
    current_page = pdf_reader.getPage(i).extractText()
    for paragraph in current_page.split(DELIMITER):
        print("NEW PARAGRAPH")
        print(paragraph)

