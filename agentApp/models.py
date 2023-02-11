# Create your models here.
from django.db import models


class Agent(models.Model):
    agent_description = models.TextField(blank=True, null=True)
    agent_name = models.CharField(max_length=200)
    is_active = ()
