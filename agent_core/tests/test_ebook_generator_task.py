"""
Unit tests for the EbookGeneratorTask module.
"""

import os
import sys
import pytest
import json
import tempfile
from unittest.mock import MagicMock, patch, mock_open

# Add the parent directory to the path so we can import the task_modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import the module to test
from task_modules.ebook_generator_task import EbookGeneratorTask

class TestEbookGeneratorTask:
    """Test the EbookGeneratorTask class."""
    
    def setup_method(self):
        """Set up the test environment."""
        # Create a mock EbookGenerator
        self.mock_generator = MagicMock()
        
        # Create the task
        self.task = EbookGeneratorTask()
        
        # Mock environment variables
        os.environ['ABACUSAI_API_KEY'] = 'test-api-key'
    
    def teardown_method(self):
        """Clean up after the test."""
        # Remove environment variables
        if 'ABACUSAI_API_KEY' in os.environ:
            del os.environ['ABACUSAI_API_KEY']
    
    def test_init(self):
        """Test the initialization of the task."""
        assert self.task.api_key is None
        assert self.task.generator is None
    
    def test_execute_missing_topic(self):
        """Test executing the task with a missing topic parameter."""
        # Arrange
        parameters = {'audience': 'Test Audience'}
        
        # Act
        result = self.task.execute(parameters)
        
        # Assert
        assert result['status'] == 'failed'
        assert 'Missing required parameter: topic' in result['message']
    
    def test_execute_missing_audience(self):
        """Test executing the task with a missing audience parameter."""
        # Arrange
        parameters = {'topic': 'Test Topic'}
        
        # Act
        result = self.task.execute(parameters)
        
        # Assert
        assert result['status'] == 'failed'
        assert 'Missing required parameter: audience' in result['message']
    
    def test_execute_missing_api_key(self):
        """Test executing the task with a missing API key."""
        # Arrange
        parameters = {'topic': 'Test Topic', 'audience': 'Test Audience'}
        
        # Remove the API key from environment
        if 'ABACUSAI_API_KEY' in os.environ:
            del os.environ['ABACUSAI_API_KEY']
        
        # Act
        result = self.task.execute(parameters)
        
        # Assert
        assert result['status'] == 'failed'
        assert 'ABACUSAI_API_KEY not found in environment variables' in result['message']
    
    @patch('task_modules.ebook_generator_task.EbookGenerator')
    @patch('tempfile.TemporaryDirectory')
    def test_execute_success(self, mock_temp_dir, mock_ebook_generator_class):
        """Test successful execution of the task."""
        # Arrange
        parameters = {'topic': 'Test Topic', 'audience': 'Test Audience', 'num_chapters': 3}
        
        # Mock the EbookGenerator instance
        mock_generator_instance = MagicMock()
        mock_ebook_generator_class.return_value = mock_generator_instance
        
        # Mock the temporary directory
        mock_temp_dir.return_value.__enter__.return_value = '/tmp/test'
        
        # Mock the outline.json file
        outline = {
            'title': 'Test Book',
            'description': 'A test book',
            'chapters': [
                {'number': 1, 'title': 'Chapter 1'},
                {'number': 2, 'title': 'Chapter 2'},
                {'number': 3, 'title': 'Chapter 3'}
            ]
        }
        
        # Mock the os.path.exists function
        with patch('os.path.exists', return_value=True):
            # Mock the open function for reading the outline
            with patch('builtins.open', mock_open(read_data=json.dumps(outline))):
                # Mock the os.path.join function
                with patch('os.path.join', side_effect=lambda *args: '/'.join(args)):
                    # Act
                    result = self.task.execute(parameters)
        
        # Assert
        assert result['status'] == 'completed'
        assert result['result']['title'] == 'Test Book'
        assert result['result']['description'] == 'A test book'
        assert result['result']['num_chapters'] == 3
        
        # Verify the generator was called with the correct parameters
        mock_ebook_generator_class.assert_called_once_with('test-api-key')
        mock_generator_instance.generate_full_book.assert_called_once_with(
            'Test Topic', 'Test Audience', '/tmp/test', 3
        )
    
    @patch('task_modules.ebook_generator_task.EbookGenerator')
    @patch('tempfile.TemporaryDirectory')
    def test_execute_generator_error(self, mock_temp_dir, mock_ebook_generator_class):
        """Test handling of errors from the generator."""
        # Arrange
        parameters = {'topic': 'Test Topic', 'audience': 'Test Audience'}
        
        # Mock the EbookGenerator instance
        mock_generator_instance = MagicMock()
        mock_generator_instance.generate_full_book.side_effect = Exception('Generator error')
        mock_ebook_generator_class.return_value = mock_generator_instance
        
        # Mock the temporary directory
        mock_temp_dir.return_value.__enter__.return_value = '/tmp/test'
        
        # Act
        result = self.task.execute(parameters)
        
        # Assert
        assert result['status'] == 'failed'
        assert 'Generator error' in result['message']
        
        # Verify the generator was called with the correct parameters
        mock_ebook_generator_class.assert_called_once_with('test-api-key')
        mock_generator_instance.generate_full_book.assert_called_once()
    
    @patch('task_modules.ebook_generator_task.EbookGenerator')
    @patch('tempfile.TemporaryDirectory')
    def test_execute_outline_missing(self, mock_temp_dir, mock_ebook_generator_class):
        """Test handling of missing outline file."""
        # Arrange
        parameters = {'topic': 'Test Topic', 'audience': 'Test Audience'}
        
        # Mock the EbookGenerator instance
        mock_generator_instance = MagicMock()
        mock_ebook_generator_class.return_value = mock_generator_instance
        
        # Mock the temporary directory
        mock_temp_dir.return_value.__enter__.return_value = '/tmp/test'
        
        # Mock the os.path.exists function to return False for the outline file
        with patch('os.path.exists', return_value=False):
            # Act
            result = self.task.execute(parameters)
        
        # Assert
        assert result['status'] == 'failed'
        assert 'Failed to generate book outline' in result['message']
