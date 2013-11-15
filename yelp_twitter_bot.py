import config
import json
import subprocess
import time
import twitter
import urllib


class YelpTwitterBot(object):

	def __init__(self, tweet_handler=None):
		twitter_client_factory = TwitterClientFactory()
		self._twitter_stream_client = twitter_client_factory.create_twitter_stream_client()

		if tweet_handler is None:
			self._tweet_handler = TweetPrinter
		else:
			self._tweet_handler = tweet_handler

	def _get_tweet_with_location(self, tweet):
		location_extractor = LocationExtractor()
		location = location_extractor.find_location_from_tweet(tweet)
		return {
			'location': location,
			'tweet': tweet
		}

	def run(self):
		tweets = self._twitter_stream_client.statuses.filter(
			track='eat where, food where, hungry, starving, where restaurants"'
		)
		for tweet in tweets:
			tweet_with_location = self._get_tweet_with_location(tweet)
			self._tweet_handler.handle_tweet(tweet_with_location)


class TweetPrinter(object):

	def __init__(self):
		return

	def handle_tweet(self, tweet_with_location):
		if tweet_with_location['location']:
			print '******* Has Location *******'
		else:
			print 'xxxxxxx Missing Location xxxxxxx'
		print tweet_with_location



class TwitterClientFactory(object):

	def create_twitter_client(self):
		return twitter.Twitter(
			auth=self._get_auth()
		)

	def _get_auth(self):
		return twitter.OAuth(
			config.OAUTH_TOKEN,
			config.OAUTH_SECRET,
			config.CONSUMER_KEY,
			config.CONSUMER_SECRET
		)

	def create_twitter_stream_client(self):
		return twitter.TwitterStream(
			auth=self._get_auth()
		)


class LocationExtractor(object):

	MAX_RETRY_COUNT = 10

	def find_location_from_tweet(self, tweet):
		"""Use a node.js script to grab the location from the tweet"""
		if tweet['place']:
			return tweet['place']['full_name']
		return self._find_location_from_text(tweet['text'])

	def _find_location_from_text(self, text):
		json_result = None

		# We try `self.max_retry_count` times because of API limit issues
		for _ in range(self.MAX_RETRY_COUNT):
			json_result_string = subprocess.check_output([
				'node',
				'placespotter.js',
				config.YAHOO_CONSUMER_KEY,
				config.YAHOO_CONSUMER_SECRET,
				text
			])

			try:
				json_result = json.loads(json_result_string)
				break

			except:
				time.sleep(1)

		if json_result:
			return self._get_place_name_from_json_result(json_result)

	def _get_place_name_from_json_result(self, json_result):
		document = json_result['document']
		if not document:
			return

		placedetails = document['placedetails']

		if isinstance(placedetails, list):
			placedetail = placedetails[0]
		else:
			placedetail = placedetails

		return placedetail['place']['name']


if __name__ == '__main__':
	 YelpTwitterBot().run()
