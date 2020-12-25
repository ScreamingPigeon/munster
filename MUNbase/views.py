from django.shortcuts import render, redirect
from .models import User, Experience, MUNuser, MUNannouncements, Registrations
from django.urls import reverse
from passlib.hash import pbkdf2_sha256
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.conf.urls import handler400, handler403, handler404, handler500


#------------------------------------------COMMON-HOMEPAGES-------------------------------------------#
def home(request):
    if detailsfilled(request) is False and getuser(request) is not None:
        return redirect(reverse("settings"), alrt ="Please fill in all the fields with a *")
    return render(request, "homepages/home.html",{"user":getuser(request), "type":getusertype(request)})
def login(request):
    if request.method == "GET":
        if request.session.get('id') is not None:
            del request.session['id']
        return render(request,"homepages/login.html",{'user':None, "type":getusertype(request)})
    else:
        username=request.POST["username"]
        password = request.POST["password"]
        if loguserin(username,password,request):
            delusers = User.objects.all()
            munusers = MUNuser.objects.all()
            user=[]
            type = []
            for row in delusers:
                if username == row.username:
                    user.append(row)
                    type.append('Delegate')
            if len(user) == 0:
                for row in munusers:
                    if username == row.username:
                        user.append(row)
                        type.append('MUN')
            user = user[0]
            request.session["id"]=user.id
            request.session['type']=type[0]
            return redirect(reverse("home"))
        else:
            return render(request,"homepages/login.html",{"errmsg":"Username or Password is wrong",'user':None, "type":getusertype(request)})
def register(request):
    #Display Page
    if request.method == "GET":
        if request.session.get('id') is not None:
            del request.session['id']
        return render(request,"homepages/register.html",{"usernames":getallusernames(), "user":None, "type":None})
    #Process Form
    else:
        #get basic details
        usrname=request.POST["username"]
        type = request.POST['type']
        if usrname in getallusernames():
            return render(request,"homepages/register.html",{"usernames":username,"errmsg":"Username already exists", "type":getusertype(request)})
        password = request.POST["password"]
        password= pbkdf2_sha256.hash(password)
        #If account is that of a delegate
        if type == "Delegate":
            try:
                user= User(username=usrname,password=password, email="", name= "", city="")
                user.save()
            except IntegrityError:
                return render(request,"homepages/register.html",{"usernames":username,"errmsg":"Something went wrong. Please try again", "type":getusertype(request)})
            request.session["id"]=user.id
            request.session["type"]='Delegate'
            return redirect(reverse("home"))
        #if account is that of a MUN
        if type =="MUN":
            try:
                user= MUNuser(username=usrname,password=password, email="", name= "", city="")
                user.save()
            except IntegrityError:
                return render(request,"homepages/register.html",{"usernames":username,"errmsg":"Something went wrong. Please try again", "type":getusertype(request)})
            request.session["id"]=user.id
            request.session['type']='MUN'
            return redirect(reverse("home"))
def featured(request):
    return render(request, "homepages/featured.html",{"user":getuser(request), "type":getusertype(request)})
def tnc(request):
    return render(request, "homepages/tnc.html",{"user":getuser(request), "type":getusertype(request)})
def logout(request):
    if request.session.get('id') is not None:
        del request.session['id']
        del request.session['type']
    return redirect(reverse('home'))
#-------------------------------------COMMON-SETTINGS---------------------------------------#
def settings(request):
    #DISPLAY PAGE
    if request.method == "GET":
        if getuser(request) is None:
            return redirect(reverse("login", errmsg="You need to login first!"))
        type = getusertype(request)
        if type =="Delegate":
            return render(request,"settings/settings.html",{"user":getuser(request), "type":getusertype(request)})
        if type =="MUN":
            return render(request,"settings/munsettings.html",{"user":getuser(request), "type":getusertype(request)})
    #MANAGING FORM SUBMISSIONS
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
            return render(request,"settings/settings.html",{"user":getuser(request),"alrt":"Profile updated successfully", "type":getusertype(request)})
        if getusertype(request) == 'MUN':
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
                return render(request,"settings/munsettings.html",{"user":getuser(request),"alrt":"Profile updated successfully", "type":getusertype(request)})
            except IntegrityError:
                return render(request,"settings/munsettings.html",{"user":getuser(request),"alrt":"We ran into an issue... Please try Again", "type":getusertype(request)})
#------------------------------------DELEGATE-EXPERIENCE----------------------------------#
def exp(request):
    user=getuser(request)
    if user is None:
        return redirect(reverse("login", errmsg="You need to login first!"))
    elif getusertype(request) != 'Delegate':
        return redirect(reverse('settings', errmsg = "That resource cannot be utilized by your account!" ))
    experience=Experience.objects.filter(delegate=user).order_by("year")
    input = experience
    return render(request, "exp/view.html", {'exp':input, 'user':user, "type":getusertype(request)})
