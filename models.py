from google.appengine.ext import ndb

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
	
	timeslot_day = ndb.StringProperty(required=True)
	timeslot_from = ndb.StringProperty(required=True)
	timeslot_to = ndb.StringProperty(required=True)
	
	mobile = ndb.StringProperty(required=True)
	pincode = ndb.StringProperty(required=True)
	
	is_active = ndb.BooleanProperty(default=False)
	email = ndb.StringProperty(required=True, indexed=True)
	password = ndb.StringProperty(required=True)
	joined = ndb.DateTimeProperty(auto_now_add=True)

	@classmethod
	def create_user(cls, fields):
		"""
		Create a new user with the provided credentials,
		and throw an exception if something's wrong
		"""

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
	def authenticate(cls, username, password):
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