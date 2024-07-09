from datetime import date
from typing import Optional, Self

import pydantic as pd

from rentals.entities.base import Entity
from rentals.entities.entities import Rental, Reservation


class APIReservationRequest(Entity):
    previous: Optional[int] = None
    checkin: date
    checkout: Optional[date] = None


class APIReservationResponse(APIReservationRequest):
    id: int

    @classmethod
    def from_entity(cls, reservation: Reservation) -> Self:
        return cls(
            id=reservation.id,
            previous=reservation.previous,
            checkin=reservation.checkin,
            checkout=reservation.checkout,
        )


class APIRentalRequest(Entity):
    name: str = pd.Field(max_lengh=100)
    reservations: list[APIReservationRequest] = []


class APIRentalResponse(APIRentalRequest):
    id: int
    reservations: list[APIReservationResponse] = []

    @classmethod
    def from_entity(cls, rental: Rental) -> Self:
        return cls(
            id=rental.id,
            name=rental.name,
            reservations=[
                APIReservationResponse.from_entity(reservation)
                for reservation in rental.reservations
            ],
        )
