# Importamos los modelos
from django.db import models

# Base user manager
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager, models.Manager):

    def _create_user(self, username, email, password, is_staff, is_superuser, is_active, **extra_fields):
        user = self.model(
            username=username,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
            **extra_fields
        )
        # Encriptando la password
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, username, email,  password=None, **extra_fields):
        return self._create_user(username, email, password, False, False,  **extra_fields)

    def create_superuser(self, username, email,  password=None, **extra_fields):
        return self._create_user(
            username,
            email,
            password,
            is_staff=True,
            is_superuser=True,
            is_active=True,
            ** extra_fields
        )

    def code_validation(self, id_user, code_registro):
        if self.filter(id=id_user, code_registro=code_registro).exists():
            return True
        else:
            return False
