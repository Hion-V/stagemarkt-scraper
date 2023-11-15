from bs4 import BeautifulSoup
from scrapeutils.datatypes import Bedrijf, BedrijfProfiel
from requests import request

def construct_company_url(relative_url:str):
    return f"https://stagemarkt.nl{relative_url}"

def scroop_profile(bedrijf:Bedrijf):
    url = construct_company_url(bedrijf.url)
    req = request("GET", url)
    soup = BeautifulSoup(req.content, "html5lib")
    list = soup.find("ul", attrs:={'class':"c-company__info__list u-reset-ul"})
    propdict = {}
    for item in list.find_all("li"):
        spans:list[BeautifulSoup] = item.find_all("span")
        key:str = spans[0].text.strip()
        key = key.lower()
        key = key.replace(" ","_")
        value = spans[1].text.strip()
        propdict[key] = value
    # print(propdict)
    return BedrijfProfiel(
        leerbedrijf_id=propdict.get("leerbedrijf_id"),
        naam=propdict.get("leerbedrijf_id"),
        kvk_naam=propdict.get("kvk_naam"),
        kvk_nummer=propdict.get("kvk_nummer"),
        kvk_vestigingsnummer=propdict.get("kvk_vestigingsnummer"),
        capaciteit=propdict.get("totale_capaciteit"),
        bedrijfsindeling=propdict.get("bedrijfsindeling"),
        telefoon=propdict.get("telefoon"),
        bedrijfsgrootte=propdict.get("bedrijfsgrootte")
    )