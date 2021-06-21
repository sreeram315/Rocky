from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MaxValueValidator
from django.db.models.signals import pre_save, post_save

VEHICLE_TYPES = (
					(0, 'Unicycle'),
					(1, '2 wheeler'),
					(2, '3 wheeler'),
					(3, '4 wheeler'),
					(4, 'Heavy passenger motor vehicle'),
					(5, 'Heavy goods motor vehicle'),
				)
VEHICLE_TYPES_DICT = {}
for v in VEHICLE_TYPES:
	VEHICLE_TYPES_DICT[str(v[0])] = v[1]

TOLL_CHARGE = {
	"0": 0.001,
	"1": 0.001,
	"2": 0.002,
	"3": 0.0033,
	"4": 0.0054,
	"5": 0.0065,
}


class Vehicles(models.Model):
	user                    = 	models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'vehicles')
	vtype 					=	models.IntegerField(choices = VEHICLE_TYPES, null = True, blank  =True)
	brand 					=	models.CharField(max_length = 50, blank=True, null=True)
	model 					=	models.CharField(max_length = 50, blank=True, null=True)
	reg_number 				=	models.CharField(max_length = 50, blank=True, null=True, validators = [RegexValidator(r'^[A-Z0-9]+$')])

	created_on          	=   models.DateTimeField(auto_now_add = True, null = True, blank  = True)
	updated_on 				=	models.DateTimeField(auto_now = True, null = True, blank  = True)


	class Meta:
		db_table            = "tbl_vehicles"
		verbose_name        = "Vehicle"
		verbose_name_plural = "Vehicles"

	def __str__(self):
		return f'{self.brand} | {VEHICLE_TYPES_DICT[str(self.vtype)]} | {self.reg_number}'



def vehicles_pre_save(sender, instance, *args, **kwargs):
	instance.reg_number = instance.reg_number.upper()

    

pre_save.connect(vehicles_pre_save, sender = Vehicles)







