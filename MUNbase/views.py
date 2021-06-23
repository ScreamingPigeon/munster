from django.shortcuts import render, redirect
from .models import User, Experience, MUNuser, MUNannouncements, Registrations, Delwatchlist, MUNwatchlist, Article, Committee, Participant, CommitteeAdmin, Agenda, Talklist, TalkListSpeaker, Motion, VotingEvent, Attendance
from django.urls import reverse
import xlsxwriter
from datetime import datetime
from passlib.hash import pbkdf2_sha256
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.conf.urls import handler400, handler403, handler404, handler500
import math
import markdown

#---------------------------------------COMMON-HOMEPAGES----------------------------------------#
def home(request):
    if detailsfilled(request) is False and getuser(request) is not None:
        if getusertype(request)=="Delegate":
            return render(request,"settings/settings.html",{"user":getuser(request),"alrt":"Please fill in all the fields marked with a *", "type":getusertype(request)})
        else:
            return render(request,"settings/munsettings.html",{"user":getuser(request),"alrt":"Please fill in all the fields marked with a *", "type":getusertype(request)})
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
def blog(request):
    articles = Article.objects.all().order_by('-date')
    return render(request, 'homepages/blog.html',{"user":getuser(request), "type":getusertype(request), "articles":articles})
def dispblog(request, title):
    article = Article.objects.filter(title=title)
    if len(article) == 0:
        return render(request,'404.html', {"msg":"That page does not exist","user":getuser(request), "type":getusertype(request)})
    article = article[0]
    article.content = markdown.markdown(article.content)
    return render(request, 'homepages/dispblog.html',{"user":getuser(request), "type":getusertype(request), "article":article})
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
            return render(request,"homepages/login.html",{"errmsg":"You need to Login first!",'user':None, "type":getusertype(request)})
        type = getusertype(request)
        if type =="Delegate":
            return render(request,"settings/settings.html",{"user":getuser(request), "type":getusertype(request)})
        if type =="MUN":
            return render(request,"settings/munsettings.html",{"user":getuser(request), "type":getusertype(request)})
    #MANAGING FORM SUBMISSIONS
    else:
        if getuser(request) is None:
            return render(request,"homepages/login.html",{"errmsg":"You need to Login first!",'user':None, "type":getusertype(request)})
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
        return render(request,"homepages/login.html",{"errmsg":"You need to Login first!",'user':None, "type":getusertype(request)})
    elif getusertype(request) != 'Delegate':
        return render(request,"settings/settings.html",{"user":getuser(request),"alrt":"That resource cannot be utilized by your account", "type":getusertype(request)})
    experience=Experience.objects.filter(delegate=user).order_by("year")
    input = experience
    return render(request, "exp/view.html", {'exp':input, 'user':user, "type":getusertype(request)})
def getexp(request):
    user = getuser(request)
    if user is None:
        return render(request,"homepages/login.html",{"errmsg":"You need to Login first!",'user':None, "type":getusertype(request)})
    elif getusertype(request) != 'Delegate':
        return render(request,"settings/settings.html",{"user":getuser(request),"alrt":"That resource cannot be utilized by your account", "type":getusertype(request)})
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
        return render(request,"homepages/login.html",{"errmsg":"You need to Login first!",'user':None, "type":getusertype(request)})
    elif getusertype(request) != 'Delegate':
        return render(request,"settings/settings.html",{"user":getuser(request),"alrt":"That resource cannot be utilized by your account", "type":getusertype(request)})
    try:
        expelement=Experience.objects.filter(MUN=MUN, year = int(year), delegate = user)[0]
    except IndexError:
        return render(request,"settings/settings.html",{"user":getuser(request),"alrt":"Sorry, that Resource does not exist!", "type":getusertype(request)})

    if user != expelement.delegate:
        return render(request,"settings/settings.html",{"user":getuser(request),"alrt":"That resource cannot be utilized by your account", "type":getusertype(request)})

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
        return render(request,"homepages/login.html",{"errmsg":"You need to Login first!",'user':None, "type":getusertype(request)})
    elif getusertype(request) != 'MUN':
        return render(request,"settings/settings.html",{"user":getuser(request),"alrt":"That resource cannot be utilized by your account", "type":getusertype(request)})
    announcements = MUNannouncements.objects.filter(announcer=getuser(request)).order_by('-dateofcreation')
    return render(request, "munfts/announcements/view.html",{'announcements':announcements,'user':getuser(request), 'type':getusertype(request)})
