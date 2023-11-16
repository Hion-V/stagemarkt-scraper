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
    detailpane = soup.find("div", {'class':'c-detail-company'})
    list = detailpane.find("ul")
    print(list)
    items = list.find_all('li')
    propdict['adres'] = items[1].text
    postcodeplaats:str = items[2].text.split(" ")
    propdict['postcode'] = f"{postcodeplaats[0]}{postcodeplaats[1]}"
    propdict['plaats'] = postcodeplaats[2]
    propdict['land'] = items[3].text
    for item in items:
        item:BeautifulSoup = item
        match item.contents[0].text.strip():
            case "Tel:":
                propdict['tel'] = item.contents[1].text
                break
            case "Email:":
                propdict['email'] = item.contents[1].text
                break
        print(item)
    print(propdict)


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