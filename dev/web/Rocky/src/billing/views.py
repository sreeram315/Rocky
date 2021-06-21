from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from accounts.models import TollBillings
import datetime

class BillingHome(TemplateView):
	template_name	=	'billing/home.html'

	def get_context_data(self, *args, **kwargs):
		context = super(BillingHome, self).get_context_data(*args, **kwargs)
		context['billings'] = TollBillings.objects.all()
		for i in range(len(context['billings'])):
			context['billings'][i].index = i+1
		billings = context['billings']
		billings = [t for t in billings]
		billings.reverse()
		context['billings'] = billings
		return context





class InvoiceView(TemplateView):
	template_name	=	'invoice.html'


	def get_context_data(self, *args, **kwargs):
		context = 	{}
		uri 	= 	self.request.get_full_path()
		import requests
		query 		= 	requests.utils.urlparse(uri).query
		params 		= 	dict(x.split('=') for x in query.split('&'))

		tid 		= 	params['tid']
		objects 	= 	TollBillings.objects.filter(ticket_number = tid)

		obj 		=	objects.first()
		amount 		=	float("{:.2f}".format((obj.amount/1.14)))
		tax 		=	float("{:.2f}".format((obj.amount) - (amount)))

		context 	=	{
							'obj': obj,
							'due_date': obj.created_on.date() + datetime.timedelta(days=40),
							'amount': amount,
							'tax': tax,
							'gtotal': float(int(amount + tax))
						}
		return context


from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
def invoice_redirect(request):
	uri 		= 	request.get_full_path()
	import requests
	query 		= 	requests.utils.urlparse(uri).query
	params 		= 	dict(x.split('=') for x in query.split('&'))
	if not 'tid' in params:
		return HttpResponse("NO TICKET ID")
	tid 		= 	params['tid']
	objects 	= 	TollBillings.objects.filter(ticket_number = tid)
	if not objects.exists():
		return HttpResponse(f"TOLLBILLING DOES NOT EXISTS FOR ID = {tid}")
	return HttpResponseRedirect(f'/billing/invoice?tid={tid}')



from django.http import HttpResponse
from django.views.generic import View
from django.template.loader import get_template
from .utils import render_to_pdf #created in step 4

class GeneratePDF(View):
	def get(self, request, *args, **kwargs):
		uri 	= 	self.request.get_full_path()
		import requests
		query 		= 	requests.utils.urlparse(uri).query
		params 		= 	dict(x.split('=') for x in query.split('&'))

		tid 		= 	params['tid']
		objects 	= 	TollBillings.objects.filter(ticket_number = tid)

		obj 		=	objects.first()
		amount 		=	float("{:.2f}".format((obj.amount/1.14)))
		tax 		=	float("{:.2f}".format((obj.amount) - (amount)))

		context 	=	{
		'obj': obj,
		'due_date': obj.created_on.date() + datetime.timedelta(days=40),
		'amount': amount,
		'tax': tax,
		'gtotal': float(int(amount + tax))
		}
		template = get_template('i.html')

		html = template.render(context)
		pdf = render_to_pdf('i.html', context)
		if pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			filename = "Invoice_%s.pdf" %("12341231")
			content = "inline; filename='%s'" %(filename)
			download = request.GET.get("download")
			if download:
				content = "attachment; filename='%s'" %(filename)
			response['Content-Disposition'] = content
			return response
		return HttpResponse("Not found")









