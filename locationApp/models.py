from django.db import models


class State(models.Model):
    state=models.CharField(max_length=30,default=None)

class City(models.Model):
    city=models.CharField(max_length=30,null=True,default=None)

class District(models.Model):
    district=models.CharField(max_length=30,null=True,default=None)

