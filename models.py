from google.appengine.ext import ndb

from utils import *

class User(ndb.Model):
	"""
	A registered user
	"""

	username = ndb.StringProperty(required=True)
	password = ndb.StringProperty(required=True)
	email = ndb.StringProperty()
	joined = ndb.DateTimeProperty(auto_now_add=True)

	@classmethod
	def create_user(cls, username, password, email=None):
		"""
		Create a new user with the provided credentials,
		and throw an exception if something's wrong
		"""

		if not is_username_valid(username):
			raise ValidationError("That's not a valid username.")

		user = cls.query(cls.username==username).fetch()
		if user:
			raise UserError("User already exists!")

		if not is_password_valid(password):
			raise ValidationError("That's not a valid password.")

		if email:
			if not is_email_valid(email):
				raise ValidationError("That's not a valid email.")

		new_user = cls(username=username, password=encrypt(password), email=email).put()
		
		return new_user.id()

	@classmethod
	def authenticate(cls, username, password):
		"""
		Check if the provided username and password are valid
		"""

		try:
			user = cls.query(cls.username==username).fetch()[0]

		except:
			raise UserError("User does not exist!")

		if user.username == username and user.password == encrypt(password):
			return str(user.key.id())
		else:
			raise AuthenticationError("Invalid username/password!")