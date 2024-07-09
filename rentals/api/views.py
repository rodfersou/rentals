from ninja import NinjaAPI

from rentals import handlers
from rentals.api.models import (
    APIRentalRequest,
    APIRentalResponse,
    UpdateAPIRentalRequest,
)

api = NinjaAPI()


@api.post("/rentals")
def create_rental(request, payload: APIRentalRequest) -> APIRentalResponse:
    rental = handlers.create_rental(payload)
    return rental.dict()


@api.get("/rentals")
def list_rentals(request) -> list[APIRentalResponse]:
    return [rental.dict() for rental in handlers.list_rentals()]


@api.get("/rentals/{rental_id}")
def get_rental(request, rental_id: int) -> APIRentalResponse:
    rental = handlers.get_rental(rental_id)
    return rental.dict()


@api.patch("/rentals/{rental_id}")
def update_rental(
    request,
    rental_id: int,
    payload: UpdateAPIRentalRequest,
) -> APIRentalResponse:
    rental = handlers.update_rental(rental_id, payload)
    return rental.dict()


@api.delete("/rentals/{rental_id}")
def delete_rental(request, rental_id: int):
    handlers.delete_rental(rental_id)
