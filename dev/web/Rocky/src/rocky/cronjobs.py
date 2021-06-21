from django_cron import CronJobBase, Schedule

import boto3
import datetime

from home.views import Cupdate

class KaronaUpdate(CronJobBase):
	RUN_EVERY_MINS 	= 	1

	schedule 		= 	Schedule(run_every_mins = RUN_EVERY_MINS)
	code 			= 	'my_app.my_cron_job'    

	def do(self):
		Cupdate().do()



















