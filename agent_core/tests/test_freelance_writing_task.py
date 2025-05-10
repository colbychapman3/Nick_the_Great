"""
Unit tests for the FreelanceWritingTask module.
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
from task_modules.freelance_writing_task import FreelanceWritingTask

class TestFreelanceWritingTask:
    """Test the FreelanceWritingTask class."""
    
    def setup_method(self):
        """Set up the test environment."""
        # Create the task
        self.task = FreelanceWritingTask()
        
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
        assert self.task.client is None
    
    def test_execute_missing_project_type(self):
        """Test executing the task with a missing project_type parameter."""
        # Arrange
        parameters = {'topic': 'Test Topic', 'target_audience': 'Test Audience'}
        
        # Act
        result = self.task.execute(parameters)
        
        # Assert
        assert result['status'] == 'failed'
        assert 'Missing required parameter: project_type' in result['message']
    
    def test_execute_missing_topic(self):
        """Test executing the task with a missing topic parameter."""
        # Arrange
        parameters = {'project_type': 'article', 'target_audience': 'Test Audience'}
        
        # Act
        result = self.task.execute(parameters)
        
        # Assert
        assert result['status'] == 'failed'
        assert 'Missing required parameter: topic' in result['message']
    
    def test_execute_missing_target_audience(self):
        """Test executing the task with a missing target_audience parameter."""
        # Arrange
        parameters = {'project_type': 'article', 'topic': 'Test Topic'}
        
        # Act
        result = self.task.execute(parameters)
        
        # Assert
        assert result['status'] == 'failed'
        assert 'Missing required parameter: target_audience' in result['message']
    
    def test_execute_missing_api_key(self):
        """Test executing the task with a missing API key."""
        # Arrange
        parameters = {
            'project_type': 'article',
            'topic': 'Test Topic',
            'target_audience': 'Test Audience'
        }
        
        # Remove the API key from environment
        if 'ABACUSAI_API_KEY' in os.environ:
            del os.environ['ABACUSAI_API_KEY']
        
        # Act
        result = self.task.execute(parameters)
        
        # Assert
        assert result['status'] == 'failed'
        assert 'ABACUSAI_API_KEY not found in environment variables' in result['message']
    
    @patch('task_modules.freelance_writing_task.ApiClient')
    @patch('tempfile.TemporaryDirectory')
    def test_execute_success(self, mock_temp_dir, mock_api_client_class):
        """Test successful execution of the task."""
        # Arrange
        parameters = {
            'project_type': 'article',
            'topic': 'Test Topic',
            'target_audience': 'Test Audience',
            'word_count': 500,
            'tone': 'casual',
            'keywords': ['test', 'example']
        }
        
        # Mock the ApiClient instance
        mock_client_instance = MagicMock()
        mock_api_client_class.return_value = mock_client_instance
        
        # Mock the temporary directory
        mock_temp_dir.return_value.__enter__.return_value = '/tmp/test'
        
        # Mock the _generate_content_outline method
        outline = {
            'title': 'Test Article',
            'introduction': 'This is an introduction',
            'sections': [
                {
                    'heading': 'Section 1',
                    'subheadings': ['Subheading 1', 'Subheading 2'],
                    'key_points': ['Point 1', 'Point 2']
                }
            ],
            'conclusion': 'This is a conclusion'
        }
        
        # Mock the _generate_full_content method
        content = "# Test Article\n\nThis is a test article content."
        
        # Patch the internal methods
        with patch.object(self.task, '_generate_content_outline', return_value=outline):
            with patch.object(self.task, '_generate_full_content', return_value=content):
                # Mock the open function for writing files
                with patch('builtins.open', mock_open()):
                    # Act
                    result = self.task.execute(parameters)
        
        # Assert
        assert result['status'] == 'completed'
        assert result['result']['project_type'] == 'article'
        assert result['result']['topic'] == 'Test Topic'
        assert result['result']['target_audience'] == 'Test Audience'
        assert result['result']['word_count'] == 500
        assert result['result']['tone'] == 'casual'
        assert result['result']['keywords'] == ['test', 'example']
        assert result['result']['content_length'] == len(content)
        assert result['result']['content_preview'] == content
        
        # Verify the ApiClient was created with the correct API key
        mock_api_client_class.assert_called_once_with('test-api-key')
    
    @patch('task_modules.freelance_writing_task.ApiClient')
    def test_execute_outline_generation_failure(self, mock_api_client_class):
        """Test handling of outline generation failure."""
        # Arrange
        parameters = {
            'project_type': 'article',
            'topic': 'Test Topic',
            'target_audience': 'Test Audience'
        }
        
        # Mock the ApiClient instance
        mock_client_instance = MagicMock()
        mock_api_client_class.return_value = mock_client_instance
        
        # Patch the _generate_content_outline method to return None (failure)
        with patch.object(self.task, '_generate_content_outline', return_value=None):
            # Act
            result = self.task.execute(parameters)
        
        # Assert
        assert result['status'] == 'failed'
        assert 'Failed to generate content outline' in result['message']
    
    @patch('task_modules.freelance_writing_task.ApiClient')
    def test_execute_content_generation_failure(self, mock_api_client_class):
        """Test handling of content generation failure."""
        # Arrange
        parameters = {
            'project_type': 'article',
            'topic': 'Test Topic',
            'target_audience': 'Test Audience'
        }
        
        # Mock the ApiClient instance
        mock_client_instance = MagicMock()
        mock_api_client_class.return_value = mock_client_instance
        
        # Mock the _generate_content_outline method
        outline = {
            'title': 'Test Article',
            'introduction': 'This is an introduction',
            'sections': [
                {
                    'heading': 'Section 1',
                    'subheadings': ['Subheading 1', 'Subheading 2'],
                    'key_points': ['Point 1', 'Point 2']
                }
            ],
            'conclusion': 'This is a conclusion'
        }
        
        # Patch the internal methods
        with patch.object(self.task, '_generate_content_outline', return_value=outline):
            with patch.object(self.task, '_generate_full_content', return_value=None):
                # Act
                result = self.task.execute(parameters)
        
        # Assert
        assert result['status'] == 'failed'
        assert 'Failed to generate full content' in result['message']
    
    @patch('task_modules.freelance_writing_task.ApiClient')
    def test_generate_content_outline(self, mock_api_client_class):
        """Test the _generate_content_outline method."""
        # Arrange
        # Mock the ApiClient instance
        mock_client_instance = MagicMock()
        mock_api_client_class.return_value = mock_client_instance
        
        # Mock the text_generation response
        mock_response = MagicMock()
        mock_generation = MagicMock()
        mock_generation.text = '{"title": "Test Article", "introduction": "Test intro", "sections": [], "conclusion": "Test conclusion"}'
        mock_response.generations = [mock_generation]
        mock_client_instance.text_generation.return_value = mock_response
        
        # Set up the task
        self.task.api_key = 'test-api-key'
        self.task.client = mock_client_instance
        
        # Act
        result = self.task._generate_content_outline(
            'article', 'Test Topic', 'Test Audience', 500, 'casual', ['test', 'example']
        )
        
        # Assert
        assert result is not None
        assert result['title'] == 'Test Article'
        assert result['introduction'] == 'Test intro'
        assert result['conclusion'] == 'Test conclusion'
        
        # Verify the client was called with the correct parameters
        mock_client_instance.text_generation.assert_called_once()
        call_args = mock_client_instance.text_generation.call_args[1]
        assert 'article' in call_args['prompt']
        assert 'Test Topic' in call_args['prompt']
        assert 'Test Audience' in call_args['prompt']
        assert '500' in call_args['prompt']
        assert 'casual' in call_args['prompt']
        assert 'test, example' in call_args['prompt']
