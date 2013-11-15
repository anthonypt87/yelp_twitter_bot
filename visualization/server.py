import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket

import yelp_twitter_bot


class YelpTwitterBotWSHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		bot = yelp_twitter_bot.YelpTwitterBot(
			lambda *args: self.write_message(str(args))
		)
		bot.run()

	def on_message(self, message):
		print 'message received %s' % message

	def on_close(self):
	  print 'connection closed'


application = tornado.web.Application([
	(r'/ws', YelpTwitterBotWSHandler),
])

if __name__ == "__main__":
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(8888)
	tornado.ioloop.IOLoop.instance().start()
