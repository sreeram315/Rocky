from django.conf.urls import url
from django.views.generic import TemplateView

from .views import VehiclesListView, AddVehicleAPIView


urlpatterns = [
	url(r'list', VehiclesListView.as_view()),


	#apis
	url(r'api/add-vehicle', AddVehicleAPIView.as_view(), name = 'vehicle-add'),
]

