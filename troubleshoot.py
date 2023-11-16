from scrapeutils import datatypes, company, search



aaa = datatypes.Bedrijf.from_json('''{
   "leerbedrijf_id": "100438765",
   "name": "Snappshot",
   "url": "/bedrijven/profiel/snappshot/profiel-8d733453-c4c2-e611-80d1-bb82e25ba0ea",
   "last_scraped": null,
   "profiel": null
  }''')
bbb = company.scroop_profile(aaa)
print(bbb)