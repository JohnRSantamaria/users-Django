from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


# Managers
from .managers import UserManager
# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):

    GENDER_CHOISES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('X', 'Otros'),
    )

    username = models.CharField(
        'Nombre de adminstrador',
        max_length=10,
        unique=True
    )
    email = models.EmailField(max_length=254)
    nombres = models.CharField(max_length=50, blank=True)
    apellidos = models.CharField(max_length=50, blank=True)
    genero = models.CharField(
        max_length=1,
        choices=GENDER_CHOISES,
        blank=True
    )

    USERNAME_FIELD = 'username'
    objects = UserManager()

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return f"{self.nombres} {self.apellidos}"
