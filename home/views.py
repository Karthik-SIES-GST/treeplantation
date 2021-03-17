from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from schedule.models import tt, participants, pastevents
from maps.models import Blog
from django.contrib import messages
import MySQLdb
from .past_or_present import past_or_present

# Create your views here.

# home page
def index(request):
    past_or_present()
    past_presents = pastevents.objects.all()
    return render(request, 'home/index.html', {'past_presents':past_presents})

# login page
def login_page(request):
    past_or_present()
    if (request.method == 'POST'):
        user_name = request.POST['user_name']
        pass_word = request.POST['pass']
        if (User.objects.filter(username=user_name).exists()):
            pass
        else:
            messages.warning(request, 'Username Doesnot Exist')
            return redirect('login')
        user = authenticate(username=user_name, password=pass_word)
        print('User Authentication: ',user)
        if user is not None:
            login(request, user)
            return redirect('/')
        elif user is None:
            messages.warning(request, 'Wrong Password')
            return redirect('login')
        else:
            messages.warning(request, 'Wrong Password')
            return redirect('login')
    else:
        return render(request, 'home/login.html')

# registration page
def register(request):
    past_or_present()
    if (request.method == 'POST'):
        first_name = request.POST['first_name']
        if first_name == '':
            messages.warning(request, 'Please put your first name')
            return redirect('register')
        else:
            pass
        last_name = request.POST['last_name']
        if last_name == '':
            messages.warning(request, 'Please put your last name')
            return redirect('register')
        else:
            pass
        user_name = request.POST['username']
        if user_name == '':
            messages.warning(request, 'Please put a username')
            return redirect('register')
        else:
            pass
        email = request.POST['email']
        if email == '':
            messages.warning(request, 'Please put an email')
            return redirect('register')
        else:
            pass
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if (pass1 == pass2):
            if (User.objects.filter(username=user_name).exists()):
                messages.warning(request, 'Username Already Taken')
                return redirect('register')
            elif (User.objects.filter(email=email).exists()):
                messages.warning(request, 'Email Already Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=user_name, first_name=first_name, last_name=last_name, email=email, password=pass1)
                user.save()
                return redirect('/login/')
        else:
            messages.warning(request, 'Password donot match')
            return redirect('register')
    else:
        return render(request, 'home/register.html')

def profile(request):
    past_or_present()
    tt_1 = tt.objects.all()
    participants_1 = participants.objects.all()
    blogs = Blog.objects.all()
    return render(request, 'home/profile.html', {'tt_1': tt_1, 'participants_1': participants_1, 'blogs': blogs})

def delete_hosted_event(request):
    past_or_present()
    unique_id = request.POST['hidden_unique_id']
    try:
        mydb = MySQLdb.connect(
            "localhost",
            "root",
            "",
            "plantation"
        )
    except:
        print("Can't connect to database")
        return
    mycursor = mydb.cursor()
    query = "DELETE FROM schedule_tt WHERE unique_id='"+unique_id+"'"
    mycursor.execute(query)
    mydb.commit()
    query_2 = "DELETE FROM schedule_participants WHERE unique_id='"+unique_id+"'"
    mycursor.execute(query_2)
    mydb.commit()
    return redirect('/profile')

def delete_participated_events(request):
    past_or_present()
    unique_id = request.POST['hidden_unique_id']
    try:
        mydb = MySQLdb.connect(
            "localhost",
            "root",
            "",
            "plantation"
        )
    except:
        print("Can't connect to database")
        return
    mycursor = mydb.cursor()
    query = "DELETE FROM schedule_participants WHERE unique_id='"+unique_id+"'"
    mycursor.execute(query)
    mydb.commit()
    return redirect('/profile')

def delete_map_blog(request):
    past_or_present()
    unique_id = request.POST['hidden_unique_id']
    try:
        mydb = MySQLdb.connect(
            "localhost",
            "root",
            "",
            "plantation"
        )
    except:
        print("Can't connect to database")
        return
    mycursor = mydb.cursor()
    query = "DELETE FROM maps_blog WHERE unique_id='"+unique_id+"'"
    mycursor.execute(query)
    mydb.commit()
    return redirect('/profile')

# logout page
def logout_page(request):
    past_or_present()
    logout(request)
    return redirect('/')

# how it works page
def functionality(request):
    past_or_present()
    return render(request, 'home/functionality.html')

# about page
def about(request):
    past_or_present()
    return render(request, 'home/about.html')

# contact us page
def contact_us(request):
    past_or_present()
    return render(request, 'home/contact_us.html')

