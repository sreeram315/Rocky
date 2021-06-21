# import picamera
import datetime
import constants
from extraction import extract_reg_number
from add_tollog_entry import add_tollog_entry

def capture_image():
	with picamera.PiCamera() as camera:
		camera.start_preview()
		try:
			name = str(datetime.datetime.now())
			camera.capture(name)
		except:
			print(constants.CAPTURE_FAILED)
	exit()
	return name

def main():
	print("-- STARTING UP --")
	# image_name = capture_image()
	image_name = "new.jpg"
	reg_number = extract_reg_number(image_name)
	reg_number = 'MH20DV2366'
	print(reg_number)
	#add_tollog_entry(reg_number, constants.Ghatkesar_Toll_Plaza_ORR, constants.TTYPE_EXIT)


main()




