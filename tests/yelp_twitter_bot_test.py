import contextlib
import mock
import unittest

import yelp_twitter_bot


def make_tweet(**extra_params):
	tweet = {
		'text': u'Where do I eat in San Francisco?',
		'user': {u'screen_name': u'100chainz_on'},
		'id': 401096914302951424,
		'created_at': u'Thu Nov 14 21:18:51 +0000 2013',
		'coordinates': None,
		'in_reply_to_screen_name': None,
		'place': None
	}
	tweet.update(extra_params)
	return tweet


class YelpTwitterBotTest(unittest.TestCase):

	def test_that_tweets_are_passed_with_location_to_tweet_handler(self):
		tweet_handler = mock.Mock()

		tweet = make_tweet()

		mock_client = mock.Mock()
		mock_client.statuses.filter.return_value = [tweet]
		with contextlib.nested(
			mock.patch.object(
				yelp_twitter_bot.TwitterClientFactory,
				'create_twitter_stream_client',
				return_value=mock_client
			),
			mock.patch.object(
				yelp_twitter_bot.LocationExtractor,
				'find_location_from_tweet',
				return_value=None
			)
		):
			bot = yelp_twitter_bot.YelpTwitterBot(tweet_handler)
			bot.run()

		tweet_handler.handle_tweet.assert_called_once_with(
			{
				'location': None,
				'tweet': tweet,
				'yelp_url': None,
			}
		)


class LocationExtractorTest(unittest.TestCase):

	def test_find_location_from_text(self):
		tweet = make_tweet(text='Where do I eat in Manhattan, New York')
		self._assert_location(tweet, 'Manhattan, New York, NY, US')

	def _assert_location(self, tweet, expected_location):
		location_extractor = yelp_twitter_bot.LocationExtractor()
		location = location_extractor.find_location_from_tweet(tweet)
		self.assertEqual(location, expected_location)

	def test_find_location_from_tweet_place_has_precedence_over_from_text(self):
		place = {u'full_name': u'Santa Monica, CA'}
		tweet = make_tweet(text='Where do I eat in Manhattan, New York', place=place)
		self._assert_location(tweet, 'Santa Monica, CA')


if __name__ == '__main__':
	 unittest.main()