def addannouncements(request):
    if request.method == 'GET':
        if getuser(request) is None:
            return render(request,"homepages/login.html",{"errmsg":"You need to Login first!",'user':None, "type":getusertype(request)})
        elif getusertype(request) != 'MUN':
            return render(request,"settings/settings.html",{"user":getuser(request),"alrt":"That resource cannot be utilized by your account", "type":getusertype(request)})
        return render(request, 'munfts/announcements/add.html',{'user':getuser(request),'type':getusertype(request)})
    if request.method == 'POST':
        if getuser(request) is None:
            return render(request,"homepages/login.html",{"errmsg":"You need to Login first!",'user':None, "type":getusertype(request)})
        elif getusertype(request) != 'MUN':
            return render(request,"settings/settings.html",{"user":getuser(request),"alrt":"That resource cannot be utilized by your account", "type":getusertype(request)})
        anc= MUNannouncements(announcer=getuser(request), heading = request.POST['heading'], content=request.POST['content'])
        try:
            anc.save()
            return redirect(reverse('announcements'))
        except IntegrityError:
            return render(request, 'munfts/announcements/add.html',{"errmsg":"Something went wrong, Please try again",'user':getuser(request),'type':getusertype(request)})
def editannouncements(request, heading, content):
    if request.method=='GET':
        if getuser(request) is None:
            return render(request,"homepages/login.html",{"errmsg":"You need to Login first!",'user':None, "type":getusertype(request)})
        elif getusertype(request) != 'MUN':
            return render(request,"settings/settings.html",{"user":getuser(request),"alrt":"That resource cannot be utilized by your account", "type":getusertype(request)})
        announcement = MUNannouncements.objects.filter(announcer = getuser(request), heading=heading, content=content)
        if announcement is None:
            return render(request, 'munfts/announcements/view.html',{"errmsg":"That Announcemnt does not exist"})
        else:
            announcement=announcement[0]
            return render(request, 'munfts/announcements/edit.html',{'announcement':announcement, 'user':getuser(request), 'type':getusertype(request)})
    if request.method == 'POST':
        if getuser(request) is None:
            return render(request,"homepages/login.html",{"errmsg":"You need to Login first!",'user':None, "type":getusertype(request)})
        elif getusertype(request) != 'MUN':
            return render(request,"settings/settings.html",{"user":getuser(request),"alrt":"That resource cannot be utilized by your account", "type":getusertype(request)})
        announcement = MUNannouncements.objects.filter(announcer = getuser(request), heading=heading, content=content)[0]
        announcement.heading = request.POST['heading']
        announcement.content = request.POST['content']
        announcement.save()
        return redirect(reverse('announcements'))
def deleteannouncements(request, heading, content):
    if getuser(request) is None:
        return render(request,"homepages/login.html",{"errmsg":"You need to Login first!",'user':None, "type":getusertype(request)})
    elif getusertype(request) != 'MUN':
        return render(request,"settings/settings.html",{"user":getuser(request),"alrt":"That resource cannot be utilized by your account", "type":getusertype(request)})
    announcement = MUNannouncements.objects.filter(announcer = getuser(request), heading=heading, content=content)[0]
    announcement.delete()
    return redirect(reverse('announcements'))
