from django.db import models
from user_management.models import MyUser


class Location(models.Model):
    zip_code = models.CharField(max_length=10, null=False)
    city = models.CharField(max_length=70, null=False)
    country = models.CharField(max_length=4, null=False)

    def __str__(self):
        return self.zip_code + "," + self.city + "," + self.country

     
class Transportations(models.Model):
    owner_id = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=False)
    from_id = models.ForeignKey(Location,related_name='from_id',on_delete=models.CASCADE,null=False)
    to_id = models.ForeignKey(Location,related_name='to_id',on_delete=models.CASCADE,null=False)
    departure_time = models.DateTimeField(null=False)
    ldm = models.FloatField(null=False)
    weight = models.FloatField(null=False)
    info = models.TextField(null=True)

    def __str__(self):
        return f'owner_id : {id}'



