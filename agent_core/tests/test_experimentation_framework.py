"""
Unit tests for the Experimentation Framework.
"""

import os
import sys
import pytest
import time
from unittest.mock import MagicMock, patch

# Add the parent directory to the path so we can import the agent_core modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the modules to test
from autonomy_framework.experimentation_framework import (
    ExperimentType,
    ExperimentStatus,
    Experiment,
    ExperimentationFramework
)

class TestExperiment:
    """Test the Experiment class."""
    
    def setup_method(self):
        """Set up the test environment."""
        self.parameters = {
            "risk_tolerance": "medium",
            "decision_strategy": "balanced",
            "notification_threshold": "medium"
        }
        
        self.success_criteria = {
            "accuracy": 0.8,
            "efficiency": 0.7,
            "user_satisfaction": 0.9
        }
        
        self.experiment = Experiment(
            name="Test Experiment",
            experiment_type=ExperimentType.RISK_TOLERANCE,
            description="A test experiment",
            parameters=self.parameters,
            success_criteria=self.success_criteria,
            max_duration_seconds=1800
        )
    
    def test_init(self):
        """Test the initialization of the experiment."""
        assert self.experiment.name == "Test Experiment"
        assert self.experiment.experiment_type == ExperimentType.RISK_TOLERANCE
        assert self.experiment.description == "A test experiment"
        assert self.experiment.parameters == self.parameters
        assert self.experiment.success_criteria == self.success_criteria
        assert self.experiment.max_duration_seconds == 1800
        assert self.experiment.status == ExperimentStatus.CREATED
        assert self.experiment.start_time is None
        assert self.experiment.end_time is None
        assert self.experiment.results == {}
        assert self.experiment.metrics == {}
        assert self.experiment.logs == []
    
    def test_start(self):
        """Test starting the experiment."""
        # Start the experiment
        result = self.experiment.start()
        
        # Verify the result
        assert result is True
        assert self.experiment.status == ExperimentStatus.RUNNING
        assert self.experiment.start_time is not None
        
        # Try to start it again (should fail)
        result = self.experiment.start()
        assert result is False
    
    def test_pause_resume(self):
        """Test pausing and resuming the experiment."""
        # Start the experiment
        self.experiment.start()
        
        # Pause the experiment
        result = self.experiment.pause()
        assert result is True
        assert self.experiment.status == ExperimentStatus.PAUSED
        
        # Try to pause it again (should fail)
        result = self.experiment.pause()
        assert result is False
        
        # Resume the experiment
        result = self.experiment.resume()
        assert result is True
        assert self.experiment.status == ExperimentStatus.RUNNING
        
        # Try to resume it again (should fail)
        result = self.experiment.resume()
        assert result is False
    
    def test_complete(self):
        """Test completing the experiment."""
        # Start the experiment
        self.experiment.start()
        
        # Complete the experiment
        results = {
            "accuracy": 0.85,
            "efficiency": 0.75,
            "user_satisfaction": 0.95
        }
        
        result = self.experiment.complete(results)
        assert result is True
        assert self.experiment.status == ExperimentStatus.COMPLETED
        assert self.experiment.end_time is not None
        assert self.experiment.results == {**results, "success": True}
        
        # Try to complete it again (should fail)
        result = self.experiment.complete(results)
        assert result is False
    
    def test_fail(self):
        """Test failing the experiment."""
        # Start the experiment
        self.experiment.start()
        
        # Fail the experiment
        error = "Test error message"
        result = self.experiment.fail(error)
        assert result is True
        assert self.experiment.status == ExperimentStatus.FAILED
        assert self.experiment.end_time is not None
        assert self.experiment.results == {"error": error, "success": False}
        
        # Try to fail it again (should fail)
        result = self.experiment.fail(error)
        assert result is False
    
    def test_cancel(self):
        """Test cancelling the experiment."""
        # Start the experiment
        self.experiment.start()
        
        # Cancel the experiment
        result = self.experiment.cancel()
        assert result is True
        assert self.experiment.status == ExperimentStatus.CANCELLED
        assert self.experiment.end_time is not None
        
        # Try to cancel it again (should fail)
        result = self.experiment.cancel()
        assert result is False
    
    def test_update_metrics(self):
        """Test updating the metrics for the experiment."""
        # Update metrics
        metrics = {
            "progress": 0.5,
            "cpu_usage": 0.3,
            "memory_usage": 0.2
        }
        
        self.experiment.update_metrics(metrics)
        assert self.experiment.metrics == metrics
        
        # Update more metrics
        more_metrics = {
            "progress": 0.7,  # This should override the previous value
            "network_usage": 0.1
        }
        
        self.experiment.update_metrics(more_metrics)
        assert self.experiment.metrics == {
            "progress": 0.7,
            "cpu_usage": 0.3,
            "memory_usage": 0.2,
            "network_usage": 0.1
        }
    
    def test_add_log(self):
        """Test adding a log entry to the experiment."""
        # Add a log entry
        message = "Test log message"
        level = "INFO"
        timestamp = time.time()
        
        self.experiment.add_log(message, level, timestamp)
        assert len(self.experiment.logs) == 1
        assert self.experiment.logs[0]["message"] == message
        assert self.experiment.logs[0]["level"] == level
        assert self.experiment.logs[0]["timestamp"] == timestamp
        
        # Add another log entry without specifying timestamp
        message2 = "Another test log message"
        level2 = "WARNING"
        
        self.experiment.add_log(message2, level2)
        assert len(self.experiment.logs) == 2
        assert self.experiment.logs[1]["message"] == message2
        assert self.experiment.logs[1]["level"] == level2
        assert self.experiment.logs[1]["timestamp"] is not None
    
    def test_evaluate_success(self):
        """Test evaluating the success of the experiment."""
        # Start the experiment
        self.experiment.start()
        
        # Complete the experiment with results that meet the success criteria
        results = {
            "accuracy": 0.8,  # Exactly matches the criterion
            "efficiency": 0.8,  # Exceeds the criterion
            "user_satisfaction": 0.9  # Exactly matches the criterion
        }
        
        self.experiment.complete(results)
        assert self.experiment.results["success"] is True
        
        # Create another experiment
        experiment2 = Experiment(
            name="Test Experiment 2",
            experiment_type=ExperimentType.RISK_TOLERANCE,
            description="Another test experiment",
            parameters=self.parameters,
            success_criteria=self.success_criteria,
            max_duration_seconds=1800
        )
        
        # Start the experiment
        experiment2.start()
        
        # Complete the experiment with results that don't meet the success criteria
        results2 = {
            "accuracy": 0.7,  # Below the criterion
            "efficiency": 0.8,  # Exceeds the criterion
            "user_satisfaction": 0.9  # Exactly matches the criterion
        }
        
        experiment2.complete(results2)
        assert experiment2.results["success"] is False
    
    def test_to_dict(self):
        """Test converting the experiment to a dictionary."""
        # Start the experiment
        self.experiment.start()
        
        # Update metrics
        metrics = {"progress": 0.5}
        self.experiment.update_metrics(metrics)
        
        # Add a log entry
        self.experiment.add_log("Test log message")
        
        # Convert to dictionary
        experiment_dict = self.experiment.to_dict()
        
        assert experiment_dict["id"] == self.experiment.id
        assert experiment_dict["name"] == "Test Experiment"
        assert experiment_dict["experiment_type"] == "risk_tolerance"
        assert experiment_dict["description"] == "A test experiment"
        assert experiment_dict["parameters"] == self.parameters
        assert experiment_dict["success_criteria"] == self.success_criteria
        assert experiment_dict["max_duration_seconds"] == 1800
        assert experiment_dict["status"] == "running"
        assert experiment_dict["start_time"] == self.experiment.start_time
        assert experiment_dict["metrics"] == metrics
        assert len(experiment_dict["logs"]) == 1
    
    def test_from_dict(self):
        """Test creating an experiment from a dictionary."""
        # Create a dictionary
        experiment_dict = {
            "id": "test-id",
            "name": "Test Experiment",
            "experiment_type": "risk_tolerance",
            "description": "A test experiment",
            "parameters": self.parameters,
            "success_criteria": self.success_criteria,
            "max_duration_seconds": 1800,
            "status": "running",
            "start_time": time.time(),
            "end_time": None,
            "results": {},
            "metrics": {"progress": 0.5},
            "logs": [
                {
                    "timestamp": time.time(),
                    "level": "INFO",
                    "message": "Test log message"
                }
            ]
        }
        
        # Create an experiment from the dictionary
        experiment = Experiment.from_dict(experiment_dict)
        
        assert experiment.id == "test-id"
        assert experiment.name == "Test Experiment"
        assert experiment.experiment_type == ExperimentType.RISK_TOLERANCE
        assert experiment.description == "A test experiment"
        assert experiment.parameters == self.parameters
        assert experiment.success_criteria == self.success_criteria
        assert experiment.max_duration_seconds == 1800
        assert experiment.status == ExperimentStatus.RUNNING
        assert experiment.start_time == experiment_dict["start_time"]
        assert experiment.metrics == {"progress": 0.5}
        assert len(experiment.logs) == 1

