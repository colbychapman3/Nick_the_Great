"""
Integration tests for the Task Modules.
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
from task_modules.ebook_generator_task import EbookGeneratorTask
from task_modules.freelance_writing_task import FreelanceWritingTask
from task_modules.niche_affiliate_website_task import NicheAffiliateWebsiteTask
from task_modules.pinterest_strategy_task import PinterestStrategyTask

class TestTaskModulesIntegration:
    """Test the integration between the Agent Core and Task Modules."""
    
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
        os.environ['DB_SYNC_ENABLED'] = 'false'
        
        # Mock the task modules
        self.mock_ebook_generator_task = MagicMock(spec=EbookGeneratorTask)
        self.mock_freelance_writing_task = MagicMock(spec=FreelanceWritingTask)
        self.mock_niche_affiliate_website_task = MagicMock(spec=NicheAffiliateWebsiteTask)
        self.mock_pinterest_strategy_task = MagicMock(spec=PinterestStrategyTask)
        
        # Patch the task modules
        self.patch_ebook_generator_task = patch('main.EbookGeneratorTask', return_value=self.mock_ebook_generator_task)
        self.patch_freelance_writing_task = patch('main.FreelanceWritingTask', return_value=self.mock_freelance_writing_task)
        self.patch_niche_affiliate_website_task = patch('main.NicheAffiliateWebsiteTask', return_value=self.mock_niche_affiliate_website_task)
        self.patch_pinterest_strategy_task = patch('main.PinterestStrategyTask', return_value=self.mock_pinterest_strategy_task)
        
        self.mock_ebook_generator_task_class = self.patch_ebook_generator_task.start()
        self.mock_freelance_writing_task_class = self.patch_freelance_writing_task.start()
        self.mock_niche_affiliate_website_task_class = self.patch_niche_affiliate_website_task.start()
        self.mock_pinterest_strategy_task_class = self.patch_pinterest_strategy_task.start()
    
    def teardown_method(self):
        """Clean up after the test."""
        # Clear experiment statuses and running tasks
        experiment_statuses.clear()
        running_tasks.clear()
        
        # Stop the patches
        self.patch_ebook_generator_task.stop()
        self.patch_freelance_writing_task.stop()
        self.patch_niche_affiliate_website_task.stop()
        self.patch_pinterest_strategy_task.stop()
        
        # Remove environment variables
        if 'ABACUSAI_API_KEY' in os.environ:
            del os.environ['ABACUSAI_API_KEY']
        if 'DB_SYNC_ENABLED' in os.environ:
            del os.environ['DB_SYNC_ENABLED']
    
    def test_start_experiment_ebook_generator(self):
        """Test starting an experiment with the EbookGeneratorTask."""
        # Arrange
        create_request = MagicMock()
        create_request.definition.type = 'AI_DRIVEN_EBOOKS'
        create_request.definition.name = 'Test Ebook Experiment'
        create_request.definition.description = 'A test ebook experiment'
        
        # Create parameters for the experiment
        parameters = Struct()
        parameters.update({
            'topic': 'Test Topic',
            'audience': 'Test Audience',
            'num_chapters': 5
        })
        create_request.definition.parameters = parameters
        
        # Create the experiment
        create_response = self.agent_service.CreateExperiment(create_request, self.mock_context)
        experiment_id = create_response.id.id
        
        # Act
        start_request = MagicMock()
        start_request.id.id = experiment_id
        start_response = self.agent_service.StartExperiment(start_request, self.mock_context)
        
        # Assert
        assert start_response.success is True
        assert experiment_id in running_tasks
        
        # Verify the EbookGeneratorTask was created and executed
        self.mock_ebook_generator_task_class.assert_called_once()
        self.mock_ebook_generator_task.execute.assert_called_once()
        
        # Verify the parameters were passed correctly
        call_args = self.mock_ebook_generator_task.execute.call_args[0][0]
        assert call_args['topic'] == 'Test Topic'
        assert call_args['audience'] == 'Test Audience'
        assert call_args['num_chapters'] == 5
    
    def test_start_experiment_freelance_writing(self):
        """Test starting an experiment with the FreelanceWritingTask."""
        # Arrange
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
            'word_count': 1000
        })
        create_request.definition.parameters = parameters
        
        # Create the experiment
        create_response = self.agent_service.CreateExperiment(create_request, self.mock_context)
        experiment_id = create_response.id.id
        
        # Act
        start_request = MagicMock()
        start_request.id.id = experiment_id
        start_response = self.agent_service.StartExperiment(start_request, self.mock_context)
        
        # Assert
        assert start_response.success is True
        assert experiment_id in running_tasks
        
        # Verify the FreelanceWritingTask was created and executed
        self.mock_freelance_writing_task_class.assert_called_once()
        self.mock_freelance_writing_task.execute.assert_called_once()
        
        # Verify the parameters were passed correctly
        call_args = self.mock_freelance_writing_task.execute.call_args[0][0]
        assert call_args['project_type'] == 'article'
        assert call_args['topic'] == 'Test Topic'
        assert call_args['target_audience'] == 'Test Audience'
        assert call_args['word_count'] == 1000
    
    def test_start_experiment_niche_affiliate_website(self):
        """Test starting an experiment with the NicheAffiliateWebsiteTask."""
        # Arrange
        create_request = MagicMock()
        create_request.definition.type = 'NICHE_AFFILIATE_WEBSITE'
        create_request.definition.name = 'Test Niche Affiliate Website Experiment'
        create_request.definition.description = 'A test niche affiliate website experiment'
        
        # Create parameters for the experiment
        parameters = Struct()
        parameters.update({
            'niche': 'Test Niche',
            'target_audience': 'Test Audience',
            'num_articles': 10
        })
        create_request.definition.parameters = parameters
        
        # Create the experiment
        create_response = self.agent_service.CreateExperiment(create_request, self.mock_context)
        experiment_id = create_response.id.id
        
        # Act
        start_request = MagicMock()
        start_request.id.id = experiment_id
        start_response = self.agent_service.StartExperiment(start_request, self.mock_context)
        
        # Assert
        assert start_response.success is True
        assert experiment_id in running_tasks
        
        # Verify the NicheAffiliateWebsiteTask was created and executed
        self.mock_niche_affiliate_website_task_class.assert_called_once()
        self.mock_niche_affiliate_website_task.execute.assert_called_once()
        
        # Verify the parameters were passed correctly
        call_args = self.mock_niche_affiliate_website_task.execute.call_args[0][0]
        assert call_args['niche'] == 'Test Niche'
        assert call_args['target_audience'] == 'Test Audience'
        assert call_args['num_articles'] == 10