def getexp(request):
    user = getuser(request)
    if user is None:
        return redirect(reverse('login', errmsg="Login to use this feature"))
    elif getusertype(request) != 'Delegate':
        return redirect(reverse('settings', errmsg = "That resource cannot be utilized by your account!" ))
    if request.method == "GET":
        return render(request, "exp/get.html",{"user":user, "type":getusertype(request)})
    elif request.method == "POST":
        mun= request.POST["MUN"]
        year=request.POST["year"]
        committee=request.POST["comm"]
        pos=request.POST["pos"]
        if mun is None or year is None or committee is None or pos is None:
            return render(request, "exp/get.html", {"errmsg":"Please fill all the fields", "type":getusertype(request)})
        exp=Experience(delegate=user,MUN=mun,committee=committee,year=year, position=pos )
        exp.save()
        return redirect(reverse('exp'), user=user)
def editexp(request,MUN, year):
    user = getuser(request)
    if user is None:
        return redirect(reverse("login", errmsg="You need to login first!"))
    elif getusertype(request) != 'Delegate':
        return redirect(reverse('settings', errmsg = "That resource cannot be utilized by your account!" ))
    try:
        expelement=Experience.objects.filter(MUN=MUN, year = int(year), delegate = user)[0]
    except IndexError:
        return redirect(reverse("settings", alrt="Sorry, that resource does not exist!"))

    if user != expelement.delegate:
        return redirect(reverse("settings", alrt="Sorry, that resource is restricted!"))

    if request.method == "GET":
        return render(request, "exp/edit.html",{"user":user,"exp":expelement, "type":getusertype(request)})
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
#------------------------------------MUN ANNOUNCEMENTS---------------------------------------#
def announcements(request):
    user=getuser(request)
    if user is None:
        return redirect(reverse("login", errmsg="You need to login first!"))
    elif getusertype(request) != 'MUN':
        return redirect(reverse('settings', errmsg = "That resource cannot be utilized by your account!" ))
    announcements = MUNannouncements.objects.filter(announcer=getuser(request)).order_by('-dateofcreation')
    return render(request, "munfts/announcements/view.html",{'announcements':announcements,'user':getuser(request), 'type':getusertype(request)})
def addannouncements(request):
    if request.method == 'GET':
        if getuser(request) is None:
            return redirect(reverse('login', errmsg ='You need to login first'))
        elif getusertype(request) != 'MUN':
            return redirect(reverse('settings', errmsg = "That resource cannot be utilized by your account!" ))
        return render(request, 'munfts/announcements/add.html',{'user':getuser(request),'type':getusertype(request)})
    if request.method == 'POST':
        if getuser(request) is None:
            return redirect(reverse('login', errmsg ='You need to login first'))
        elif getusertype(request) != 'MUN':
            return redirect(reverse('settings', errmsg = "That resource cannot be utilized by your account!" ))
        anc= MUNannouncements(announcer=getuser(request), heading = request.POST['heading'], content=request.POST['content'])
        try:
            anc.save()
            return redirect(reverse('announcements'))
        except IntegrityError:
            return render(request, 'munfts/announcements/add.html',{"errmsg":"Something went wrong, Please try again",'user':getuser(request),'type':getusertype(request)})
def editannouncements(request, heading, content):
    if request.method=='GET':
        if getuser(request) is None:
            return redirect(reverse('login', errmsg ='You need to login first'))
        elif getusertype(request) != 'MUN':
            return redirect(reverse('settings', errmsg = "That resource cannot be utilized by your account!" ))
        announcement = MUNannouncements.objects.filter(announcer = getuser(request), heading=heading, content=content)
        if announcement is None:
            return render(request, 'munfts/announcements/view.html',{"errmsg":"That Announcemnt does not exist"})
        else:
            announcement=announcement[0]
            return render(request, 'munfts/announcements/edit.html',{'announcement':announcement, 'user':getuser(request), 'type':getusertype(request)})
    if request.method == 'POST':
        if getuser(request) is None:
            return redirect(reverse('login', errmsg ='You need to login first'))
        elif getusertype(request) != 'MUN':
            return redirect(reverse('settings', errmsg = "That resource cannot be utilized by your account!" ))
        announcement = MUNannouncements.objects.filter(announcer = getuser(request), heading=heading, content=content)[0]
        announcement.heading = request.POST['heading']
        announcement.content = request.POST['content']
        announcement.save()
        return redirect(reverse('announcements'))
