from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from branch_management.models import Branch

class CustomUserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, branch, password, **other_fields):
        if not email:
            raise ValueError('User must have an email')

        if not first_name:
            raise ValueError('User must have a first name')

        if not last_name:
            raise ValueError('User must have a last name')

        if not branch:
            raise ValueError('User must have a branch')

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, branch=branch, **other_fields)

        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, email, first_name, last_name, branch, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')

        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True')

        return self.create_user(email, first_name, last_name, branch, password, **other_fields)



class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=60, unique=True)
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE,null=False)
    is_staff = models.BooleanField(default=True) 
    is_superuser = models.BooleanField(default=False)
    # is_active = models.BooleanField(default=True)
    

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'branch']

    def __str__(self):
        return f'{self.email}, {self.last_name} {self.first_name}, admin: {self.is_superuser}'


