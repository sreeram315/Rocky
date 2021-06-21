from annoying.functions import get_object_or_None
from django.db.models import Count
from django.conf import settings
from django.db import connection
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from rest_framework.exceptions import APIException

from django.contrib.auth.models import User
from .models import Vehicles, VEHICLE_TYPES, VEHICLE_TYPES_DICT
from .models import Vehicles



class AddVehicleSerializer(serializers.Serializer):
	username 			=	serializers.CharField(max_length = 64)
	vtype				=	serializers.CharField(max_length = 64)
	brand 				=	serializers.CharField(max_length = 64)
	model 				=	serializers.CharField(max_length = 64)
	reg_number			=	serializers.CharField(max_length = 64)

	def validate_username(self, username):
		if not User.objects.filter(username = username).exists():
			raise serializers.ValidationError("Username does not exist")
		return username

	def validate_vtype(self, vtype):
		if not vtype in VEHICLE_TYPES_DICT.keys():
			raise serializers.ValidationError("Vehicle type does not exitst")
		return vtype

	def validate_reg_number(self, reg_number):
		import re
		if not bool(re.match(r'^[A-Z0-9]+$', reg_number)):
			raise serializers.ValidationError("Invalid Reg Number: Only Capital letter and numbers are allowed vro.")
		return reg_number
