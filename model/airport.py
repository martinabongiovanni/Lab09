from dataclasses import dataclass


@dataclass
class Airport:
    ID: int
    IATA_CODE: str
    AIRPORT: str
    CITY: str
    STATE: str
    COUNTRY: str
    LATITUDE: float
    LONGITUDE: float
    TIMEZONE_OFFSET: float


    def __hash__(self):
        return hash(self.ID)

    def __eq__(self, other):
        return self.ID == other.ID