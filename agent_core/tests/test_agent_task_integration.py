"""
Integration tests for the Agent Core Service and Task Modules.
"""

import os
import sys
import pytest
import uuid
from unittest.mock import MagicMock, patch
from google.protobuf.struct_pb2 import Struct
from google.protobuf.timestamp_pb2 import Timestamp
import concurrent.futures

# Add the parent directory to the path so we can import the agent_core modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the modules to test
from main import AgentServiceServicer, experiment_statuses, running_tasks, task_executor

class TestAgentTaskIntegration:
    """Test the integration between Agent Core and Task Modules."""
    
    def setup_method(self):
        """Set up the test environment."""
        # Create an instance of the AgentServiceServicer
        self.agent_service = AgentServiceServicer()
        
        # Create a mock gRPC context
        self.mock_context = MagicMock()
        
        # Clear experiment statuses and running tasks
        experiment_statuses.clear()
        running_tasks.clear()
        
        # Set environment variables
        os.environ['ABACUSAI_API_KEY'] = 'test-api-key'
    
    def teardown_method(self):
        """Clean up after the test."""
        # Clear experiment statuses and running tasks
        experiment_statuses.clear()
        running_tasks.clear()
        
        # Remove environment variables
        if 'ABACUSAI_API_KEY' in os.environ:
            del os.environ['ABACUSAI_API_KEY']
    
    @patch('task_modules.ebook_generator_task.EbookGeneratorTask.execute')
    def test_ebook_experiment_lifecycle(self, mock_execute):
        """Test the full lifecycle of an ebook experiment."""
        # Arrange
        # Mock the task execution to return a successful result
        mock_execute.return_value = {
            "status": "completed",
            "result": {
                "title": "Test Book",
                "description": "A test book",
                "num_chapters": 3,
                "chapters_generated": 3,
                "chapters": [
                    {
                        "number": 1,
                        "title": "Chapter 1",
                        "content_length": 100,
                        "content_preview": "Chapter 1 content"
                    }
                ]
            }
        }
        
        # Create a request to create an experiment
        create_request = MagicMock()
        create_request.definition.type = 'AI_DRIVEN_EBOOKS'
        create_request.definition.name = 'Test Ebook Experiment'
        create_request.definition.description = 'A test ebook experiment'
        
        # Create parameters for the experiment
        parameters = Struct()
        parameters.update({
            'topic': 'Test Topic',
            'audience': 'Test Audience',
            'num_chapters': 3
        })
        create_request.definition.parameters = parameters
        
        # Act - Create the experiment
        create_response = self.agent_service.CreateExperiment(create_request, self.mock_context)
        
        # Assert - Verify the experiment was created
        assert create_response is not None
        assert create_response.status.success is True
        assert create_response.id is not None
        experiment_id = create_response.id.id
        assert experiment_id in experiment_statuses
        
        # Verify the experiment was created correctly
        experiment = experiment_statuses[experiment_id]
        assert experiment.name == 'Test Ebook Experiment'
        assert experiment.type == 'AI_DRIVEN_EBOOKS'
        assert experiment.state == 'STATE_DEFINED'
        
        # Act - Start the experiment
        start_request = MagicMock()
        start_request.id.id = experiment_id
        
        # Use a real ThreadPoolExecutor for this test
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            # Replace the global task_executor with our test executor
            global task_executor
            original_executor = task_executor
            task_executor = executor
            
            try:
                # Start the experiment
                start_response = self.agent_service.StartExperiment(start_request, self.mock_context)
                
                # Assert - Verify the experiment was started
                assert start_response is not None
                assert start_response.success is True
                assert experiment_statuses[experiment_id].state == 'STATE_RUNNING'
                
                # Wait for the task to complete
                future = running_tasks[experiment_id]
                future.result()  # This will block until the task completes
                
                # Verify the task was executed with the correct parameters
                mock_execute.assert_called_once()
                call_args = mock_execute.call_args[0][0]
                assert call_args.definition.parameters.fields['topic'].string_value == 'Test Topic'
                assert call_args.definition.parameters.fields['audience'].string_value == 'Test Audience'
                assert call_args.definition.parameters.fields['num_chapters'].number_value == 3
                
                # Verify the experiment state was updated
                assert experiment_statuses[experiment_id].state == 'STATE_COMPLETED'
                
                # Get the experiment status
                status_request = MagicMock()
                status_request.id = experiment_id
                status_response = self.agent_service.GetExperimentStatus(status_request, self.mock_context)
                
                # Verify the status response
                assert status_response is not None
                assert status_response.id.id == experiment_id
                assert status_response.state == 'STATE_COMPLETED'
                
                # Stop the experiment (should be a no-op since it's already completed)
                stop_request = MagicMock()
                stop_request.id.id = experiment_id
                stop_response = self.agent_service.StopExperiment(stop_request, self.mock_context)
                
                # Verify the stop response
                assert stop_response is not None
                assert stop_response.success is True
                
            finally:
                # Restore the original task_executor
                task_executor = original_executor
    
    @patch('task_modules.freelance_writing_task.FreelanceWritingTask.execute')
    def test_freelance_writing_experiment_lifecycle(self, mock_execute):
        """Test the full lifecycle of a freelance writing experiment."""
        # Arrange
        # Mock the task execution to return a successful result
        mock_execute.return_value = {
            "status": "completed",
            "result": {
                "project_type": "article",
                "topic": "Test Topic",
                "target_audience": "Test Audience",
                "word_count": 500,
                "tone": "casual",
                "keywords": ["test", "example"],
                "content_length": 500,
                "content_preview": "This is a test article content."
            }
        }
        
        # Create a request to create an experiment
        create_request = MagicMock()
        create_request.definition.type = 'FREELANCE_WRITING'
        create_request.definition.name = 'Test Freelance Writing Experiment'
        create_request.definition.description = 'A test freelance writing experiment'
        
        # Create parameters for the experiment
        parameters = Struct()
        parameters.update({
            'project_type': 'article',
            'topic': 'Test Topic',
            'target_audience': 'Test Audience',
            'word_count': 500,
            'tone': 'casual',
            'keywords': ['test', 'example']
        })
        create_request.definition.parameters = parameters
        
        # Act - Create the experiment
        create_response = self.agent_service.CreateExperiment(create_request, self.mock_context)
        
        # Assert - Verify the experiment was created
        assert create_response is not None
        assert create_response.status.success is True
        assert create_response.id is not None
        experiment_id = create_response.id.id
        assert experiment_id in experiment_statuses
        
        # Verify the experiment was created correctly
        experiment = experiment_statuses[experiment_id]
        assert experiment.name == 'Test Freelance Writing Experiment'
        assert experiment.type == 'FREELANCE_WRITING'
        assert experiment.state == 'STATE_DEFINED'
        
        # Act - Start the experiment
        start_request = MagicMock()
        start_request.id.id = experiment_id
        
        # Use a real ThreadPoolExecutor for this test
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            # Replace the global task_executor with our test executor
            global task_executor
            original_executor = task_executor
            task_executor = executor
            
            try:
                # Start the experiment
                start_response = self.agent_service.StartExperiment(start_request, self.mock_context)
                
                # Assert - Verify the experiment was started
                assert start_response is not None
                assert start_response.success is True
                assert experiment_statuses[experiment_id].state == 'STATE_RUNNING'
                
                # Wait for the task to complete
                future = running_tasks[experiment_id]
                future.result()  # This will block until the task completes
                
                # Verify the experiment state was updated
                assert experiment_statuses[experiment_id].state == 'STATE_COMPLETED'
                
            finally:
                # Restore the original task_executor
                task_executor = original_executor
