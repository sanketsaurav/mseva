from base import BaseHandler
from models import User, Log

from config import *

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

		email = self.request.get('email')
		password = self.request.get('password')

		try:
			user_id = User.authenticate(email, password)
			self.set_secure_cookie('user', str(user_id))
			self.redirect('/')
		
		except Exception, e:
			self.render("login.html", user=self.user, error = e)

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
	def get(self):
		self.render('signup.html')

	def post(self):
		"""
		For a POST request, register a new doctor.
		"""

		fields = {field:self.request.get(field) for field in DOCTOR_REG_FIELDS}

		try:
			new_user = User.create_user(fields)
			self.redirect('/login')

		except Exception, error_msg:
			self.render('signup.html', error = error_msg, fields=fields, user = self.user)

class Connect(BaseHandler):
	"""
	Grab the category of doctor that needs to be connected to, and return the
	doctor's number in plaintext
	"""

	def get(self, category):
		"""
		Grab the category, and return the number of an available doctor
		"""

		exotel_response = {field:self.request.get(field) for field in EXOTEL_RESPONSE_FIELDS}

		today = datetime.datetime.now(IST())

		day = str(today.weekday())
		hour = str(today.hour) + str(today.minutes)

		doctor = User.get_available(category, day, hour)

		if doctor:
			#put logging in taskqueue with URL-safe key
			Log.log_call_pre(call_sid=exotel_response['CallSid'],
							from_number=exotel_response['From'],
							doctor=doctor)
			self.response.out.write(doctor.mobile)

class PassthruLog(BaseHandler):
	"""
	Log the call details received from passthru applet
	"""

	def get():
		"""
		Log the post-call data
		"""

		call_sid = self.request.get('CallSid')
		call = Log.query(Log.call_sid==call_sid).fetch()

		if call:
			call_duration = self.request.get('DialCallDuration')
			start_time = self.request.get('StartTime')
			end_time = self.request.get('EndTime')

			call.put()

class Browse(BaseHandler):
	"""
	Handle browse
	"""

	def get(self):

		doctors=User.get_all() or []
		self.render('browse.html', doctors=doctors, user=self.user)

