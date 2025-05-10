"""
Unit tests for the enhanced Autonomy Framework with risk tolerance and experimentation.
"""

import os
import sys
import pytest
from unittest.mock import MagicMock, patch

# Add the parent directory to the path so we can import the agent_core modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the modules to test
from autonomy_framework import (
    AutonomyFramework,
    DecisionCategory,
    ApprovalLevel,
    RiskCategory,
    RiskLevel,
    ExperimentType,
    ExperimentStatus
)

class TestEnhancedAutonomyFramework:
    """Test the enhanced Autonomy Framework."""
    
    def setup_method(self):
        """Set up the test environment."""
        self.autonomy_framework = AutonomyFramework()
    
    def test_init(self):
        """Test the initialization of the enhanced autonomy framework."""
        assert self.autonomy_framework.decision_matrix is not None
        assert self.autonomy_framework.notification_system is not None
        assert self.autonomy_framework.approval_workflow is not None
        assert self.autonomy_framework.pending_actions == {}
        
        # Test risk tolerance framework initialization
        assert self.autonomy_framework.risk_profiles is not None
        assert "conservative" in self.autonomy_framework.risk_profiles
        assert "balanced" in self.autonomy_framework.risk_profiles
        assert "aggressive" in self.autonomy_framework.risk_profiles
        assert self.autonomy_framework.current_risk_profile is not None
        assert self.autonomy_framework.current_risk_profile.name == "Balanced"
        assert self.autonomy_framework.risk_assessment is not None
        
        # Test experimentation framework initialization
        assert self.autonomy_framework.experimentation_framework is not None
    
    def test_can_execute_with_risk_assessment(self):
        """Test the can_execute method with risk assessment."""
        # Test with low risk (within tolerance)
        context = {"amount": 10.0}
        can_execute, reason = self.autonomy_framework.can_execute(
            DecisionCategory.FINANCIAL,
            "spend_money",
            context
        )
        assert can_execute is True
        assert reason == "Notification required"
        
        # Test with high risk (exceeds tolerance)
        context = {"amount": 2000.0}
        can_execute, reason = self.autonomy_framework.can_execute(
            DecisionCategory.FINANCIAL,
            "spend_money",
            context
        )
        assert can_execute is False
        assert "Risk exceeds tolerance" in reason
        
        # Test with prohibited action (risk assessment should be skipped)
        context = {"amount": 60.0}
        can_execute, reason = self.autonomy_framework.can_execute(
            DecisionCategory.FINANCIAL,
            "spend_money",
            context
        )
        assert can_execute is False
        assert reason == "Action prohibited"
    
    def test_set_risk_profile(self):
        """Test setting the risk tolerance profile."""
        # Test setting a valid profile
        result = self.autonomy_framework.set_risk_profile("conservative")
        assert result is True
        assert self.autonomy_framework.current_risk_profile.name == "Conservative"
        
        # Test setting an invalid profile
        result = self.autonomy_framework.set_risk_profile("non_existent_profile")
        assert result is False
        assert self.autonomy_framework.current_risk_profile.name == "Conservative"
    
    def test_update_risk_tolerance(self):
        """Test updating the risk tolerance level for a specific category."""
        # Test updating a valid category
        result = self.autonomy_framework.update_risk_tolerance(
            RiskCategory.FINANCIAL,
            RiskLevel.HIGH
        )
        assert result is True
        assert self.autonomy_framework.current_risk_profile.get_tolerance_level(RiskCategory.FINANCIAL) == RiskLevel.HIGH
        
        # Test updating with an invalid category (should not raise an exception)
        mock_category = MagicMock()
        mock_category.value = "invalid_category"
        result = self.autonomy_framework.update_risk_tolerance(
            mock_category,
            RiskLevel.MEDIUM
        )
        assert result is True
    
    def test_create_experiment(self):
        """Test creating an experiment."""
        # Test creating a valid experiment
        parameters = {
            "risk_tolerance": "medium",
            "decision_strategy": "balanced"
        }
        
        success_criteria = {
            "accuracy": 0.8,
            "efficiency": 0.7
        }
        
        experiment = self.autonomy_framework.create_experiment(
            name="Test Experiment",
            experiment_type=ExperimentType.RISK_TOLERANCE,
            description="A test experiment",
            parameters=parameters,
            success_criteria=success_criteria,
            max_duration_seconds=1800
        )
        
        assert experiment is not None
        assert experiment.name == "Test Experiment"
        assert experiment.experiment_type == ExperimentType.RISK_TOLERANCE
        assert experiment.description == "A test experiment"
        assert experiment.parameters == parameters
        assert experiment.success_criteria == success_criteria
        assert experiment.max_duration_seconds == 1800
        assert experiment.status == ExperimentStatus.CREATED
        
        # Test creating an experiment with an exception
        with patch.object(self.autonomy_framework.experimentation_framework, 'create_experiment', side_effect=Exception("Test exception")):
            experiment = self.autonomy_framework.create_experiment(
                name="Test Experiment",
                experiment_type=ExperimentType.RISK_TOLERANCE,
                description="A test experiment",
                parameters=parameters,
                success_criteria=success_criteria
            )
            assert experiment is None
    
    def test_get_experiment(self):
        """Test getting an experiment by ID."""
        # Create an experiment
        parameters = {"risk_tolerance": "medium"}
        success_criteria = {"accuracy": 0.8}
        
        experiment = self.autonomy_framework.create_experiment(
            name="Test Experiment",
            experiment_type=ExperimentType.RISK_TOLERANCE,
            description="A test experiment",
            parameters=parameters,
            success_criteria=success_criteria
        )
        
        # Get the experiment
        retrieved_experiment = self.autonomy_framework.get_experiment(experiment.id)
        assert retrieved_experiment is experiment
        
        # Try to get a non-existent experiment
        non_existent = self.autonomy_framework.get_experiment("non-existent-id")
        assert non_existent is None
    
    def test_get_experiments(self):
        """Test getting all experiments."""
        # Create some experiments
        parameters = {"risk_tolerance": "medium"}
        success_criteria = {"accuracy": 0.8}
        
        experiment1 = self.autonomy_framework.create_experiment(
            name="Test Experiment 1",
            experiment_type=ExperimentType.RISK_TOLERANCE,
            description="A test experiment",
            parameters=parameters,
            success_criteria=success_criteria
        )
        
        experiment2 = self.autonomy_framework.create_experiment(
            name="Test Experiment 2",
            experiment_type=ExperimentType.DECISION_MAKING,
            description="Another test experiment",
            parameters=parameters,
            success_criteria=success_criteria
        )
        
        # Get all experiments
        experiments = self.autonomy_framework.get_experiments()
        assert len(experiments) == 2
        assert experiment1 in experiments
        assert experiment2 in experiments
        
        # Start one experiment
        experiment1.start()
        
        # Get running experiments
        running_experiments = self.autonomy_framework.get_experiments(status=ExperimentStatus.RUNNING)
        assert len(running_experiments) == 1
        assert experiment1 in running_experiments
        
        # Get created experiments
        created_experiments = self.autonomy_framework.get_experiments(status=ExperimentStatus.CREATED)
        assert len(created_experiments) == 1
        assert experiment2 in created_experiments