#------------------------------------MUN REGISTRATIONS---------------------------------------#
def registermun(request, mun):
    if getuser(request) is None:
        return render(request,"homepages/login.html",{"errmsg":"You need to Login first!",'user':None, "type":getusertype(request)})
    elif getusertype(request) != 'Delegate':
        return render(request,"settings/settings.html",{"user":getuser(request),"alrt":"That resource cannot be utilized by your account", "type":getusertype(request)})
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
def viewregistrations(request):
    if getuser(request) is None:
        return render(request,"homepages/login.html",{"errmsg":"You need to Login first!",'user':None, "type":getusertype(request)})
    elif getusertype(request) != 'MUN':
        return render(request,"settings/settings.html",{"user":getuser(request),"alrt":"That resource cannot be utilized by your account", "type":getusertype(request)})
    registrations = Registrations.objects.filter(MUN = getuser(request))
    path = ""
    return render(request, 'munfts/registrations/view.html', {"user":getuser(request), "type":getusertype(request), "registrations": registrations, 'path':path})
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
#------------------------------------E - MUN-------------------------------------------------#
def addcommittee(request):
    if request.method == 'GET':
            if getuser(request) is None:
                return render(request,"homepages/login.html",{"errmsg":"You need to Login first!",'user':None, "type":getusertype(request)})
            elif getusertype(request) != 'MUN':
                return render(request,"settings/settings.html",{"user":getuser(request),"alrt":"That resource cannot be utilized by your account", "type":getusertype(request)})
            return render(request, 'munfts/mymun/comms/addcommittee.html',{'user':getuser(request),'type':getusertype(request)})
    if request.method == 'POST':
        if getuser(request) is None:
            return render(request,"homepages/login.html",{"errmsg":"You need to Login first!",'user':None, "type":getusertype(request)})
        elif getusertype(request) != 'MUN':
            return render(request,"settings/settings.html",{"user":getuser(request),"alrt":"That resource cannot be utilized by your account", "type":getusertype(request)})
        committeename = request.POST['cname']
        committeedesc = request.POST['desc']
        if committeedesc == "":
            committeedesc+=" "
        if committeename == "":
            committeename+=" "
        mun = getuser(request)
        comm = Committee(name = committeename, mun = mun, description = committeedesc)
        comm.save()
        return redirect(reverse('viewcommittees'))
def editcommittee(request, commname, mundesc):
    user = getuser(request)
    if user is None:
        return render(request,"homepages/login.html",{"errmsg":"You need to Login first!",'user':None, "type":getusertype(request)})
    elif getusertype(request) != 'MUN':
        return render(request,"settings/settings.html",{"user":getuser(request),"alrt":"That resource cannot be utilized by your account", "type":getusertype(request)})
    try:
        comm=Committee.objects.filter(name=commname, description=mundesc, mun = user)[0]
    except IndexError:
        return render(request,"settings/settings.html",{"user":getuser(request),"alrt":"Sorry, that Resource does not exist!", "type":getusertype(request)})
    if user != comm.mun:
        return render(request,"settings/settings.html",{"user":getuser(request),"alrt":"That resource cannot be utilized by your account", "type":getusertype(request)})
    if request.method == 'GET':
        return render(request, 'munfts/mymun/comms/editcommittee.html',{'user':getuser(request),'type':getusertype(request),'name':comm.name,'description':comm.description})
    if request.method == 'POST':
        comm = Committee.objects.filter(mun = getuser(request), name=commname, description=mundesc)[0]
        comm.name = request.POST['cname']
        comm.desc = request.POST['desc']
        comm.save()
        return redirect(reverse('viewcommittees'))
def viewcommittee(request):
    if getuser(request) is None:
        return render(request,"homepages/login.html",{"errmsg":"You need to Login first!",'user':None, "type":getusertype(request)})
    elif getusertype(request) != 'MUN':
        return render(request,"settings/settings.html",{"user":getuser(request),"alrt":"That resource cannot be utilized by your account", "type":getusertype(request)})
    comms = Committee.objects.filter(mun = getuser(request))
    return render(request, 'munfts/mymun/comms/viewcommittees.html',{'comms':comms})
def deletecommittee(request, commname, mundesc):
    user = getuser(request)
    if user is None:
        return render(request,"homepages/login.html",{"errmsg":"You need to Login first!",'user':None, "type":getusertype(request)})
    elif getusertype(request) != 'MUN':
        return render(request,"settings/settings.html",{"user":getuser(request),"alrt":"That resource cannot be utilized by your account", "type":getusertype(request)})
    try:
        comm=Committee.objects.filter(name=commname, description=mundesc, mun = user)[0]
    except IndexError:
        return render(request,"settings/settings.html",{"user":getuser(request),"alrt":"Sorry, that Resource does not exist!", "type":getusertype(request)})
    if user != comm.mun:
        return render(request,"settings/settings.html",{"user":getuser(request),"alrt":"That resource cannot be utilized by your account", "type":getusertype(request)})
    comm = Committee.objects.filter(mun = getuser(request), name=commname, description=mundesc)[0]
    comm.delete()
    return redirect(reverse('viewcommittees'))
    if request.method == 'GET':
            if getuser(request) is None:
                return render(request,"homepages/login.html",{"errmsg":"You need to Login first!",'user':None, "type":getusertype(request)})
            elif getusertype(request) != 'MUN':
                return render(request,"settings/settings.html",{"user":getuser(request),"alrt":"That resource cannot be utilized by your account", "type":getusertype(request)})
            return render(request, 'munfts/mymun/comms/addcommittee.html',{'user':getuser(request),'type':getusertype(request)})
