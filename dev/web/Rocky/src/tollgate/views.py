from django.shortcuts import render
from rest_framework import viewsets, permissions, exceptions, response
# Create your views here.
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from django.views.generic import TemplateView
from .models import Tollgates, TollgateLogs, TOLL_TYPE_DICT
from .serializers import AddTollLogSerializer, AddTollLogByNumberSerializer
from vehicles.models import Vehicles


class TollgateLogAddAPIView(APIView):

	def post(self, request):
		# print("HIT ADD ID")
		request_data 	= 	self.request.data
		serializer 		= 	AddTollLogSerializer(data = request_data)
		if not serializer.is_valid():
			raise exceptions.ValidationError(serializer.errors)

		tollgate 	= Tollgates.objects.get(id = serializer.data["tollgate_id"])
		vehicle 	= Vehicles.objects.get(id = serializer.data["vehicle_id"])
		ttype 		= TOLL_TYPE_DICT[str(serializer.data["ttype"])]

		tollgate_log = TollgateLogs.objects.create(
														tollgate = tollgate,
														vehicle  = vehicle,
														ttype    = str(serializer.data["ttype"])
													)

		return response.Response(f'''Tollgate: {tollgate.name.upper()}, Vehicle: {vehicle.brand.upper()} | {vehicle.reg_number.upper()},ttype: {ttype.upper()}''')


class TollgateLogAddByNumberAPIView(APIView):

	def post(self, request):
		# print("HIT ADD REG")
		request_data 	= 	self.request.data
		serializer 		= 	AddTollLogByNumberSerializer(data = request_data)
		if not serializer.is_valid():
			raise exceptions.ValidationError(serializer.errors)

		tollgate 	= Tollgates.objects.get(id = serializer.data["tollgate_id"])
		ttype 		= TOLL_TYPE_DICT[str(serializer.data["ttype"])]

		vehicle_reg = serializer.data["vehicle_reg"].upper()
		vehicles 	= Vehicles.objects.filter(reg_number = vehicle_reg)
		if not vehicles.exists():
			raise APIException(f"No vehicle found for reg_number: {vehicle_reg}")
		vehicle 	= vehicles.first()

		tollgate_log = TollgateLogs.objects.create(
														tollgate = tollgate,
														vehicle  = vehicle,
														ttype    = str(serializer.data["ttype"])
													)

		return response.Response(f'''Tollgate: {tollgate.name.upper()}, Vehicle: {vehicle.brand.upper()} | {vehicle.reg_number.upper()},ttype: {ttype.upper()}''')


class MyTollgateListView(TemplateView):
	template_name = 'tollgate/my_log.html'

	def get_context_data(self, *args, **kwargs):
		context = super(MyTollgateListView, self).get_context_data(*args, **kwargs)
		context['toll_gate_log'] = TollgateLogs.objects.filter(vehicle__user = self.request.user)
		for i in range(len(context['toll_gate_log'])):
			context['toll_gate_log'][i].index = i+1
			context['toll_gate_log'][i].ttype = TOLL_TYPE_DICT[str(context['toll_gate_log'][i].ttype)]
		return context

class TollgateLogView(TemplateView):
	template_name	=	'tollgate/log.html'

	def get_context_data(self, *args, **kwargs):
		context = super(TollgateLogView, self).get_context_data(*args, **kwargs)
		context['toll_gate_log'] = TollgateLogs.objects.all()
		for i in range(len(context['toll_gate_log'])):
			context['toll_gate_log'][i].index = i+1
			context['toll_gate_log'][i].ttype = TOLL_TYPE_DICT[str(context['toll_gate_log'][i].ttype)]
		return context



class TollgateListView(TemplateView):
	template_name = 'tollgate/list.html'

	def get_context_data(self, *args, **kwargs):
		context = super(TollgateListView, self).get_context_data(*args, **kwargs)
		context['toll_gates'] = Tollgates.objects.all()
		for i in range(len(context['toll_gates'])):
			context['toll_gates'][i].index = i+1
		return context