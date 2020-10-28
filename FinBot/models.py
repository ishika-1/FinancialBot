from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserDetails (models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)
	name = models.CharField(max_length = 30)
	monthly_income = models.IntegerField()
	account_balance = models.IntegerField()
	monthly_savings = models.IntegerField(default=0)
	monthly_expenditure = models.IntegerField(default = 0)
	housing_expenditure = models.IntegerField(default = 0)
	transportation_expenditure = models.IntegerField(default = 0)
	food_expenditure = models.IntegerField(default = 0)
	healthcare_expenditure = models.IntegerField(default = 0)
	recreation_expenditure = models.IntegerField(default = 0)
	utilities_expenditure = models.IntegerField(default = 0)
	miscellaneous_expenditure = models.IntegerField(default = 0)
	date = models.DateField(auto_now = True)