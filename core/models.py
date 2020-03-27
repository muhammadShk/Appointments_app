from django.db import models
import re
from datetime import datetime, timezone, date
# Create your models here.

# define a function to validate and build a dictionary -> pass to views py -> views passes to html 
class UserManager(models.Manager):
    def registration_validator(self, post_data):
        errors = {}
        if len(post_data['first_name']) == 0:
            errors['first_name'] = "First name cannot be empty"
        if len(post_data['last_name']) == 0:
            errors['last_name'] = "Last name cannot be empty"

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Invalid Email"
        
        if len(post_data['password']) < 8 :
            errors['password'] = "Password must be at least 8 characters"

        if post_data['password'] != post_data['password_confirmation']:
            errors['password_confirmation'] = "Password and Password Confirmation do not match"

        # dont let them if email exists
        if len(User.objects.filter(email=post_data['email'])) > 0:
            errors['email'] = "Email already exists"
        # User.objects.get(email=post_data['email']) -> {} or ERROR
        return errors
    
    def login_validator(self, post_data):
        errors = {}
        if len(User.objects.filter(email=post_data['login_email'])) == 0:
            errors['login_email'] = "Email not found"
        return errors
    

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class AppointmentManager(models.Manager):
    def create_validator(self, post_data):
        errors = {}
        if len(post_data['task']) < 3:
            errors['task'] = "Task must be at least 3 characters long"
        
        if len(post_data['date']) < 2:
            errors['date'] = "date cannot be empty"
        elif datetime.strptime(post_data['date'], "%Y-%m-%d")<datetime.now():
            errors['date']=" date cannot be in the past"
        
        if len(post_data['status']) < 2:
            errors['status'] = "status cannot be empty"
        return errors

    def update_validator(self, post_data):
        errors = {}
        if len(post_data['task']) < 3:
            errors['task'] = "Task must be at least 3 characters long"
        if len(post_data['date']) < 2:
            errors['date'] = "date cannot be empty"
        elif datetime.strptime(post_data['date'], "%Y-%m-%d")<datetime.now():
            errors['date']= "date cannot be in the past"

        if len(post_data['status']) < 2:
            errors['status'] = "status cannot be empty"
        return errors

class Appointment(models.Model):
    task = models.CharField(max_length=255)
    date=models.DateField()
    status = models.CharField(max_length=255)   
    # db relationships with One To Many and Many to Many
    creator = models.ForeignKey(User, related_name="appointments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AppointmentManager()