from annoying.functions import get_object_or_None
from django.db.models import Count
from django.conf import settings
from django.db import connection
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from rest_framework.exceptions import APIException

from django.contrib.auth.models import User
from .models import UserProfile







class UserProfileCreateSerializer(serializers.Serializer):
	first_name 			=	serializers.CharField(max_length = 64)
	last_name			=	serializers.CharField(max_length = 64)
	username 			=	serializers.CharField(max_length = 64)
	password 			=	serializers.CharField(max_length = 64)
	email				=	serializers.EmailField()
	contact_number		=	serializers.IntegerField()

	def validate_email(self, email):
		if UserProfile.objects.filter(email = email).exists():
			raise serializers.ValidationError("Email already registered")
		return email

	def validate_contact_number(self, contact_number):
		if UserProfile.objects.filter(contact_number = contact_number).exists():
			raise serializers.ValidationError("Contact number already registered")
		return contact_number

	def validate_username(self, username):
		if User.objects.filter(username = username).exists():
			raise serializers.ValidationError("username already registered")
		return username



class VerifyAccountSerializer(serializers.Serializer):
	username 			=	serializers.CharField(max_length = 64)
	otp					=	serializers.IntegerField()

	def validate_username(self, username):
		if not User.objects.filter(username = username).exists():
			raise serializers.ValidationError(f"account does not exist with username: {username}")
		return username

class SendOTPSerializer(serializers.Serializer):
	username 			=	serializers.CharField(max_length = 64)

	def validate_username(self, username):
		if not User.objects.filter(username = username).exists():
			raise serializers.ValidationError(f"account does not exist with username: {username}")
		return username

class AddMoneySerializer(serializers.Serializer):
	username 				=	serializers.CharField(max_length = 64)
	amount					=	serializers.IntegerField()

	def validate_username(self, username):
		if not User.objects.filter(username = username).exists():
			raise serializers.ValidationError(f"account does not exist with username: {username}")
		return username













