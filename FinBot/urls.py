from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls import url

from . import views

urlpatterns = [
	path('home', views.homepage, name = 'homepage'),
	path('save_message/',views.savemessage, name='same_messs'),
	path('',views.login,name='login'),
	path('registration/',views.registration,name='registration'),
	path('userlogout/',views.userlogout,name="userlogout"),
	path('chart/',views.chart, name="chart"),
	url(r'^password_reset/$', auth_views.PasswordResetView.as_view(),
		{'template_name': "registration/password_reset_form.html"}, name='password_reset'),
	url(r'^password_reset/done/$',auth_views.PasswordResetDoneView.as_view(),
		{'template_name': "registration/password_reset_done.html"}, name='password_reset_done'),
	path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm',),
	#url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.PasswordResetConfirmView.as_view(),
	#	{'template_name': "registration/password_reset_confirm.html"}, name='password_reset_confirm'),
	url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(),
		{'template_name': "registration/password_reset_complete.html"}, name='password_reset_complete'),
]
