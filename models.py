from google.appengine.ext import ndb
from google.appengine.api import memcache

from utils import *

class User(ndb.Model):
	"""
	A registered Doctor.
	"""

	SPECIALITY_OPTIONS = ['GENERAL',
						'CARDIAC',
						'GYNAEC',
						'PEDIATRIC']

	LANGUAGE_OPTIONS = ['HI', 'EN', 'BN']

	name = ndb.StringProperty(required=True)
	regno = ndb.StringProperty(required=True)
	speciality = ndb.StringProperty(required=True,
									choices=SPECIALITY_OPTIONS)
	language = ndb.StringProperty(required=True,
								choices=LANGUAGE_OPTIONS)
	
	timeslot_from = ndb.StringProperty(required=True)
	timeslot_to = ndb.StringProperty(required=True)
	
	mobile = ndb.StringProperty(required=True)
	pincode = ndb.StringProperty(required=True)
	
	is_active = ndb.BooleanProperty(default=False)
	email = ndb.StringProperty(required=True, indexed=True)
	password = ndb.StringProperty(required=True)
	joined = ndb.DateTimeProperty(auto_now_add=True)

	latest_call = ndb.DateTimeProperty(default=datetime.datetime.now())

	def log_latest_call(self):
		"""
		Log the latest call dispatched to the doctor
		"""

		self.latest_call = datetime.datetime.now()
		self.put()

	@classmethod
	def fetch_available_users(cls, speciality, hour):
		"""
		Returns the available users
		"""
		top_users = cls.query(cls.speciality==speciality).filter(cls.timeslot_from < hour).fetch()
		return list(top_users)[0]

	@classmethod
	def create_user(cls, fields):
		"""
		Create a new user with the provided credentials,
		and throw an exception if something's wrong
		"""

		# TODO: Add validation for PIN code and Registration
		# number.

		if not is_email_valid(fields['email']):
			raise ValidationError("That's not a valid email.")

		user = cls.query(cls.email==fields['email']).fetch()

		if user:
			raise UserError("This email is already registered!")

		if not is_password_valid(fields['password']):
			raise ValidationError("That's not a valid password.")

		fields['password'] = encrypt(fields['password'])

		new_user = cls(**fields).put()
		
		return new_user.id()

	@classmethod
	def authenticate(cls, email, password):
		"""
		Check if the provided username and password are valid
		"""

		try:
			user = cls.query(cls.email==email).fetch()[0]

		except:
			raise UserError("User does not exist!")

		if user.email == email and user.password == encrypt(password):
			return str(user.key.id())
		else:
			raise AuthenticationError("Invalid email/password!")

class Log(ndb.Model):
	"""
	Call logs to store each incoming call, and the doctor to whom each
	call is being connected to
	"""

	call_sid = ndb.StringProperty(required=True, indexed=True)
	from_number = ndb.StringProperty(required=True)
	call_duration = ndb.StringProperty()
	start_time = ndb.StringProperty()
	end_time = ndb.StringProperty()
	doctor = ndb.KeyProperty(required=True, kind='User')
	added = ndb.DateTimeProperty(auto_now_add=True)

	@classmethod
	def log_call_pre(cls, call_sid, from_number, doctor):
		"""
		Logs the details when a call has been routed
		"""

		call = cls(call_sid=call_sid, from_number=from_number, doctor=doctor).put()
		return call.urlsafe()

	def log_call_post(cls, call_sid, call_duration, start_time, end_time):
		"""
		Add call log data after the call has finished
		"""

		call = cls.query(cls.call_sid==call_sid).fetch()

		if call:
			call.call_duration = call_duration
			call.start_time = start_time
			call.end_time = end_time

			return call.put()
