from django.db import models

class Known_location(models.Model):
    zip_code = models.CharField(max_length=10,null=False)
    city = models.CharField(max_length=70,null=False)
    country = models.CharField(max_length=4,null=False)

    def __str__(self):
        return f'{self.zip_code}, {self.city}, {self.country}'
