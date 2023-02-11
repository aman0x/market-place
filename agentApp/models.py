# Create your models here.
from django.db import models

AGENT_TYPE = (
    ("INDIVIDUAL", "Individual"),
    ("AGENCY", "Agency"),
    ("SALESMAN", "Salesman"),
)

class Agent(models.Model):
    
    agent_description = models.TextField(blank=True, null=True)
    agent_name = models.CharField(max_length=200)
    agent_type = models.CharField(max_length=11,
                  choices=AGENT_TYPE,
                  default="INDIVIDUAL"
                )
    agent_state = models.CharField(max_length=200, null=True)
    agent_district = models.CharField(max_length=200, null=True)
    agent_city = models.CharField(max_length=200, null=True)
    agent_image = models.ImageField(upload_to='images/agent/', null=True)
    is_active = ()
