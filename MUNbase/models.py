from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=50,default=None)
    email=models.CharField(max_length=50,default=None )
    username = models.CharField(max_length=16)
    password=models.CharField(max_length=100)
    city=models.CharField(max_length=60, default="")

class Experience(models.Model):
    delegate=models.ForeignKey(User,on_delete=models.CASCADE)
    MUN=models.CharField(max_length=50, default="")
    committee=models.CharField(max_length=50, default="")
    year=models.IntegerField(default=2020)
    position=models.CharField(max_length=20, default="")
