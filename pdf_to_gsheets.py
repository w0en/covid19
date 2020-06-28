import gspread
from google.oauth2 import service_account
import PyPDF2
from datetime import datetime, timedelta
from pprint import pprint as pp
import words2num
import re

ROMAN_REGEX = "^[mdclxvi]+. $"
DATE_STRING = (datetime.today() - timedelta(days=1)).strftime('%d %b %Y')
PDF_PATH = 'downloaded_pdfs/%s.pdf' % DATE_STRING
CLUSTERS_NEW_CASES = {}
CLUSTERS_CONFIRMED_CASES = {}

"""
# setup
credentials = service_account.Credentials.from_service_account_file("credentials.json")
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
scoped_credentials = credentials.with_scopes(scope)
client = gspread.authorize(scoped_credentials)
url = "https://docs.google.com/spreadsheets/d/1UFWHuTJiDdJhtgygfqX9GRIGLqFIjQuI88cN-S8PhL0"
"""


def clean_list(page):
    contents = get_contents(page)
    raw_clusters = parse_contents(contents)
    cleaned_clusters = list(map(lambda x: clean_cluster(x), raw_clusters))
    return cleaned_clusters


def get_contents(page):
    extracted_text = page.extractText().split('\n')
    extracted_text.pop(0)
    return list(filter(lambda x: not x.isspace(), map(lambda x: x.strip() + ' ', extracted_text)))


def parse_contents(cleaned_text):
    clusters = [""]
    for e in cleaned_text:
        if re.match(pattern=ROMAN_REGEX, string=e):
            clusters.append("")
        else:
            clusters[-1] += e
    clusters.pop(0)
    return clusters


def convert_cluster_numbers(cluster):
    # clusters are strings
    cluster = convert_first_number(cluster)
    second_split = cluster.split("of")
    second_split[1] = convert_first_number(second_split[1])
    cleaned_cluster = "".join(second_split)
    return cleaned_cluster


def convert_first_number(string):
    split = string.split(maxsplit=1)
    split[0] = try_convert(split[0])
    return "".join(split)


def try_convert(num):
    try:
        num = str(words2num.w2n(num)) + ' '
        return num
    except ValueError:
        return num + ' '


def clean_cluster(cluster):
    return clean_cluster_address(convert_cluster_numbers(cluster))


def clean_cluster_address(cluster):
    split_one = cluster.split(',')
    split_two = split_one[0].split('at')
    address = split_two[1]
    split_address = address.split()
    concatenated_address = []
    for i in range(len(split_address) - 1):
        if (split_address[i][-1].isdigit() and split_address[i + 1][0].isdigit()) \
                or ((split_address[i][0].isupper() and split_address[i + 1][0].islower()) and split_address[i + 1] != 'dormitory'):
            concatenated_address.append(str(split_address[i]) + str(split_address[i + 1]) + ' ')
        else:
            concatenated_address.append(split_address[i] + ' ')
    cleaned_address = [concatenated_address[0]]
    for i in range(1, len(concatenated_address)):
        if not (concatenated_address[i] in concatenated_address[i - 1]):
            cleaned_address.append(concatenated_address[i])
        else:
            continue
    final_address = "".join(cleaned_address)
    # if "(" in final_address and ")" not in final_address:
    #     final_address += ")"
    join_two = split_two[0] + "at " + final_address
    join_one = join_two.strip() + "," + split_one[-1]
    return join_one


pdf = open(PDF_PATH, 'rb')
pdf_reader = PyPDF2.PdfFileReader(pdf)
print("=====================================================")
print("=====================================================")
print("BEGIN PARSING")
print("=====================================================")
print("=====================================================")

for i in range(pdf_reader.numPages):
    print("=====================================================")
    print("PAGE " + str(i + 1) + " OF " + str(pdf_reader.numPages))
    print("=====================================================")
    clusters = clean_list(pdf_reader.getPage(i))
    for cluster in clusters:
        print(cluster)

print("=====================================================")
print("=====================================================")
print("FINISHED PRINTING")
print("=====================================================")
print("=====================================================")


# TODO: Special function for new clusters
# TODO: Parentheses for address
# TODO: missing words in address (e.g. 'road')
# TODO: resolve what happens when a space in the first word happens e.g. o ne
# TODO: fix parsing of first page
# TODO: fix parsing of random spaces within cluster text
