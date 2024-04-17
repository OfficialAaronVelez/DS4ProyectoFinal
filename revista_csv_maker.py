from bs4 import BeautifulSoup
import requests
import csv



class Revista:
    def __init__(self,titulo:str,catalogo:str, cites:int, cuartil:str, sjr:float,url:str, categories: list):
        self.titulo = titulo
        self.catalogos = set()
        self.catalogos.add(catalogo)
        self.cites = cites
        self.cuartil = cuartil
        self.sjr = sjr
        self.url = url
        self.categories = categories

       

    
    def __str__(self):
        return f'{self.titulo} - {self.catalogos}-{self.cites}-{self.cuartil}-{self.sjr}-{self.url}-{self.categories}'

    def __repr__(self):
        return f'{self.titulo} - {self.catalogos}-{self.cites}-{self.cuartil}-{self.sjr}-{self.url}-{self.categories}'
    



url = "https://www.scimagojr.com/journalrank.php"

def get_html():
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

def get_revistas(soup):
    revistas = []
    for row in soup.find_all('tr'):
        cols = row.find_all('td')
        if len(cols) > 0:
            titulo = cols[1].get_text()
            catalogo = cols[2].get_text()
            cites = cols[8].get_text()
            
            sjr, cuartil = cols[3].get_text().split()
            url = cols[1].find('a')['href']
            area = cols[3].find('span').get('title')
            categories = area.split('categories: ')[1].rstrip(')').split('; ')
            revista = Revista(titulo,catalogo,int(cites),cuartil,float(sjr),url,categories)
            revistas.append(revista)
            
    return revistas


def write_csv(revistas):
    with open('revistas.csv', 'w', newline='') as csvfile:
        fieldnames = ['titulo', 'catalogos', 'cites', 'cuartil', 'sjr', 'url', 'categories']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for revista in revistas:
            writer.writerow({'titulo': revista.titulo, 'catalogos': revista.catalogos, 'cites': revista.cites, 'cuartil': revista.cuartil, 'sjr': revista.sjr, 'url': revista.url, 'categories': revista.categories})

if __name__ == '__main__':
    soup = get_html()
    revistas = get_revistas(soup)
    print(revistas)
    write_csv(revistas)
