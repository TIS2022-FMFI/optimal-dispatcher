from django.db import models

class Location(models.Model):
    zip_code = models.CharField(max_length=13,null=False)
    city = models.CharField(max_length=70,null=False)
    country = models.CharField(max_length=4,null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['zip_code', 'city', 'country'], name='unique_location'),
        ]
    
        ordering = ['zip_code']

    def __str__(self):
        return f'{self.zip_code},{self.city},{self.country}'
