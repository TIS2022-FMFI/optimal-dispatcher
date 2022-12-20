from django.db import models


class Branch(models.Model):
    name = models.CharField(max_length=70,null=False,unique=True)

    def __str__(self):
        return self.name

