import os
import jinja2
import datetime

EXOTEL_SID = "mseva"
EXOTEL_TOKEN = "72a23675d8e7dd8834ba12e3c9b3ca0ea723fb18"
EXOTEL_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')

JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
								autoescape=True)

SECRET = "gfyf6s$^&gsbb78bcasb153347dsa6uh^(&yhd6"

DOCTOR_REG_FIELDS = ('name', 'regno', 'speciality', 'language', 
					'timeslot_day', 'timeslot_from', 'timeslot_to',
					'pincode', 'mobile', 'email', 'password')

EXOTEL_RESPONSE_FIELDS = ('CallSid', 'From', 'To', 
						'CallStatus', 'Direction')