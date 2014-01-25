from base import BaseHandler

class Home(BaseHandler):
	"""
	Handle the homepage, which shows the 10 most recent blog posts
	"""

	def get(self):
		"""
		For a GET request, return the homepage
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

		pass

