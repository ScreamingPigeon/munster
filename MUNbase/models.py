from django.db import models

#delegate account
class User(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=50,default=None)
    email=models.CharField(max_length=50,default=None )
    username = models.CharField(max_length=16)
    password=models.CharField(max_length=100)
    institution=models.CharField(max_length=50, default ="")
    age =models.IntegerField(default = 0)
    city=models.CharField(max_length=60, default="")
#delegate experience
class Experience(models.Model):
    delegate=models.ForeignKey(User,on_delete=models.CASCADE)
    MUN=models.CharField(max_length=50, default="")
    committee=models.CharField(max_length=50, default="")
    year=models.IntegerField(default=2020)
    position=models.CharField(max_length=20, default="")
#delegate watchlist
class Delwatchlist(models.Model):
    delegate = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")

#--------------------------------------------MUN Organizer Features-------------------#

#MUN organizer account
class MUNuser(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=50,default=None)
    email=models.CharField(max_length=50,default=None )
    username = models.CharField(max_length=16)
    password=models.CharField(max_length=100)
    institution=models.CharField(max_length=50, default ="")
    number = models.CharField(max_length = 15, default ="+91 ")
    description = models.CharField(max_length = 300, default = "")
    url = models.CharField(max_length = 200, default = "http://")
    city=models.CharField(max_length=60, default="")

#MUN page announcements
class MUNannouncements(models.Model):
    announcer = models.ForeignKey(MUNuser, on_delete = models.CASCADE)
    heading = models.CharField(max_length = 100)
    content = models.CharField(max_length = 300)
    dateofcreation = models.DateField(auto_now=True)
#Registrees
class Registrations (models.Model):
    delegate = models.ForeignKey(User, on_delete = models.CASCADE)
    MUN = models.ForeignKey(MUNuser, on_delete = models.CASCADE)
#MUN watchlist for delegates
class MUNwatchlist(models.Model):
    delegate = models.ForeignKey(User, on_delete=models.CASCADE)
    following = models.ForeignKey(MUNuser, on_delete=models.CASCADE)
class Article(models.Model):
    title = models.CharField(max_length = 200)
    date =  models.DateField(auto_now=True)
    content = models.CharField(max_length = 20000)
    author = models.CharField(max_length = 200)
