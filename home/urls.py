from django.contrib import admin
from django.conf.urls import url
from django.urls import path
from home import views
urlpatterns = [
    # url(r'^home/$',views.greetings),
    # url(r'^home/search$',views.search),
    path('', views.index, name='home'),

    path('greetings', views.greetings, name='greetings'),
    path('search', views.search),

    path('about', views.about, name='about'),
    path('services', views.services, name='services'),
    path('contact', views.contact, name='contact'),
    path('login', views.loginuser, name='login'),
    path('logout', views.logoutuser, name='logout'),
    path('d3js', views.d3js, name='d3js'),
    path('predict', views.predict, name='predict'),

     

    

]
