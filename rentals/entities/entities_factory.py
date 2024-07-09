from polyfactory.factories.pydantic_factory import ModelFactory

from rentals.entities import entities


class ReservationFactory(ModelFactory[entities.Reservation]): ...


class RentalFactory(ModelFactory[entities.Rental]): ...
