from django.shortcuts import render

from django.views.generic import TemplateView
from django.http import HttpResponse
# Create your views here.
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from rest_framework import viewsets, permissions, exceptions, response
from .serializers import NewDonationSerializer
from .models import SugarDonations

from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView


class RedirectViewTest(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return 'https://tinyurl.com/ydbo47zj'




class TestTemplateView(TemplateView):
	template_name = 'test.html'

	def get_context_data(self, *args, **kwargs):
		print(self.request.META.get('HTTP_X_FORWARDED_FOR'))
		
		print(self.request.META.get('REMOTE_ADDR'))
		print(self.request.META.get('HTTP_USER_AGENT'))


class HomeTemplateView(TemplateView):
	template_name	=	'home.html'


class RegisterView(TemplateView):
	template_name   =  'register.html'

	def post(self, request):
		return HttpResponse('Hello')


class SugarCampView(TemplateView):
	template_name = 'sc.html'

	def get_context_data(self, *args, **kwargs):
		context = super(SugarCampView, self).get_context_data(*args, **kwargs)
		context['donations'] = SugarDonations.objects.all().order_by("-created_on")
		for i in range(len(context['donations'])):
			context['donations'][i].index = i+1
		return context





class NewDonationAPIView(APIView):
	permission_classes = (
        permissions.AllowAny,
    )

	def post(self, request):
		request_data 	= 	self.request.data
		serializer = NewDonationSerializer(data = request_data)
		if not serializer.is_valid():
			raise exceptions.ValidationError(serializer.errors)

		obj = SugarDonations.objects.create(
										name 			= serializer.data["name"],
										amount 			= serializer.data["amount"]
									)

		return response.Response(f'{obj.name} - {obj.amount}')


class Cupdate():

	def send_data(self, today_data):
		from datetime import datetime
		from django.template import loader
		from django.conf import settings
		# CONFIRMED 
		TOTAL_CONFIRMED = int(today_data['Confirmed']['tt'])
		TOTAL_CONFIRMED_TS = int(today_data['Confirmed']['tg'])
		today_data['Confirmed'].pop('status', None)
		today_data['Confirmed'].pop('date', None)
		today_data['Confirmed'].pop('tt', None)
		today_data['Confirmed'] = {k: v for k, v in sorted(today_data['Confirmed'].items(), key=lambda item: int(item[1]), reverse = True)}
		today_confirmed = [ [k,v] for k,v in today_data['Confirmed'].items() ][:3]
		# print(today_confirmed)

		# CONFIRMED 
		TOTAL_RECOVERED = int(today_data['Recovered']['tt'])
		TOTAL_RECOVERED_TS = int(today_data['Recovered']['tg'])
		today_data['Recovered'].pop('status', None)
		today_data['Recovered'].pop('date', None)
		today_data['Recovered'].pop('tt', None)
		today_data['Recovered'] = {k: v for k, v in sorted(today_data['Recovered'].items(), key=lambda item: int(item[1]), reverse = True)}
		today_recovered = [ [k,v] for k,v in today_data['Recovered'].items() ][:3]
		# print(today_recovered)

		# CONFIRMED 
		TOTAL_DECEASED = int(today_data['Deceased']['tt'])
		TOTAL_DECEASED_TS = int(today_data['Deceased']['tg'])
		today_data['Deceased'].pop('status', None)
		today_data['Deceased'].pop('date', None)
		today_data['Deceased'].pop('tt', None)
		today_data['Deceased'] = {k: v for k, v in sorted(today_data['Deceased'].items(), key=lambda item: int(item[1]), reverse = True)}
		today_deceased = [ [k,v] for k,v in today_data['Deceased'].items() ][:3]
		# print(today_deceased)

		# settings.configure()
		sms_context 	= 	{
								"TODAY_DATE": datetime.today(),

								"TOTAL_CONFIRMED": TOTAL_CONFIRMED,
								"TOTAL_CONFIRMED_TS": TOTAL_CONFIRMED_TS,
								"today_confirmed": today_confirmed,

								"TOTAL_RECOVERED": TOTAL_RECOVERED,
								"TOTAL_RECOVERED_TS": TOTAL_RECOVERED_TS,
								"today_recovered": today_recovered,

								"TOTAL_DECEASED": TOTAL_DECEASED,
								"TOTAL_DECEASED_TS": TOTAL_DECEASED_TS,
								"today_deceased": today_deceased

							}
		sms_template 	= 	"cupdate_sms.txt"
		message 		= 	loader.render_to_string(sms_template, sms_context)
		self.publich_re(message)




	def do(self):	
		import json
		from datetime import datetime


		months = {
		"1": "Jan",
		"2":"Feb",
		"3": "Mar",
		"4": "Apr",
		"5": "May",
		"6": "Jun",
		"7": "Jul",
		"8": "Aug",
		"9": "Sep",
		"10": "Oct",
		"11": "Nov",
		"12": "Dec",
		}

		data = open('states_daily.json').read()

		import requests
		data = requests.get(url = 'https://api.covid19india.org/states_daily.json').json()

		# data = json.loads(data)
		today = datetime.today()
		date = today.day-1
		if date < 10:
			date = f'0{date}'
		today = f'{str(date)}-{months[str(today.month)]}-{str(today.year)[2:]}'
		today_data = {}
		for obj in data['states_daily']:
			if today == obj["date"]:
				today_data[obj['status']] = obj
		if today_data == {}:
			pass
			# print("NO DATA YET")
		else:
			self.send_data(today_data)


	def publich_re(self, message):
		phones = ['8847373493', '9676937839', '7569887295', '9848854349', '9505551602', '8919937557', '7799403424']
		# phones = ['8919937557']
		for num in phones:
			from accounts.utils import send_message
			send_message(num, message)



















