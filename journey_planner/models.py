from django.db import models

# Create your models here.
class Journey(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True)
    start_date = models.DateTimeField(blank=False)
    end_date = models.DateTimeField(blank=False)
    is_current = models.BooleanField(default=False)
    location = models.CharField(blank=True, max_length=30)

class Status(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return  self.name


class Journey_Point(models.Model):
    journey_id = models.ForeignKey(Journey, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300,blank=True)
    start_date = models.DateTimeField(blank=False)
    end_date =models.DateTimeField(blank=False)
    cost = models.FloatField(default=0.00)
    location = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=200, blank=True)
    maps_url = models.URLField(max_length=300, blank=True)
    place_url = models.URLField(max_length=300, blank=True)
    is_selected = models.BooleanField(default=False)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)


class User_Journey(models.Model):
    journey_id = models.ForeignKey(Journey, on_delete=models.CASCADE)
    user_id = models.IntegerField()







def get_models():
    return [
            'journey',
            'journey_point',
            'user_journey',
        'status',

    ]