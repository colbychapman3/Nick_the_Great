"""
Experimentation Framework for the Nick the Great Unified Agent.

This module implements the experimentation framework that allows the agent to
test different autonomy settings and strategies.
"""

import logging
import enum
import uuid
import time
import random
from typing import Dict, Any, Optional, List, Tuple, Callable

from .risk_tolerance import RiskToleranceProfile, RiskAssessment, RiskCategory, RiskLevel

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ExperimentType(enum.Enum):
    """Types of experiments that the agent can run."""
    RISK_TOLERANCE = "risk_tolerance"  # Experiment with different risk tolerance levels
    DECISION_MAKING = "decision_making"  # Experiment with different decision-making strategies
    NOTIFICATION = "notification"  # Experiment with different notification strategies
    APPROVAL = "approval"  # Experiment with different approval workflows
    CUSTOM = "custom"  # Custom experiment type

class ExperimentStatus(enum.Enum):
    """Status of an experiment."""
    CREATED = "created"  # Experiment has been created but not started
    RUNNING = "running"  # Experiment is currently running
    PAUSED = "paused"  # Experiment is paused
    COMPLETED = "completed"  # Experiment has completed successfully
    FAILED = "failed"  # Experiment has failed
    CANCELLED = "cancelled"  # Experiment has been cancelled

