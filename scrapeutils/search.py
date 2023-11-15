from bs4 import BeautifulSoup
from bs4 import ResultSet
from requests import request
from time import sleep
from datetime import datetime;
import scrapeutils.datatypes as datatypes

def construct_search_url(page_num):
    return f"https://stagemarkt.nl/leerbedrijven/?Termen=Software+developer+(25604)\
&Land=e883076c-11d5-11d4-90d3-009027dcddb5&ZoekenIn=A\
&Page={page_num}\
&RandomSeed=384\
&Sortering=2\
&Bron=ORG"

def find_pagestring(soup:BeautifulSoup):
    element_pagination = soup.find(name="div", attrs={"class": "s-results-pagination"})
    #remove divs from results
    element_pagination.div.extract()
    #select the span
    span = element_pagination.find('span')
    return span.text    

def select_company_blocks(soup:BeautifulSoup):
    element_company_blocks = soup.find(name="div", attrs={"class": "c-link-blocks"})
    return element_company_blocks

def extract_company_block_data(soup:BeautifulSoup):
    url = soup.attrs.get('href')
    element_c_link_blocks_single_company = soup.find(name='div', attrs={'class':'c-link-blocks-single-company'})
    leerbedrijf_id = element_c_link_blocks_single_company\
        .find(name='p')\
        .contents[2]\
        .split()[2]
    name = soup.find(name='div', attrs={'class':'c-link-blocks-single-info'}).find('h2').text
    return datatypes.Bedrijf(
         name=name,
         leerbedrijf_id=leerbedrijf_id,
         url=url,
         last_scraped= None
    )

def scrape_search_page(soup:BeautifulSoup, mapReference:map):
        company_blocks = select_company_blocks(soup) 
        result_set = company_blocks.find_all(name="a", attrs={"class": "c-link-blocks-single"})
        companies_map = mapReference
        for r in result_set:
            company_block_data = extract_company_block_data(r)
            companies_map[company_block_data.leerbedrijf_id] = company_block_data
        return companies_map