"""
Simplified Autonomy Framework for the Nick the Great Unified Agent.

This module implements a simplified version of the autonomy framework that determines
when the agent can act autonomously and when it needs human approval.
"""

import logging
import time
import uuid
from enum import Enum
from typing import Dict, Any, List, Optional, Callable, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DecisionCategory(Enum):
    """Categories of decisions that the agent can make."""
    EXPERIMENT_MANAGEMENT = "experiment_management"
    CONTENT_CREATION = "content_creation"
    FINANCIAL = "financial"
    PLATFORM_INTERACTION = "platform_interaction"
    SYSTEM = "system"
    RESOURCE_ALLOCATION = "resource_allocation"
    STRATEGY_ADJUSTMENT = "strategy_adjustment"
    NEW_OPPORTUNITY = "new_opportunity"
    PLATFORM_EXPANSION = "platform_expansion"

class RiskLevel(Enum):
    """Risk levels for different actions."""
    LOW = "low"  # Low risk actions
    MEDIUM = "medium"  # Medium risk actions
    HIGH = "high"  # High risk actions
    CRITICAL = "critical"  # Critical risk actions

class ApprovalLevel(Enum):
    """Levels of approval required for different actions."""
    AUTONOMOUS = "autonomous"  # Agent can act without human approval
    NOTIFY = "notify"  # Agent can act but must notify humans
    APPROVAL_REQUIRED = "approval_required"  # Agent must get human approval before acting
    PROHIBITED = "prohibited"  # Agent cannot perform this action

