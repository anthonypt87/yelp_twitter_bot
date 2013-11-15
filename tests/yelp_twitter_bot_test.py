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


class YelpTweetResponderTest(unittest.TestCase):

	def test_yelp_tweet_responder_responds_to_tweet_correctly(self):
		tweet = make_tweet()
		submit_tweet_function = mock.Mock()
		location_extractor = mock.Mock(return_value='San Francisco')
		tweet_responder = yelp_twitter_bot.YelpTweetResponder(
			submit_tweet_function,
			location_extractor
		)
		tweet_responder.handle_tweet(tweet)
		mock_url = 'http://www.yelp.com/search?find_desc=restaurants&find_loc=San+Francisco'
		submit_tweet_function.assert_called_once_with(tweet['user']['screen_name'], 'We know just the place: %s' % mock_url)


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
