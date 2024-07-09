from rentals.api.models import APIRentalRequest
from rentals.entities.entities import Rental, Reservation
from rentals.repository.repository import Repository


def create_rental(payload: APIRentalRequest) -> Rental:
    repo = Repository()
    reservations = []
    for reserv_api in payload.reservations:
        reserv = Reservation(
            checkin=reserv_api.checkin,
            checkout=reserv_api.checkout,
        )
        reservations.append(reserv)
    rental = Rental(
        name=payload.name,
        reservations=reservations,
    )
    return repo.save(rental)
