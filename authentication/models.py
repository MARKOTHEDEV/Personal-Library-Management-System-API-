from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password, **other_fields):
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            **other_fields
        )
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self, email, password, **other_fields):

        user = self.create_user(email, password, **other_fields)
        user.is_staff =True
        user.is_admin =True
        user.is_active=True
        user.is_superuser =True
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255,default='')
    last_name = models.CharField(max_length=255,default='')
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now = True, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS= ["first_name", "last_name",]

    objects = UserManager()


    @property
    def full_name(self):
          return f'{self.first_name} {self.last_name}'