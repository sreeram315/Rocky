from annoying.functions import get_object_or_None
from django.db.models import Count
from django.conf import settings
from django.db import connection
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from rest_framework.exceptions import APIException
from . import models
from vehicles.models import Vehicles
from django.contrib.auth.models import User



class AddTollLogSerializer(serializers.Serializer):
	tollgate_id 			=	serializers.IntegerField()
	vehicle_id				=	serializers.IntegerField()
	ttype 					=	serializers.IntegerField()

	def validate_tollgate_id(self, tollgate_id):
		if not models.Tollgates.objects.filter(id = tollgate_id).exists():
			raise serializers.ValidationError(f"Tollgate does not exist for id:{tollgate_id}")
		return tollgate_id

	def validate_vehicle_id(self, vehicle_id):
		if not Vehicles.objects.filter(id = vehicle_id).exists():
			raise serializers.ValidationError(f"Vehicle does not exist for id:{vehicle_id}")
		return vehicle_id

	def validate_ttype(self, ttype):
		if not ttype in [t[0] for t in models.TOLL_TYPE]:
			raise serializers.ValidationError(f"Not a valid toll type :{ttype}")
		return ttype




class AddTollLogByNumberSerializer(serializers.Serializer):
	tollgate_id 			=	serializers.IntegerField()
	vehicle_reg				=	serializers.CharField()
	ttype 					=	serializers.IntegerField()

	def validate_tollgate_id(self, tollgate_id):
		if not models.Tollgates.objects.filter(id = tollgate_id).exists():
			raise serializers.ValidationError(f"Tollgate does not exist for id:{tollgate_id}")
		return tollgate_id

	# def validate_vehicle_id(self, vehicle_id):
	# 	if not Vehicles.objects.filter(id = vehicle_id).exists():
	# 		raise serializers.ValidationError(f"Vehicle does not exist for id:{vehicle_id}")
	# 	return vehicle_id

	def validate_ttype(self, ttype):
		if not ttype in [t[0] for t in models.TOLL_TYPE]:
			raise serializers.ValidationError(f"Not a valid toll type :{ttype}")
		return ttype
