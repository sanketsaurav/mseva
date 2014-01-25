import os
import jinja2

EXOTEL_SID = "mseva"
EXOTEL_TOKEN = "b27ba2bedf4aa491952ac2729e078d04f69afa7e"

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')

JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
								autoescape=True)

SECRET = "gfyf6s$^&gsbb78bcasb153347dsa6uh^(&yhd6"

DOCTOR_REG_FIELDS = ('name', 'regno', 'speciality', 'language', 
					'timeslot_day', 'timeslot_from', 'timeslot_to',
					'pincode', 'mobile', 'email', 'password')

EXOTEL_RESPONSE_FIELDS = ('CallSid', 'From', 'To', 
						'CallStatus', 'Direction')