from __future__ import unicode_literals
from datetime import datetime
import re
import bcrypt
from django.db import models

email_check = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def user_email(self):
        return self.order_by('email')

    def register(self, form_data):
        hash_pw = bcrypt.hashpw(form_data['password'].encode(), bcrypt.gensalt()).decode()
        return self.create(
            first_name=form_data['first_name'],
            last_name=form_data['last_name'],
            email=form_data['email'],
            password=hash_pw,
            birthday=form_data['birthday'],
        )

    def authenticate(self, email, password):
        user_email = self.filter(email=email)
        if not user_email:
            return False
        user = user_email[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

    def validator(self, form_data):
        errors = {}
        if len(form_data['first_name']) < 1:
            errors["first_name"] = "First name is required"

        if len(form_data['last_name']) < 1:
            errors["last_name"] = "Last name is required"

        if len(form_data['email']) < 1:
            errors["email"] = "Email is required"

        if not email_check.match(form_data['email']):
            errors["email"] = "Invalid Email"

        if form_data['password'] != form_data['confirm']:
            errors["password"] = "Passwords do not match"

        user_email = self.filter(email=form_data['email'])
        if user_email:
            errors['email'] = "Email address in use"

        if len(form_data['birthday']) < 1:
            errors["birthday"] = "Birthday required"

        elif (datetime.strptime(form_data['birthday'], '%Y-%m-%d') > datetime.now()):
            errors['birthday'] = 'Date must be in the past'

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    birthday = models.DateField(auto_now_add=False,auto_now=False)
    password = models.CharField(max_length=255)
    objects = UserManager()