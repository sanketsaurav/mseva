import webapp2

app = webapp2.WSGIApplication([
		('/?', 'views.Home'),
	], debug=True)