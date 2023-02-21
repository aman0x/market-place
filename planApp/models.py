from django.db import models
from bazaarApp.models import Bazaar




ADD_PLAN_CHOICE=(
    ("FREE",'free'),
    ("PAID","paid")
)

class AddPlan(models.Model):
    Add_New_Plan=models.CharField(max_length=50,choices=ADD_PLAN_CHOICE,default="PAID")


class PlanPaid(models.Model):
    First_name=models.CharField(max_length=50,default=None,null=True)
    Amount=models.IntegerField()
    User_per_branch=models.IntegerField()


class Plan(models.Model):
    ADD_new_plan=models.ForeignKey(AddPlan,on_delete=models.CASCADE)
    plan_paid=models.ForeignKey(PlanPaid,on_delete=models.CASCADE)
    Plan_Title=models.CharField(max_length=50,default=None,null=True)
    Start_Time=models.DateTimeField(auto_now_add=False)
    End_Time=models.DateTimeField(auto_now_add=False)
    Branches=models.IntegerField()
    bazaar=models.ForeignKey(Bazaar,on_delete=models.CASCADE)
    state=models.CharField(max_length=50,default=None,null=True)
    District=models.CharField(max_length=50,default=None,null=True)
    City=models.CharField(max_length=50,default=None,null=True)
    Price=models.CharField(max_length=50,default=None,null=True)




