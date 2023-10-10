from django.db import models

# Create your models here.
class Journey(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    user_id = models.IntegerField()
    start_date = models.DateTimeField(blank=False)
    end_date = models.DateTimeField(blank=True, null=True)
    is_current = models.BooleanField(default=False)


class Journey_Point:
    journey_id = models.ForeignKey(Journey, on_delete=models.CASCADE, name='points')
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    start_date = models.DateTimeField(blank=False)
    end_date =models.DateTimeField(blank=True, null=True)
    cost = models.FloatField(default=0.00)
    location = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=200, blank=True)
    maps_url = models.URLField(max_length=300, blank=True)
    place_url = models.URLField(max_length=300, blank=True)
    is_selected = models.BooleanField(default=False)


class User_Journey:
    journey_id = models.ForeignKey(Journey, on_delete=models.CASCADE, name='users')
    user_id = models.IntegerField()


def get_models():
    return [
            'journey',
            'journey_point',
            'user_journey',

    ]