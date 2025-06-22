from dataclasses import dataclass


@dataclass
class Airline:
    ID: int
    IATA_CODE: str
    AIRLINE: str