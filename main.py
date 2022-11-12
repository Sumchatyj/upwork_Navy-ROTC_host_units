import requests
import re
from bs4 import BeautifulSoup
import csv


URL = 'https://www.netc.navy.mil/Commands/Naval-Service-Training-Command/NROTC/Navy-ROTC-Schools/#'
RN = r'RN'
NAVY_ONLY = r'Navy.*Option.*only'
RN_ONLY = r'RN.*Option.*only'

def get_request(url):
    response = requests.get(url)
    with open("site.txt", 'w') as f:
        f.write(response.text)


def status_search(soup_obj):
    soup_obj = soup_obj.next_element
    while soup_obj.name not in ['a', 'div']:
        if re.search(NAVY_ONLY, soup_obj.text) is not None:
            return 'Navy option only'
        elif re.search(RN_ONLY, soup_obj.text):
            return 'RN option only'
        elif re.search(RN, soup_obj.text):
            return 'RN'
        soup_obj = soup_obj.next_element
    return None


def get_data():
    result = []
    with open("site.txt", 'r') as f:
        soup = BeautifulSoup(f.read(), 'lxml')
        states = soup.find_all(class_ = 'abcList')
        counter = 0
        for state in states:
            universitys = state.find_all('a', target="_blank")
            for university in universitys:
                status = status_search(university)
                result.append([counter, university.text, status])
                counter += 1
    header = ['N', 'university', 'status']
    with open('result.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for university in result:
            writer.writerow(university)


if __name__ == '__main__':
    get_request(URL)
    get_data()
