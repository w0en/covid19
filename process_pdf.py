import gspread
from google.oauth2 import service_account
import PyPDF2
from datetime import datetime, timedelta
import words2num
import re
from pprint import pprint as pp

ROMAN_REGEX = "^[mdclxvi]+. $"
DATE_STRING = (datetime.today() - timedelta(days=1)).strftime('%d %b %Y')
PDF_PATH = 'downloaded_pdfs/%s.pdf' % DATE_STRING
CLUSTERS_CASES = {}  # address:(new, total)
VALID_WORDS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "confirmed", "cases",
               "additional", "the", "cluster", "now", "linked"]


"""
# setup
credentials = service_account.Credentials.from_service_account_file("credentials.json")
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
scoped_credentials = credentials.with_scopes(scope)
client = gspread.authorize(scoped_credentials)
url = "https://docs.google.com/spreadsheets/d/1UFWHuTJiDdJhtgygfqX9GRIGLqFIjQuI88cN-S8PhL0"
"""


def parse_clusters_from_page(page):
    contents = get_contents(page)
    raw_clusters = parse_clusters_from_contents(contents)
    cleaned_clusters = list(map(lambda x: clean_cluster(x), raw_clusters))
    return cleaned_clusters


def get_contents(page):
    extracted_text = page.extractText().split('\n')
    extracted_text.pop(0)
    return list(filter(lambda x: not x.isspace(), map(lambda x: x.strip() + ' ', extracted_text)))


def parse_clusters_from_contents(cleaned_text):
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
    cleaned_cluster = "of ".join(second_split)
    return cleaned_cluster


def convert_first_number(string):
    split = string.split(maxsplit=1)
    split[0] = try_convert(split[0])
    return "".join(split)


def try_convert(num):
    try:
        num = str(words2num.w2n(num)) + ' '
        return num
    except (ValueError, words2num.core.NumberParseException):
        return num + ' '


def clean_cluster(cluster):
    if "new cluster" in cluster:
        return clean_new_cluster(cluster)
    else:
        return clean_cluster_address(convert_cluster_numbers(cluster))


def clean_cluster_address(cluster):
    split_one = cluster.split(',', maxsplit=1)  # no maxsplit catches some of the dorms with > 1k confirmed cases
    split_two = split_one[0].split('at', maxsplit=1)  # no maxsplit catches some parts of the addresses
    address = split_two[1]
    cleaned_address = format_address(concatenate_address(address.split()))
    if "(" in cleaned_address and ")" not in cleaned_address:
        cleaned_address += ")"
    join_two = split_two[0] + "at " + cleaned_address
    join_one = join_two.strip() + "," + split_one[-1]
    return join_one


def concatenate_address(address_list):
    concatenated_list = []
    for i in address_list:
        if i[0].isdigit():
            if address_list.index(i) == 0:
                concatenated_list.append(i)
            else:
                concatenated_list[-1] += i
        elif i[0].islower():
            if address_list.index(i) == 0:
                concatenated_list.append(i)
            else:
                concatenated_list[-1] += i
        else:
            concatenated_list.append(i)
    return " ".join(concatenated_list)


def clean_new_cluster(cluster):
    numbers_converted = list(map(lambda x: try_convert(x), cluster.split()))
    return "".join(numbers_converted)


def get_address(cluster):
    if "new cluster" in cluster:
        return cluster.split("at")[-1].strip().strip('.')
    else:
        return format_address(cluster.split(',')[0].split("at", maxsplit=1)[1].strip())


def format_address(address):
    return road_number_check(dormitory_check(address))


def dormitory_check(address):
    if "dormitory" in address:
        banana = address.split("dormitory")
        return " Dormitory".join(banana)
    elif "constructionsite" in address:
        banana = address.split("constructionsite")
        return " Construction Site".join(banana)
    elif "construction" in address:
        banana = address.split("construction")
        return " Construction".join(banana)
    elif "site" in address:
        banana = address.split("site")
        return " Site".join(banana)
    else:
        return address


def road_number_check(address):
    for i in range(len(address) - 1):
        if address[i].isalpha() and address[i + 1].isdigit():
            split_address = [address[0:i + 1], address[i + 1:len(address)]]
            return " ".join(split_address)
    return address


def get_new_cases(cluster):
    try:
        return int(cluster.split()[0])
    except ValueError:
        return -1


def get_total_cases(cluster):
    split_cluster = cluster.split()
    if "new cluster" in cluster:
        return int(split_cluster[0]) + int(split_cluster[9])
    for i in range(len(split_cluster)):
        if split_cluster[i] == "total":
            return int(split_cluster.pop(i + 2).replace(',', ''))
        if split_cluster[i] == "confirmed":
            return int(split_cluster.pop(i - 1).replace(',', ''))


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
    clusters = parse_clusters_from_page(pdf_reader.getPage(i))
    for cluster in clusters:
        print(cluster)
        CLUSTERS_CASES[get_address(cluster)] = (get_new_cases(cluster), get_total_cases(cluster))

print("=====================================================")
print("=====================================================")
print("FINISHED PRINTING")
print("=====================================================")
print("=====================================================")

print("CASES TODAY:")
pp(CLUSTERS_CASES)


# TODO: fix parsing of random spaces within cluster text
