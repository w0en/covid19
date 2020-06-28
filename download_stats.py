import requests
import bs4
from datetime import datetime, timedelta

DATE_STRING = (datetime.today()-timedelta(days=1)).strftime('%d %b %Y')
DISCHARGED_STRING = 'more-cases-discharged'
NEW_CASES_STRING = 'new-cases-of-covid-19-infection-confirmed'
COVID_WEBSITE = 'https://www.moh.gov.sg/covid-19/past-updates'


covid_soup = bs4.BeautifulSoup(requests.get(COVID_WEBSITE).text, features="html.parser")

links = covid_soup.find_all('a', href=True)


def find_annexb(url):
    annex_soup = bs4.BeautifulSoup(requests.get(url).text, features="html.parser")
    lonks = annex_soup.find_all('a', href=True)
    for lonk in lonks:
        if '.pdf' in lonk['href'] and 'annex-b' in lonk['href']:
            print(lonk['href'])
            return lonk['href']
        else:
            continue


for link in links:
    if link['href'].endswith('confirmed'):
        PDF_LINK = find_annexb(link['href'])
        r = requests.get(PDF_LINK)
        FILE_PATH = 'downloaded_pdfs/%s.pdf' % DATE_STRING
        with open(FILE_PATH, 'wb') as f:
            f.write(r.content)
        break
    else:
        continue
