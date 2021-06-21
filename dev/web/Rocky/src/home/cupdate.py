
import json
from datetime import datetime
from django.template import loader
from django.conf import settings


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

data = json.loads(data)
today = datetime.today()
today = f'28-{months[str(today.month)]}-{str(today.year)[2:]}'
today_data = {}
for obj in data['states_daily']:
	if today == obj["date"]:
		today_data[obj['status']] = obj

# CONFIRMED 
TOTAL_CONFIRMED = int(today_data['Confirmed']['tt'])
TOTAL_CONFIRMED_TS = int(today_data['Confirmed']['tg'])
today_data['Confirmed'].pop('status', None)
today_data['Confirmed'].pop('date', None)
today_data['Confirmed'].pop('tt', None)
today_data['Confirmed'] = {k: v for k, v in sorted(today_data['Confirmed'].items(), key=lambda item: int(item[1]), reverse = True)}
today_confirmed = [ {k:v} for k,v in today_data['Confirmed'].items() ][:3]
# print(today_confirmed)

# CONFIRMED 
TOTAL_CONFIRMED = int(today_data['Recovered']['tt'])
TOTAL_CONFIRMED_TS = int(today_data['Recovered']['tg'])
today_data['Recovered'].pop('status', None)
today_data['Recovered'].pop('date', None)
today_data['Recovered'].pop('tt', None)
today_data['Recovered'] = {k: v for k, v in sorted(today_data['Recovered'].items(), key=lambda item: int(item[1]), reverse = True)}
today_confirmed = [ {k:v} for k,v in today_data['Recovered'].items() ][:3]
# print(today_confirmed)

# CONFIRMED 
TOTAL_CONFIRMED = int(today_data['Deceased']['tt'])
TOTAL_CONFIRMED_TS = int(today_data['Deceased']['tg'])
today_data['Deceased'].pop('status', None)
today_data['Deceased'].pop('date', None)
today_data['Deceased'].pop('tt', None)
today_data['Deceased'] = {k: v for k, v in sorted(today_data['Deceased'].items(), key=lambda item: int(item[1]), reverse = True)}
today_confirmed = [ {k:v} for k,v in today_data['Deceased'].items() ][:3]
# print(today_confirmed)

settings.configure()
sms_context 	= 	{"name": "Sreeram", "time": today}
sms_template 	= 	"cupdate_sms.txt"
message 		= 	loader.render_to_string(sms_template, sms_context)

# print(message)





