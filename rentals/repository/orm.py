from django.db import models
from django.forms.models import model_to_dict


class Model(models.Model):
    to_dict = model_to_dict

    def __str__(self):
        return " | ".join(
            f"{k}={v}" for k, v in self.to_dict().items() if not k.startswith("_")
        )

    class Meta:
        abstract = True


class Rental(Model):
    name = models.CharField(max_length=100)


class Reservation(Model):
    previous = models.ForeignKey(
        "Reservation", on_delete=models.CASCADE, blank=True, null=True
    )
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    checkin = models.DateField(null=True, blank=True)
    checkout = models.DateField(null=True, blank=True)
