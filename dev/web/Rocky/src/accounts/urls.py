from django.conf.urls import url
from django.views.generic import TemplateView

from .views import (AccountsListView, UserAccountCreate, VerifyAccount, 
						SendOTP, MyVehiclesView, AddVehicleView, WalletHome, AddMoneyAPIView )


urlpatterns = [
	#templates
	url(r'list/$', AccountsListView.as_view(), name = 'account-list'),
	url(r'my-vehicles/$', MyVehiclesView.as_view(), name = 'my-vehicles'),
	url(r'add-vehicle/$', AddVehicleView.as_view(), name = 'add-vehicle'),
	#Wallet template

	url(r'wallet/$', WalletHome.as_view(), name = 'wallet-home'),
	url(r'api/wallet/add-money/$', AddMoneyAPIView.as_view(), name = 'add-money-api'),
	url(r'wallet/add-money/$', WalletHome.as_view(), name = 'add-money'),
	


	#apis
	url(r'api/create/$', UserAccountCreate.as_view(), name = 'account-create'),
	url(r'api/verify/$', VerifyAccount.as_view(), name = 'account-verify'),
	url(r'api/send-otp/$', SendOTP.as_view(), name = 'account-verify'),
	#wallet api
	

]

