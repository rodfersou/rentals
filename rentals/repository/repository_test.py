from copy import deepcopy

from rentals.entities.entities import Rental, Reservation
from rentals.entities.entities_factory import RentalFactory, ReservationFactory
from rentals.repository.repository import AbstractRepository


class TestRepository(AbstractRepository):
    __test__ = False

    def __init__(self, data: list = None):
        if data is None:
            data = []
        self._last_rental = 0
        self._last_reserv = 0
        for rental_data in data:
            self._fill_ids(rental_data)
        rentals_data = {}
        for rental_data in data:
            reservs_data = {}
            for reserv_data in rental_data.get("reservations", []):
                reservs_data[reserv_data["id"]] = reserv_data
            rental_data["reservations"] = reservs_data
            rentals_data[rental_data["id"]] = rental_data
        self._data = rentals_data

    def _fill_ids(self, rental_data: dict) -> dict:
        if "id" not in rental_data:
            self._last_rental += 1
            rental_data["id"] = self._last_rental
        reserv_data = {}
        for reserv_data in rental_data.get("reservations", []):
            if "id" in reserv_data:
                continue
            self._last_reserv += 1
            reserv_data["id"] = self._last_reserv
        self._last_rental = rental_data["id"]
        self._last_reserv = reserv_data.get("id", 0)
        return rental_data

    def save(self, rental: Rental) -> Rental:
        rental_data = rental.model_dump(exclude_none=True)
        rental_data = self._fill_ids(rental_data)
        rental = Rental(**rental_data)
        reservs_data = {}
        for reserv_data in rental_data.get("reservations", []):
            reservs_data[reserv_data["id"]] = reserv_data
        rental_data["reservations"] = reservs_data
        self._data[rental_data["id"]] = rental_data
        return rental

    def list(self) -> list[Rental]:
        data = deepcopy(self._data)
        rentals = []
        for rental_data in data.values():
            rental_data["reservations"] = [*rental_data["reservations"].values()]
            rental = Rental(**rental_data)
            rentals.append(rental)
        return rentals

    def get(self, rental_id: int) -> Rental:
        rental_data = deepcopy(self._data[rental_id])
        rental_data["reservations"] = [*rental_data["reservations"].values()]
        return Rental(**rental_data)

    def update(self, rental_id: int, fields: dict) -> Rental:
        rental = self.get(rental_id)
        if name := fields.get("name"):
            rental.name = name
        reserv_fields = {
            reserv["id"]: reserv for reserv in fields.get("reservations", [])
        }
        for reserv in rental.reservations:
            if reserv.id not in reserv_fields:
                continue
            for key, value in reserv_fields[reserv.id].items():
                setattr(reserv, key, value)
        return self.save(rental)

    def delete(
        self,
        rental_id: int | None = None,
        reservation_id: int | None = None,
    ):
        if rental_id is None and reservation_id is None:
            return
        if rental_id is not None:
            del self._data[rental_id]
            return
        if reservation_id is not None:
            for rental in self._data.values():
                if reservation_id not in rental["reservations"]:
                    continue
                del self._data[rental["id"]]["reservations"][reservation_id]
            return


def test_save():
    repo = TestRepository()
    assert repo._data == {}
    rental = RentalFactory.build()
    rental = repo.save(rental)
    assert repo.get(rental.id) == rental


def test_list():
    repo = TestRepository()
    assert repo.list() == []
    rental = RentalFactory.build()
    rental = repo.save(rental)
    assert repo.list() == [rental]


def test_get():
    rental = RentalFactory.build(id=1)
    repo = TestRepository(data=[rental.model_dump()])
    assert repo.get(rental.id) == rental


def test_update():
    rental = RentalFactory.build(id=1, reservations=[ReservationFactory.build(id=1)])
    repo = TestRepository(data=[rental.model_dump()])
    expected = {**rental.model_dump(), "name": "foo"}
    assert repo.update(1, {"name": "foo"}) == Rental(**expected)

    rental = repo.update(1, {"reservations": [{"id": 1, "checkin": "2024-07-09"}]})
    reserv = rental.reservations[0]
    expected = {**reserv.model_dump(), "checkin": "2024-07-09"}
    assert reserv == Reservation(**expected)


def test_delete():
    rental = RentalFactory.build(id=1, reservations=[ReservationFactory.build(id=1)])
    repo = TestRepository(data=[rental.model_dump()])
    assert repo.get(1) == rental

    repo.delete(reservation_id=1)
    del rental.reservations[0]
    assert repo.get(1) == rental

    repo.delete(rental_id=1)
    assert repo.list() == []
