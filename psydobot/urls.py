"""psydobot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib import admin

from prediction import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('login_1/',views.login_1, name='login_1'),
    path('signup/',views.signup, name='signup'),
    path('admin/',admin.site.urls),
    path('home/',views.home,name='home'),
    path('stress/',views.stress,name='stress'),
    path('low_stress/',views.lowstress,name='low_stress'),
    path('high_stress/',views.highstress,name='high_stress'),
    path('moderate_stress/',views.moderatestress,name='moderate_stress'),
    path('map/',views.map,name='map'),
    path('chatbot/',views.chatbot,name='chatbot'),
]