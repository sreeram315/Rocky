from django.contrib import admin
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.utils.timezone import now
from django import forms

import datetime

from . import models

@admin.register(models.Vehicles)
class AccountAdmin(admin.ModelAdmin):
    fields          =   ("user", "vtype" , "brand", "model", "reg_number")
    list_display    = 	fields + ( "created_on", "updated_on" )

    list_display_links  = list_display
    model           =   models.Vehicles
    extra           =   0