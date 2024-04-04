import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from source.data_collection import get_top_news_topics, fetch_comments_from_reddit
from unittest.mock import patch, MagicMock

class TestGetTopNewsTopics(unittest.TestCase):
    def test_get_top_news_topics(self):
        # Test case for a valid city
        city = "New York"
        topics = get_top_news_topics(city)
        self.assertIsNotNone(topics)  # Check if topics list is not None
        self.assertIsInstance(topics, list)  # Check if topics is a list
        self.assertGreater(len(topics), 0)  # Check if topics list is not empty
        
        # Test case for an invalid city
        city = "InvalidCity"
        topics = get_top_news_topics(city)
        self.assertIsNone(topics)  # Check if topics list is None for invalid city

class TestFetchCommentsFromReddit(unittest.TestCase):
    @patch('source.data_collection.praw.Reddit')
    def test_fetch_comments_success(self, mock_reddit):
        # Mock submission
        mock_submission = MagicMock()
        mock_submission.comments.__getitem__.side_effect = lambda x: MagicMock(body=f"Comment {x}")
        mock_submission.comments.__iter__.return_value = range(15)
        
        # Mock Reddit instance
        mock_reddit.return_value.submission.return_value = mock_submission

        # Call the function with a fake post_id
        post_id = "fake_post_id"
        comments = fetch_comments_from_reddit(post_id)

        # Assertions
        self.assertEqual(len(comments), 15)
        self.assertEqual(comments[0], "Comment 0")
        self.assertEqual(comments[14], "Comment 14")

    @patch('source.data_collection.praw.Reddit')
    def test_fetch_comments_no_comments(self, mock_reddit):
        # Mock submission with no comments
        mock_submission = MagicMock()
        mock_submission.comments.__iter__.return_value = []

        # Mock Reddit instance
        mock_reddit.return_value.submission.return_value = mock_submission

        # Call the function with a fake post_id
        post_id = "fake_post_id"
        comments = fetch_comments_from_reddit(post_id)

        # Assertions
        self.assertEqual(len(comments), 0)


if __name__ == '__main__':
    unittest.main()