from django.conf.urls import url
from django.views.generic import TemplateView

from .views import BillingHome, InvoiceView, invoice_redirect, GeneratePDF


urlpatterns = [
	#templates
	url(r'generate-invoice$', invoice_redirect, name = 'generate-invoice'),
	url(r'download-invoice$', GeneratePDF.as_view(), name = 'download-invoice'),
	url(r'invoice$', InvoiceView.as_view(), name = 'invoice'),
	
	url(r'$', BillingHome.as_view(), name = 'billing-home'),
]