def adddelegate(request):
    if request.method == 'GET':
        if getuser(request) is None:
            return render(request,"homepages/login.html",{"errmsg":"You need to Login first!",'user':None, "type":getusertype(request)})
        elif getusertype(request) != 'MUN':
            return render(request,"settings/settings.html",{"user":getuser(request),"alrt":"That resource cannot be utilized by your account", "type":getusertype(request)})
        committees = Committee.objects.filter(mun = getuser(request))
        dels =[]
        if len(committees) == 0:
            return redirect(reverse('viewcommittees') )
        for row in committees:
            dels+=Participant.objects.filter(committee=row)
            countries = ["Afghanistan","Albania","Algeria","Andorra","Angola","Anguilla","Antigua &amp; Barbuda","Argentina","Armenia","Aruba","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bermuda","Bhutan","Bolivia","Bosnia &amp; Herzegovina","Botswana","Brazil","British Virgin Islands","Brunei","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Cape Verde","Cayman Islands","Chad","Chile","China","Colombia","Congo","Cook Islands","Costa Rica","Cote D Ivoire","Croatia","Cruise Ship","Cuba","Cyprus","Czech Republic","Denmark","Djibouti","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Equatorial Guinea","Estonia","Ethiopia","Falkland Islands","Faroe Islands","Fiji","Finland","France","French Polynesia","French West Indies","Gabon","Gambia","Georgia","Germany","Ghana","Gibraltar","Greece","Greenland","Grenada","Guam","Guatemala","Guernsey","Guinea","Guinea Bissau","Guyana","Haiti","Honduras","Hong Kong","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Isle of Man","Israel","Italy","Jamaica","Japan","Jersey","Jordan","Kazakhstan","Kenya","Kuwait","Kyrgyz Republic","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Macau","Macedonia","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Mauritania","Mauritius","Mexico","Moldova","Monaco","Mongolia","Montenegro","Montserrat","Morocco","Mozambique","Namibia","Nepal","Netherlands","Netherlands Antilles","New Caledonia","New Zealand","Nicaragua","Niger","Nigeria","Norway","Oman","Pakistan","Palestine","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal","Puerto Rico","Qatar","Reunion","Romania","Russia","Rwanda","Saint Pierre &amp; Miquelon","Samoa","San Marino","Satellite","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore","Slovakia","Slovenia","South Africa","South Korea","Spain","Sri Lanka","St Kitts &amp; Nevis","St Lucia","St Vincent","St. Lucia","Sudan","Suriname","Swaziland","Sweden","Switzerland","Syria","Taiwan","Tajikistan","Tanzania","Thailand","Timor L'Este","Togo","Tonga","Trinidad &amp; Tobago","Tunisia","Turkey","Turkmenistan","Turks &amp; Caicos","Uganda","Ukraine","United Arab Emirates","United Kingdom","Uruguay","Uzbekistan","Venezuela","Vietnam","Virgin Islands (US)","Yemen","Zambia","Zimbabwe"]
        return render(request, 'munfts/mymun/dels/adddelegates.html',{'user':getuser(request),'type':getusertype(request), 'committees':committees, 'dels':dels, 'countries':countries})
    if request.method == 'POST':
        if getuser(request) is None:
            return render(request,"homepages/login.html",{"errmsg":"You need to Login first!",'user':None, "type":getusertype(request)})
        elif getusertype(request) != 'MUN':
            return render(request,"settings/settings.html",{"user":getuser(request),"alrt":"That resource cannot be utilized by your account", "type":getusertype(request)})
        fname = request.POST['fname']
        lname = request.POST['sname']
        number = request.POST['number']
        comm = request.POST['committee']
        committee = Committee.objects.filter(name = comm, mun = getuser(request))[0]
        country=  request.POST['alloc']
        part = Participant( firstname = fname, secondname = lname, contactnum = number, committee = committee, country = country, password=fname[0]+lname[0]+number)
        part.save()
        return redirect(reverse('viewdelegates'))
