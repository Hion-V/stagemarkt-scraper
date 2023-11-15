from bs4 import BeautifulSoup
from requests import request
from time import sleep
import json
import scrapeutils.search as search

url = search.construct_search_url(1)
req = request("GET",url)
soup = BeautifulSoup(req.content, "html5lib")
numpages = search.find_pagestring(soup).split(' ')[3]

def parseJSON():
    print("this is where I would parse my JSON, if I had one")
    with open("bedrijven.json", 'r') as bedrijvenFile:
        cache = json.decoder.JSONDecoder().decode(bedrijvenFile.read())
        



def scrape_search_pages(startpage = 1, numpages = 20):
    pageresults = {}
    for current_page in range(startpage,int(numpages)):
        finished = False
        retries = 0
        while(not finished and retries < 3):
            try:
                print(f'scraping page: {current_page}')
                req = request("GET",search.construct_search_url(current_page))
                soup = BeautifulSoup(req.content, "html5lib")
                result = search.scrape_search_page(soup)
                print(result)
                pageresults.append(result)
                finished = True
            except AttributeError:
                print("dat is pech pagina weg")
                sleep(1)
                retries +=1
    with open("bedrijven.json", "w") as bedrijvenFile:
        output = json.dumps(pageresults,indent=1)
        bedrijvenFile.write(output)
        print(output)

# scrape_search_pages(1,20)
parseJSON()