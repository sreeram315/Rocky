from django.conf.urls import url
from django.views.generic import TemplateView

from .views import TollgateLogView, TollgateListView, MyTollgateListView, TollgateLogAddAPIView, TollgateLogAddByNumberAPIView


urlpatterns = [
	#templates

	url(r'my-log/$', MyTollgateListView.as_view(), name = 'my-tollgate-log'),
	url(r'log/$', TollgateLogView.as_view(), name = 'tollgate-log'),
	url(r'list/$', TollgateListView.as_view(), name = 'tollgate-log'),


	url(r'api/log/by-id-add$', TollgateLogAddAPIView.as_view(), name = 'tollgate-log-add-by-id'),


	url(r'api/log/add$', TollgateLogAddByNumberAPIView.as_view(), name = 'tollgate-log-add'),



	


	

]

