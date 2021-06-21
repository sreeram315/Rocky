
from rest_framework import viewsets, permissions, filters, exceptions, response
from rest_framework.views import APIView
from home.models import DeviceInfo
import datetime
from re import sub



class UserDeviceSave:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		response = self.get_response(request)
		return response

	def process_view(self, request, view_func, view_args, view_kwargs):
		try:
			addr 		= request.META.get('REMOTE_ADDR')
			device 		= request.META.get('HTTP_USER_AGENT')
			url 		= request.META.get('PATH_INFO', None),
			# print(url)
			# print(url[0].split('/'))
			# print(url[0].split('/')[1])
			DeviceInfo.objects.create(
										address 	= addr,
										device_info = device,
										url 		= url[0],
										is_admin_url= True if url[0].split('/')[1] == 'admin' else False
				)
		except:
			pass
		return None