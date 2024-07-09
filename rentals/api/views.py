from ninja import NinjaAPI

from rentals import handlers
from rentals.api.models import APIRentalRequest

api = NinjaAPI()


@api.post("/rentals")
def create_rental(request, payload: APIRentalRequest) -> dict:
    rental = handlers.create_rental(payload)
    return {
        "message": "Rental successfully created!",
        "rental": [
            rental.dict(),
        ],
    }
