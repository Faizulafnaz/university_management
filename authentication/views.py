from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import User, Faculty, Verification
import random
from academic_management.models import Department


# Create your views here.
def handlelogin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        print(username, password)
        
        user = authenticate(username=username, password=password)

        if user is not None:

            if user.is_hod() and not user.is_verified:
                messages.error(request, "Your account is not verified by the admin yet. Please contact the admin for more information.")
                return redirect("handlelogin")
            
            
            login(request, user)
            return redirect('/')
        
        else:
            messages.error(request, "Username or password do no match")
            return redirect("handlelogin")

    if request.user.is_authenticated:
        return redirect('/')
    
    return render(request, 'login.html')

def handle_signup(request):
        
    if request.method=="POST":
        
        username = request.POST.get('username')
        fullname = request.POST.get('fullname')
        department = request.POST.get('department')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass')
        pass2 = request.POST.get('re_pass')
        specialization = request.POST.get('specialization')
        qualification = request.POST.get('qualification')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        phone_number =  request.POST.get('phone_number')

        image = request.FILES.get('image', None)
        if not image:
            messages.info(request, "Image field can't be empty")
            return redirect('signup')
        
        if not username.strip():
            messages.error(request, "Username is required")
            return redirect('signup')

        if not fullname.strip():
            messages.error(request, "Fullname is required")
            return redirect('signup')

        if not email.strip():
            messages.error(request, "Email is required")
            return redirect('signup')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'This username is already taken')
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'This email address is already taken')
            return redirect('signup')
        
        GENDER_CHOICES = ['male', 'female', 'other']
        if gender.lower() not in GENDER_CHOICES:
            messages.error(f"Invalid gender choice: {gender}. Valid options are {GENDER_CHOICES}")
            return redirect('signup')

        
        fname = fullname.split()[0] if len(fullname.split()) > 0 else ''
        lname = fullname.split()[-1] if len(fullname.split()) > 1 else ''


        try:
            myuser = User.objects.create_user(username=username, email=email, password=pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.role = 'hod'
            myuser.is_staff = True
            print(myuser.groups)
            myuser.save()
            print(myuser.groups)


        except Exception as e:
            print(e)
            messages.error(request, f'Something went wrong. Error {e}')
            return redirect(handle_signup)

        try:
            department = Department.objects.get(id=int(department))

            faculty = Faculty.objects.create(
                user = myuser,
                department = department,
                specialization = specialization,
                qualification = qualification,
                gender = gender.lower(),
                phone_number = phone_number,
                date_of_birth = dob,
                images = image
                )
            faculty.save()
            
        except Exception as e:
            print(e)
            myuser.delete()
            messages.error(request, f'Something went wrong. Error {e}')
            return redirect(handle_signup)
        
        try:
            varification = Verification.objects.create( faculty = faculty).save()
        except Exception as e:
            print(e)
            myuser.delete()
            messages.error(request, f'Something went wrong. Error {e}')
            return redirect(handle_signup)
        
        messages.success(request, 'Your account is under verification. We will inform you of the verification status via email.')
        return render(request,'login.html')
    
    if request.user.is_authenticated:
        return redirect('/')
    
    departments = Department.objects.all()
    print(departments)

    return render(request, 'signup.html', {'departments' : departments})

@login_required(login_url='handlelogin')
def landing_page(request):
    print(request.user.username)
    print(f"User Groups main: {request.user.groups.all()}")
    return render(request, 'home.html')



@login_required(login_url='handlelogin')
def handlelogout(request):
    logout(request)
    return redirect(handlelogin)


@login_required(login_url='handlelogin')
def about(request):
    return render(request, 'about.html')

    