from polyfactory.factories.pydantic_factory import ModelFactory

from rentals.api import models


class UpdateAPIReservationRequestFactory(
    ModelFactory[models.UpdateAPIReservationRequest]
): ...


class APIReservationRequestFactory(ModelFactory[models.APIReservationRequest]): ...


class APIReservationResponseFactory(ModelFactory[models.APIReservationResponse]): ...


class UpdateAPIRentalRequestFactory(ModelFactory[models.UpdateAPIRentalRequest]): ...


class APIRentalRequestFactory(ModelFactory[models.APIRentalRequest]): ...


class APIRentalResponseFactory(ModelFactory[models.APIRentalResponse]): ...
