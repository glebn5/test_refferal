from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from string import ascii_letters, digits
import random

# Create your models here.

def generate_random_ivinte_code():
    return "".join(random.choices(ascii_letters + digits, k=6))


class MyUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Phone number is required")
        
        user = self.model(
            phone_number = phone_number,
            **extra_fields
        )

        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, phone_number, password=None, **extra_fields):
            extra_fields.setdefault('is_staff', True)
            extra_fields.setdefault('is_superuser', True)
            return self.create_user(phone_number, password, **extra_fields)
    
    def get_by_natural_key(self, phone_number):
        return self.get(phone_number=phone_number)
    
class User(AbstractBaseUser):
    phone_number = models.CharField(max_length=20, unique=True)
    self_invite_code = models.CharField(unique=True, max_length=6, default=generate_random_ivinte_code)
    target_invite_code = models.CharField(max_length=6)
    invited_by = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='referrals')

    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = MyUserManager()


    def __str__(self):
        return self.phone_number
