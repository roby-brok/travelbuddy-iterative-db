from django.db import models


class Trip(models.Model):
    destination = models.CharField(max_length=100)
    start_date = models.DateField()

    def __str__(self):
        return f"{self.destination} ({self.start_date})"
