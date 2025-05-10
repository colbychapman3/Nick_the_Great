"""
Experimentation Framework for the Nick the Great Unified Agent.

This module implements an experimentation framework that allows the agent to run
controlled experiments within predefined boundaries.
"""

import logging
import time
import uuid
from enum import Enum
from typing import Dict, Any, List, Optional, Callable, Tuple

from autonomy_framework import (
    DecisionCategory, 
    RiskLevel, 
    ApprovalLevel, 
    NotificationType, 
    NotificationPriority,
    AutonomyFramework
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ExperimentType(Enum):
    """Types of experiments that the agent can run."""
    A_B_TEST = "a_b_test"
    MULTIVARIATE_TEST = "multivariate_test"
    FEATURE_TEST = "feature_test"
    CONTENT_TEST = "content_test"
    PRICING_TEST = "pricing_test"
    AUDIENCE_TEST = "audience_test"
    PLATFORM_TEST = "platform_test"
    PRODUCT_TEST = "product_test"

class ExperimentStatus(Enum):
    """Status of an experiment."""
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class ExperimentParameter:
    """A parameter for an experiment."""
    
    def __init__(self, 
                name: str, 
                value_type: str,
                default_value: Any,
                min_value: Optional[Any] = None,
                max_value: Optional[Any] = None,
                allowed_values: Optional[List[Any]] = None,
                description: Optional[str] = None):
        """
        Initialize an experiment parameter.
        
        Args:
            name: The name of the parameter
            value_type: The type of the parameter value (e.g., "int", "float", "str", "bool")
            default_value: The default value of the parameter
            min_value: The minimum allowed value (for numeric parameters)
            max_value: The maximum allowed value (for numeric parameters)
            allowed_values: A list of allowed values (for enum-like parameters)
            description: A description of the parameter
        """
        self.name = name
        self.value_type = value_type
        self.default_value = default_value
        self.min_value = min_value
        self.max_value = max_value
        self.allowed_values = allowed_values
        self.description = description
    
    def validate(self, value: Any) -> Tuple[bool, Optional[str]]:
        """
        Validate a parameter value.
        
        Args:
            value: The value to validate
        
        Returns:
            Tuple[bool, Optional[str]]: (is_valid, error_message)
        """
        # Check type
        if self.value_type == "int":
            if not isinstance(value, int):
                return False, f"Parameter {self.name} must be an integer"
        elif self.value_type == "float":
            if not isinstance(value, (int, float)):
                return False, f"Parameter {self.name} must be a number"
        elif self.value_type == "str":
            if not isinstance(value, str):
                return False, f"Parameter {self.name} must be a string"
        elif self.value_type == "bool":
            if not isinstance(value, bool):
                return False, f"Parameter {self.name} must be a boolean"
        
        # Check range
        if self.min_value is not None and value < self.min_value:
            return False, f"Parameter {self.name} must be at least {self.min_value}"
        
        if self.max_value is not None and value > self.max_value:
            return False, f"Parameter {self.name} must be at most {self.max_value}"
        
        # Check allowed values
        if self.allowed_values is not None and value not in self.allowed_values:
            return False, f"Parameter {self.name} must be one of {self.allowed_values}"
        
        return True, None

class ExperimentTemplate:
    """A template for an experiment."""
    
    def __init__(self, 
                name: str, 
                experiment_type: ExperimentType,
                description: str,
                parameters: List[ExperimentParameter],
                sample_size_range: Tuple[int, int],
                duration_range: Tuple[int, int],
                budget_limit: float,
                approval_required: bool,
                success_criteria: Dict[str, Any],
                risk_level: RiskLevel):
        """
        Initialize an experiment template.
        
        Args:
            name: The name of the template
            experiment_type: The type of experiment
            description: A description of the template
            parameters: The parameters for the experiment
            sample_size_range: The allowed range for sample size (min, max)
            duration_range: The allowed range for duration in days (min, max)
            budget_limit: The maximum budget for the experiment
            approval_required: Whether approval is required to run the experiment
            success_criteria: The criteria for determining success
            risk_level: The risk level of the experiment
        """
        self.id = str(uuid.uuid4())
        self.name = name
        self.experiment_type = experiment_type
        self.description = description
        self.parameters = {param.name: param for param in parameters}
        self.sample_size_range = sample_size_range
        self.duration_range = duration_range
        self.budget_limit = budget_limit
        self.approval_required = approval_required
        self.success_criteria = success_criteria
        self.risk_level = risk_level
        self.created_time = int(time.time())

class Experiment:
    """An experiment run by the agent."""
    
    def __init__(self, 
                name: str, 
                experiment_type: ExperimentType,
                description: str,
                parameters: Dict[str, Any],
                sample_size: int,
                duration: int,
                budget: float,
                success_criteria: Dict[str, Any],
                template_id: Optional[str] = None,
                user_id: Optional[str] = None):
        """
        Initialize an experiment.
        
        Args:
            name: The name of the experiment
            experiment_type: The type of experiment
            description: A description of the experiment
            parameters: The parameters for the experiment
            sample_size: The sample size for the experiment
            duration: The duration of the experiment in days
            budget: The budget for the experiment
            success_criteria: The criteria for determining success
            template_id: The ID of the template used (if any)
            user_id: The ID of the user who created the experiment
        """
        self.id = str(uuid.uuid4())
        self.name = name
        self.experiment_type = experiment_type
        self.description = description
        self.parameters = parameters
        self.sample_size = sample_size
        self.duration = duration
        self.budget = budget
        self.success_criteria = success_criteria
        self.template_id = template_id
        self.user_id = user_id
        self.status = ExperimentStatus.DRAFT
        self.created_time = int(time.time())
        self.start_time = None
        self.end_time = None
        self.results = {}
        self.metrics = {}
        self.notes = []

class ExperimentationFramework:
    """Framework for running controlled experiments."""
    
    def __init__(self, autonomy_framework: AutonomyFramework):
        """
        Initialize the experimentation framework.
        
        Args:
            autonomy_framework: The autonomy framework to use for approvals
        """
        self.autonomy_framework = autonomy_framework
        self.templates = {}  # Dictionary of template_id to ExperimentTemplate
        self.experiments = {}  # Dictionary of experiment_id to Experiment
        self.running_experiments = {}  # Dictionary of experiment_id to experiment runner
        logger.info("Experimentation Framework initialized")
        
        # Initialize with default templates
        self._initialize_default_templates()
    
    def _initialize_default_templates(self) -> None:
        """Initialize default experiment templates."""
        # A/B Content Test Template
        ab_content_template = ExperimentTemplate(
            name="A/B Content Test",
            experiment_type=ExperimentType.A_B_TEST,
            description="Test two versions of content to determine which performs better",
            parameters=[
                ExperimentParameter("content_a", "str", "", description="First content variant"),
                ExperimentParameter("content_b", "str", "", description="Second content variant"),
                ExperimentParameter("target_audience", "str", "all", description="Target audience for the test"),
                ExperimentParameter("metric", "str", "engagement", allowed_values=["engagement", "conversion", "retention"], description="Primary metric to optimize for")
            ],
            sample_size_range=(1000, 5000),
            duration_range=(3, 7),
            budget_limit=500.0,
            approval_required=False,
            success_criteria={
                "min_improvement": 0.05,  # 5% improvement
                "confidence_level": 0.95  # 95% confidence
            },
            risk_level=RiskLevel.LOW
        )
        self.templates[ab_content_template.id] = ab_content_template
        
        # Pricing Test Template
        pricing_template = ExperimentTemplate(
            name="Pricing Test",
            experiment_type=ExperimentType.PRICING_TEST,
            description="Test different price points to determine optimal pricing",
            parameters=[
                ExperimentParameter("price_a", "float", 0.0, min_value=0.0, description="First price point"),
                ExperimentParameter("price_b", "float", 0.0, min_value=0.0, description="Second price point"),
                ExperimentParameter("product_id", "str", "", description="ID of the product being tested"),
                ExperimentParameter("target_audience", "str", "all", description="Target audience for the test")
            ],
            sample_size_range=(500, 2000),
            duration_range=(5, 14),
            budget_limit=1000.0,
            approval_required=True,
            success_criteria={
                "min_revenue_increase": 0.1,  # 10% revenue increase
                "confidence_level": 0.95  # 95% confidence
            },
            risk_level=RiskLevel.MEDIUM
        )
        self.templates[pricing_template.id] = pricing_template
        
        logger.info(f"Initialized {len(self.templates)} default experiment templates")
    
    def create_experiment(self, 
                         name: str, 
                         experiment_type: ExperimentType,
                         description: str,
                         parameters: Dict[str, Any],
                         sample_size: int,
                         duration: int,
                         budget: float,
                         success_criteria: Dict[str, Any],
                         template_id: Optional[str] = None,
                         user_id: Optional[str] = None) -> Tuple[Experiment, List[str]]:
        """
        Create a new experiment.
        
        Args:
            name: The name of the experiment
            experiment_type: The type of experiment
            description: A description of the experiment
            parameters: The parameters for the experiment
            sample_size: The sample size for the experiment
            duration: The duration of the experiment in days
            budget: The budget for the experiment
            success_criteria: The criteria for determining success
            template_id: The ID of the template to use (if any)
            user_id: The ID of the user creating the experiment
        
        Returns:
            Tuple[Experiment, List[str]]: The created experiment and a list of validation warnings
        """
        warnings = []
        
        # If a template is specified, validate against it
        if template_id and template_id in self.templates:
            template = self.templates[template_id]
            
            # Check sample size
            min_size, max_size = template.sample_size_range
            if sample_size < min_size:
                warnings.append(f"Sample size {sample_size} is below the recommended minimum of {min_size}")
            elif sample_size > max_size:
                warnings.append(f"Sample size {sample_size} is above the recommended maximum of {max_size}")
            
            # Check duration
            min_duration, max_duration = template.duration_range
            if duration < min_duration:
                warnings.append(f"Duration {duration} days is below the recommended minimum of {min_duration} days")
            elif duration > max_duration:
                warnings.append(f"Duration {duration} days is above the recommended maximum of {max_duration} days")
            
            # Check budget
            if budget > template.budget_limit:
                warnings.append(f"Budget ${budget} is above the recommended limit of ${template.budget_limit}")
            
            # Validate parameters
            for param_name, param in template.parameters.items():
                if param_name not in parameters:
                    parameters[param_name] = param.default_value
                    warnings.append(f"Parameter {param_name} not specified, using default value: {param.default_value}")
                else:
                    is_valid, error = param.validate(parameters[param_name])
                    if not is_valid:
                        warnings.append(error)
                        parameters[param_name] = param.default_value
                        warnings.append(f"Invalid value for parameter {param_name}, using default value: {param.default_value}")
        
        # Create the experiment
        experiment = Experiment(
            name=name,
            experiment_type=experiment_type,
            description=description,
            parameters=parameters,
            sample_size=sample_size,
            duration=duration,
            budget=budget,
            success_criteria=success_criteria,
            template_id=template_id,
            user_id=user_id
        )
        
        self.experiments[experiment.id] = experiment
        logger.info(f"Created experiment: {experiment.id} - {name}")
        
        return experiment, warnings
    
    def start_experiment(self, experiment_id: str) -> Tuple[bool, Optional[str]]:
        """
        Start an experiment.
        
        Args:
            experiment_id: The ID of the experiment to start
        
        Returns:
            Tuple[bool, Optional[str]]: (success, error_message)
        """
        if experiment_id not in self.experiments:
            return False, f"Experiment {experiment_id} not found"
        
        experiment = self.experiments[experiment_id]
        
        if experiment.status != ExperimentStatus.DRAFT and experiment.status != ExperimentStatus.PAUSED:
            return False, f"Experiment {experiment_id} is not in DRAFT or PAUSED status"
        
        # Check if approval is required
        if experiment.template_id and experiment.template_id in self.templates:
            template = self.templates[experiment.template_id]
            
            if template.approval_required:
                # Check if we have approval to run this experiment
                can_execute, reason = self.autonomy_framework.can_execute(
                    category=DecisionCategory.NEW_OPPORTUNITY,
                    action="run_experiment",
                    context={
                        "experiment_id": experiment_id,
                        "experiment_type": experiment.experiment_type.value,
                        "budget": experiment.budget,
                        "metrics": {
                            "budget": experiment.budget
                        },
                        "risk_level": template.risk_level
                    }
                )
                
                if not can_execute:
                    # Set status to pending approval
                    experiment.status = ExperimentStatus.PENDING_APPROVAL
                    
                    # Create an approval request
                    self.autonomy_framework.get_approval_workflow().create_approval_request(
                        title=f"Experiment Approval: {experiment.name}",
                        description=f"Approval is required to run the following experiment:\n\n"
                                   f"Name: {experiment.name}\n"
                                   f"Type: {experiment.experiment_type.value}\n"
                                   f"Budget: ${experiment.budget}\n"
                                   f"Sample Size: {experiment.sample_size}\n"
                                   f"Duration: {experiment.duration} days\n\n"
                                   f"Description: {experiment.description}",
                        category=DecisionCategory.NEW_OPPORTUNITY,
                        action="run_experiment",
                        context={
                            "experiment_id": experiment_id,
                            "experiment_type": experiment.experiment_type.value,
                            "budget": experiment.budget,
                            "risk_level": template.risk_level
                        },
                        user_id=experiment.user_id,
                        callback=self._experiment_approval_callback
                    )
                    
                    return False, f"Experiment {experiment_id} requires approval to start"
        
        # Start the experiment
        experiment.status = ExperimentStatus.RUNNING
        experiment.start_time = int(time.time())
        
        # In a real implementation, we would start the experiment runner here
        # For now, we'll just log that the experiment has started
        logger.info(f"Started experiment: {experiment_id}")
        
        return True, None
    
    def _experiment_approval_callback(self, request_id: str, status: str, details: Optional[str]) -> None:
        """
        Callback for experiment approval requests.
        
        Args:
            request_id: The ID of the approval request
            status: The status of the approval request
            details: Additional details about the decision
        """
        # Find the experiment associated with this approval request
        for experiment_id, experiment in self.experiments.items():
            if experiment.status == ExperimentStatus.PENDING_APPROVAL:
                # This is a simplification - in a real implementation, we would store the request ID with the experiment
                
                if status == "approved":
                    # Start the experiment
                    experiment.status = ExperimentStatus.RUNNING
                    experiment.start_time = int(time.time())
                    logger.info(f"Started experiment {experiment_id} after approval")
                else:
                    # Mark as cancelled
                    experiment.status = ExperimentStatus.CANCELLED
                    experiment.notes.append(f"Cancelled due to approval rejection: {details}")
                    logger.info(f"Cancelled experiment {experiment_id} due to approval rejection")
                
                break
