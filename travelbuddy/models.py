from django.db import models


class Trip(models.Model):
    start_date = models.DateField()
    # Optional, so the trips that are already saved (with no budget) still work
    budget = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    # city and country replace the old destination field (see migrations 0003-0005)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.city} ({self.start_date})"
