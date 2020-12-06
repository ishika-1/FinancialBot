from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponse,HttpResponseRedirect
import json
from FinBot import expenseTracker
from django.contrib import messages
from FinBot.forms import UserForm, UserProfileInfoForm
from FinBot.models import UserDetails
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.urls import reverse

# Create your views here.

def homepage (request) :
	return render (request, 'index.html')

def savemessage(request):
	text_response = ""
	user_id = UserDetails.objects.filter(user=request.user)[0].pk
	statement= request.GET['message']
	return HttpResponse (json.dumps(expenseTracker.tracker(statement, user_id)))


def login(request):
	if request.method=='POST':
		uname=request.POST.get('username')
		passw=request.POST.get('password')

		user=authenticate(username=uname,password=passw)
		#We are storing it into a csv file

		if user:
			if user.is_active:
				#After authentication-> user will be true
				print("hi")
				auth_login(request,user)
				return HttpResponseRedirect(reverse('homepage'))
			else:
				return HttpResponse("User is inactive")
		else:
			messages.info(request, 'Sorry, wrong username or password. Please try again.')
			return render(request,'login.html',{'err':'Invalid User Credentials!'})

	else:
		return render(request,'login.html')


def registration(request):
	#here the form-class links the views to the form
	form_class = UserForm
	form = form_class(request.POST)
	if request.method == 'POST':
		# obtains the data of the request 'POST' in our form
		#This form is our inbuilt form
		form = UserForm(data=request.POST)
		#checks for implicit errors
		if form.is_valid():
			#This form refers to the user form which has only the inbuilt fields from the model
			user=form.save()
			#hash the password
			user.set_password(user.password)
			#save
			user.save()
			#For the rest of the details
			name=request.POST.get('name')
			account_balance=request.POST.get('account_balance')
			monthly_income=request.POST.get('monthly_income')
			
			# creating an instance of the model
			b=UserDetails.objects.create(name=name, account_balance=account_balance, monthly_income=monthly_income )
			b.user=user
			b.save()
			
			#save it to a csv
			#After registration we would want to redirect to the login page
			return HttpResponseRedirect(reverse('login'))
		else :
			messages.info(request, '\nSorry, this username already exists. Please try again with a different name.')
			return render(request,'register.html', {'user_form':form})

	#context is a dictionary instance
	#pass the userform as a context
	return render(request,'register.html', {'user_form':form} )


def userlogout(request):
	logout(request)
	#redirect the user
	return HttpResponseRedirect(reverse('login'))


def chart(request):
	user = UserDetails.objects.filter(user=request.user)[0]
	label= ['Housing', 'Transportation','Food', 'Healthcare','Recreation', 'Utilities', 'Miscellaneous']
	data=[user.housing_expenditure,user.transportation_expenditure,user.food_expenditure,
			user.healthcare_expenditure,user.recreation_expenditure,user.utilities_expenditure,
			user.miscellaneous_expenditure]
	return render(request, 'chart.html', {
		'labels': label,
		'data': data
	})