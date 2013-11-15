import config
import json
import subprocess
import time
import twitter
import urllib


class YelpTwitterBot(object):

	def __init__(self):
		self._yelp_tweet_responder = self._construct_yelp_tweet_responder()

		twitter_client_factory = TwitterClientFactory()
		self._twitter_stream_client = twitter_client_factory.create_twitter_stream_client()


	def _construct_yelp_tweet_responder(self):
		location_extractor = LocationExtractor()
		submit_tweet_function = self._submit_tweet_function
		return YelpTweetResponder(
			submit_tweet_function,
			location_extractor.find_location_from_tweet
		)

	def _submit_tweet_function(self, *args):
		print '**********', args

	def run(self):
		tweets = self._twitter_stream_client.statuses.filter(track='eat where, food where, hungry, starving"')
		for tweet in tweets:
			print tweet
			self._yelp_tweet_responder.handle_tweet(tweet)


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


class YelpTweetResponder(object):

	def __init__(self, submit_tweet_function, get_location_function):
		self._submit_tweet = submit_tweet_function
		self._get_location = get_location_function

	def handle_tweet(self, tweet):
		location = self._get_location(tweet)
		if location:
			tweet_response = self._get_tweet_response(location)
			self._submit_tweet(
				tweet['user']['screen_name'],
				tweet_response
			)

	def _get_tweet_response(self, location):
		return 'We know just the place: %s' % self._get_yelp_url(location)

	def _get_yelp_url(self, location):
		escaped_location = urllib.quote_plus(location)
		yelp_url = 'http://www.yelp.com/search?find_desc=restaurants&find_loc=%s' % escaped_location
		return yelp_url


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
