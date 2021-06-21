from django.contrib import admin
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.utils.timezone import now
from django import forms

import datetime

from . import models

@admin.register(models.Tollgates)
class TollgatesAdmin(admin.ModelAdmin):
	common 				=	("name", "area", "latitude" , "longitude" , "min_charge")
	fields          	=   common
	list_display    	= 	common + ( "created_on", "updated_on" )

	list_display_links  = 	list_display
	model           	=   models.Tollgates
	extra           	=   0


@admin.register(models.TollgateLogs)
class TollgateLogsAdmin(admin.ModelAdmin):
    fields          	=   (  "tollgate", "vehicle" , "ttype", "date", "time")
    list_display    	= 	fields + ( "created_on", "updated_on" )

    list_display_links  = 	list_display
    model           	=   models.TollgateLogs
    extra           	=   0