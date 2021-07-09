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
#E-MUN
class Committee(models.Model):
    name = models.CharField(max_length = 50)
    mun = models.ForeignKey(MUNuser, on_delete=models.CASCADE)
    description = models.CharField(max_length = 2000)
    countrylist = models.CharField(max_length = 2000, null = True, blank = True)
class Participant(models.Model):
    firstname = models.CharField(max_length = 50)
    secondname = models.CharField(max_length = 50)
    country = models.CharField(max_length = 100)
    contactnum = models.CharField(max_length = 15)
    committee = models.ForeignKey(Committee, on_delete = models.CASCADE)
    password = models.CharField(max_length = 200)
    status = models.CharField(max_length = 20)
class CommitteeAdmin(models.Model):
    committee = models.ForeignKey(Committee, on_delete = models.CASCADE)
    password = models.CharField(max_length = 50)
class Agenda(models.Model):
    agenda = models.CharField(max_length = 400)
    committee = models.ForeignKey(Committee, on_delete = models.CASCADE)
    active = models.CharField(max_length=5)
class Talklist(models.Model):
    name = models.CharField(max_length = 500)
    minutes = models.CharField(max_length = 10, blank  = True, null = True)
    agenda = models.ForeignKey(Agenda, on_delete = models.CASCADE)
class TalkListSpeaker(models.Model):
    speaker = models.ForeignKey(Participant, on_delete = models.CASCADE)
    list = models.ForeignKey(Talklist, on_delete = models.CASCADE)
    agenda = models.ForeignKey(Agenda, on_delete = models.CASCADE)
    talklist = models.ForeignKey(TalkList, on_delete = models.CASCADE)
class Motion(models.Model):
    agenda = models.ForeignKey(Agenda, on_delete = models.CASCADE)
    name = models.CharField(max_length = 400)
    delproposer = models.ForeignKey(Participant, on_delete = models.CASCADE)
    defproposer = models.ForeignKey(CommitteeAdmin, on_delete = models.CASCADE)
    type = models.CharField(max_length = 100)
class VotingEvent(models.Model):
    agenda = models.ForeignKey(Agenda, on_delete = models.CASCADE)
    motion = models.ForeignKey(Motion, on_delete = models.CASCADE)
    yes = models.CharField(max_length = 10)
    no = models.CharField(max_length = 10)
    abstain = models.CharField(max_length = 10)
    yes = models.CharField(max_length = 10)
