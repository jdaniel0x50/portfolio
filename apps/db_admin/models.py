# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# local app-specific imports
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re
import bcrypt

PASSWORD_REGEX = re.compile(
    r'^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])[\w\d!@#$%^&?._]{8,15}$')


def create_error_dictionary(field_name, tag, message):
    error_dict = {
        "field_name": field_name,
        "tag": tag,
        "message": message,
    }
    return error_dict


class UserManager(models.Manager):
    def hash_password(self, password):
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return hashed

    def unique_validator(self, field, value):
        # determine whether a designated field is unique
        # returns a boolean true or false:
        # true -- value is unique
        # false -- value is not unique (generally the error condition)
        users = User.objects.filter(**{ field: value }).count()
        if users > 0:
            return False
        else:
            return True

    def basic_validator(self, postData):
        errors = []
        # errors will be a list of dictionaries containing error messages
        # each error message will be defined as a dictionary
        # error dictionary keys = field_name, tag, error_message

        # 1. confirm required fields are full
        required_fields = [
            "username", "first_name", "last_name", "password", "password_confirm"
        ]
        field_labels = {
            "username": "username",
            "first_name": "first name",
            "last_name": "last name",
            "password": "password",
            "password_confirm": "confirm password"
        }
        for field in required_fields:
            if len(postData[field]) < 1:
                tag = "blank"
                message = field_labels[field].capitalize(
                ) + " field cannot be empty"
                error_dict = create_error_dictionary(field, tag, message)
                errors.append(error_dict)

        # 2. confirm first_name, last_name are only alpha
        alpha_fields = [
            "first_name", "last_name"
        ]
        for field in alpha_fields:
            if not postData[field].isalpha():
                tag = "invalid"
                message = field_labels[field].capitalize(
                ) + " can only receive alphabetic characters"
                error_dict = create_error_dictionary(field, tag, message)
                errors.append(error_dict)

        # 3. confirm username is alphanumeric
        alphanumeric_fields = [
            "username"
        ]
        for field in alphanumeric_fields:
            if not postData[field].isalnum():
                tag = "invalid"
                message = field_labels[field].capitalize(
                ) + " can only receive alphabetic or numeric characters"
                error_dict = create_error_dictionary(field, tag, message)
                errors.append(error_dict)

        # 4. confirm username is unique
        try:
            User.objects.get(username=postData['username'])
            tag = "duplicate"
            field = "username"
            message = "The username already exists; please choose another"
            error_dict = create_error_dictionary(field, tag, message)
            errors.append(error_dict)
        except:
            pass

        # 5. confirm password is valid, or required length, and passwords match
        password_fields = [
            "password", "password_confirm"
        ]
        min_chars = 8
        for field in password_fields:
            if not PASSWORD_REGEX.match(postData[field]):
                tag = "invalid"
                message = "Passwords must have at least one number and one uppercase letter"
                error_dict = create_error_dictionary(field, tag, message)
                errors.append(error_dict)
            if len(postData[field]) < (min_chars + 1):
                tag = "short"
                message = "Passwords must have at least " + \
                    str(min_chars) + " characters"
                error_dict = create_error_dictionary(field, tag, message)
                errors.append(error_dict)
        if not postData[password_fields[0]] == postData[password_fields[1]]:
            tag = "match"
            field = "password"
            message = "Password fields do not match"
            error_dict = create_error_dictionary(field, tag, message)
            errors.append(error_dict)


    def login_validator(self, request, postData):
        # the validator will confirm the user is in the database
        # and the supplied password matches the db record
        # the result will be a dictionary object containing:
        # user: the logged in user if successful
        # errors: a list of errors if the login fails

        result = {}
        errors = []
        username = postData['username']
        str_message = "The username and/or password are not valid"
        user_regex = re.compile(r'^[a-zA-Z0-9_@\-\.]+$')
        print username
        print user_regex
        if re.match(user_regex, username) is None:
            # username failed regex validation
            print "FAILED REGEX"
            field_name = "username"
            tag = "login"
            error = create_error_dictionary(field_name, tag, str_message)
            errors.append(error)
        else:
            # username passed regex validation
            # continue to attempt to login with password validation
            try:
                # get user from database by username
                user_obj = User.objects.get(username=username)
                stored_hash = user_obj.password
                if bcrypt.checkpw(postData['password'].encode(), stored_hash.encode()):
                    # passwords match
                    # set user key in result dictionary
                    user = {
                        "id": user_obj.id,
                        "username": user_obj.username,
                        "first_name": user_obj.first_name
                    }
                    result['user'] = user
                else:
                    # passwords do not match
                    # generate a new error message
                    field_name = "password"
                    tag = "login"
                    error = create_error_dictionary(field_name, tag, str_message)
                    errors.append(error)
            except:
                # there were errors in the attempt to get user and password
                # generate a new error message
                field_name = "password"
                tag = "login"
                error = create_error_dictionary(field_name, tag, str_message)
                errors.append(error)
        result['errors'] = errors
        return result


class User(models.Model):
    username = models.CharField(
        max_length=50,
        blank=False,
        validators=[
            RegexValidator(
                regex='[a-zA-Z0-9@-_\.]+',
                message='Usernames may contain letters, numbers, ampersand, hyphen, underscore, and periods (no spaces)'
            ),
        ]
    )
    first_name = models.CharField(
        max_length=50,
        blank=False,
        validators=[
            RegexValidator(
                regex='[a-zA-Z\s\.]+',
                message='Names may contain letters, spaces, and periods'
            ),
        ]
    )
    last_name = models.CharField(
        max_length=50,
        blank=False,
        validators=[
            RegexValidator(
                regex='[a-zA-Z\s\.]+',
                message='Names may contain letters, spaces, and periods'
            ),
        ]
    )
    password = models.CharField(max_length=255, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
