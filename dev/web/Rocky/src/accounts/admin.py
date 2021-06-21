from django.contrib import admin
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.utils.timezone import now
from django import forms

import datetime

from . import models

@admin.register(models.UserProfile)
class AccountAdmin(admin.ModelAdmin):
    fields          =   (  "user", "wallet_balance", "otp" , "otp_datetime", "contact_number", "email", "is_verified")
    list_display    = 	fields + ( "created_on", "updated_on" )

    list_display_links  = list_display
    model           =   models.UserProfile
    extra           =   0


@admin.register(models.WalletTransactions)
class WalletTransactionsAdmin(admin.ModelAdmin):
    fields          =   ( "transaction_id", "user", "amount", "ttype" )
    list_display    = 	fields + ( "created_on", "updated_on" )

    list_display_links  = list_display
    model           =   models.WalletTransactions
    extra           =   0


@admin.register(models.TollBillings)
class TollBillingsAdmin(admin.ModelAdmin):
    fields          	=   ("vehicle", "tollgate_in", "tollgate_out", "distance" )
    list_display    	= 	("ticket_number", "amount") + fields + ( "created_on", "updated_on" )
    readonly_fields 	=	("ticket_number", "amount")

    list_display_links  = list_display
    model           	=   models.TollBillings
    extra           	=   0




