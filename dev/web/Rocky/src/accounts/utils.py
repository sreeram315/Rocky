import requests 
import json
import boto3
from django.conf import settings
from random import randint
from . import models  
from django.conf import settings
from django.template import loader


def send_message(contact_number, Message):
	sns = boto3.client(
							'sns',
							aws_access_key_id 		= 	settings.AWS_ACCESS_KEY_ID,
	                        aws_secret_access_key	=	settings.AWS_ACCESS_KEY,
	                        region_name 			=	settings.AWS_REGION
	                 )

	number 			= 		"+91" + str(contact_number)
	response 		= 		sns.publish(
											PhoneNumber = number, 
											Message = Message,  
											MessageAttributes = {
												                   'AWS.SNS.SMS.SMSType': {
												                       'DataType': 'String',
												                       'StringValue': 'Transactional'  # or 'Transactional'
												                   }
												               }
									)
	return True




def send_otp(name, contact_number, otp):
	sns = boto3.client(
							'sns',
							aws_access_key_id 		= 	settings.AWS_ACCESS_KEY_ID,
	                        aws_secret_access_key	=	settings.AWS_ACCESS_KEY,
	                        region_name 			=	settings.AWS_REGION
	                 )

	number 			= 		"+91" + str(contact_number)
	Message			=		f"Welcome {name},\nYour OTP for account verification is: {otp}.\nThank you, Team ROCKY."
	response 		= 		sns.publish(
											PhoneNumber = number, 
											Message = Message,  
											MessageAttributes = {
												                   'AWS.SNS.SMS.SMSType': {
												                       'DataType': 'String',
												                       'StringValue': 'Transactional'  # or 'Transactional'
												                   }
												               }
									)
	return True


def send_toll_bill_sms(toll_billing):
	user_full_name 	= toll_billing.vehicle.user.first_name + ' ' + toll_billing.vehicle.user.last_name
	ticket_number  	= toll_billing.ticket_number
	vehicle 		= toll_billing.vehicle
	tollgate_in    	= toll_billing.tollgate_in.tollgate.name
	tollgate_out   	= toll_billing.tollgate_out.tollgate.name
	transaction 	= toll_billing.transaction
	amount 			= toll_billing.amount
	wallet_balance  =toll_billing.vehicle.user.userprofile.wallet_balance


	sms_template 	= 	"billing_sms.txt"
	sms_context		=	{
							'user_full_name': user_full_name,
							'ticket_number': ticket_number,
							'vehicle': vehicle,
							'tollgate_in': tollgate_in,
							'tollgate_out': tollgate_out,
							'transaction': transaction,
							'distance': toll_billing.distance,
							'amount': amount, 
							'wallet_balance': wallet_balance
					}
	message 		= 	loader.render_to_string(sms_template, sms_context)

	send_message(toll_billing.vehicle.user.userprofile.contact_number, message)


# send_otp("Ram", 8919937557, 774184)

def get_ticket_number():
	tn = randint(111111, 999999)
	while models.TollBillings.objects.filter(ticket_number = tn).exists():
		tn = randint(111111, 999999)
	return f'TCKT{str(tn)}'

def get_transaction_id():
	tn = randint(111111, 999999)
	while models.WalletTransactions.objects.filter(transaction_id = tn).exists():
		tn = randint(111111, 999999)
	return f'RCKY{str(tn)}'

def get_distance(origin, destination):
	import googlemaps
	gmaps 			= 	googlemaps.Client(key = settings.GMAPS_KEY)
	# origin 			= 	(17.331674, 78.546539)
	# destination 	= 	(17.443062, 78.376958)
	gmap_reponse 	= 	gmaps.distance_matrix(origin, destination)
	distance 		=	int(gmap_reponse['rows'][0]['elements'][0]['distance']['value'])
	return distance





