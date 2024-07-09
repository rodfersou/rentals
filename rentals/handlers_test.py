import random

from rentals import handlers
from rentals.api.models_factory import (
    APIRentalRequestFactory,
    UpdateAPIRentalRequestFactory,
)
from rentals.repository.repository_test import TestRepository


def test_create_rental():
    payload = APIRentalRequestFactory.build()
    repo = TestRepository()
    rental = handlers.create_rental(payload, repo)
    assert rental.name == payload.name

    payload_reserv = payload.reservations[0]
    reserv = rental.reservations[0]
    assert reserv.checkin == payload_reserv.checkin
    assert reserv.checkout == payload_reserv.checkout


def test_list_rentals():
    repo = TestRepository()

    rentals = []
    for _ in range(3):
        payload = APIRentalRequestFactory.build()
        rentals.append(handlers.create_rental(payload, repo))

    assert handlers.list_rentals(repo) == rentals


def test_get_rentals():
    repo = TestRepository()

    rentals = []
    for _ in range(3):
        payload = APIRentalRequestFactory.build()
        rentals.append(handlers.create_rental(payload, repo))
    rental = random.choice(rentals)

    assert handlers.get_rental(rental.id, repo) == rental


def test_update_rental():
    repo = TestRepository()

    rentals = []
    for _ in range(3):
        payload = APIRentalRequestFactory.build()
        rentals.append(handlers.create_rental(payload, repo))
    rental = random.choice(rentals)

    payload = UpdateAPIRentalRequestFactory.build()
    payload.reservations[0].id = rental.reservations[0].id
    updated = handlers.update_rental(rental.id, payload, repo)

    rental_data = payload.model_dump(exclude_none=True)
    if "name" in rental_data:
        assert updated.name == rental_data["name"]

    reserv_data = rental_data["reservations"][0]
    for key, value in reserv_data.items():
        assert getattr(updated.reservations[0], key) == value


def test_delete_rental():
    repo = TestRepository()

    rentals = []
    for _ in range(3):
        payload = APIRentalRequestFactory.build()
        rentals.append(handlers.create_rental(payload, repo))
    rental = random.choice(rentals)

    assert rental in handlers.list_rentals(repo)
    handlers.delete_rental(rental.id, repo)
    assert rental not in handlers.list_rentals(repo)
