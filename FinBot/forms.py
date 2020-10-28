from django import forms
from django.contrib.auth.models import User
from FinBot.models import UserDetails

#Adding features to the form that is going to be rendered
#Purpose of the class Meta: inbuilt class- gives the meta-data
# link to a model-> changes made in the form will be reflected in the form
class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput(attrs={'width':'100%'}))
	class Meta:
		model = User
		fields = ('username' , 'email' , 'password')


class UserProfileInfoForm(forms.ModelForm):
	class Meta:
		model = UserDetails
		fields = ('name','account_balance','monthly_income')
