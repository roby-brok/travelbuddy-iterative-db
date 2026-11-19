from django.db import models


class Trip(models.Model):
    destination = models.CharField(max_length=100)
    start_date = models.DateField()
    # Optional, so the trips that are already saved (with no budget) still work
    budget = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.destination} ({self.start_date})"
