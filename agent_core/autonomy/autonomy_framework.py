"""
Autonomy Framework for the Nick the Great Unified Agent.

This module implements the autonomy framework that determines when the agent can act
autonomously and when it needs human approval.
"""

import logging
import time
import uuid
from typing import Dict, Any, List, Optional, Callable, Tuple

from .decision_matrix import DecisionMatrix, DecisionCategory, ApprovalLevel
from .notification_system import NotificationSystem, NotificationType, NotificationPriority
from .approval_workflow import ApprovalWorkflow, ApprovalStatus
from .risk_tolerance import RiskToleranceProfile, RiskAssessment, RiskCategory, RiskLevel, create_default_profiles
from .experimentation_framework import ExperimentationFramework, Experiment, ExperimentType, ExperimentStatus

# Import db_client for persistence
try:
    from agent_core.db_client import db_client
except ImportError:
    try:
        from ..db_client import db_client # If autonomy is a sub-package
    except ImportError:
        logger.warning("db_client could not be imported for AutonomyFramework. Persistence features will be disabled.")
        db_client = None


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AutonomyFramework:
    """
    Framework for managing agent autonomy.

    This class ties together the decision matrix, notification system, approval workflow,
    risk tolerance framework, and experimentation framework to provide a unified interface
    for determining when the agent can act autonomously.
    """

    def __init__(self, external_db_client: Optional[Any] = None):
        """
        Initialize the autonomy framework.
        
        Args:
            external_db_client: An optional database client instance. If None, will try to use the global db_client.
        """
        self.db_client = external_db_client if external_db_client else db_client
        
        self.decision_matrix = DecisionMatrix()
        # Pass db_client to NotificationSystem and ApprovalWorkflow
        self.notification_system = NotificationSystem(db_client=self.db_client)
        self.approval_workflow = ApprovalWorkflow(
            notification_system=self.notification_system,
            db_client=self.db_client,
            autonomy_framework_callback=self._handle_approval_result # Pass the callback method
        )
        self.pending_actions = {}  # Dictionary of action ID to pending action info

        # Initialize risk tolerance framework
        self.risk_profiles = create_default_profiles()
        self.current_risk_profile = self.risk_profiles["balanced"]
        self.risk_assessment = RiskAssessment(self.current_risk_profile)

        # Initialize experimentation framework
        self.experimentation_framework = ExperimentationFramework()

        logger.info("Autonomy Framework initialized")

    def can_execute(self,
                   category: DecisionCategory,
                   action: str,
                   context: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Determine if the agent can execute an action without human approval.

        Args:
            category: The decision category
            action: The specific action
            context: The context in which the action is being performed

        Returns:
            Tuple[bool, Optional[str]]: (can_execute, reason)
        """
        # First, check the decision matrix
        approval_level = self.decision_matrix.get_approval_level(category, action, context)

        if approval_level == ApprovalLevel.PROHIBITED:
            return False, "Action prohibited"

        # Next, assess the risk
        risk_assessment = self.risk_assessment.assess_risk(action, context)
        within_tolerance, risk_reason = self.risk_assessment.is_within_tolerance(risk_assessment)

        if not within_tolerance:
            # If the risk exceeds tolerance, require approval regardless of the decision matrix
            return False, f"Risk exceeds tolerance: {risk_reason}"

        # If the risk is within tolerance, proceed with the decision matrix result
        if approval_level == ApprovalLevel.AUTONOMOUS:
            return True, None

        if approval_level == ApprovalLevel.NOTIFY:
            return True, "Notification required"

        if approval_level == ApprovalLevel.APPROVAL_REQUIRED:
            return False, "Approval required"

        return False, "Unknown approval level"

    def execute_action(self,
                      category: DecisionCategory,
                      action: str,
                      context: Dict[str, Any],
                      title: str,
                      description: str,
                      execute_function: Callable[[Dict[str, Any]], Any],
                      user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute an action with the appropriate approval flow.

        Args:
            category: The decision category
            action: The specific action
            context: The context in which the action is being performed
            title: A short title describing the action
            description: A detailed description of the action
            execute_function: Function to call to execute the action
            user_id: The ID of the user to notify or request approval from

        Returns:
            Dict: Result of the action execution or information about the approval request
        """
        # Determine if the agent can execute the action
        can_execute, reason = self.can_execute(category, action, context)

        # Generate a unique ID for this action
        action_id = str(uuid.uuid4())

        if can_execute:
            # Execute the action
            try:
                result = execute_function(context)

                # If notification is required, send it
                approval_level = self.decision_matrix.get_approval_level(category, action, context)
                if approval_level == ApprovalLevel.NOTIFY:
                    self.notification_system.create_notification(
                        title=f"Action Executed: {title}",
                        message=description,
                        notification_type=NotificationType.INFO,
                        priority=NotificationPriority.MEDIUM,
                        user_id=user_id,
                        related_entity_id=action_id,
                        related_entity_type=f"{category.value}_{action}"
                    )

                return {
                    "action_id": action_id,
                    "status": "executed",
                    "result": result
                }
            except Exception as e:
                logger.error(f"Error executing action {category.value}.{action}: {e}")

                # Notify about the error
                self.notification_system.create_notification(
                    title=f"Action Failed: {title}",
                    message=f"Error executing action: {e}\n\n{description}",
                    notification_type=NotificationType.ERROR,
                    priority=NotificationPriority.HIGH,
                    user_id=user_id,
                    related_entity_id=action_id,
                    related_entity_type=f"{category.value}_{action}"
                )

                return {
                    "action_id": action_id,
                    "status": "failed",
                    "error": str(e)
                }
        else:
            # Action requires approval or is prohibited
            approval_level = self.decision_matrix.get_approval_level(category, action, context)

            if approval_level == ApprovalLevel.PROHIBITED:
                logger.warning(f"Attempted to execute prohibited action {category.value}.{action}")

                # Notify about the prohibited action attempt
                self.notification_system.create_notification(
                    title=f"Prohibited Action Attempted: {title}",
                    message=f"The agent attempted to execute a prohibited action:\n\n{description}",
                    notification_type=NotificationType.WARNING,
                    priority=NotificationPriority.HIGH,
                    user_id=user_id,
                    related_entity_id=action_id,
                    related_entity_type=f"{category.value}_{action}"
                )

                return {
                    "action_id": action_id,
                    "status": "prohibited",
                    "reason": reason
                }

            # Store the execute function for later use
            self.pending_actions[action_id] = {
                "category": category,
                "action": action,
                "context": context,
                "execute_function": execute_function,
                "created_time": int(time.time())
            }

            # Create an approval request
            def approval_callback(request_id, status, details):
                self._handle_approval_result(action_id, request_id, status, details)

            request = self.approval_workflow.create_approval_request(
                title=title,
                description=description,
                category=category,
                action=action,
                context=context,
                user_id=user_id,
                callback=approval_callback
            )

            return {
                "action_id": action_id,
                "status": "approval_requested",
                "approval_request_id": request.id,
                "reason": reason
            }

    def _handle_approval_result(self, action_id: str, request_id: str, status: ApprovalStatus, details: Dict[str, Any]):
        """
        Handle the result of an approval request.

        Args:
            action_id: The ID of the action
            request_id: The ID of the approval request (used for tracking)
            status: The approval status
            details: Additional details about the approval decision
        """
        if action_id not in self.pending_actions:
            logger.warning(f"Received approval result for unknown action: {action_id}")
            return

        pending_action = self.pending_actions[action_id]

        if status == ApprovalStatus.APPROVED:
            logger.info(f"Action {action_id} approved by user {details.get('user_id')}")

            # Execute the action
            try:
                action_result = pending_action["execute_function"](pending_action["context"])

                # Notify about the successful execution
                self.notification_system.create_notification(
                    title=f"Approved Action Executed",
                    message=f"The approved action has been executed successfully.",
                    notification_type=NotificationType.INFO,
                    priority=NotificationPriority.MEDIUM,
                    user_id=details.get("user_id"),
                    related_entity_id=action_id,
                    related_entity_type=f"{pending_action['category'].value}_{pending_action['action']}"
                )

                # Log the result
                logger.info(f"Action {action_id} executed with result: {action_result}")

                # Clean up
                del self.pending_actions[action_id]

            except Exception as e:
                logger.error(f"Error executing approved action {action_id}: {e}")

                # Notify about the error
                self.notification_system.create_notification(
                    title=f"Approved Action Failed",
                    message=f"Error executing the approved action: {e}",
                    notification_type=NotificationType.ERROR,
                    priority=NotificationPriority.HIGH,
                    user_id=details.get("user_id"),
                    related_entity_id=action_id,
                    related_entity_type=f"{pending_action['category'].value}_{pending_action['action']}"
                )

        elif status == ApprovalStatus.REJECTED:
            logger.info(f"Action {action_id} rejected by user {details.get('user_id')}")

            # Notify about the rejection
            self.notification_system.create_notification(
                title=f"Action Rejected",
                message=f"The action has been rejected. Reason: {details.get('reason', 'No reason provided')}",
                notification_type=NotificationType.INFO,
                priority=NotificationPriority.MEDIUM,
                user_id=details.get("user_id"),
                related_entity_id=action_id,
                related_entity_type=f"{pending_action['category'].value}_{pending_action['action']}"
            )

            # Clean up
            del self.pending_actions[action_id]

        elif status in [ApprovalStatus.EXPIRED, ApprovalStatus.CANCELLED]:
            logger.info(f"Action {action_id} {status.value}")

            # Clean up
            del self.pending_actions[action_id]

    def get_decision_matrix(self) -> DecisionMatrix:
        """Get the decision matrix."""
        return self.decision_matrix

    def get_notification_system(self) -> NotificationSystem:
        """Get the notification system."""
        return self.notification_system

    def get_approval_workflow(self) -> ApprovalWorkflow:
        """Get the approval workflow."""
        return self.approval_workflow

    def get_risk_profile(self) -> RiskToleranceProfile:
        """Get the current risk tolerance profile."""
        return self.current_risk_profile

    def set_risk_profile(self, profile_name: str) -> bool:
        """
        Set the current risk tolerance profile.

        Args:
            profile_name: The name of the profile to set

        Returns:
            bool: True if the profile was set successfully, False otherwise
        """
        if profile_name not in self.risk_profiles:
            logger.warning(f"Unknown risk profile: {profile_name}")
            return False

        self.current_risk_profile = self.risk_profiles[profile_name]
        self.risk_assessment = RiskAssessment(self.current_risk_profile)

        logger.info(f"Set risk profile to: {profile_name}")
        return True

    def update_risk_tolerance(self, category: RiskCategory, level: RiskLevel) -> bool:
        """
        Update the risk tolerance level for a specific category.

        Args:
            category: The risk category
            level: The new tolerance level

        Returns:
            bool: True if the tolerance level was updated successfully, False otherwise
        """
        try:
            self.current_risk_profile.update_tolerance_level(category, level)
            logger.info(f"Updated risk tolerance for {category.value} to {level.value}")
            return True
        except Exception as e:
            logger.error(f"Error updating risk tolerance: {e}")
            return False

    def create_experiment(self,
                         name: str,
                         experiment_type: ExperimentType,
                         description: str,
                         parameters: Dict[str, Any],
                         success_criteria: Dict[str, Any],
                         max_duration_seconds: int = 3600,
                         callback: Optional[Callable[[Dict[str, Any]], None]] = None) -> Optional[Experiment]:
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
            Optional[Experiment]: The created experiment, or None if creation failed
        """
        try:
            experiment = self.experimentation_framework.create_experiment(
                name=name,
                experiment_type=experiment_type,
                description=description,
                parameters=parameters,
                success_criteria=success_criteria,
                max_duration_seconds=max_duration_seconds,
                callback=callback
            )

            logger.info(f"Created experiment: {name} ({experiment.id})")
            return experiment
        except Exception as e:
            logger.error(f"Error creating experiment: {e}")
            return None

    def get_experiment(self, experiment_id: str) -> Optional[Experiment]:
        """
        Get an experiment by ID.

        Args:
            experiment_id: The ID of the experiment

        Returns:
            Optional[Experiment]: The experiment, or None if not found
        """
        return self.experimentation_framework.get_experiment(experiment_id)

    def get_experiments(self, status: Optional[ExperimentStatus] = None) -> List[Experiment]:
        """
        Get all experiments, optionally filtered by status.

        Args:
            status: The status to filter by

        Returns:
            List[Experiment]: The experiments
        """
        return self.experimentation_framework.get_experiments(status)
