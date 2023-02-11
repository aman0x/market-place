# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Bazaar(models.Model):
    bazaar_description = models.TextField(blank=True, null=True)
    bazaar_name = models.CharField(max_length=200, null=True)
    bazaar_state = models.CharField(max_length=200, null=True)
    bazaar_district = models.CharField(max_length=200, null=True)
    bazaar_city = models.CharField(max_length=200, null=True)
    bazaar_image = models.ImageField(upload_to='images/', null=True)
    is_active = ()

    def username(self):
        return self.user.username
