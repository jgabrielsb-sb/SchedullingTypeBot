from django.db import models

# Create your models here

class Reservation(models.Model):
    date = models.DateField() 
    period = models.IntegerField()
    reservationCode = models.CharField(max_length=100)

    def __str__(self):
        return f"Reservation on {self.date}, period {self.period}"
    