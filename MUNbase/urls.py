"""munbase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings # to import static in deployment
from django.conf.urls.static import static # to import static in deployment

urlpatterns = [
    #homepages
    path("", views.home, name="home"),
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path("featured", views.featured, name="featured"),
    path("tnc", views.tnc, name="tnc"),
    path("logout", views.logout, name="logout"),
    #account settings
    path("settings", views.settings, name="settings"),
    #experience
    path("experience", views.exp, name="exp"),
    path("addexperience", views.getexp, name="getexp"),
    #view Delegate
    path("view/delegate/<str:dele>", views.viewdel, name="viewdel"),
    #search for a delegate
    path("search/delegate", views.searchdel, name ="searchdel"),
    # loading static files in deployment
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.STATIC_ROOT})
    ]
handler404 = 'MUNbase.views.error_404_view'
