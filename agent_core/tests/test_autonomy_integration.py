"""
Integration tests for the Autonomy Framework with the Agent Core.
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
from autonomy_framework import (
    AutonomyFramework,
    DecisionCategory,
    ApprovalLevel,
    RiskCategory,
    RiskLevel,
    ExperimentType,
    ExperimentStatus
)

class TestAutonomyIntegration:
    """Test the integration between the Autonomy Framework and the Agent Core."""
    
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
        
        # Create an instance of the AutonomyFramework
        self.autonomy_framework = AutonomyFramework()
    
    def teardown_method(self):
        """Clean up after the test."""
        # Clear experiment statuses and running tasks
        experiment_statuses.clear()
        running_tasks.clear()
        
        # Remove environment variables
        if 'ABACUSAI_API_KEY' in os.environ:
            del os.environ['ABACUSAI_API_KEY']
    
    def test_experiment_creation_with_risk_assessment(self):
        """Test creating an experiment with risk assessment."""
        # Set a conservative risk profile
        self.autonomy_framework.set_risk_profile("conservative")
        
        # Create a request to create an experiment with high financial risk
        create_request = MagicMock()
        create_request.definition.type = 'AI_DRIVEN_EBOOKS'
        create_request.definition.name = 'High Risk Experiment'
        create_request.definition.description = 'An experiment with high financial risk'
        
        # Create parameters for the experiment with high cost
        parameters = Struct()
        parameters.update({
            'topic': 'Test Topic',
            'audience': 'Test Audience',
            'num_chapters': 20,
            'estimated_cost': 500.0  # High cost
        })
        create_request.definition.parameters = parameters
        
        # Mock the can_execute method to simulate risk assessment
        original_can_execute = self.autonomy_framework.can_execute
        
        def mock_can_execute(category, action, context):
            if category == DecisionCategory.EXPERIMENT_MANAGEMENT and action == "create_experiment":
                if context.get("estimated_cost", 0) > 100.0:
                    return False, "Risk exceeds tolerance: Financial risk too high"
            return original_can_execute(category, action, context)
        
        # Patch the can_execute method
        with patch.object(self.autonomy_framework, 'can_execute', side_effect=mock_can_execute):
            # Patch the agent service to use our autonomy framework
            with patch.object(self.agent_service, 'autonomy_framework', self.autonomy_framework):
                # Act - Create the experiment
                create_response = self.agent_service.CreateExperiment(create_request, self.mock_context)
                
                # Assert - Verify the experiment was not created due to risk assessment
                assert create_response is not None
                assert create_response.status.success is False
                assert "Risk exceeds tolerance" in create_response.status.message
    
    def test_experiment_creation_with_approval(self):
        """Test creating an experiment that requires approval."""
        # Set a balanced risk profile
        self.autonomy_framework.set_risk_profile("balanced")
        
        # Create a request to create an experiment with medium financial risk
        create_request = MagicMock()
        create_request.definition.type = 'AI_DRIVEN_EBOOKS'
        create_request.definition.name = 'Medium Risk Experiment'
        create_request.definition.description = 'An experiment with medium financial risk'
        
        # Create parameters for the experiment with medium cost
        parameters = Struct()
        parameters.update({
            'topic': 'Test Topic',
            'audience': 'Test Audience',
            'num_chapters': 10,
            'estimated_cost': 50.0  # Medium cost
        })
        create_request.definition.parameters = parameters
        
        # Mock the can_execute method to simulate approval requirement
        def mock_can_execute(category, action, context):
            if category == DecisionCategory.EXPERIMENT_MANAGEMENT and action == "create_experiment":
                return False, "Approval required"
            return True, None
        
        # Mock the approval workflow
        mock_approval_workflow = MagicMock()
        mock_approval_request = MagicMock()
        mock_approval_request.id = str(uuid.uuid4())
        mock_approval_workflow.create_approval_request.return_value = mock_approval_request
        
        # Patch the autonomy framework
        with patch.object(self.autonomy_framework, 'can_execute', side_effect=mock_can_execute):
            with patch.object(self.autonomy_framework, 'approval_workflow', mock_approval_workflow):
                # Patch the agent service to use our autonomy framework
                with patch.object(self.agent_service, 'autonomy_framework', self.autonomy_framework):
                    # Act - Create the experiment
                    create_response = self.agent_service.CreateExperiment(create_request, self.mock_context)
                    
                    # Assert - Verify the experiment was not created and approval was requested
                    assert create_response is not None
                    assert create_response.status.success is False
                    assert "Approval required" in create_response.status.message
                    
                    # Verify that an approval request was created
                    mock_approval_workflow.create_approval_request.assert_called_once()
                    call_args = mock_approval_workflow.create_approval_request.call_args[1]
                    assert "Medium Risk Experiment" in call_args["title"]
                    assert call_args["category"] == DecisionCategory.EXPERIMENT_MANAGEMENT
                    assert call_args["action"] == "create_experiment"
    
    def test_experiment_creation_with_autonomy(self):
        """Test creating an experiment that can be executed autonomously."""
        # Set an aggressive risk profile
        self.autonomy_framework.set_risk_profile("aggressive")
        
        # Create a request to create an experiment with low financial risk
        create_request = MagicMock()
        create_request.definition.type = 'AI_DRIVEN_EBOOKS'
        create_request.definition.name = 'Low Risk Experiment'
        create_request.definition.description = 'An experiment with low financial risk'
        
        # Create parameters for the experiment with low cost
        parameters = Struct()
        parameters.update({
            'topic': 'Test Topic',
            'audience': 'Test Audience',
            'num_chapters': 5,
            'estimated_cost': 10.0  # Low cost
        })
        create_request.definition.parameters = parameters
        
        # Mock the can_execute method to simulate autonomous execution
        def mock_can_execute(category, action, context):
            if category == DecisionCategory.EXPERIMENT_MANAGEMENT and action == "create_experiment":
                return True, None
            return True, None
        
        # Patch the autonomy framework
        with patch.object(self.autonomy_framework, 'can_execute', side_effect=mock_can_execute):
            # Patch the agent service to use our autonomy framework
            with patch.object(self.agent_service, 'autonomy_framework', self.autonomy_framework):
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
                assert experiment.name == 'Low Risk Experiment'
                assert experiment.type == 'AI_DRIVEN_EBOOKS'
                assert experiment.state == 'STATE_DEFINED'
    
    def test_experiment_with_risk_tolerance_experiment(self):
        """Test creating a risk tolerance experiment."""
        # Create a risk tolerance experiment
        experiment = self.autonomy_framework.create_experiment(
            name="Risk Tolerance Experiment",
            experiment_type=ExperimentType.RISK_TOLERANCE,
            description="An experiment to test different risk tolerance levels",
            parameters={
                "initial_profile": "balanced",
                "test_profiles": ["conservative", "aggressive"],
                "test_actions": ["create_experiment", "spend_money", "publish_content"]
            },
            success_criteria={
                "completion_rate": 1.0,
                "error_rate": 0.0
            }
        )
        
        assert experiment is not None
        assert experiment.name == "Risk Tolerance Experiment"
        assert experiment.experiment_type == ExperimentType.RISK_TOLERANCE
        
        # Start the experiment
        result = experiment.start()
        assert result is True
        assert experiment.status == ExperimentStatus.RUNNING
        
        # Simulate running the experiment
        # In a real implementation, this would test different risk profiles
        # and collect metrics on the outcomes
        
        # For this test, we'll just update some metrics and complete the experiment
        experiment.update_metrics({
            "completion_rate": 1.0,
            "error_rate": 0.0,
            "conservative_approval_rate": 0.8,
            "balanced_approval_rate": 0.5,
            "aggressive_approval_rate": 0.2
        })
        
        # Complete the experiment
        result = experiment.complete({
            "completion_rate": 1.0,
            "error_rate": 0.0,
            "best_profile": "balanced"
        })
        
        assert result is True
        assert experiment.status == ExperimentStatus.COMPLETED
        assert experiment.results["success"] is True
