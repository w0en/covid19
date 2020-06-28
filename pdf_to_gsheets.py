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


def extract_text_remove_page_number(page):
    extracted_text = page.extractText().split('\n')
    extracted_text.pop(0)
    return extracted_text


def clean_spaces(paragraphs):
    return list(filter(lambda x: not x.isspace(), map(lambda x: x.strip() + ' ', paragraphs)))


def concatenate_into_clusters(cleaned_text):
    clusters = [""]
    for e in cleaned_text:
        if re.match(pattern=ROMAN_REGEX, string=e):
            clusters.append("")
        else:
            clusters[-1] += e
    clusters.pop(0)
    return clusters


def convert_first_number(clusters):
    raw_clusters = list(map(lambda x: x.split(maxsplit=1), clusters))
    for a in range(len(raw_clusters)):
        raw_clusters[a][0] = try_convert(raw_clusters[a][0])
        b = "".join(raw_clusters[a])
        raw_clusters[a] = b
    return raw_clusters


def clean_list(page):
    page_no_number = extract_text_remove_page_number(page)
    cleaned_text = clean_spaces(page_no_number)
    clusters = concatenate_into_clusters(cleaned_text)
    formatted_clusters = convert_first_number(clusters)
    cleaned_clusters = map(lambda x: x, formatted_clusters)
    return cleaned_clusters


def try_convert(num):
    try:
        num = str(words2num.w2n(num)) + ' '
        return num
    except ValueError:
        return num + ' '


def clean_address(cluster_text):
    split_at_at = cluster_text.split('at', maxsplit=1)
    split_at_at[0] += 'at'
    print(split_at_at)
    text_split_after_comma = (split_at_at[1]).split[',']
    broken_address = text_split_after_comma[0]
    print(broken_address)
    temp = []
    for chunk in broken_address:
        if not chunk[0].islower:
            temp.append(chunk)
    return None



pdf = open(PDF_PATH, 'rb')
pdf_reader = PyPDF2.PdfFileReader(pdf)
for i in range(pdf_reader.numPages):
    print("PAGE " + str(i + 1) + " OF " + str(pdf_reader.numPages))
    clusters = clean_list(pdf_reader.getPage(i))
    for cluster in clusters:
        print(cluster)
print("FINISHED PRINTING")