def viewdelegates(request):
    if getuser(request) is None:
        return render(request,"homepages/login.html",{"errmsg":"You need to Login first!",'user':None, "type":getusertype(request)})
    elif getusertype(request) != 'MUN':
        return render(request,"settings/settings.html",{"user":getuser(request),"alrt":"That resource cannot be utilized by your account", "type":getusertype(request)})
    compre = []
    comms = Committee.objects.filter(mun = getuser(request))
    for row in comms:
        dels = Participant.objects.filter(committee = row).order_by('committee')
        for rows in dels:
            compre.append(rows)
    return render(request, 'munfts/mymun/dels/viewdelegates.html',{'dels':compre})
def editdelegate(request, commname, allocation):
    if request.method == 'GET':
        if getuser(request) is None:
            return render(request,"homepages/login.html",{"errmsg":"You need to Login first!",'user':None, "type":getusertype(request)})
        elif getusertype(request) != 'MUN':
            return render(request,"settings/settings.html",{"user":getuser(request),"alrt":"That resource cannot be utilized by your account", "type":getusertype(request)})
        committees = Committee.objects.filter(mun = getuser(request))
        dels =[]
        if len(committees) == 0:
            return redirect(reverse('viewcommittees') )
        for row in committees:
            dels+=Participant.objects.filter(committee=row)
            countries = ["Afghanistan","Albania","Algeria","Andorra","Angola","Anguilla","Antigua &amp; Barbuda","Argentina","Armenia","Aruba","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bermuda","Bhutan","Bolivia","Bosnia &amp; Herzegovina","Botswana","Brazil","British Virgin Islands","Brunei","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Cape Verde","Cayman Islands","Chad","Chile","China","Colombia","Congo","Cook Islands","Costa Rica","Cote D Ivoire","Croatia","Cruise Ship","Cuba","Cyprus","Czech Republic","Denmark","Djibouti","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Equatorial Guinea","Estonia","Ethiopia","Falkland Islands","Faroe Islands","Fiji","Finland","France","French Polynesia","French West Indies","Gabon","Gambia","Georgia","Germany","Ghana","Gibraltar","Greece","Greenland","Grenada","Guam","Guatemala","Guernsey","Guinea","Guinea Bissau","Guyana","Haiti","Honduras","Hong Kong","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Isle of Man","Israel","Italy","Jamaica","Japan","Jersey","Jordan","Kazakhstan","Kenya","Kuwait","Kyrgyz Republic","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Macau","Macedonia","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Mauritania","Mauritius","Mexico","Moldova","Monaco","Mongolia","Montenegro","Montserrat","Morocco","Mozambique","Namibia","Nepal","Netherlands","Netherlands Antilles","New Caledonia","New Zealand","Nicaragua","Niger","Nigeria","Norway","Oman","Pakistan","Palestine","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal","Puerto Rico","Qatar","Reunion","Romania","Russia","Rwanda","Saint Pierre &amp; Miquelon","Samoa","San Marino","Satellite","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore","Slovakia","Slovenia","South Africa","South Korea","Spain","Sri Lanka","St Kitts &amp; Nevis","St Lucia","St Vincent","St. Lucia","Sudan","Suriname","Swaziland","Sweden","Switzerland","Syria","Taiwan","Tajikistan","Tanzania","Thailand","Timor L'Este","Togo","Tonga","Trinidad &amp; Tobago","Tunisia","Turkey","Turkmenistan","Turks &amp; Caicos","Uganda","Ukraine","United Arab Emirates","United Kingdom","Uruguay","Uzbekistan","Venezuela","Vietnam","Virgin Islands (US)","Yemen","Zambia","Zimbabwe"]
        comm = Committee.objects.filter(name = commname, mun = getuser(request))[0]
        part = Participant.objects.filter(committee = comm, contactnum = contactnum)[0]
        country = part.country
        return render(request, 'munfts/mymun/dels/editdelegate.html',{'user':getuser(request),'type':getusertype(request), 'committees':committees, 'countries':countries, 'del':part, 'country':country, 'comm':commname})
    if request.method == 'POST':
        if getuser(request) is None:
            return render(request,"homepages/login.html",{"errmsg":"You need to Login first!",'user':None, "type":getusertype(request)})
        elif getusertype(request) != 'MUN':
            return render(request,"settings/settings.html",{"user":getuser(request),"alrt":"That resource cannot be utilized by your account", "type":getusertype(request)})
        comm = Committee.objects.filter(name = commname, mun = getuser(request))[0]
        part = Participant.objects.filter(committee = comm, contactnum = contactnum)[0]
        part.country=  request.POST['alloc']
        part.firstname = request.POST['fname']
        part.secondname = request.POST['sname']
        part.contactnum = request.POST['number']
        part.committee =Committee.objects.filter(name = request.POST['committee'], mun = getuser(request))[0]
        part.save()
        return redirect(reverse('viewdelegates'))
