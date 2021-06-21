from django.shortcuts import render
from rest_framework import viewsets, permissions, exceptions, response

from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from django.contrib.auth.models import User

# Create your views here.
from .models import Vehicles, VEHICLE_TYPES, VEHICLE_TYPES_DICT
from .serializers import AddVehicleSerializer


class VehiclesListView(TemplateView):
	template_name	=	'vehicles/list.html'

	def get_context_data(self, *args, **kwargs):
		context = super(VehiclesListView, self).get_context_data(*args, **kwargs)
		context['vehicles'] = Vehicles.objects.all()
		for i in range(len(context['vehicles'])):
			context['vehicles'][i].index = i+1
			context['vehicles'][i].vtype = VEHICLE_TYPES_DICT[str(context['vehicles'][i].vtype)]
		return context



class AddVehicleAPIView(APIView):

	def post(self, request):
		request_data 	= 	self.request.data
		serializer 		= 	AddVehicleSerializer(data = request_data)
		if not serializer.is_valid():
			raise exceptions.ValidationError(serializer.errors)

		user 			=	User.objects.get(username = serializer.data["username"])
		vehicle 		= 	Vehicles.objects.create(
									user 		= 	user,
									vtype		= 	serializer.data["vtype"],
									brand		= 	serializer.data["brand"],
									model 		=	serializer.data["model"],
									reg_number 	=	serializer.data["reg_number"]
								)

		return response.Response(request_data)







