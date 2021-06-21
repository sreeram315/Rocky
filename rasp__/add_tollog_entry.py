import requests
import json
import constants


def add_tollog_entry(vehicle_reg, tollgate_id, ttype):
	headers = {
				"content-type":"application/json",
			}
	data = 	json.dumps({
					"tollgate_id": 	tollgate_id,
					"vehicle_reg": 	vehicle_reg,
					"ttype": 		ttype
			})

	resp = requests.post(
							url 	= constants.ADD_LOG_URL,
							headers = headers,
							data 	= data
				)
	print(resp.json())

# add_tollog_entry("Mh20dV2366", 7, constants.TTYPE_EXIT)