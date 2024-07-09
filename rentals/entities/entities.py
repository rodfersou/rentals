from datetime import date
from typing import Optional

import pydantic as pd

from rentals.entities.base import Entity


class Reservation(Entity):
    id: Optional[int] = None
    previous: Optional[int] = None
    checkin: date
    checkout: Optional[date] = None


class Rental(Entity):
    id: Optional[int] = None
    name: str = pd.Field(max_lengh=100)
    reservations: list[Reservation] = []
