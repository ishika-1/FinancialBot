from django.urls import path

from . import views

urlpatterns = [
        path('home', views.homepage, name = 'homepage'),
        path('save_message/',views.savemessage, name='same_messs'),
        path('',views.login,name='login'),
        path('registration/',views.registration,name='registration'),
        path('userlogout/',views.userlogout,name="userlogout"),
        path('chart/',views.chart, name="chart"),
]
