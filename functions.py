import csv
from bs4 import BeautifulSoup
import requests

#get all titles from revistas.csv and split them into a list of all the words

def get_words():
    with open('revistas.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  
        titles = [row[0] for row in reader]
        words = []
        for title in titles:
            words += title.split()
    return words


def get_journal_previews():
    with open('revistas.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        data = [(row[0], row[1].strip("'{}'"), row[4]) for row in reader]
    return data

def get_url(title):
    full_url = None 
    with open('revistas.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        print(title)
        for row in reader:
            if title in row[0]:
                full_url = 'https://www.scimagojr.com/' + row[5]
        print(full_url)
    return full_url  # Return None if no matching title is found

def get_extra_journal_info_scraper(title):
    url = get_url(title)
    print(url)
    if url is None:
        print(f"No URL found for title: {title}")
        return
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    journal_info = []
    journal_grid = soup.find('div', class_='journalgrid')
    grids = journal_grid.find_all('div')
    publisher = grids[2].getText().strip().split('\n')[-1]
    issn = grids[5].getText().strip().split('\n')[-1]
    journal_info.append((publisher, issn))
    return journal_info

def get_all_journal_info_from_csv(title):
    extra_data = get_extra_journal_info_scraper(title)
    with open('revistas.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        journal_info = []
        for row in reader:
            if title in row[0]:
                journal_info.append((row[0], row[1].strip("'{}'"), row[4], row[5], row[6]))
                journal_info.append(extra_data[0])
        return journal_info



def display_title_and_sjr():
    with open('revistas.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  
        titles = []
        sjr = []
        for row in reader:
            titles.append(row[0])
            sjr.append(row[5])
    return titles, sjr

if __name__ == '__main__':
  
    print(get_all_journal_info_from_csv("Ca-A Cancer Journal for Clinicians"))