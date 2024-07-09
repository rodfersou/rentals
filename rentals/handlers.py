from rentals.api.models import APIRentalRequest, UpdateAPIRentalRequest
from rentals.entities.entities import Rental, Reservation
from rentals.repository.repository import AbstractRepository, Repository


def create_rental(
    payload: APIRentalRequest,
    repo: AbstractRepository | None = None,
) -> Rental:
    if repo is None:
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


def list_rentals(repo: AbstractRepository | None = None) -> list[Rental]:
    if repo is None:
        repo = Repository()
    return repo.list()


def get_rental(
    rental_id: int,
    repo: AbstractRepository | None = None,
) -> Rental:
    if repo is None:
        repo = Repository()
    return repo.get(rental_id)


def update_rental(
    rental_id: int,
    payload: UpdateAPIRentalRequest,
    repo: AbstractRepository | None = None,
) -> Rental:
    if repo is None:
        repo = Repository()
    return repo.update(
        rental_id,
        payload.model_dump(exclude_none=True),
    )


def delete_rental(
    rental_id: int,
    repo: AbstractRepository | None = None,
):
    if repo is None:
        repo = Repository()
    return repo.delete(rental_id=rental_id)
