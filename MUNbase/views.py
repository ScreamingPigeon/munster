from django.shortcuts import render, redirect
from .models import User, Experience
from django.urls import reverse
from passlib.hash import pbkdf2_sha256
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.conf.urls import handler400, handler403, handler404, handler500


#------------------------------------------HOMEPAGES-------------------------------------------#
def home(request):
    if detailsfilled(request) is False and getuser(request) is not None:
        return redirect(reverse("settings"))
    return render(request, "homepages/home.html",{"user":getuser(request)})
def login(request):
    if request.method == "GET":
        if request.session.get('id') is not None:
            del request.session['id']
        return render(request,"homepages/login.html",{'user':None})
    else:
        username=request.POST["username"]
        password = request.POST["password"]
        if loguserin(username,password,request):
            return redirect(reverse("home"))
        else:
            return render(request,"homepages/login.html",{"errmsg":"Username or Password is wrong",'user':None})
def register(request):
    #Display Page
    if request.method == "GET":
        if request.session.get('id') is not None:
            del request.session['id']
        return render(request,"homepages/register.html",{"usernames":getallusernames(), "user":None})
    #Process Form
    else:
        #get basic details
        usrname=request.POST["username"]
        type = request.POST['type']
        if usrname in getallusernames():
            return render(request,"homepages/register.html",{"usernames":username,"errmsg":"Username already exists"})
        password = request.POST["password"]
        password= pbkdf2_sha256.hash(password)
        #If account is that of a delegate
        if type = "Delegate":
            try:
                user= User(username=usrname,password=password, email="", name= "", city="")
                user.save()
            except IntegrityError:
                return render(request,"homepages/register.html",{"usernames":username,"errmsg":"Something went wrong. Please try again"})
            request.session["id"]=user.id
            request.session['type']='Delegate'
            return redirect(reverse("home"))
        #if account is that of a MUN
        if type ="MUN":
            try:
                user= MUNuser(username=usrname,password=password, email="", name= "", city="")
                user.save()
            except IntegrityError:
                return render(request,"homepages/register.html",{"usernames":username,"errmsg":"Something went wrong. Please try again"})
            request.session["id"]=user.id
            request.session['type']='MUN'
            return redirect(reverse("home"))
def featured(request):
    return render(request, "homepages/featured.html",{"user":getuser(request)})
def tnc(request):
    return render(request, "homepages/tnc.html",{"user":getuser(request)})
def logout(request):
    if request.session.get('id') is not None:
        del request.session['id']
    return redirect(reverse('home'))
#-------------------------------------SETTINGS---------------------------------------#
def settings(request):
    #DISPLAY PAGE
    if request.method == "GET":
        if getuser(request) is None:
            return redirect(reverse("login", errmsg="You need to login first!"))
            type = getusertpye(request)
            if type =="Delegate":
                return render(request,"settings/settings.html",{"user":getuser(request)})
            if type =="MUN":
                return render(request,"settings/munsettings.html",{"user":getuser(request)})
    #HANDLE FORMS
    else:
        if getuser(request) is None:
            return redirect(reverse("login", errmsg="You need to login first!"))
        #for type Delegate
        if getusertype(request) =="Delegate":
            name = request.POST["name"]
            email = request.POST["email"]
            user=getuser(request)
            user.name = name
            user.email = email
            user.city = request.POST["city"]
            user.age = request.POST['age']
            user.institution = request.POST['institution']
            user.save()
            return render(request,"settings/settings.html",{"user":getuser(request),"alrt":"Profile updated successfully"})
        if getusertpye(request) == 'MUN':
            user = getuser(request)
            user.name = request.POST['name']
            user.email = request.POST['email']
            user.number = request.POST['number']
            user.url = request.POST['url']
            user.city = request.POST['city']
            user.institution = request.POST['institution']
            user.description = request.POST['desc']
            try:
                user.save()
                return render(request,"settings/munsettings.html",{"user":getuser(request),"alrt":"Profile updated successfully"})
            except IntegrityError:
                return render(request,"settings/munsettings.html",{"user":getuser(request),"alrt":"We ran into an issue... Please try Again"})



#------------------------------------VIEW EXPERIENCE----------------------------------#
def exp(request):
    user=getuser(request)
    if user is None:
        return redirect(reverse("login", errmsg="You need to login first!"))
    experience=Experience.objects.filter(delegate=user).order_by("year")
    input = experience
    return render(request, "exp/view.html", {'exp':input, 'user':user})
