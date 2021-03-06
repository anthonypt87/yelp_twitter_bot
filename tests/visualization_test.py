import mock
import json
import unittest

from visualization import server


class MessageWriterTweetHandlerTest(unittest.TestCase):

	def test_tweets_are_given_to_submit_function(self):
		mock_submit_function = mock.Mock()
		handler = server.MessageWriterTweetHandler(
			mock_submit_function
		)
		tweet = {'tweet': None}
		handler.handle_tweet(tweet)
		mock_submit_function.assert_called_once_with(json.dumps(tweet))


if __name__ == '__main__':
	 unittest.main()
