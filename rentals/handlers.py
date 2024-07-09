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


def list_rentals() -> list[Rental]:
    repo = Repository()
    return repo.list()


def get_rental(rental_id: int) -> Rental:
    repo = Repository()
    return repo.get(rental_id)


def update_rental(rental_id: int, payload: APIRentalRequest) -> Rental:
    repo = Repository()
    return repo.update(
        rental_id,
        payload.dict(exclude_none=True),
    )


def delete_rental(rental_id: int):
    repo = Repository()
    return repo.delete(rental_id=rental_id)
