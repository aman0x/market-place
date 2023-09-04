from django.db import models
from django.contrib.auth.models import User


import os

USER_TYPE = (
    ('CUSTOMER', 'Customer'),
    ('WHOLESELLER', 'Wholeseller'),
    ('AGENT', 'Agent'),
    ('ADMIN', 'Admin')
)


class Account(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name='account')
    user_type = models.CharField(
        max_length=11, choices=USER_TYPE, default='ADMIN')
    flat_wing = models.CharField(max_length=200)
    is_active = ()

