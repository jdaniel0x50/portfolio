# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from portfolio.settings_environ import DOMAIN_NAME
from datetime import date, datetime, timedelta
import os


# Global Helper function to generate a case-insensitive
# sorting query (use return values with .extra() query)
def case_insensitive_criteria(sort_field_name):
    if sort_field_name[0] == '-':
        order_field = '-lower_field'
    else:
        order_field = 'lower_field'
    field_only = sort_field_name.strip('-')
    lower_field = "lower(" + field_only + ")"
    return (lower_field, order_field)

def sort_field_translator(sort_field_name, default):
    # translate the sort field to a model field
    translator = {
        "none": default,
        "first": "first_name",
        "-first": "-first_name",
        "last": "last_name",
        "-last": "-last_name",
        "email": "email",
        "-email": "-email",
        "created_at": "created_at",
        "-created_at": "-created_at",
        "updated_at": "updated_at",
        "-updated_at": "-updated_at"
    }
    return translator[sort_field_name]


class ContactManager(models.Manager):
    def get_all(self, sort_field="none", default="first_name"):
        model_field_name = sort_field_translator(sort_field, default)
        if "created_at" in model_field_name or "updated_at" in model_field_name:
            lower_field = model_field_name
            order_field = model_field_name
        else:
            lower_field, order_field = case_insensitive_criteria(
                model_field_name
            )
        contacts = (Contact.objects.all()
                    .extra(select={'lower_field':lower_field})
                    .order_by(order_field))
        return contacts

    def get_total(self):
        totals = {}
        totals['total'] = Contact.objects.all().count()
        return totals

    def get_or_create_contact(self, first_name, last_name, email):
        created = False
        try:
            contact = Contact.objects.get(email=email)
        except Contact.DoesNotExist:
            contact = Contact.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            created = True
        return contact, created
    def update_timestamp(self, email):
        contact = Contact.objects.get(email=email)
        contact.save()
        return


class Contact(models.Model):
    first_name = models.CharField(max_length=30, default="")
    last_name = models.CharField(max_length=30, default="")
    email = models.EmailField(max_length=100, default="test@test.com")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ContactManager()

