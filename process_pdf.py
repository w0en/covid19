import PyPDF2
import re
import words2num
from datetime import datetime, timedelta
from pprint import pprint as pp

ROMAN_REGEX = "^[mdclxvi]+. $"
DELIMITER_REGEX = " at |,"
DATE_STRING = (datetime.today() - timedelta(days=1)).strftime('%d %b %Y')
PDF_PATH = 'downloaded_pdfs/%s.pdf' % DATE_STRING
CLUSTERS_CASES = {}  # address:(new, total)


class Cluster:
    # TODO: Split cluster name and address
    total_cases = 0

    def __init__(self, address, new_cases):
        self.address = address  # static
        self.new_cases = new_cases  # list of (cases, date) tuples?

    # output formats
    def __repr__(self):
        return_string = "Cluster at: {} \n Recent cases: {} on {} \n Total cases: {}".format(self.address,
                                                                                             self.new_cases[-1][1],
                                                                                             self.new_cases[-1][0],
                                                                                             self.total_cases)
        return return_string

    def __str__(self):
        return_string = "{}: {}. Latest update: {} on {}".format(self.address, self.total_cases,
                                                                 self.new_cases[-1][0], self.new_cases[-1][1])
        return return_string

    # getters
    def get_address(self):
        return self.address

    def get_new_cases(self, date):
        for i in self.new_cases:
            if i[1] == date:
                return i[0]
        return -1

    def get_total_cases(self):
        return sum(map(lambda x: x[0], self.new_cases))

    # setters
    def add_new_case(self, cases, date):
        for i in self.new_cases:
            if i[1] == date:
                break
            else:
                self.new_cases.append((cases, date))

    def set_total_cases(self, total_cases):
        if self.total_cases != total_cases:
            print("Total cases mismatch!")
            self.total_cases = total_cases
            print("Updated total cases to reflect numbers in Annex B")


def parse_clusters_from_page(page):
    contents = get_contents(page)
    raw_clusters = parse_clusters_from_contents(contents)
    cleaned_raw_clusters = list(map(clean_cluster, raw_clusters))
    return cleaned_raw_clusters


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


def clean_cluster(cluster):
    gaps_fixed = keyword_check(cluster)
    if "new cluster" in gaps_fixed:
        return "".join(convert_cluster_numbers(gaps_fixed))
    else:
        return clean_cluster_address(convert_cluster_numbers(gaps_fixed))


def try_convert(num):
    try:
        num = str(words2num.w2n(num))
        return num
    except (ValueError, words2num.core.NumberParseException):
        return num


def convert_cluster_numbers(cluster):
    return " ".join(map(try_convert, cluster.split()))


def clean_cluster_address(cluster):
    split_one = cluster.split(',', maxsplit=1)  # no maxsplit catches the dorms with > 1k confirmed cases
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
        total_cases = 0
        new_cluster_split = cluster.split("at", maxsplit=1)
        for i in new_cluster_split[0].split():
            if i.isdigit():
                total_cases += int(i)
        return total_cases
    for i in range(len(split_cluster)):
        if split_cluster[i] == "total":
            return int(split_cluster.pop(i + 2).replace(',', ''))
        if split_cluster[i] == "confirmed":
            return int(split_cluster.pop(i - 1).replace(',', ''))


def keyword_check(cluster):
    split = cluster.split()
    for i in range(len(split) - 1):
        if split[i] == 'o' and split[i + 1] == 'ne':  # numbers
            split[i] += split.pop(i + 1)
        elif split[i] == 'on' and split[i + 1] == 'e':
            split[i] += split.pop(i + 1)
        elif split[i] == 't' and split[i + 1] == 'wo':
            split[i] += split.pop(i + 1)
        elif split[i] == 'tw' and split[i + 1] == 'o':
            split[i] += split.pop(i + 1)
        elif split[i] == 't' and split[i + 1] == 'hree':
            split[i] += split.pop(i + 1)
        elif split[i] == 'th' and split[i + 1] == 'ree':
            split[i] += split.pop(i + 1)
        elif split[i] == 'thr' and split[i + 1] == 'ee':
            split[i] += split.pop(i + 1)
        elif split[i] == 'thre' and split[i + 1] == 'e':
            split[i] += split.pop(i + 1)
        elif split[i] == 'f' and split[i + 1] == 'our':
            split[i] += split.pop(i + 1)
        elif split[i] == 'fo' and split[i + 1] == 'ur':
            split[i] += split.pop(i + 1)
        elif split[i] == 'fou' and split[i + 1] == 'r':
            split[i] += split.pop(i + 1)
        elif split[i] == 'f' and split[i + 1] == 'ive':
            split[i] += split.pop(i + 1)
        elif split[i] == 'fi' and split[i + 1] == 've':
            split[i] += split.pop(i + 1)
        elif split[i] == 'fiv' and split[i + 1] == 'e':
            split[i] += split.pop(i + 1)
        elif split[i] == 's' and split[i + 1] == 'ix':
            split[i] += split.pop(i + 1)
        elif split[i] == 'si' and split[i + 1] == 'x':
            split[i] += split.pop(i + 1)
        elif split[i] == 's' and split[i + 1] == 'even':
            split[i] += split.pop(i + 1)
        elif split[i] == 'se' and split[i + 1] == 'ven':
            split[i] += split.pop(i + 1)
        elif split[i] == 'sev' and split[i + 1] == 'en':
            split[i] += split.pop(i + 1)
        elif split[i] == 'seve' and split[i + 1] == 'n':
            split[i] += split.pop(i + 1)
        elif split[i] == 'e' and split[i + 1] == 'eight':
            split[i] += split.pop(i + 1)
        elif split[i] == 'ei' and split[i + 1] == 'ght':
            split[i] += split.pop(i + 1)
        elif split[i] == 'eig' and split[i + 1] == 'ht':
            split[i] += split.pop(i + 1)
        elif split[i] == 'eigh' and split[i + 1] == 't':
            split[i] += split.pop(i + 1)
        elif split[i] == 'n' and split[i + 1] == 'ine':
            split[i] += split.pop(i + 1)
        elif split[i] == 'ni' and split[i + 1] == 'ne':
            split[i] += split.pop(i + 1)
        elif split[i] == 'nin' and split[i + 1] == 'e':
            split[i] += split.pop(i + 1)
        elif split[i] == 'a' and split[i + 1] == 't':  # at
            split[i] += split.pop(i + 1)
        elif split[i] == 'o' and split[i + 1] == 'f':  # of
            split[i] += split.pop(i + 1)
    return " ".join(split)


pdf = open(PDF_PATH, 'rb')
pdf_reader = PyPDF2.PdfFileReader(pdf)
print("=====================================================")
print("=====================================================")
print("BEGIN PARSING")

for i in range(pdf_reader.numPages):
    print("=====================================================")
    print("PAGE " + str(i + 1) + " OF " + str(pdf_reader.numPages))
    print("=====================================================")
    clusters = parse_clusters_from_page(pdf_reader.getPage(i))
    for cluster in clusters:
        print(cluster)
        CLUSTERS_CASES[get_address(cluster)] = (get_new_cases(cluster), get_total_cases(cluster))

print("FINISHED PRINTING")
print("=====================================================")
print("=====================================================")

print("CASES TODAY:")
pp(CLUSTERS_CASES)


# TODO: fix parsing of random spaces within cluster text