def deleteannouncements(request, heading, content):
    if getuser(request) is None:
        return redirect(reverse('login', errmsg ='You need to login first'))
    elif getusertype(request) != 'MUN':
        return redirect(reverse('settings', errmsg = "That resource cannot be utilized by your account!" ))
    announcement = MUNannouncements.objects.filter(announcer = getuser(request), heading=heading, content=content)[0]
    announcement.delete()
    return redirect(reverse('announcements'))
#------------------------------------MUN REGISTRATIONS---------------------------------------#
def register(request, mun):
    if getuser(request) is None:
        return redirect(reverse('login', errmsg ='You need to login first'))
    elif getusertype(request) != 'Delegate':
        return redirect(reverse('settings', errmsg = "That resource cannot be utilized by your account!" ))
    MUN = MUNuser.objects.filter(username=mun)
    try:
        MUN = MUN[0]
    except IndexError:
        return render(request,'404.html', {"msg":"You can't register to a non-existent account","user":getuser(request), "type":getusertype(request)})
    if len(Registrations.objects.filter(MUN = MUN, delegate = getuser(request)))!=0:
        Registrations.objects.filter(MUN = MUN, delegate = getuser(request))[0].delete()
        return redirect('viewmun', mun = MUN.username)
    else:
        registration = Registrations(delegate=getuser(request), MUN = MUN)
        registration.save()
        return redirect('viewmun', mun = MUN.username)
#----------------------------------COMMON VIEW PROFILE----------------------------------------#
def viewdel(request, dele):
    try:
        dele=User.objects.filter(username=dele)[0]
        exp = Experience.objects.filter(delegate=dele).order_by("year")
    except IndexError:
        return render(request,'404.html', {"msg":"That account does not exist","user":getuser(request), "type":getusertype(request)})
    if getuser(request)== dele:
        return render(request, "view/del.html", {"del":dele, "user":getuser(request), "exp": exp, "type":getusertype(request)})
    else:
        return render(request, "view/del.html", {"del":dele, "exp":exp, "user":getuser(request), "type":getusertype(request)})
def viewmun(request, mun):
    MUN = MUNuser.objects.filter(username=mun)
    try:
        MUN = MUN[0]
        announcements = MUNannouncements.objects.filter(announcer = MUN).order_by('-dateofcreation')
        #include registrations
        issame=False
        if getuser(request)==MUN:
            issame=True
        #checking whether the user is registered or not
        if getusertype(request) == "Delegate":
            registrations = Registrations.objects.filter(MUN = MUN, delegate=getuser(request))
            isreg = False
            if len(registrations)==1:
                isreg = True
        else:
            isreg = True
        return render(request, 'view/mun.html', {'mun':MUN,'announcements':announcements, 'user':getuser(request), "type": getusertype(request), 'same':issame,'isreg':isreg})
    except IndexError:
        return render(request,'404.html', {"msg":"That account does not exist","user":getuser(request), "type":getusertype(request)})
#----------------------------------- COMMON EARCH--------------------------------------------#
def searchdel(request):
    if request.method=="GET":
        if getuser(request) is None:
            return redirect(reverse("login", errmsg="You need to login first!"))
        users=User.objects.all()
        return render(request,"search/search.html",{'users':users, 'user':getuser(request), "type":getusertype(request)})
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
        return render(request,"search/search.html",{'users':users, 'user':getuser(request), "type":getusertype(request)})
#----------------------------------------HELPERS-----------------------------------------#
def getusertype(request):
    type = request.session.get('type')
    if type != "Delegate" and type != "MUN":
        return None
    return type
def getuser(request):
    user=request.session.get('id')
    if user is None:
        return None
    type = request.session.get('type')
    if type is None:
        return None
    if type =="Delegate":
        user= User.objects.filter(id=user)[0]
    if type =="MUN":
        user= MUNuser.objects.filter(id=user)[0]
    return user
def detailsfilled(request):
    if getuser(request) is None:
        return False
    user= getuser(request)
    type = getusertype(request)
    if type == "delegate":
        if user.email is "" or user.name is "" or user.city is "" or user.age is None or user.email is "":
            return False
    if type == "MUN":
        if user.email == "" or user.name == "" or user.city == "" or user.email == "" or user.description == "":
            return False
    return True
def loguserin(username,password,request):
    deluser= User.objects.filter(username=username)
    munuser = MUNuser.objects.filter(username=username)
    user=[]
    if len(deluser) ==1:
        user.append(deluser[0])
    elif len(munuser)==1:
        user.append(munuser[0])
    user = user[0]
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
        users.append(row)
    for row in munusers:
        users.append(row)
    return users
def getallusernames():
    #getting a list of usernames
    users=getallusers()
    usernames=[]
    for user in users:
        uname=user.username
        usernames.append(uname)
    return usernames
#-----------------------------------------ERROR HANDLERS-----------------------------------#
def error_404_view(request,exception):
    return render(request,'404.html')
