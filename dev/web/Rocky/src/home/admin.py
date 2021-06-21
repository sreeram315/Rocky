from django.contrib import admin

# Register your models here.

from . import models



@admin.register(models.DeviceInfo)
class DeviceInfoAdmin(admin.ModelAdmin):
	fields          	=   (  "address", "device_info", "url", "is_admin_url", "comments")
	list_display    	= 	fields + ( "created_on", "updated_on" )

	list_display_links  =   list_display
	model           	=   models.DeviceInfo
	extra           	=   0

	list_filter = (
		'is_admin_url',
	)



@admin.register(models.SugarDonations)
class AccountAdmin(admin.ModelAdmin):
    fields          	=   (  "name", "contact_number", "amount")
    list_display    	= 	fields + ( "created_on", "updated_on" )

    list_display_links  =   list_display
    model           	=   models.SugarDonations
    extra           	=   0