from django.db import models
from userauth.models import User


# Create your models here.

class Flat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    phone_number = models.CharField(max_length=13)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    people = models.IntegerField()
    room_count = models.IntegerField()
    price_per_person = models.IntegerField()
    long = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)  # longitude
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)  # latitude
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    has_wifi = models.BooleanField(default=False)
    has_ac = models.BooleanField(default=False)
    has_contract = models.BooleanField(default=False)
    has_parking = models.BooleanField(default=False)


class Image(models.Model):
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE)
    image = models.FileField(upload_to='flats/')


class Comment(models.Model):
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE)
    comment = models.TextField
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
