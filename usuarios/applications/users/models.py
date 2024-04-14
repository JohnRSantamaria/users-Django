from django.db import models

from django.contrib.auth.models import AbstractBaseUser

# Create your models here.


class User(AbstractBaseUser):

    GENDER_CHIOSES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('X', 'Otros'),
    )

    username = models.CharField('usuarios', max_length=10, unique=True)
    email = models.EmailField(max_length=254)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    genero = models.CharField(
        max_length=1,
        choices=GENDER_CHIOSES,
        blank=True
    )

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return f"{self.nombres} {self.apellidos}"
    
