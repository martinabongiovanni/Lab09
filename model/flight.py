from dataclasses import dataclass
from datetime import datetime


@dataclass
class Flight:
    ID: int
    AIRLINE_ID: int
    FLIGHT_NUMBER: int
    TAIL_NUMBER: str
    ORIGIN_AIRPORT_ID: int
    DESTINATION_AIRPORT_ID: int
    SCHEDULED_DEPARTURE_DATE: datetime
    DEPARTURE_DELAY: int
    ELAPSED_TIME: int
    DISTANCE: int
    ARRIVAL_DATE: datetime
    ARRIVAL_DELAY: int
