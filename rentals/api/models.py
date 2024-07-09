from datetime import date
from typing import Optional

import pydantic as pd

from rentals.entities.base import Entity


class UpdateAPIReservationRequest(Entity):
    id: int
    checkin: Optional[date] = None
    checkout: Optional[date] = None


class APIReservationRequest(Entity):
    checkin: date
    checkout: Optional[date] = None


class APIReservationResponse(APIReservationRequest):
    id: int
    previous: Optional[int] = None


class UpdateAPIRentalRequest(Entity):
    name: Optional[str] = pd.Field(max_lengh=100, default=None)
    reservations: list[UpdateAPIReservationRequest] = []


class APIRentalRequest(Entity):
    name: str = pd.Field(max_lengh=100)
    reservations: list[APIReservationRequest] = []


class APIRentalResponse(APIRentalRequest):
    id: int
    reservations: list[APIReservationResponse] = []
