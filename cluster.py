import datetime

"""
A Cluster is a class representing the cluster cases in Singapore. It should contain:
1) the Name of the cluster
2) the Address of the cluster
3) A history of cases in the cluster (which can be extrapolated to give)
4) the total cases in the cluster thus far. 

Hopefully, it can contain:
1) The total number of residents (if applicable) in the cluster.

Sometimes discrepancies will come up, such as new infections discovered due to differing testing methods having
different update speeds. Other ways discrepancies can come up is movement of residents between clusters, including 
shuffling between clusters, or people currently not carrying the disease returning back to the cluster.
"""


class Generator:

    def __init__(self, input_paragraph):  # designed to work with Annex B updates from the MOH CoVID-19 website
        self.input_paragraph = input_paragraph

    # Due to how PyPDF2 processes PDFs, some random spaces are inserted, and sometimes spaces are randomly removed.
    # This checker tries to catch that.
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
            elif split[i] == 'now' and split[i + 1] == '.':  # end of sentence space remover
                split[i] += split.pop(i + 1)

        return " ".join(split)


class Cluster:
    # TODO: Split cluster name and address
    total_cases = 0
    total_cases_by_date = []

    def __init__(self, address, new_case_date_tuple):
        self.address = address  # static
        self.new_cases = [new_case_date_tuple]  # list of (cases, date) tuples?

    # output formats
    def __repr__(self):
        return_string = "Cluster at: {} \n\tTotal cases : {}\n\tRecent cases: {} new case(s) on {}" \
            .format(self.address, self.total_cases, self.new_cases[-1][0], self.new_cases[-1][1], )
        return return_string

    def __str__(self):
        return_string = "{}: \n\tTotal Cases  : {} \n\tLatest update: {} new case(s) on {}" \
            .format(self.address, self.total_cases, self.new_cases[-1][0], self.new_cases[-1][1])
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
