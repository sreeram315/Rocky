from django.shortcuts import render
import datetime
from rest_framework import viewsets, permissions, exceptions, response
from django.views.generic import TemplateView
# Create your views here.

from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from django.contrib.auth.models import User

from .serializers import UserProfileCreateSerializer, VerifyAccountSerializer, SendOTPSerializer, AddMoneySerializer
from .models import UserProfile, WalletTransactions, TTYPE_CHOICES_DICT
from . import signals
from vehicles.models import Vehicles, VEHICLE_TYPES_DICT
from .utils import send_otp
import random



class WalletHome(TemplateView):
	template_name = 'wallet/home.html'

	def get_context_data(self, *args, **kwargs):
		context = super(WalletHome, self).get_context_data(*args, **kwargs)
		context['transactions'] = WalletTransactions.objects.filter(user = self.request.user).order_by("-created_on")
		for i in range(len(context['transactions'])):
			context['transactions'][i].index = i+1
			amount 	=	context['transactions'][i].amount
			context['transactions'][i].is_credit = True if context['transactions'][i].ttype==0 else False
			context['transactions'][i].amount = f'+{amount}' if context['transactions'][i].ttype==0 else f'-{amount}'
			context['transactions'][i].ttype = TTYPE_CHOICES_DICT[str(context['transactions'][i].ttype)]
			
			
			
		return context


class AccountsListView(TemplateView):
	template_name	=	'accounts/list.html'

	def get_context_data(self, *args, **kwargs):
		context = super(AccountsListView, self).get_context_data(*args, **kwargs)
		context['accounts'] = UserProfile.objects.all()
		for i in range(len(context['accounts'])):
			context['accounts'][i].index = i+1
		return context


class MyVehiclesView(TemplateView):
	template_name = 'accounts/my_vehicles.html'

	def get_context_data(self, *args, **kwargs):
		context = super(MyVehiclesView, self).get_context_data(*args, **kwargs)
		context['vehicles'] = Vehicles.objects.filter(user = self.request.user)
		for i in range(len(context['vehicles'])):
			context['vehicles'][i].index = i+1
			context['vehicles'][i].vtype = VEHICLE_TYPES_DICT[str(context['vehicles'][i].vtype)]
		return context

class AddVehicleView(TemplateView):
	template_name = 'accounts/add_vehicle.html'


class UserAccountCreate(APIView):
	permission_classes = (
        permissions.AllowAny,
    )

	def post(self, request):
		request_data 	= 	self.request.data
		serializer = UserProfileCreateSerializer(data = request_data)
		if not serializer.is_valid():
			raise exceptions.ValidationError(serializer.errors)

		user = User.objects.create(
									username = serializer.data["username"],
									first_name	= serializer.data["first_name"],
									last_name	= serializer.data["last_name"],
									email 		=	serializer.data["email"]
								)
		user.set_password(serializer.data["password"])
		user.save()
		UserProfile.objects.create(
							            user     		=   user,             
									    otp              =   25235151,  
									    otp_datetime      =   datetime.datetime.now(),   
									    profile_pic        =   None, 
									    contact_number 		=	serializer.data["contact_number"],
									    email = serializer.data["email"]
							        )
		signals.user_registered.send(sender = self.__class__, user = user, request = self.request)
		return response.Response(request_data)



class SendOTP(APIView):
	permission_classes = (
        permissions.AllowAny,
    )

	def random_digits(self, digits):
	    lower = 10 ** (digits - 1)
	    upper = 10 ** digits - 1
	    return random.randint(lower, upper)

	def post(self, request):
		request_data 	= 	self.request.data

		serializer = SendOTPSerializer(data = request_data)
		if not serializer.is_valid():
			raise exceptions.ValidationError(serializer.errors)
		username = serializer.data["username"]
		otp 		   = self.random_digits(6)
		userprofile = User.objects.get(username = username).userprofile
		userprofile.otp = otp
		userprofile.save()
		send_otp(userprofile.user.first_name, userprofile.contact_number, otp)

		return response.Response(f"DONE OTP:{str(otp)}")




class VerifyAccount(APIView):
	permission_classes = (
        permissions.AllowAny,
    )

	def post(self, request):
		request_data 	= 	self.request.data

		serializer = VerifyAccountSerializer(data = request_data)
		if not serializer.is_valid():
			raise exceptions.ValidationError(serializer.errors)

		user = User.objects.get(username = serializer.data["username"])
		if user.userprofile.otp == serializer.data["otp"]:
			user.userprofile.is_verified = True
			user.userprofile.save()
		else:
			raise APIException("WRONG OTP")
		return response.Response("VERIFID")


from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")

from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
	template_name = 'login.html'



class AddMoneyAPIView(APIView):
	def post(self, request):
		request_data 	= 	self.request.data

		serializer = AddMoneySerializer(data = request_data)
		if not serializer.is_valid():
			raise exceptions.ValidationError(serializer.errors)

		user = User.objects.get(username = serializer.data["username"])
		WalletTransactions.objects.create(user = user, ttype = 0, amount = serializer.data["amount"])
		 

		return response.Response(user.userprofile.wallet_balance)





















