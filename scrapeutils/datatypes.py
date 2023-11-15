from dataclasses import dataclass, astuple, asdict
from dataclasses_json import dataclass_json
from typing import Optional
from datetime import datetime, timedelta



@dataclass_json()
@dataclass(frozen=False)
class BedrijfProfiel:
    leerbedrijf_id: str
    naam: str
    kvk_naam: str
    kvk_nummer: str
    kvk_vestigingsnummer: str
    bedrijfsindeling: str
    telefoon: str
    bedrijfsgrootte: str
    capaciteit: str

@dataclass_json
@dataclass(frozen=False)
class Bedrijf:
    leerbedrijf_id: str
    name: str
    url: str
    last_scraped: datetime
    profiel:Optional[BedrijfProfiel] = None
    

@dataclass_json
@dataclass(frozen=False)
class BedrijfIndex:
    bedrijf_dict:dict[str, Bedrijf]