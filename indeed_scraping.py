import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup


def get_url(search, location):
    template = 'https://jp.indeed.com/jobs?q={}&l={}'
    url = template.format(search, location)
    return url


def get_record(card):
    atag = card.h2.a
    job_title = atag.get('title')
    job_url = 'https://jp.indeed.com/' + card.h2.a.get('href')
    company = card.find('span', 'company').text.strip()

    job_location = card.find('div', 'recJobLoc').get('data-rc-loc')
    summary = card.find('div', 'summary').text.strip()
    date = card.find('span', 'date').text
    today = datetime.today().strftime('%m月-%d日')
    try:
        salary = card.find('span', 'salaryText').text.strip()
    except AttributeError:
        salary = ' '

    record = (today, date, job_title, company,
              job_location, summary, salary, job_url)
    return record


def main(search, location):
    records = []
    url = get_url(search, location)

    result = 0
    while True:
        resuponse = requests.get(url)
        soup = BeautifulSoup(resuponse.text, 'html.parser')
        cards = soup.find_all('div', 'jobsearch-SerpJobCard')
        for card in cards:
            record = get_record(card)
            records.append(record)
        try:
            url = 'https://jp.indeed.com/' + \
                soup.find('a', {'aria-label': '次へ'}).get('href')
            result = len(cards) + result
        except AttributeError:
            break
    print(records)
    with open('results.csv', 'w', newline='', encoding='utf_8_sig') as f:
        writer = csv.writer(f)
        writer.writerow(['today', 'date', 'title', 'company',
                        'location', 'summary', 'salary', 'URL'])
        writer.writerows(records)


search = input('探す仕事:')
location = input('場所:')
print('done...')
main(search, location)
print('finish')
