from django.db import models


class State(models.Model):
    state=models.CharField(max_length=30,default=None)

class District(models.Model):
    district=models.CharField(max_length=30,null=True,default=None)
    state=models.ForeignKey(
        State, on_delete=models.CASCADE, related_name='state_district')
    
    def __str__(self):
        return self.state

class City(models.Model):
    city=models.CharField(max_length=30,null=True,default=None)
    state=models.ForeignKey(
        State, on_delete=models.CASCADE, related_name='state_district_city')
    district=models.ForeignKey(
        District, on_delete=models.CASCADE, related_name='district_city')
