from django.db import models

Status_Choice=(
    ("ACTIVE",'Active'),
    ('EXPIRED','Expired')
)
class Ads(models.Model):
    Ad_Name=models.CharField(max_length=50,default=None,null=True)
    Start_Date=models.DateTimeField(auto_now_add=False)
    End_Date=models.DateTimeField(auto_now_add=False)
    Created_for=models.CharField(max_length=50,default=None,null=True)
    Active_for=models.CharField(max_length=50,default=None,null=True)
    Status=models.CharField(max_length=20,choices=Status_Choice,default="Active")
