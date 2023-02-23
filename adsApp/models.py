from django.db import models


commission_choice=(
    ("FIXED","Fixed"),
    ("PERCENTAGE","Percentage")
)
class Referral(models.Model):
    referred_by=models.CharField(max_length=100,default=None,null=True)
    commission=models.CharField(max_length=20,choices=commission_choice,default="Percentage")
    enter_percentage=models.CharField(max_length=20,default=None,null=True)

class Selectstate(models.Model):
    state_name=models.CharField(max_length=30,default=None,null=True)
    city_name=models.CharField(max_length=30,default=None,null=True)

class Ads(models.Model):
    ad_title=models.CharField(max_length=50,default=None,null=True)
    select_state=models.ManyToManyField(Selectstate,related_name="select_state")
    created_for=models.CharField(max_length=50,null=True,default=None)
    start_date=models.DateField(auto_now=False)
    start_time=models.TimeField(auto_now_add=False)
    choose_plan=models.CharField(max_length=50,default=True,null=True)
    gst=models.CharField(max_length=20,default=None,null=True)
    media=models.ImageField(upload_to="images/agent/",null=True)
    referral=models.ForeignKey(Referral,on_delete=models.CASCADE)
