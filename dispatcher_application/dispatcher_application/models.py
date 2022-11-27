from django.db import models


class Location:
    zip_code = models.CharField(max_length=10, null=False)
    city = models.CharField(max_length=70, null=False)
    country = models.CharField(max_length=4, null=False)

    def __str__(self):
        return self.zip_code + "," + self.city + "," + self.country


class Branch:
    location = models.ForeignKey(Location,on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.location

class Users(models.Model):
    first_name = models.CharField(max_length=60,null=False)
    last_name = models.CharField(max_length=60,null=False)
    email = models.CharField(max_length=60,null=False)
    branch_id = models.ForeignKey(Branch,on_delete=models.CASCADE,null=False)
    superuser = models.BooleanField(default=False,null=False)

    def __str__(self):
        return self.email + " admin: " + self.superuser 

class Transportations(models.Model):
    owner_id = models.ForeignKey(Users,on_delete=models.CASCADE,null=False)
    from_id = models.ForeignKey(Location,on_delete=models.CASCADE,null=False)
    to_id = models.ForeignKey(Location,on_delete=models.CASCADE,null=False)
    departure_time = models.DateTimeField(auto_now_add=True,null=False)
    idm = models.FloatField(min=0,max=100,null=False)
    weight = models.FloatField(min=0,max=100000,null=False)
    info = models.TextField(max_length=350,blank=True,null=True)

    def __str__(self):
        return id

class Groups:
    group_name = models.CharField(max_length=40,null=False)

    def __str__(self):
        return self.group_name

class Group_access:
    group_id = models.ForeignKey(Groups,on_delete=models.CASCADE,null=False) 
    user_id = models.ForeignKey(Users,on_delete=models.CASCADE,null=False) 


class Access_groups:
    group_id = models.ForeignKey(Groups,on_delete=models.CASCADE,null=False)
    branch_id = models.ForeignKey(Branch,on_delete=models.CASCADE,null=False)
    write_access = models.BooleanField(default=False,null=False)


class User_access:
    group_id = models.ForeignKey(Groups,on_delete=models.CASCADE,null=False)
    branch_id = models.ForeignKey(Branch,on_delete=models.CASCADE,null=False)
    write_access = models.BooleanField(default=False)


class Known_locations:
    zip_code = models.CharField(max_length=10,null=False)
    city = models.CharField(max_length=70,null=False)
    country = models.CharField(max_length=4,null=False)

    def __str__(self):
        return self.zip_code + "," + self.city + "," + self.country
