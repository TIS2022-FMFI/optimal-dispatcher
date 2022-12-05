from django.db import models
from known_locations_management.models import Known_location


class Branch(models.Model):
    name = models.CharField(max_length=70,null=False,unique=True)
    location = models.ForeignKey(Known_location,on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f'{self.name}, {self.location}'