class Experiment:
    """
    Experiment for testing different autonomy settings.
    
    This class represents an experiment that tests different autonomy settings.
    """
    
    def __init__(self, 
                name: str, 
                experiment_type: ExperimentType, 
                description: str, 
                parameters: Dict[str, Any],
                success_criteria: Dict[str, Any],
                max_duration_seconds: int = 3600,
                callback: Optional[Callable[[Dict[str, Any]], None]] = None):
        """
        Initialize the experiment.
        
        Args:
            name: The name of the experiment
            experiment_type: The type of experiment
            description: A description of the experiment
            parameters: Parameters for the experiment
            success_criteria: Criteria for determining if the experiment is successful
            max_duration_seconds: Maximum duration of the experiment in seconds
            callback: Function to call when the experiment completes
        """
        self.id = str(uuid.uuid4())
        self.name = name
        self.experiment_type = experiment_type
        self.description = description
        self.parameters = parameters
        self.success_criteria = success_criteria
        self.max_duration_seconds = max_duration_seconds
        self.callback = callback
        
        self.status = ExperimentStatus.CREATED
        self.start_time = None
        self.end_time = None
        self.results = {}
        self.metrics = {}
        self.logs = []
        
        logger.info(f"Created experiment: {name} ({self.id})")
    
    def start(self) -> bool:
        """
        Start the experiment.
        
        Returns:
            bool: True if the experiment was started successfully, False otherwise
        """
        if self.status != ExperimentStatus.CREATED and self.status != ExperimentStatus.PAUSED:
            logger.warning(f"Cannot start experiment {self.id} with status {self.status.value}")
            return False
        
        self.status = ExperimentStatus.RUNNING
        self.start_time = time.time()
        
        logger.info(f"Started experiment: {self.name} ({self.id})")
        return True
    
    def pause(self) -> bool:
        """
        Pause the experiment.
        
        Returns:
            bool: True if the experiment was paused successfully, False otherwise
        """
        if self.status != ExperimentStatus.RUNNING:
            logger.warning(f"Cannot pause experiment {self.id} with status {self.status.value}")
            return False
        
        self.status = ExperimentStatus.PAUSED
        
        logger.info(f"Paused experiment: {self.name} ({self.id})")
        return True
    
    def resume(self) -> bool:
        """
        Resume the experiment.
        
        Returns:
            bool: True if the experiment was resumed successfully, False otherwise
        """
        if self.status != ExperimentStatus.PAUSED:
            logger.warning(f"Cannot resume experiment {self.id} with status {self.status.value}")
            return False
        
        self.status = ExperimentStatus.RUNNING
        
        logger.info(f"Resumed experiment: {self.name} ({self.id})")
        return True
    
    def complete(self, results: Dict[str, Any]) -> bool:
        """
        Complete the experiment.
        
        Args:
            results: The results of the experiment
        
        Returns:
            bool: True if the experiment was completed successfully, False otherwise
        """
        if self.status != ExperimentStatus.RUNNING:
            logger.warning(f"Cannot complete experiment {self.id} with status {self.status.value}")
            return False
        
        self.status = ExperimentStatus.COMPLETED
        self.end_time = time.time()
        self.results = results
        
        # Calculate success based on success criteria
        success = self._evaluate_success()
        self.results["success"] = success
        
        logger.info(f"Completed experiment: {self.name} ({self.id}), success: {success}")
        
        # Call the callback if provided
        if self.callback:
            try:
                self.callback(self.results)
            except Exception as e:
                logger.error(f"Error calling experiment callback: {e}")
        
        return True
    
    def fail(self, error: str) -> bool:
        """
        Mark the experiment as failed.
        
        Args:
            error: The error message
        
        Returns:
            bool: True if the experiment was marked as failed successfully, False otherwise
        """
        if self.status != ExperimentStatus.RUNNING:
            logger.warning(f"Cannot fail experiment {self.id} with status {self.status.value}")
            return False
        
        self.status = ExperimentStatus.FAILED
        self.end_time = time.time()
        self.results = {"error": error, "success": False}
        
        logger.info(f"Failed experiment: {self.name} ({self.id}), error: {error}")
        
        # Call the callback if provided
        if self.callback:
            try:
                self.callback(self.results)
            except Exception as e:
                logger.error(f"Error calling experiment callback: {e}")
        
        return True
    
    def cancel(self) -> bool:
        """
        Cancel the experiment.
        
        Returns:
            bool: True if the experiment was cancelled successfully, False otherwise
        """
        if self.status != ExperimentStatus.RUNNING and self.status != ExperimentStatus.PAUSED:
            logger.warning(f"Cannot cancel experiment {self.id} with status {self.status.value}")
            return False
        
        self.status = ExperimentStatus.CANCELLED
        self.end_time = time.time()
        
        logger.info(f"Cancelled experiment: {self.name} ({self.id})")
        return True
    
    def update_metrics(self, metrics: Dict[str, Any]) -> None:
        """
        Update the metrics for the experiment.
        
        Args:
            metrics: The metrics to update
        """
        self.metrics.update(metrics)
        logger.debug(f"Updated metrics for experiment {self.id}: {metrics}")
    
    def add_log(self, message: str, level: str = "INFO", timestamp: Optional[float] = None) -> None:
        """
        Add a log entry to the experiment.
        
        Args:
            message: The log message
            level: The log level
            timestamp: The timestamp for the log entry (defaults to current time)
        """
        if timestamp is None:
            timestamp = time.time()
        
        log_entry = {
            "timestamp": timestamp,
            "level": level,
            "message": message
        }
        
        self.logs.append(log_entry)
        logger.debug(f"Added log entry to experiment {self.id}: {message}")
    
    def _evaluate_success(self) -> bool:
        """
        Evaluate whether the experiment was successful based on the success criteria.
        
        Returns:
            bool: True if the experiment was successful, False otherwise
        """
        # This is a simplified implementation. In a real system, this would use
        # more sophisticated success evaluation algorithms.
        
        for key, value in self.success_criteria.items():
            if key not in self.results:
                logger.warning(f"Success criterion {key} not found in results")
                return False
            
            if self.results[key] != value:
                logger.info(f"Success criterion not met: {key} = {self.results[key]}, expected {value}")
                return False
        
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the experiment to a dictionary.
        
        Returns:
            Dict: The experiment as a dictionary
        """
        return {
            "id": self.id,
            "name": self.name,
            "experiment_type": self.experiment_type.value,
            "description": self.description,
            "parameters": self.parameters,
            "success_criteria": self.success_criteria,
            "max_duration_seconds": self.max_duration_seconds,
            "status": self.status.value,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "results": self.results,
            "metrics": self.metrics,
            "logs": self.logs
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Experiment':
        """
        Create an experiment from a dictionary.
        
        Args:
            data: The dictionary containing the experiment data
        
        Returns:
            Experiment: The created experiment
        """
        experiment = cls(
            name=data.get("name", "Unknown"),
            experiment_type=ExperimentType(data.get("experiment_type", "custom")),
            description=data.get("description", ""),
            parameters=data.get("parameters", {}),
            success_criteria=data.get("success_criteria", {}),
            max_duration_seconds=data.get("max_duration_seconds", 3600)
        )
        
        experiment.id = data.get("id", experiment.id)
        experiment.status = ExperimentStatus(data.get("status", "created"))
        experiment.start_time = data.get("start_time")
        experiment.end_time = data.get("end_time")
        experiment.results = data.get("results", {})
        experiment.metrics = data.get("metrics", {})
        experiment.logs = data.get("logs", [])
        
        return experiment

class ExperimentationFramework:
    """
    Framework for running experiments with different autonomy settings.
    
    This class provides methods for creating, running, and managing experiments.
    """
    
    def __init__(self):
        """Initialize the experimentation framework."""
        self.experiments = {}
        logger.info("Initialized experimentation framework")
    
    def create_experiment(self, 
                         name: str, 
                         experiment_type: ExperimentType, 
                         description: str, 
                         parameters: Dict[str, Any],
                         success_criteria: Dict[str, Any],
                         max_duration_seconds: int = 3600,
                         callback: Optional[Callable[[Dict[str, Any]], None]] = None) -> Experiment:
        """
        Create a new experiment.
        
        Args:
            name: The name of the experiment
            experiment_type: The type of experiment
            description: A description of the experiment
            parameters: Parameters for the experiment
            success_criteria: Criteria for determining if the experiment is successful
            max_duration_seconds: Maximum duration of the experiment in seconds
            callback: Function to call when the experiment completes
        
        Returns:
            Experiment: The created experiment
        """
        experiment = Experiment(
            name=name,
            experiment_type=experiment_type,
            description=description,
            parameters=parameters,
            success_criteria=success_criteria,
            max_duration_seconds=max_duration_seconds,
            callback=callback
        )
        
        self.experiments[experiment.id] = experiment
        return experiment
    
    def get_experiment(self, experiment_id: str) -> Optional[Experiment]:
        """
        Get an experiment by ID.
        
        Args:
            experiment_id: The ID of the experiment
        
        Returns:
            Optional[Experiment]: The experiment, or None if not found
        """
        return self.experiments.get(experiment_id)
    
    def get_experiments(self, status: Optional[ExperimentStatus] = None) -> List[Experiment]:
        """
        Get all experiments, optionally filtered by status.
        
        Args:
            status: The status to filter by
        
        Returns:
            List[Experiment]: The experiments
        """
        if status is None:
            return list(self.experiments.values())
        
        return [exp for exp in self.experiments.values() if exp.status == status]
    
    def delete_experiment(self, experiment_id: str) -> bool:
        """
        Delete an experiment.
        
        Args:
            experiment_id: The ID of the experiment
        
        Returns:
            bool: True if the experiment was deleted, False otherwise
        """
        if experiment_id not in self.experiments:
            logger.warning(f"Experiment {experiment_id} not found")
            return False
        
        experiment = self.experiments[experiment_id]
        if experiment.status == ExperimentStatus.RUNNING:
            logger.warning(f"Cannot delete running experiment {experiment_id}")
            return False
        
        del self.experiments[experiment_id]
        logger.info(f"Deleted experiment: {experiment.name} ({experiment_id})")
        return True
