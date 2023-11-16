from bs4 import BeautifulSoup
from requests import request
from time import sleep

import json
import scrapeutils.search as search
import scrapeutils.company as company
import pathlib
import json
import scrapeutils.datatypes as datatypes
from scrapeutils.datatypes import Bedrijf, BedrijfIndex, BedrijfProfiel
from datetime import datetime, timedelta
from pytz import utc

url = search.construct_search_url(1)
req = request("GET", url)
soup = BeautifulSoup(req.content, "html5lib")
numpages = search.find_pagestring(soup).split(" ")[3]

outdir = pathlib.Path("./output")
print(f"outputting to {outdir.absolute()}")


def parseJSON():
    print("this is where I would parse my JSON, if I had one")
    with open(outdir / "bedrijven.json", "r") as bedrijvenFile:
        cache: BedrijfIndex = BedrijfIndex.from_json(bedrijvenFile.read())
        return cache


def writefile(data: BedrijfIndex):
    with open(outdir / "bedrijven.json", "w") as bedrijvenFile:
        # output = json.dumps(pageresults, indent=1,cls=EnhancedJSONEncoder)
        # output = json.dumps(pageresults, indent=1)
        output = data.to_json(indent=1)
        bedrijvenFile.write(output)
        # print(output)


def scrape_search_pages(startpage=1, numpages=20):
    pageresults = {}
    for current_page in range(startpage, int(numpages)):
        finished = False
        retries = 0
        while not finished and retries < 3:
            try:
                print(f"scraping page: {current_page}")
                req = request("GET", search.construct_search_url(current_page))
                soup = BeautifulSoup(req.content, "html5lib")
                result = search.scrape_search_page(soup, pageresults)
                # print(result)
                pageresults = result
                finished = True
            except AttributeError:
                print("dat is pech pagina weg")
                print(search.construct_search_url(current_page))
                sleep(1)
                retries += 1
    bedrijf_index = BedrijfIndex(pageresults)
    writefile(bedrijf_index)
    return bedrijf_index


cache = parseJSON()
result = scrape_search_pages(1, numpages=numpages)

newdict: dict[str, Bedrijf] = {}


rescrape_expiry = utc.localize(datetime.now() - timedelta(hours=0))


for bedrijf_id in result.bedrijf_dict:
    bedrijf: Bedrijf = result.bedrijf_dict.get(bedrijf_id)
    cachedBedrijf = cache.bedrijf_dict.get(bedrijf_id)
    # print(bedrijf)
    # print(cachedBedrijf)
    if cachedBedrijf == None:
        newdict[bedrijf_id] = bedrijf
        print("not cached")
    else:
        print("cached")
        newdict[bedrijf_id] = cachedBedrijf

    if newdict[bedrijf_id].profiel != None and newdict[bedrijf_id].last_scraped != None:
        if(newdict[bedrijf_id].last_scraped > rescrape_expiry):
            print("cached bedrijf niet expired, skipping scrape")
            continue
    finished = False
    retries = 0
    while not finished and retries < 3:
            try:
                newdict[bedrijf_id].profiel = company.scroop_profile(newdict[bedrijf_id])
                newdict[bedrijf_id].last_scraped = utc.localize(datetime.now())
                print(newdict[bedrijf_id])
                finished = True
            except AttributeError:
                print("dat is pech bedrijfpagina weg, retry")
                sleep(1)
                retries += 1


# print(newdict)
writefile(BedrijfIndex(newdict))