def deletedelegate(request,commname, contactnum):
    return None
#----------------------------------- COMMON SEARCH--------------------------------------------#
def searchdel(request):
    if request.method=="GET":
        if getuser(request) is None:
            return render(request,"homepages/login.html",{"errmsg":"You need to Login first!",'user':None, "type":getusertype(request)})
        users=User.objects.all()
        musers=MUNuser.objects.all()
        return render(request,"search/search.html",{'users':users,'musers':musers, 'user':getuser(request), "type":getusertype(request)})
    else:
        if getuser(request) is None:
            return render(request,"homepages/login.html",{"errmsg":"You need to Login first!",'user':None, "type":getusertype(request)})
        search = request.POST["search"]
        users = User.objects.all()
        unames=[]
        for row in users:
            if search in row.username or search in row.name:
                unames.append(row)
        users=unames
        musers = MUNuser.objects.all()
        return render(request,"search/search.html",{'users':users,'musers':musers, 'user':getuser(request), "type":getusertype(request)})
def searchmun(request):
    if request.method=="GET":
        if getuser(request) is None:
            return render(request,"homepages/login.html",{"errmsg":"You need to Login first!",'user':None, "type":getusertype(request)})
        users=MUNser.objects.all()
        dusers = User.objects.all()
        return render(request,"search/search.html",{'musers':users, 'users':dusers, 'user':getuser(request), "type":getusertype(request)})
    else:
        if getuser(request) is None:
            return render(request,"homepages/login.html",{"errmsg":"You need to Login first!",'user':None, "type":getusertype(request)})
        search = request.POST["munsearch"]
        users = MUNuser.objects.all()
        unames=[]
        for row in users:
            if search in row.username or search in row.name:
                unames.append(row)
        users=unames
        dusers = User.objects.all()
        return render(request,"search/search.html",{'musers':users, 'users':dusers, 'user':getuser(request), "type":getusertype(request)})
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
def expstring(exp):
    str = ""
    for row in exp:
        str += f"{row.MUN}/{row.committee}/({row.year})/{row.position}|--|"
    return str
    """
def excelr(request):
    user = getuser(request)
    registrations = Registration.objects.filter(MUN = user)
    path = str(f"registrationsdb/{user.username}{str(datetime.now())}registrations.xlsx")
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()
    worksheet.write(0,0, 'Delegate Name')
    worksheet.write (0,1, 'Age')
    worksheet.write(0,2, 'Instiution')
    worksheet.write (0,3, 'Email - ID')
    worksheet.write(0,4, 'City')
    worksheet.write(0,5, 'Experience')
    experience=[]
    for row in registrations:
        dele = row.delegate
        exp = Experience.objects.filter(delegate = dele)
        experience.append(exp)
    for i in range(0, len(registrations)):
        worksheet.write(i+1,0, str(registrations[i].delegate.name))
        worksheet.write(i+1,1, str(registrations[i].delegate.age))
        worksheet.write(i+1,2, str(registrations[i].delegate.institution))
        worksheet.write(i+1,3, str(registrations[i].delegate.email))
        worksheet.write(i+1,4, str(registrations[i].delegate.city))
        worksheet.write(i+1,5, str(expstring(exp[i]))
    workbook.close()
    return path
    """
#-----------------------------------------ERROR HANDLERS-----------------------------------#
def error_404_view(request,exception):
    return render(request,'404.html')
