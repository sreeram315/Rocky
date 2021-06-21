import requests
import base64
import json





def photo_to_reg(image):
	with open(image, "rb") as image_file:
		encoded_string = base64.b64encode(image_file.read()).decode("ascii")


	url = 'https://www.de-vis-software.ro/platebber.aspx'
	userAndPass = base64.b64encode(b"wiramaram@gmail.com:sreerAM31@").decode("ascii")
	headers = {
				"Authorization": 'Basic %s' %  userAndPass,
				"Content-Type": "application/json",
				"Accept": "application/json"
	}

	data = {
			  "base64ImageString": '%s' % encoded_string,
			  "languageCode": "auto",
			  "plate_output": "no"
	}
	data=json.dumps(data)
	res = requests.post(
							url 	= 	url,
							headers	=	headers,
							data	=	data
				)
	data = res.json()
	print(data)
	exit()
	# data = [{'id': 'license_plate', 'description': 'License plate', 'timestamp': '2020-06-06 04:05:24', 'bounding_box_confidence': 0.846912682056427, 'x1': 242, 'y1': 439, 'x2': 406, 'y2': 439, 'x3': 406, 'y3': 489, 'x4': 242, 'y4': 489, 'plate_text': 'MH02CP8000|MH02CP8000', 'base64PlatePhoto': ''}]
	reg_number = (data[0]['plate_text'].split('|')[0]).strip()
	
	print(reg_number)


def photo_to_reg2(image):
	reg_number = (((requests.post(url='https://www.de-vis-software.ro/platebber.aspx',headers={"Authorization": 'Basic %s' %  base64.b64encode(b"sreerammaram2@gmail.com:sreerAM31@").decode("ascii"),"Content-Type": "application/json","Accept": "application/json"},data=json.dumps({"base64ImageString": '%s' % base64.b64encode((open(image, "rb")).read()).decode("ascii"),"languageCode": "auto","plate_output": "no"}))).json())[0]['plate_text'].split('|')[0]).strip()
	print(reg_number)

photo_to_reg("new.jpg")























