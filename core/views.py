from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt


def index(request):
    return render(request,"login.html")

def register(request):
    errors = User.objects.registration_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        ### dont indent return!
        return redirect("/")
    else:
        hashed_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hashed_password
        )
        fresh_user = User.objects.last()
        request.session['userid'] = fresh_user.id
        return redirect("/dashboard")
        
def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect("/")
    else:
        potential_user = User.objects.filter(email=request.POST['login_email'])[0]
        if bcrypt.checkpw(request.POST['login_password'].encode(),potential_user.password.encode()):
            request.session['userid'] = potential_user.id
            return redirect("/dashboard")
        else:
            messages.error(request, "Invalid Login", extra_tags="login_password")
            return redirect("/")

def logout(request):
    request.session.clear()
    return redirect("/")

def dashboard(request):
    if 'userid' not in request.session:
        return redirect("/")
    context = {
        "logged_in_user": User.objects.get(id=request.session['userid']),
        "appointments": User.objects.get(id=request.session['userid']).appointments.all()
    }
    return render(request, "dashboard.html", context)

###########################################################################################################################
#                                              CRUD
###########################################################################################################################

def create(request):
    if request.method == "GET":
        return render(request, "add.html")
    if request.method == "POST":
        print("task :" + request.POST['task'])
        print("status :" + request.POST['status'])
        print("date :" + request.POST['date'])
        errors = Appointment.objects.create_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect("/create") # this is a GET request
        else:
            logged_in_user = User.objects.get(id=request.session['userid'])
            Appointment.objects.create(
                task = request.POST['task'],
                date = request.POST['date'],
                status = request.POST['status'],
                creator = logged_in_user
            )
            # recent_event = .objects.last()
            # # recent_event.title = "bob"
            # # recent_event.save()
            # recent_event.guests.add(logged_in_user)

        return redirect("/dashboard")
    
def update(request, id):
    if request.method == "GET":
        context = {
            "appointment":Appointment.objects.get(id=id)
        }
        return render(request, "update.html",context)
    if request.method == "POST":
        errors = Appointment.objects.update_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect(f"/edit/{id}") # this is a GET request
        else:
            this_appointment = Appointment.objects.get(id=id)
            this_appointment.task = request.POST['task']
            this_appointment.date = request.POST['date']
            this_appointment.status = request.POST['status']
            this_appointment.save()
        return redirect("/dashboard")

def delete(request, id):
    Appointment.objects.get(id=id).delete()
    return redirect("/dashboard")