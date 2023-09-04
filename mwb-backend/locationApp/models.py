from django.db import models


class State(models.Model):
    state = models.CharField(max_length=30, default=None, unique=True)

    def __str__(self):
        return self.state
    
class District(models.Model):
    district=models.CharField(max_length=30,null=True,default=None, unique=True)
    state=models.ForeignKey(
        State, on_delete=models.CASCADE, related_name='state_district')
    
    def __str__(self):
        return self.district


class City(models.Model):
    city = models.CharField(max_length=30, null=True,
                            default=None, unique=True)
    state=models.ForeignKey(
        State, on_delete=models.CASCADE, related_name='state_district_city')
    district=models.ForeignKey(
        District, on_delete=models.CASCADE, related_name='district_city')
    
    def __str__(self):
        return self.city
