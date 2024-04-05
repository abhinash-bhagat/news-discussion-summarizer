import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from source.data_collection import get_top_news_topics, fetch_comments_from_reddit, save_data
from unittest.mock import patch, MagicMock

class TestGetTopNewsTopics(unittest.TestCase):
    def test_get_top_news_topics(self):
        # Test case for a valid city
        city = "New York"
        topics = get_top_news_topics(city)
        self.assertIsNotNone(topics)  # Check if topics list is not None
        self.assertIsInstance(topics, list)  # Check if topics is a list
        self.assertGreater(len(topics), 0)  # Check if topics list is not empty


class TestSaveData(unittest.TestCase):
    
    @patch('source.data_collection.get_top_news_topics')
    @patch('source.data_collection.praw.Reddit')
    @patch('source.data_collection.fetch_comments_from_reddit')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_save_data_success(self, mock_open, mock_fetch_comments, mock_reddit, mock_get_top_news_topics):
        # Setup mocks
        mock_get_top_news_topics.return_value = ['topic1', 'topic2']
        mock_submission1 = MagicMock()
        mock_submission1.title = 'Post 1'
        mock_submission2 = MagicMock()
        mock_submission2.title = 'Post 2'
        mock_search_results = [mock_submission1, mock_submission2]
        mock_reddit.subreddit.return_value.search.return_value = mock_search_results
        mock_fetch_comments.return_value = ['comment1', 'comment2', 'comment3', 'comment4']
        
        # Call the function
        result = save_data('New York')
        
        # Assertions
        self.assertTrue(result)  # Check if save_data returns True indicating success
        mock_open.assert_called_once_with("data\city_data.json", "w")  # Check if open function is called
        handle = mock_open()
        handle.write.assert_called_once()  # Check if write function is called
        
    @patch('source.data_collection.get_top_news_topics')
    def test_save_data_failure(self, mock_get_top_news_topics):
        # Setup mock
        mock_get_top_news_topics.return_value = None
        
        # Call the function
        result = save_data('Invalid City')
        
        # Assertions
        self.assertFalse(result)  # Check if save_data returns False indicating failure


if __name__ == '__main__':
    unittest.main()