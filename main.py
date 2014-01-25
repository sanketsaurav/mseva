import webapp2

app = webapp2.WSGIApplication([
								('/?', 'views.Home'),
								('/login/?', 'views.Login'),
								('/logout/?', 'views.Logout'),
								('/signup/?', 'views.Signup'),
								('/connect/([a-z]+)/?', 'views.Connect')
							], debug=True)