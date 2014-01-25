import os
import jinja2

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')

JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
								autoescape=True)

SECRET = "gfyf6s$^&gsbb78bcasb153347dsa6uh^(&yhd6"

DOCTOR_REG_FIELDS = ('name', 'regno', 'speciality', 'language', 
					'timeslot_day', 'timeslot_from', 'timeslot_to',
					'pincode', 'mobile', 'email', 'password')