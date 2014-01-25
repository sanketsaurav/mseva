from base import BaseHandler
from models import User

class Home(BaseHandler):
	"""
	Handle the homepage
	"""

	def get(self):
		"""
		For a GET request, render the homepage
		"""

		if self.user:
			# if the user is logged in, reder the dashboard
			self.render('dashboard.html', user=self.user)

		else:
			self.render('home.html')

class Login(BaseHandler):
	"""
	Handle the login
	"""

	def get(self):
		"""
		For a GET request, render the login page.
		"""

		if self.user:
			# if the user is already logged in, redirect her to the dashboard
			self.redirect('/')

		else:
			self.render('login.html')

	def post(self):
		"""
		For a POST request, log the user in and redirect her to the homepage
		"""

		email = self.response.get('email')
		password = self.response.get('password')

class Logout(BaseHandler):
	"""
	Handle the logout
	"""

	def get(self):
		"""
		For a GET request, log the user out by clearing the cookies
		"""

		self.set_secure_cookie('user', '')
		self.redirect('/')

class Signup(BaseHandler):
	"""
	Handle a new doctor registration.
	"""

	def post(self):
		"""
		For a POST request, register a new doctor.
		"""

		fields = {field:self.request.get(field) for field in DOCTOR_REG_FIELDS}

		try:
			new_user = User.create_user(fields)
			self.redirect('/login')

		except Exception, error_msg:
			self.render('signup.html', error = error, user = self.user)

def Connect(BaseHandler):
	"""
	Grab the category of doctor that needs to be connected to, and return the
	doctor's number in plaintext
	"""

	def get(self, category):
		"""
		Grab the category, and return the number of an available doctor
		"""

		exotel_response = {field:self.request.get(field) for field in EXOTEL_RESPONSE_FIELDS}
