import webapp2

app = webapp2.WSGIApplication([
								('/?', 'views.Home'),
								('/login/?', 'views.Login'),
								('/logout/?', 'views.Logout'),
								('/browse/?', 'views.Browse'),
								('/signup/?', 'views.Signup'),
								('/logs/?', 'views.UserLogs'),
								('/connect/([a-z]+)/?', 'views.Connect')
							], debug=True)