def getexp(request):
    user = getuser(request)
    if user is None:
        return redirect(reverse('login', errmsg="Login to use this feature"))
    if request.method == "GET":
        return render(request, "exp/get.html",{"user":user})
    elif request.method == "POST":
        mun= request.POST["MUN"]
        year=request.POST["year"]
        committee=request.POST["comm"]
        pos=request.POST["pos"]
        if mun is None or year is None or committee is None or pos is None:
            return render(request, "exp/get.html", {"errmsg":"Please fill all the fields"})
        exp=Experience(delegate=user,MUN=mun,committee=committee,year=year, position=pos )
        exp.save()
        return redirect(reverse('exp'), user=user)
def editexp(request,MUN, year):
    user = getuser(request)
    if user is None:
        return redirect(reverse("login", errmsg="You need to login first!"))
    try:
        expelement=Experience.objects.filter(MUN=MUN, year = int(year), delegate = user)[0]
    except IndexError:
        return redirect(reverse("settings", alrt="Sorry, that resource does not exist!"))

    if user != expelement.delegate:
        return redirect(reverse("settings", alrt="Sorry, that resource is restricted!"))

    if request.method == "GET":
        return render(request, "exp/edit.html",{"user":user,"exp":expelement})
    if request.method == "POST":
        expelement.delete()
        mun= request.POST["MUN"]
        year=request.POST["year"]
        committee=request.POST["comm"]
        pos=request.POST["pos"]
        expelement.MUN = mun
        expelement.year=year
        expelement.committee=committee
        expelement.position=pos
        expelement.save()

        return redirect(reverse('exp'), user=user)


#----------------------------------VIEW PROFILE----------------------------------------#
def viewdel(request, dele):
    try:
        dele=User.objects.filter(username=dele)[0]
        exp = Experience.objects.filter(delegate=dele).order_by("year")
    except IndexError:
        return render(request,'404.html', {"msg":"That account does not exist","user":getuser(request)})
    if getuser(request)== dele:
        return render(request, "view/del.html", {"del":dele, "user":getuser(request), "exp": exp})
    else:
        return render(request, "view/del.html", {"del":dele, "exp":exp,"user":getuser(request)})
#----------------------------------- SEARCH--------------------------------------------#
def searchdel(request):
    if request.method=="GET":
        if getuser(request) is None:
            return redirect(reverse("login", errmsg="You need to login first!"))
        users=User.objects.all()
        return render(request,"search/search.html",{'users':users, 'user':getuser(request)})
    else:
        if getuser(request) is None:
            return redirect(reverse("login", errmsg="You need to login first!"))
        search = request.POST["search"]
        users = User.objects.all()
        unames=[]
        for row in users:
            if search in row.username or search in row.name:
                unames.append(row)
        users=unames
        return render(request,"search/search.html",{'users':users, 'user':getuser(request)})

#----------------------------------------HELPERS-----------------------------------------#
def getuser(request):
    user=request.session.get('id')
    if user is None:
        return None
    type = getusertype(request)
    if type =="Delegate":
        user= User.objects.filter(id=user)[0]
    if type =="MUN":
        user= MUNuser.objects.filter(id=user)[0]
    return user
def getusertpye(request):
    type = request.session.get('type')
    return type
def detailsfilled(request):
    if getuser(request) is None:
        return False
    user= getuser(request)
    if user.email is "" or user.name is "" or user.city is "" or user.age is None or user.institution is "":
        return False
    return True
def loguserin(username,password,request):
    user= User.objects.filter(username=username)
    try:
         user=user[0]
    except IndexError:
         return False
    if(pbkdf2_sha256.verify(password, user.password)):
        request.session['id']=user.id
        return True
    else:
        return False
def getallusers():
    users =[]
    delusers = User.objects.all()
    munusers = MUNuser.objects.all()
    for row in delusers:
        users.append(row.username)
    for row in munusers:
        users.append(row.username)
    return users[]
def getallusernames():
    #getting a list of usernames
    users=getallusers()
    usernames=[]
    for user in users:
        uname=user.username
        username.append(uname)
    return usernames
#-----------------------------------------ERROR HANDLERS-----------------------------------#
def error_404_view(request,exception):
    return render(request,'404.html')
