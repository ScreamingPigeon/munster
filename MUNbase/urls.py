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
    2. Add a URL to urlpatterns:
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings # to import static in deployment
from django.conf.urls.static import static # to import static in deployment

urlpatterns = [
    #COMMON HOMEPAGES--------------------------------------------------------------
    path("", views.home, name="home"),
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path('blogs', views.blog, name ='blog'),
    path('blogs/<str:title>', views.dispblog, name = 'dispblog'),
    path("featured", views.featured, name="featured"),
    path("tnc", views.tnc, name="tnc"),
    path("logout", views.logout, name="logout"),
    #COMMON SETTINGS-------------------------------------------------------------------
    path("settings", views.settings, name="settings"),
    #DELEGATE EXPERIENCE----------------------------------------------------------------
    path("experience", views.exp, name="exp"),
    path("addexperience", views.getexp, name="getexp"),
    path("editexperience/<str:MUN>/<str:year>",views.editexp,name="editexp"),
    #COMMON VIEW-------------------------------------------------------------------------
    path("view/delegate/<str:dele>", views.viewdel, name="viewdel"),#Delegate
    path('view/mun/<str:mun>', views.viewmun, name='viewmun'),#MUN
    #REGISTRATION PROCESS----------------------------------------------------------------
    path('register/<str:mun>', views.registermun, name ='register'),#Delegate registers through this link
    path('viewregistrations', views.viewregistrations, name ='viewregistrations'),
    #MUN FEATURES----------------------------------------------------
    path('announcements', views.announcements, name='announcements'),
    path('add-announcements',views.addannouncements, name ='addannouncements'),
    path('edit-announcements/<str:heading>/<str:content>', views.editannouncements, name ='editannouncements'),
    path('delete-announcements/<str:heading>/<str:content>', views.deleteannouncements, name ='deleteannouncements'),
    #E - MUN core
    path('mymun/addcommittee', views.addcommittee, name='addcommittee'),
    path('mymun/viewcommittees', views.viewcommittee, name='viewcommittees'),
    path('mymun/editcommittee/<str:commname>/<str:mundesc>', views.editcommittee, name='editcommittee'),
    path('mymun/deletecommittee/<str:commname>/<str:mundesc>', views.deletecommittee, name='deletecommittee'),
    path('mymun/adddelegate', views.adddelegate, name='adddelegate'),
    path('mymun/viewdelegates', views.viewdelegates, name='viewdelegates'),
    path('mymun/editdelegate/<str:commname>/<str:contactnum>', views.editdelegate, name='editdelegate'),
    path('mymun/deletedelegate/<str:commname>/<str:contactnum>', views.deletedelegate, name='deletedelegate'),
    #E-MUN funct
    path('emun/<str:munname>', views.logincomm, name='logincomm'),
    path ('emun/<str:munname>/<str:commname>/admin', views.adminview, name ='adminview'),
    path ('emun/<str:munname>/<str:commname>/delegate', views.partview, name ='partview'),
    path ('emun/mun/logout', views.commlogout, name ='commlogout'),
    #------FETCH FUNCTIONS------#
    path('emun/<str:munname>/<str:commname>/attendance', views.getattendance, name = 'getattendance'),
    path('emun/<str:munname>/<str:commname>/updateattendance/<str:country>/<str:status>', views.updateattendance, name = 'updateattendance'),

    path('emun/newdiscussion/<str:munname>/<str:commname>/<str:agenda>/<str:tps>/<str:ns>/<str:active>', views.newdiscussion, name ='newdiscussion'),
    path('emun/getdiscussions/<str:munname>/<str:commname>', views.getdiscussions, name ='getdiscussions'),
    path('emun/getactivediscussion/<str:munname>/<str:commname>', views.getactivediscussion, name ='getactivediscussion'),
    path('emun/speaker/<str:munname>/<str:commname>/<str:agenda>/<str:tps>/<str:ns>/<str:alloc>', views.addcountry, name ='addcountry'),
    path('emun/nextspeaker/<str:munname>/<str:commname>/<str:agenda>/<str:alloc>/<str:seconds>', views.nextspeaker, name ='nextspeaker'),
    path('emun/newmotion/<str:munname>/<str:commname>/<str:name>/<str:proposer>', views.newmotion, name ='newmotion'),
    path('emun/showallmotions/<str:munname>/<str:commname>', views.showallmotions, name ='showallmotions'),
    path('emun/getvoterdata/<str:munname>/<str:commname>/<str:motionid>', views.getvoterdata, name ='getvoterdata'),
    path('emun/summonvote/<str:munname>/<str:commname>/<str:motionid>/<str:country>', views.summonvote, name ='summonvote'),

    #COMMON SEARCH-------------------------------------------------------------
    path("search/delegate", views.searchdel, name ="searchdel"),
    path('search/mun', views.searchmun, name = 'searchmun')
    # loading static files in deployment
    ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
handler404 = 'MUNbase.views.error_404_view'