class TestExperimentationFramework:
    """Test the ExperimentationFramework class."""
    
    def setup_method(self):
        """Set up the test environment."""
        self.framework = ExperimentationFramework()
        
        self.parameters = {
            "risk_tolerance": "medium",
            "decision_strategy": "balanced",
            "notification_threshold": "medium"
        }
        
        self.success_criteria = {
            "accuracy": 0.8,
            "efficiency": 0.7,
            "user_satisfaction": 0.9
        }
    
    def test_init(self):
        """Test the initialization of the experimentation framework."""
        assert self.framework.experiments == {}
    
    def test_create_experiment(self):
        """Test creating an experiment."""
        # Create an experiment
        experiment = self.framework.create_experiment(
            name="Test Experiment",
            experiment_type=ExperimentType.RISK_TOLERANCE,
            description="A test experiment",
            parameters=self.parameters,
            success_criteria=self.success_criteria,
            max_duration_seconds=1800
        )
        
        assert experiment.name == "Test Experiment"
        assert experiment.experiment_type == ExperimentType.RISK_TOLERANCE
        assert experiment.description == "A test experiment"
        assert experiment.parameters == self.parameters
        assert experiment.success_criteria == self.success_criteria
        assert experiment.max_duration_seconds == 1800
        assert experiment.id in self.framework.experiments
        assert self.framework.experiments[experiment.id] == experiment
    
    def test_get_experiment(self):
        """Test getting an experiment by ID."""
        # Create an experiment
        experiment = self.framework.create_experiment(
            name="Test Experiment",
            experiment_type=ExperimentType.RISK_TOLERANCE,
            description="A test experiment",
            parameters=self.parameters,
            success_criteria=self.success_criteria
        )
        
        # Get the experiment
        retrieved_experiment = self.framework.get_experiment(experiment.id)
        assert retrieved_experiment == experiment
        
        # Try to get a non-existent experiment
        non_existent = self.framework.get_experiment("non-existent-id")
        assert non_existent is None
    
    def test_get_experiments(self):
        """Test getting all experiments."""
        # Create some experiments
        experiment1 = self.framework.create_experiment(
            name="Test Experiment 1",
            experiment_type=ExperimentType.RISK_TOLERANCE,
            description="A test experiment",
            parameters=self.parameters,
            success_criteria=self.success_criteria
        )
        
        experiment2 = self.framework.create_experiment(
            name="Test Experiment 2",
            experiment_type=ExperimentType.DECISION_MAKING,
            description="Another test experiment",
            parameters=self.parameters,
            success_criteria=self.success_criteria
        )
        
        # Get all experiments
        experiments = self.framework.get_experiments()
        assert len(experiments) == 2
        assert experiment1 in experiments
        assert experiment2 in experiments
        
        # Start one experiment
        experiment1.start()
        
        # Get running experiments
        running_experiments = self.framework.get_experiments(status=ExperimentStatus.RUNNING)
        assert len(running_experiments) == 1
        assert experiment1 in running_experiments
        
        # Get created experiments
        created_experiments = self.framework.get_experiments(status=ExperimentStatus.CREATED)
        assert len(created_experiments) == 1
        assert experiment2 in created_experiments
    
    def test_delete_experiment(self):
        """Test deleting an experiment."""
        # Create an experiment
        experiment = self.framework.create_experiment(
            name="Test Experiment",
            experiment_type=ExperimentType.RISK_TOLERANCE,
            description="A test experiment",
            parameters=self.parameters,
            success_criteria=self.success_criteria
        )
        
        # Delete the experiment
        result = self.framework.delete_experiment(experiment.id)
        assert result is True
        assert experiment.id not in self.framework.experiments
        
        # Try to delete a non-existent experiment
        result = self.framework.delete_experiment("non-existent-id")
        assert result is False
        
        # Try to delete a running experiment
        experiment = self.framework.create_experiment(
            name="Test Experiment",
            experiment_type=ExperimentType.RISK_TOLERANCE,
            description="A test experiment",
            parameters=self.parameters,
            success_criteria=self.success_criteria
        )
        
        experiment.start()
        result = self.framework.delete_experiment(experiment.id)
        assert result is False
        assert experiment.id in self.framework.experiments
