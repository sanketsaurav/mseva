from base import BaseHandler

class Home(BaseHandler):
	"""
	Handle the homepage.
	"""

	def get(self):
		"""
		For a GET request, render the homepage
		"""

		self.render('home.html')

class Signup(BaseHandler):
	"""
	Handle a new doctor registration.
	"""

	def post(self):
		"""
		For a POST request, register a new doctor.
		"""

		fields = {}

		for field in DOCTOR_REG_FIELDS:
			fields[field] = self.request.get(field)

		
