from django.db import models
from rest_framework.exceptions import APIException
from django.contrib.auth.models import User
from vehicles.models import Vehicles
# Create your models here.
from django.db.models.signals import pre_save, post_save
from django.core.exceptions import ValidationError
import datetime
from django.utils.translation import gettext_lazy as _


def curr_date():
	return datetime.datetime.now().date()

def curr_time():
	return datetime.datetime.now().time()


TOLL_TYPE = (
					(0, 'Entry'),
					(1, 'Exit'),
				)

RTOLL_TYPE = {}
for t in TOLL_TYPE:
	RTOLL_TYPE[str(t[1])] = t[0]

TOLL_TYPE_DICT = {}
for t in TOLL_TYPE:
	TOLL_TYPE_DICT[str(t[0])] = t[1]



class Tollgates(models.Model):
	name 					=	models.CharField(max_length = 256, blank = True, null = True)
	area                	= 	models.CharField(max_length = 127, blank = True, null = True)
	latitude        		=   models.DecimalField(_("Latitude"), max_digits = 9, decimal_places = 6, help_text = _("Tollgate Latitude"))
	longitude       		=   models.DecimalField(_("Longitude"), max_digits = 9, decimal_places = 6, help_text = _("Tollgate Longitude"))
	min_charge 				=	models.PositiveIntegerField(default = 0)


	created_on          	=   models.DateTimeField(auto_now_add = True, null = True, blank  =True)
	updated_on 				=	models.DateTimeField(auto_now = True, null = True, blank  =True)



	class Meta:
		db_table            = "tbl_tollgates"
		verbose_name        = "Tollgate"
		verbose_name_plural = "Tollgates"

	def __str__(self):
		return f'{self.area}'



class TollgateLogs(models.Model):
	tollgate 				=	models.ForeignKey(Tollgates, on_delete=models.CASCADE, related_name = 'log')
	vehicle 				=	models.ForeignKey(Vehicles, on_delete=models.CASCADE, related_name = 'log')
	ttype  					=	models.PositiveIntegerField(choices = TOLL_TYPE, null = True, blank  =True)
	date 					=	models.DateField(default = curr_date)
	time 					=	models.TimeField(default = curr_time)

	created_on          	=   models.DateTimeField(auto_now_add = True, null = True, blank  =True)
	updated_on 				=	models.DateTimeField(auto_now = True, null = True, blank  =True)


	class Meta:
		db_table            = "tbl_tollgatelog"
		verbose_name        = "TollgateLog"
		verbose_name_plural = "TollgateLogs"

	def __str__(self):
		return f'{self.id}:  TollgateLog:{TOLL_TYPE_DICT[str(self.ttype)]}  {self.vehicle} - {self.date} - {self.time}'

def tollgate_log_pre_save(sender, instance, *args, **kwargs):
	is_new = not TollgateLogs.objects.filter(id = instance.id).exists()
	# print(f'is_new = {is_new}')
	if is_new:
		entries = TollgateLogs.objects.filter(vehicle = instance.vehicle).order_by("-created_on")
		#print(str(instance.ttype))
		#print(TOLL_TYPE_DICT[str(instance.ttype)])
		if TOLL_TYPE_DICT[str(instance.ttype)] == 'Entry':
			# Check last entry is EXIT or NOT exists
			if (entries.exists()) and (TOLL_TYPE_DICT[str(entries.first().ttype)] == 'Entry'):
				raise APIException("Your Last entry is Toll gate-ENTRY or Does not exist")
		if TOLL_TYPE_DICT[str(instance.ttype)] == 'Exit':
			# Check exists and last entry is ENTRY
			# print("EXIT Check")
			if (not entries.exists()):
				raise APIException("First ENTER to EXIT")
			if (TOLL_TYPE_DICT[str(entries.first().ttype)] == 'Exit'):
				raise APIException("Your Last entry is Toll gate EXIT")
			if instance.tollgate == TollgateLogs.objects.filter(vehicle = instance.vehicle, ttype=0).order_by("-created_on").first().tollgate:
				raise APIException('Cannot Enter and exit at same gate')



pre_save.connect(tollgate_log_pre_save, sender = TollgateLogs)



def tollgate_log_post_save(sender, instance, *args, **kwargs):
	if TOLL_TYPE_DICT[str(instance.ttype)] == 'Exit':
		# print("EXIT TOLL")
		from accounts.models import TollBillings
		used_exits = TollBillings.objects.all().values_list("tollgate_out")
		used_exits = [t[0] for t in used_exits]
		# print(used_exits)
		if instance.id not in used_exits:
			ENTRY = TollgateLogs.objects.filter(vehicle = instance.vehicle, ttype=0).order_by("-created_on").first()
			EXIT  = instance
			TollBillings.objects.create(
										vehicle = instance.vehicle,
										tollgate_in = ENTRY,
										tollgate_out = EXIT
								)


post_save.connect(tollgate_log_post_save, sender = TollgateLogs)




