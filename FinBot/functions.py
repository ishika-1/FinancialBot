from FinBot.models import UserDetails

def account_balance(user):
	return user.account_balance

def total_expenditure(user):
	return user.monthly_expenditure

def monthly_savings(user):
	return user.monthly_savings

def housing(user, amount):
	exp = user.monthly_expenditure + amount
	bal = user.account_balance - amount
	hou = user.housing_expenditure + amount
	UserDetails.objects.filter(pk= user.pk).update(monthly_expenditure = exp, account_balance = bal, housing_expenditure = hou)

def transportation(user, amount):
	exp = user.monthly_expenditure + amount
	bal = user.account_balance - amount
	trans = user.transportation_expenditure + amount
	UserDetails.objects.filter(pk= user.pk).update(monthly_expenditure = exp, account_balance = bal, transportation_expenditure = trans)

def food(user, amount):
	exp = user.monthly_expenditure + amount
	bal = user.account_balance - amount
	f = user.food_expenditure + amount
	UserDetails.objects.filter(pk= user.pk).update(monthly_expenditure = exp, account_balance = bal, food_expenditure = f)

def recreation(user, amount):
	exp = user.monthly_expenditure + amount
	bal = user.account_balance - amount
	rec = user.recreation_expenditure + amount
	UserDetails.objects.filter(pk= user.pk).update(monthly_expenditure = exp, account_balance = bal, recreation_expenditure = rec)

def healthcare(user, amount):
	exp = user.monthly_expenditure + amount
	bal = user.account_balance - amount
	hea = user.healthcare_expenditure + amount
	UserDetails.objects.filter(pk= user.pk).update(monthly_expenditure = exp,account_balance = bal, healthcare_expenditure = hea)

def utilities(user, amount):
	exp = user.monthly_expenditure + amount
	bal = user.account_balance - amount
	uti = user.utilities_expenditure + amount
	UserDetails.objects.filter(pk= user.pk).update(monthly_expenditure = exp, account_balance = bal, utilities_expenditure = uti)

def miscellaneous(user, amount):
	print('changed')
	exp = user.monthly_expenditure + amount
	bal = user.account_balance - amount
	misc = user.miscellaneous_expenditure + amount
	UserDetails.objects.filter(pk= user.pk).update(monthly_expenditure = exp, account_balance = bal, miscellaneous_expenditure = misc)
