from enum import unique
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
class Coupon(models.Model):
    code = models.CharField(max_length=20,unique=True)
    startFrom = models.DateTimeField()
    endOn = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
    active = models.BooleanField()

    def __str__(self):
        return self.code