class NotificationType(Enum):
    """Types of notifications that the agent can send."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"

class NotificationPriority(Enum):
    """Priority levels for notifications."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ApprovalStatus(Enum):
    """Status of an approval request."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"

class NotificationChannel(Enum):
    """Channels through which notifications can be sent."""
    EMAIL = "email"
    SMS = "sms"
    DASHBOARD = "dashboard"
    MOBILE_PUSH = "mobile_push"
    SLACK = "slack"
    WEBHOOK = "webhook"

class NotificationPreference:
    """User preferences for notifications."""

    def __init__(self,
                user_id: str,
                channels: Dict[NotificationPriority, List[NotificationChannel]] = None,
                do_not_disturb: List[Dict[str, Any]] = None,
                batching: Dict[NotificationPriority, int] = None):
        """
        Initialize notification preferences.

        Args:
            user_id: The ID of the user
            channels: Dictionary mapping priority levels to preferred channels
            do_not_disturb: List of time periods during which notifications should not be sent
            batching: Dictionary mapping priority levels to batching intervals (in minutes)
        """
        self.user_id = user_id

        # Default channel preferences if none provided
        self.channels = channels or {
            NotificationPriority.LOW: [NotificationChannel.DASHBOARD],
            NotificationPriority.MEDIUM: [NotificationChannel.DASHBOARD, NotificationChannel.EMAIL],
            NotificationPriority.HIGH: [NotificationChannel.DASHBOARD, NotificationChannel.EMAIL, NotificationChannel.SMS],
            NotificationPriority.CRITICAL: [NotificationChannel.DASHBOARD, NotificationChannel.EMAIL, NotificationChannel.SMS, NotificationChannel.MOBILE_PUSH]
        }

        # Default do-not-disturb periods if none provided
        self.do_not_disturb = do_not_disturb or []

        # Default batching intervals if none provided
        self.batching = batching or {
            NotificationPriority.LOW: 60,  # 60 minutes
            NotificationPriority.MEDIUM: 30,  # 30 minutes
            NotificationPriority.HIGH: 15,  # 15 minutes
            NotificationPriority.CRITICAL: 0  # No batching (immediate)
        }

class Notification:
    """A notification sent by the agent to humans."""

    def __init__(self,
                title: str,
                message: str,
                notification_type: NotificationType,
                priority: NotificationPriority,
                user_id: Optional[str] = None,
                related_entity_id: Optional[str] = None,
                related_entity_type: Optional[str] = None,
                metadata: Optional[Dict[str, Any]] = None):
        """
        Initialize a notification.

        Args:
            title: A short title for the notification
            message: The detailed notification message
            notification_type: The type of notification
            priority: The priority of the notification
            user_id: The ID of the user to notify (if applicable)
            related_entity_id: The ID of the related entity (if applicable)
            related_entity_type: The type of the related entity (if applicable)
            metadata: Additional metadata for the notification
        """
        self.id = str(uuid.uuid4())
        self.title = title
        self.message = message
        self.notification_type = notification_type
        self.priority = priority
        self.user_id = user_id
        self.related_entity_id = related_entity_id
        self.related_entity_type = related_entity_type
        self.metadata = metadata or {}
        self.created_time = int(time.time())
        self.read = False
        self.sent = False
        self.sent_time = None
        self.sent_channels = []

class ApprovalRequest:
    """A request for human approval of an agent action."""

    def __init__(self,
                title: str,
                description: str,
                category: DecisionCategory,
                action: str,
                context: Dict[str, Any],
                user_id: Optional[str] = None,
                callback: Optional[Callable] = None,
                expiration_time: Optional[int] = None,
                auto_approve_after: Optional[int] = None,
                auto_reject_after: Optional[int] = None):
        """
        Initialize an approval request.

        Args:
            title: A short title for the approval request
            description: A detailed description of the action requiring approval
            category: The decision category
            action: The specific action
            context: The context in which the action is being performed
            user_id: The ID of the user to request approval from
            callback: Function to call when the approval status changes
            expiration_time: Time (in seconds since epoch) when the request expires
            auto_approve_after: Time (in seconds) after which the request is automatically approved
            auto_reject_after: Time (in seconds) after which the request is automatically rejected
        """
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.category = category
        self.action = action
        self.context = context
        self.user_id = user_id
        self.callback = callback
        self.status = ApprovalStatus.PENDING
        self.created_time = int(time.time())
        self.updated_time = self.created_time
        self.response_details = None

        # Set expiration time if provided, otherwise default to 24 hours
        if expiration_time:
            self.expiration_time = expiration_time
        elif auto_approve_after:
            self.expiration_time = self.created_time + auto_approve_after
        elif auto_reject_after:
            self.expiration_time = self.created_time + auto_reject_after
        else:
            self.expiration_time = self.created_time + (24 * 60 * 60)  # 24 hours

        self.auto_approve_after = auto_approve_after
        self.auto_reject_after = auto_reject_after

class NotificationSystem:
    """System for sending notifications to humans."""

    def __init__(self):
        """Initialize the notification system."""
        self.notifications = []
        self.user_preferences = {}  # Dictionary of user_id to NotificationPreference
        self.notification_batches = {}  # Dictionary of user_id to batched notifications
        self.last_batch_time = {}  # Dictionary of user_id to last batch time
        logger.info("Notification System initialized")

    def create_notification(self,
                           title: str,
                           message: str,
                           notification_type: NotificationType,
                           priority: NotificationPriority,
                           user_id: Optional[str] = None,
                           related_entity_id: Optional[str] = None,
                           related_entity_type: Optional[str] = None,
                           metadata: Optional[Dict[str, Any]] = None) -> Notification:
        """
        Create a new notification.

        Args:
            title: A short title for the notification
            message: The detailed notification message
            notification_type: The type of notification
            priority: The priority of the notification
            user_id: The ID of the user to notify (if applicable)
            related_entity_id: The ID of the related entity (if applicable)
            related_entity_type: The type of the related entity (if applicable)
            metadata: Additional metadata for the notification

        Returns:
            Notification: The created notification
        """
        notification = Notification(
            title, message, notification_type, priority, user_id,
            related_entity_id, related_entity_type, metadata
        )
        self.notifications.append(notification)
        logger.info(f"Created notification: {notification.id} - {title}")

        # Process the notification based on user preferences
        if user_id and user_id in self.user_preferences:
            self._process_notification(notification)
        else:
            # Default processing for users without preferences
            notification.sent = True
            notification.sent_time = int(time.time())
            notification.sent_channels = [NotificationChannel.DASHBOARD]

        return notification

    def _process_notification(self, notification: Notification) -> None:
        """
        Process a notification based on user preferences.

        Args:
            notification: The notification to process
        """
        user_id = notification.user_id
        if not user_id or user_id not in self.user_preferences:
            return

        preferences = self.user_preferences[user_id]

        # Check if we're in a do-not-disturb period
        current_time = int(time.time())
        in_dnd = False
        for dnd_period in preferences.do_not_disturb:
            start_time = dnd_period.get("start_time")
            end_time = dnd_period.get("end_time")
            if start_time and end_time and start_time <= current_time <= end_time:
                in_dnd = True
                break

        # If in DND period and not critical, batch for later
        if in_dnd and notification.priority != NotificationPriority.CRITICAL:
            self._add_to_batch(notification)
            return

        # Check if we should batch based on priority
        batch_interval = preferences.batching.get(notification.priority, 0)
        if batch_interval > 0:
            last_batch = self.last_batch_time.get(user_id, {}).get(notification.priority, 0)
            if current_time - last_batch < batch_interval * 60:  # Convert minutes to seconds
                self._add_to_batch(notification)
                return

        # Send immediately if not batched
        self._send_notification(notification)

    def _add_to_batch(self, notification: Notification) -> None:
        """
        Add a notification to the batch for later sending.

        Args:
            notification: The notification to batch
        """
        user_id = notification.user_id
        if user_id not in self.notification_batches:
            self.notification_batches[user_id] = {}

        priority = notification.priority
        if priority not in self.notification_batches[user_id]:
            self.notification_batches[user_id][priority] = []

        self.notification_batches[user_id][priority].append(notification)
        logger.info(f"Batched notification: {notification.id} for user {user_id}")

    def _send_notification(self, notification: Notification) -> None:
        """
        Send a notification through the appropriate channels.

        Args:
            notification: The notification to send
        """
        user_id = notification.user_id
        if not user_id or user_id not in self.user_preferences:
            # Default to dashboard only
            notification.sent = True
            notification.sent_time = int(time.time())
            notification.sent_channels = [NotificationChannel.DASHBOARD]
            return

        preferences = self.user_preferences[user_id]
        channels = preferences.channels.get(notification.priority, [NotificationChannel.DASHBOARD])

        # In a real implementation, we would send through each channel here
        # For now, we'll just mark it as sent
        notification.sent = True
        notification.sent_time = int(time.time())
        notification.sent_channels = channels

        logger.info(f"Sent notification: {notification.id} to user {user_id} via {', '.join([c.value for c in channels])}")

    def process_batches(self) -> None:
        """Process all batched notifications that are due to be sent."""
        current_time = int(time.time())

        for user_id, priority_batches in self.notification_batches.items():
            if user_id not in self.user_preferences:
                continue

            preferences = self.user_preferences[user_id]

            for priority, notifications in priority_batches.items():
                if not notifications:
                    continue

                batch_interval = preferences.batching.get(priority, 0)
                last_batch = self.last_batch_time.get(user_id, {}).get(priority, 0)

                if current_time - last_batch >= batch_interval * 60:  # Convert minutes to seconds
                    # Send the batch
                    for notification in notifications:
                        self._send_notification(notification)

                    # Update last batch time
                    if user_id not in self.last_batch_time:
                        self.last_batch_time[user_id] = {}
                    self.last_batch_time[user_id][priority] = current_time

                    # Clear the batch
                    self.notification_batches[user_id][priority] = []

    def set_user_preferences(self, preferences: NotificationPreference) -> None:
        """
        Set notification preferences for a user.

        Args:
            preferences: The notification preferences
        """
        self.user_preferences[preferences.user_id] = preferences
        logger.info(f"Set notification preferences for user {preferences.user_id}")

    def get_notifications(self, user_id: Optional[str] = None, include_read: bool = False) -> List[Notification]:
        """
        Get all notifications for a user.

        Args:
            user_id: The ID of the user to get notifications for (if None, get all)
            include_read: Whether to include read notifications

        Returns:
            List[Notification]: The list of notifications
        """
        if user_id is None:
            notifications = self.notifications
        else:
            notifications = [n for n in self.notifications if n.user_id == user_id]

        if not include_read:
            notifications = [n for n in notifications if not n.read]

        return notifications

    def mark_as_read(self, notification_id: str) -> bool:
        """
        Mark a notification as read.

        Args:
            notification_id: The ID of the notification to mark as read

        Returns:
            bool: True if the notification was found and marked as read, False otherwise
        """
        for notification in self.notifications:
            if notification.id == notification_id:
                notification.read = True
                logger.info(f"Marked notification {notification_id} as read")
                return True

        logger.warning(f"Notification not found: {notification_id}")
        return False

class ApprovalDelegate:
    """A delegate who can approve or reject requests on behalf of a user."""

    def __init__(self,
                user_id: str,
                delegate_id: str,
                categories: List[DecisionCategory] = None,
                risk_levels: List[RiskLevel] = None,
                expiration_time: Optional[int] = None):
        """
        Initialize an approval delegate.

        Args:
            user_id: The ID of the user delegating approval authority
            delegate_id: The ID of the user receiving delegation
            categories: The decision categories the delegate can approve (None for all)
            risk_levels: The risk levels the delegate can approve (None for all)
            expiration_time: Time (in seconds since epoch) when the delegation expires
        """
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.delegate_id = delegate_id
        self.categories = categories
        self.risk_levels = risk_levels
        self.created_time = int(time.time())
        self.expiration_time = expiration_time or (self.created_time + 30 * 24 * 60 * 60)  # Default 30 days
        self.active = True

    def can_approve(self, category: DecisionCategory, risk_level: RiskLevel) -> bool:
        """
        Check if this delegate can approve a request with the given category and risk level.

        Args:
            category: The decision category
            risk_level: The risk level

        Returns:
            bool: True if the delegate can approve, False otherwise
        """
        if not self.active or int(time.time()) > self.expiration_time:
            return False

        if self.categories and category not in self.categories:
            return False

        if self.risk_levels and risk_level not in self.risk_levels:
            return False

        return True

class ApprovalWorkflow:
    """Workflow for requesting and processing human approvals."""

    def __init__(self, notification_system: NotificationSystem):
        """Initialize the approval workflow."""
        self.notification_system = notification_system
        self.approval_requests = []
        self.delegates = {}  # Dictionary of user_id to list of ApprovalDelegate
        self.approval_templates = {}  # Dictionary of template_id to template
        logger.info("Approval Workflow initialized")

    def create_approval_request(self,
                               title: str,
                               description: str,
                               category: DecisionCategory,
                               action: str,
                               context: Dict[str, Any],
                               user_id: Optional[str] = None,
                               callback: Optional[Callable] = None,
                               expiration_time: Optional[int] = None,
                               auto_approve_after: Optional[int] = None,
                               auto_reject_after: Optional[int] = None,
                               template_id: Optional[str] = None) -> ApprovalRequest:
        """
        Create a new approval request.

        Args:
            title: A short title for the approval request
            description: A detailed description of the action requiring approval
            category: The decision category
            action: The specific action
            context: The context in which the action is being performed
            user_id: The ID of the user to request approval from
            callback: Function to call when the approval status changes
            expiration_time: Time (in seconds since epoch) when the request expires
            auto_approve_after: Time (in seconds) after which the request is automatically approved
            auto_reject_after: Time (in seconds) after which the request is automatically rejected
            template_id: ID of a template to use for this request

        Returns:
            ApprovalRequest: The created approval request
        """
        # Apply template if provided
        if template_id and template_id in self.approval_templates:
            template = self.approval_templates[template_id]

            # Apply template defaults for any unspecified parameters
            title = title or template.get("title")
            description = description or template.get("description")
            category = category or template.get("category")
            action = action or template.get("action")
            context = {**template.get("context", {}), **context}
            user_id = user_id or template.get("user_id")
            expiration_time = expiration_time or template.get("expiration_time")
            auto_approve_after = auto_approve_after or template.get("auto_approve_after")
            auto_reject_after = auto_reject_after or template.get("auto_reject_after")

        # Create the request
        request = ApprovalRequest(
            title, description, category, action, context, user_id, callback,
            expiration_time, auto_approve_after, auto_reject_after
        )
        self.approval_requests.append(request)

        # Check for delegates who can approve this request
        risk_level = context.get("risk_level", RiskLevel.MEDIUM)
        delegates = self._get_delegates(user_id, category, risk_level)

        # Create a notification for the approval request
        self.notification_system.create_notification(
            title=f"Approval Required: {title}",
            message=f"The agent requires your approval for the following action:\n\n{description}",
            notification_type=NotificationType.WARNING,
            priority=NotificationPriority.HIGH,
            user_id=user_id,
            related_entity_id=request.id,
            related_entity_type="approval_request",
            metadata={
                "category": category.value,
                "action": action,
                "delegates": [d.delegate_id for d in delegates]
            }
        )

        # Notify delegates
        for delegate in delegates:
            self.notification_system.create_notification(
                title=f"Delegated Approval Required: {title}",
                message=f"You have been delegated to approve the following action for {user_id}:\n\n{description}",
                notification_type=NotificationType.WARNING,
                priority=NotificationPriority.HIGH,
                user_id=delegate.delegate_id,
                related_entity_id=request.id,
                related_entity_type="approval_request",
                metadata={
                    "category": category.value,
                    "action": action,
                    "delegated_by": user_id
                }
            )

        logger.info(f"Created approval request: {request.id} - {title}")
        return request

    def process_approval(self,
                        request_id: str,
                        approved: bool,
                        details: Optional[str] = None,
                        approver_id: Optional[str] = None) -> bool:
        """
        Process an approval decision.

        Args:
            request_id: The ID of the approval request
            approved: Whether the request was approved
            details: Additional details about the decision
            approver_id: The ID of the user making the approval decision

        Returns:
            bool: True if the request was found and processed, False otherwise
        """
        for request in self.approval_requests:
            if request.id == request_id:
                if request.status != ApprovalStatus.PENDING:
                    logger.warning(f"Attempted to process non-pending approval request: {request_id}")
                    return False

                # Check if the approver is authorized
                if approver_id and approver_id != request.user_id:
                    # Check if the approver is a delegate
                    risk_level = request.context.get("risk_level", RiskLevel.MEDIUM)
                    if not self._is_delegate(approver_id, request.user_id, request.category, risk_level):
                        logger.warning(f"Unauthorized approval attempt by {approver_id} for request {request_id}")
                        return False

                request.status = ApprovalStatus.APPROVED if approved else ApprovalStatus.REJECTED
                request.updated_time = int(time.time())
                request.response_details = details

                # Create a notification about the approval decision
                self.notification_system.create_notification(
                    title=f"Approval {'Granted' if approved else 'Rejected'}: {request.title}",
                    message=f"The approval request has been {'approved' if approved else 'rejected'}.\n\n{details or ''}",
                    notification_type=NotificationType.SUCCESS if approved else NotificationType.WARNING,
                    priority=NotificationPriority.MEDIUM,
                    user_id=request.user_id,
                    related_entity_id=request.id,
                    related_entity_type="approval_request",
                    metadata={
                        "approver_id": approver_id or request.user_id,
                        "delegated": approver_id is not None and approver_id != request.user_id
                    }
                )

                # Call the callback if provided
                if request.callback:
                    try:
                        request.callback(request.id, request.status, details)
                    except Exception as e:
                        logger.error(f"Error in approval callback for request {request_id}: {e}")

                logger.info(f"Processed approval request {request_id}: {'approved' if approved else 'rejected'} by {approver_id or request.user_id}")
                return True

        logger.warning(f"Approval request not found: {request_id}")
        return False

    def check_expired_requests(self) -> None:
        """Check for expired approval requests and process them."""
        current_time = int(time.time())

        for request in self.approval_requests:
            if request.status != ApprovalStatus.PENDING:
                continue

            if current_time >= request.expiration_time:
                # Check if we should auto-approve or auto-reject
                if request.auto_approve_after and current_time >= request.created_time + request.auto_approve_after:
                    self.process_approval(
                        request.id,
                        True,
                        "Automatically approved due to timeout",
                        "system"
                    )
                elif request.auto_reject_after and current_time >= request.created_time + request.auto_reject_after:
                    self.process_approval(
                        request.id,
                        False,
                        "Automatically rejected due to timeout",
                        "system"
                    )
                else:
                    # Mark as expired
                    request.status = ApprovalStatus.EXPIRED
                    request.updated_time = current_time
                    request.response_details = "Request expired without a decision"

                    # Create a notification about the expired request
                    self.notification_system.create_notification(
                        title=f"Approval Request Expired: {request.title}",
                        message=f"The approval request has expired without a decision.\n\n{request.description}",
                        notification_type=NotificationType.WARNING,
                        priority=NotificationPriority.MEDIUM,
                        user_id=request.user_id,
                        related_entity_id=request.id,
                        related_entity_type="approval_request"
                    )

                    # Call the callback if provided
                    if request.callback:
                        try:
                            request.callback(request.id, request.status, "Request expired without a decision")
                        except Exception as e:
                            logger.error(f"Error in approval callback for expired request {request.id}: {e}")

                    logger.info(f"Marked approval request {request.id} as expired")

    def add_delegate(self, delegate: ApprovalDelegate) -> None:
        """
        Add a delegate for a user.

        Args:
            delegate: The delegate to add
        """
        if delegate.user_id not in self.delegates:
            self.delegates[delegate.user_id] = []

        self.delegates[delegate.user_id].append(delegate)
        logger.info(f"Added delegate {delegate.delegate_id} for user {delegate.user_id}")

    def remove_delegate(self, delegate_id: str) -> bool:
        """
        Remove a delegate.

        Args:
            delegate_id: The ID of the delegate to remove

        Returns:
            bool: True if the delegate was found and removed, False otherwise
        """
        for user_id, delegates in self.delegates.items():
            for i, delegate in enumerate(delegates):
                if delegate.id == delegate_id:
                    delegates.pop(i)
                    logger.info(f"Removed delegate {delegate.delegate_id} for user {user_id}")
                    return True

        logger.warning(f"Delegate not found: {delegate_id}")
        return False

    def _get_delegates(self, user_id: str, category: DecisionCategory, risk_level: RiskLevel) -> List[ApprovalDelegate]:
        """
        Get all delegates who can approve a request with the given category and risk level.

        Args:
            user_id: The ID of the user
            category: The decision category
            risk_level: The risk level

        Returns:
            List[ApprovalDelegate]: The list of delegates
        """
        if user_id not in self.delegates:
            return []

        return [d for d in self.delegates[user_id] if d.can_approve(category, risk_level)]

    def _is_delegate(self, delegate_id: str, user_id: str, category: DecisionCategory, risk_level: RiskLevel) -> bool:
        """
        Check if a user is a delegate for another user for a specific category and risk level.

        Args:
            delegate_id: The ID of the potential delegate
            user_id: The ID of the user
            category: The decision category
            risk_level: The risk level

        Returns:
            bool: True if the user is a delegate, False otherwise
        """
        delegates = self._get_delegates(user_id, category, risk_level)
        return any(d.delegate_id == delegate_id for d in delegates)

    def add_approval_template(self, template_id: str, template: Dict[str, Any]) -> None:
        """
        Add an approval request template.

        Args:
            template_id: The ID of the template
            template: The template data
        """
        self.approval_templates[template_id] = template
        logger.info(f"Added approval template: {template_id}")

    def get_approval_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        """
        Get an approval request template.

        Args:
            template_id: The ID of the template

        Returns:
            Optional[Dict[str, Any]]: The template data, or None if not found
        """
        return self.approval_templates.get(template_id)

    def get_pending_count(self) -> int:
        """
        Get the number of pending approval requests.

        Returns:
            int: The number of pending approval requests
        """
        return sum(1 for r in self.approval_requests if r.status == ApprovalStatus.PENDING)

    def get_pending_requests(self, user_id: Optional[str] = None) -> List[ApprovalRequest]:
        """
        Get all pending approval requests for a user.

        Args:
            user_id: The ID of the user to get requests for (if None, get all)

        Returns:
            List[ApprovalRequest]: The list of pending approval requests
        """
        if user_id is None:
            return [r for r in self.approval_requests if r.status == ApprovalStatus.PENDING]

        # Include requests where the user is the owner or a delegate
        result = []
        for request in self.approval_requests:
            if request.status != ApprovalStatus.PENDING:
                continue

            if request.user_id == user_id:
                result.append(request)
                continue

            # Check if the user is a delegate for this request
            risk_level = request.context.get("risk_level", RiskLevel.MEDIUM)
            if self._is_delegate(user_id, request.user_id, request.category, risk_level):
                result.append(request)

        return result

class DecisionMatrix:
    """
    Decision matrix for determining approval levels based on decision categories and risk levels.
    """

    def __init__(self):
        """Initialize the decision matrix with default values."""
        # Default decision matrix based on the risk tolerance framework
        self.matrix = {
            # Format: {DecisionCategory: {RiskLevel: ApprovalLevel}}
            DecisionCategory.EXPERIMENT_MANAGEMENT: {
                RiskLevel.LOW: ApprovalLevel.AUTONOMOUS,
                RiskLevel.MEDIUM: ApprovalLevel.NOTIFY,
                RiskLevel.HIGH: ApprovalLevel.APPROVAL_REQUIRED,
                RiskLevel.CRITICAL: ApprovalLevel.PROHIBITED
            },
            DecisionCategory.CONTENT_CREATION: {
                RiskLevel.LOW: ApprovalLevel.AUTONOMOUS,
                RiskLevel.MEDIUM: ApprovalLevel.NOTIFY,
                RiskLevel.HIGH: ApprovalLevel.APPROVAL_REQUIRED,
                RiskLevel.CRITICAL: ApprovalLevel.PROHIBITED
            },
            DecisionCategory.FINANCIAL: {
                RiskLevel.LOW: ApprovalLevel.NOTIFY,
                RiskLevel.MEDIUM: ApprovalLevel.APPROVAL_REQUIRED,
                RiskLevel.HIGH: ApprovalLevel.APPROVAL_REQUIRED,
                RiskLevel.CRITICAL: ApprovalLevel.PROHIBITED
            },
            DecisionCategory.PLATFORM_INTERACTION: {
                RiskLevel.LOW: ApprovalLevel.AUTONOMOUS,
                RiskLevel.MEDIUM: ApprovalLevel.NOTIFY,
                RiskLevel.HIGH: ApprovalLevel.APPROVAL_REQUIRED,
                RiskLevel.CRITICAL: ApprovalLevel.PROHIBITED
            },
            DecisionCategory.SYSTEM: {
                RiskLevel.LOW: ApprovalLevel.AUTONOMOUS,
                RiskLevel.MEDIUM: ApprovalLevel.NOTIFY,
                RiskLevel.HIGH: ApprovalLevel.APPROVAL_REQUIRED,
                RiskLevel.CRITICAL: ApprovalLevel.PROHIBITED
            },
            DecisionCategory.RESOURCE_ALLOCATION: {
                RiskLevel.LOW: ApprovalLevel.AUTONOMOUS,  # <10% change
                RiskLevel.MEDIUM: ApprovalLevel.NOTIFY,   # 10-25% change
                RiskLevel.HIGH: ApprovalLevel.APPROVAL_REQUIRED,  # >25% change
                RiskLevel.CRITICAL: ApprovalLevel.PROHIBITED
            },
            DecisionCategory.STRATEGY_ADJUSTMENT: {
                RiskLevel.LOW: ApprovalLevel.AUTONOMOUS,  # Tactical optimizations
                RiskLevel.MEDIUM: ApprovalLevel.NOTIFY,   # Secondary strategy shifts
                RiskLevel.HIGH: ApprovalLevel.APPROVAL_REQUIRED,  # Primary strategy changes
                RiskLevel.CRITICAL: ApprovalLevel.PROHIBITED
            },
            DecisionCategory.NEW_OPPORTUNITY: {
                RiskLevel.LOW: ApprovalLevel.AUTONOMOUS,  # Research and analysis
                RiskLevel.MEDIUM: ApprovalLevel.NOTIFY,   # Small-scale testing
                RiskLevel.HIGH: ApprovalLevel.APPROVAL_REQUIRED,  # Significant resource commitment
                RiskLevel.CRITICAL: ApprovalLevel.PROHIBITED
            },
            DecisionCategory.PLATFORM_EXPANSION: {
                RiskLevel.LOW: ApprovalLevel.AUTONOMOUS,  # Additional content on existing platforms
                RiskLevel.MEDIUM: ApprovalLevel.NOTIFY,   # New features on existing platforms
                RiskLevel.HIGH: ApprovalLevel.APPROVAL_REQUIRED,  # New platform adoption
                RiskLevel.CRITICAL: ApprovalLevel.PROHIBITED
            }
        }

        # Default risk thresholds for different categories
        self.risk_thresholds = {
            # Format: {DecisionCategory: {metric: {threshold: RiskLevel}}}
            DecisionCategory.RESOURCE_ALLOCATION: {
                "change_percentage": {
                    10: RiskLevel.LOW,    # <10% change is low risk
                    25: RiskLevel.MEDIUM, # 10-25% change is medium risk
                    float('inf'): RiskLevel.HIGH  # >25% change is high risk
                }
            },
            # Add more thresholds for other categories as needed
        }

    def get_approval_level(self, category: DecisionCategory, risk_level: RiskLevel) -> ApprovalLevel:
        """
        Get the approval level for a given decision category and risk level.

        Args:
            category: The decision category
            risk_level: The risk level

        Returns:
            ApprovalLevel: The approval level
        """
        if category not in self.matrix:
            # Default to requiring approval for unknown categories
            return ApprovalLevel.APPROVAL_REQUIRED

        if risk_level not in self.matrix[category]:
            # Default to requiring approval for unknown risk levels
            return ApprovalLevel.APPROVAL_REQUIRED

        return self.matrix[category][risk_level]

    def assess_risk_level(self, category: DecisionCategory, metrics: Dict[str, Any]) -> RiskLevel:
        """
        Assess the risk level for a given decision category and metrics.

        Args:
            category: The decision category
            metrics: The metrics to assess risk from

        Returns:
            RiskLevel: The assessed risk level
        """
        if category not in self.risk_thresholds:
            # Default to medium risk for unknown categories
            return RiskLevel.MEDIUM

        category_thresholds = self.risk_thresholds[category]

        # Check each metric against its thresholds
        highest_risk = RiskLevel.LOW  # Start with lowest risk

        for metric, value in metrics.items():
            if metric in category_thresholds:
                metric_thresholds = category_thresholds[metric]

                # Find the appropriate risk level based on thresholds
                for threshold, risk in sorted(metric_thresholds.items()):
                    if value < threshold:
                        # If the value is less than the threshold, assign this risk level
                        if self._risk_level_value(risk) > self._risk_level_value(highest_risk):
                            highest_risk = risk
                        break

        return highest_risk

    def _risk_level_value(self, risk_level: RiskLevel) -> int:
        """
        Convert a risk level to a numeric value for comparison.

        Args:
            risk_level: The risk level

        Returns:
            int: The numeric value
        """
        risk_values = {
            RiskLevel.LOW: 1,
            RiskLevel.MEDIUM: 2,
            RiskLevel.HIGH: 3,
            RiskLevel.CRITICAL: 4
        }
        return risk_values.get(risk_level, 0)

    def update_matrix(self, category: DecisionCategory, risk_level: RiskLevel, approval_level: ApprovalLevel) -> None:
        """
        Update the decision matrix for a specific category and risk level.

        Args:
            category: The decision category
            risk_level: The risk level
            approval_level: The new approval level
        """
        if category not in self.matrix:
            self.matrix[category] = {}

        self.matrix[category][risk_level] = approval_level
        logger.info(f"Updated decision matrix: {category.value} + {risk_level.value} -> {approval_level.value}")

    def update_risk_threshold(self, category: DecisionCategory, metric: str, threshold: float, risk_level: RiskLevel) -> None:
        """
        Update a risk threshold for a specific category and metric.

        Args:
            category: The decision category
            metric: The metric name
            threshold: The threshold value
            risk_level: The risk level for this threshold
        """
        if category not in self.risk_thresholds:
            self.risk_thresholds[category] = {}

        if metric not in self.risk_thresholds[category]:
            self.risk_thresholds[category][metric] = {}

        self.risk_thresholds[category][metric][threshold] = risk_level
        logger.info(f"Updated risk threshold: {category.value}.{metric}[{threshold}] -> {risk_level.value}")


class AutonomyFramework:
    """
    Framework for managing agent autonomy.

    This class ties together the decision matrix, notification system, and approval workflow
    to provide a unified interface for determining when the agent can act autonomously.
    """

    def __init__(self):
        """Initialize the autonomy framework."""
        self.notification_system = NotificationSystem()
        self.approval_workflow = ApprovalWorkflow(self.notification_system)
        self.decision_matrix = DecisionMatrix()
        self.pending_actions = {}  # Dictionary of action ID to pending action info
        self.decision_history = []  # List of past decisions for learning
        self.experimentation_framework = None  # Will be set after initialization to avoid circular imports
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
        # Extract metrics from context for risk assessment
        metrics = context.get("metrics", {})

        # If risk_level is explicitly provided in the context, use it
        if "risk_level" in context:
            risk_level = context["risk_level"]
        else:
            # Assess risk level based on metrics
            risk_level = self.decision_matrix.assess_risk_level(category, metrics)

        # Get approval level based on category and risk level
        approval_level = self.decision_matrix.get_approval_level(category, risk_level)

        # Record the decision in history
        self.decision_history.append({
            "timestamp": int(time.time()),
            "category": category,
            "action": action,
            "context": context,
            "risk_level": risk_level,
            "approval_level": approval_level
        })

        # Determine if the action can be executed based on approval level
        if approval_level == ApprovalLevel.AUTONOMOUS:
            return True, None
        elif approval_level == ApprovalLevel.NOTIFY:
            return True, "Notification required"
        elif approval_level == ApprovalLevel.APPROVAL_REQUIRED:
            return False, f"{category.value} actions with {risk_level.value} risk require approval"
        elif approval_level == ApprovalLevel.PROHIBITED:
            return False, f"{category.value} actions with {risk_level.value} risk are prohibited"
        else:
            return False, "Unknown approval level"

    def get_approval_workflow(self) -> ApprovalWorkflow:
        """
        Get the approval workflow.

        Returns:
            ApprovalWorkflow: The approval workflow
        """
        return self.approval_workflow

    def get_notification_system(self) -> NotificationSystem:
        """
        Get the notification system.

        Returns:
            NotificationSystem: The notification system
        """
        return self.notification_system

    def get_decision_matrix(self) -> DecisionMatrix:
        """
        Get the decision matrix.

        Returns:
            DecisionMatrix: The decision matrix
        """
        return self.decision_matrix

    def update_decision_matrix(self, category: DecisionCategory, risk_level: RiskLevel, approval_level: ApprovalLevel) -> None:
        """
        Update the decision matrix.

        Args:
            category: The decision category
            risk_level: The risk level
            approval_level: The new approval level
        """
        self.decision_matrix.update_matrix(category, risk_level, approval_level)

    def get_recent_decisions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent decisions from the history.

        Args:
            limit: The maximum number of decisions to return

        Returns:
            List[Dict[str, Any]]: The recent decisions
        """
        return self.decision_history[-limit:] if self.decision_history else []

    def set_experimentation_framework(self, experimentation_framework) -> None:
        """
        Set the experimentation framework.

        Args:
            experimentation_framework: The experimentation framework
        """
        self.experimentation_framework = experimentation_framework

    def get_experimentation_framework(self):
        """
        Get the experimentation framework.

        Returns:
            The experimentation framework
        """
        return self.experimentation_framework

    def process_pending_items(self) -> None:
        """Process all pending items such as notifications and approval requests."""
        # Process batched notifications
        self.notification_system.process_batches()

        # Check for expired approval requests
        self.approval_workflow.check_expired_requests()
