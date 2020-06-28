import gspread
from google.oauth2 import service_account
import PyPDF2
from datetime import datetime, timedelta
from pprint import pprint as pp
import words2num
import re


ROMAN_REGEX = "^[mdclxvi]+. $"
DATE_STRING = (datetime.today()-timedelta(days=1)).strftime('%d %b %Y')
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


def is_roman(string):
    if string.endswith('.'):
        if string.strip("i").strip("v").strip("x").strip("m").strip("c").isblank():
            return True
    else:
        return False


def clean_list(page):
    raw_text = page.extractText().split('\n')
    cleaned_text = filter(lambda x: not x.isspace(), map(lambda x: x.strip() + ' ', raw_text))
    banana = list(cleaned_text)
    pp(list(cleaned_text))
    paragraphs = [""]
    for e in banana:
        if re.match(pattern=ROMAN_REGEX, string=e):
            paragraphs.append(e)
            print("REGEX MATCHED")
            print(e)
        else:
            print("REGEX NOT MATCHED")
            paragraphs[-1] += e
    pp(paragraphs)
    return None


pdf = open(PDF_PATH, 'rb')
pdf_reader = PyPDF2.PdfFileReader(pdf)
for i in range(pdf_reader.numPages):
    print("PAGE " + str(i + 1) + " OF " + str(pdf_reader.numPages))
    clean_list(pdf_reader.getPage(i))
print("FINISHED PRINTING")
