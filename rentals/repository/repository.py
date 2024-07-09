import abc
from datetime import date

from django.db import transaction

from rentals.entities.entities import Rental, Reservation
from rentals.repository import orm


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def save(self, rental: Rental) -> Rental:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> list[Rental]:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, rental_id: int) -> Rental:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, rental_id: int, fields: dict) -> Rental:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(
        self,
        rental_id: int | None = None,
        reservation_id: int | None = None,
    ):
        raise NotImplementedError


class Repository(AbstractRepository):
    def _from_db(
        self, rental_db: orm.Rental, reservations_db: list[orm.Reservation]
    ) -> Rental:
        reservations = []
        prev = None
        for reserv_db in reservations_db:
            reserv = Reservation(
                id=reserv_db.id,
                previous=prev.id if prev else None,
                checkin=reserv_db.checkin,
                checkout=reserv_db.checkout,
            )
            reservations.append(reserv)
            prev = reserv_db
        return Rental(
            id=rental_db.id,
            name=rental_db.name,
            reservations=reservations,
        )

    def _to_db(self, rental: Rental) -> tuple[orm.Rental, list[orm.Reservation]]:
        rental_db = orm.Rental(
            id=rental.id,
            name=rental.name,
        )
        reservations_db = [
            orm.Reservation(
                id=reserv.id,
                rental=rental_db,
                checkin=reserv.checkin,
                checkout=reserv.checkout,
            )
            for reserv in rental.reservations
        ]
        return rental_db, reservations_db

    def save(self, rental: Rental) -> Rental:
        with transaction.atomic():
            rental_db, reservations_db = self._to_db(rental)
            rental_db.save()
            for reserv_db in reservations_db:
                reserv_db.save()
            return self._from_db(rental_db, reservations_db)

    def list(self) -> list[Rental]:
        rentals = []
        for rental_db in orm.Rental.objects.all():
            reservations_db = orm.Reservation.objects.filter(rental__id=rental_db.id)
            rentals.append(self._from_db(rental_db, reservations_db))
        return rentals

    def get(self, rental_id: int) -> Rental:
        rental_db = orm.Rental.objects.get(id=rental_id)
        reservations_db = orm.Reservation.objects.filter(rental__id=rental_db.id)
        return self._from_db(rental_db, reservations_db)

    def update(self, rental_id: int, fields: dict) -> Rental:
        with transaction.atomic():
            rental_db = orm.Rental.objects.get(id=rental_id)
            if name := fields.get("name"):
                rental_db.name = name
            rental_db.save()
            reservations_db = []
            for reserv_fields in fields["reservations"]:
                reserv_id = reserv_fields.get("id")
                if not reserv_id:
                    reserv_db = orm.Reservation(checkin=date.today())
                else:
                    reserv_db = orm.Reservation.objects.get(
                        id=reserv_id, rental=rental_db
                    )
                reserv_db = orm.Reservation.objects.get(id=reserv_id, rental=rental_db)
                for key, value in reserv_fields.items():
                    setattr(reserv_db, key, value)
                reserv_db.save()
                reservations_db.append(reserv_db)
            return self._from_db(rental_db, reservations_db)

    def delete(
        self,
        rental_id: int | None = None,
        reservation_id: int | None = None,
    ):
        if rental_id is None and reservation_id is None:
            return
        with transaction.atomic():
            if rental_id is not None:
                rental_db = orm.Rental.objects.get(id=rental_id)
                rental_db.delete()
                return
            if reservation_id is not None:
                reserv_db = orm.Reservation.objects.get(id=reservation_id)
                reserv_db.delete()
                return
