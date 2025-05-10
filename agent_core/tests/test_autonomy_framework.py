"""
Unit tests for the Autonomy Framework.
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
    ApprovalStatus,
    NotificationType,
    NotificationPriority,
    Notification,
    ApprovalRequest,
    NotificationSystem,
    ApprovalWorkflow
)

class TestAutonomyFramework:
    """Test the Autonomy Framework."""

    def setup_method(self):
        """Set up the test environment."""
        self.autonomy_framework = AutonomyFramework()

    def test_init(self):
        """Test the initialization of the autonomy framework."""
        assert self.autonomy_framework.notification_system is not None
        assert self.autonomy_framework.approval_workflow is not None
        assert self.autonomy_framework.pending_actions == {}

    def test_can_execute_experiment_management(self):
        """Test the can_execute method for experiment management actions."""
        # Arrange
        category = DecisionCategory.EXPERIMENT_MANAGEMENT
        action = "create_experiment"
        context = {"experiment_type": "AI_DRIVEN_EBOOKS"}

        # Act
        can_execute, reason = self.autonomy_framework.can_execute(category, action, context)

        # Assert
        assert can_execute is True
        assert reason is None

    def test_can_execute_financial(self):
        """Test the can_execute method for financial actions."""
        # Arrange
        category = DecisionCategory.FINANCIAL
        action = "make_payment"
        context = {"amount": 100.0, "recipient": "Test Recipient"}

        # Act
        can_execute, reason = self.autonomy_framework.can_execute(category, action, context)

        # Assert
        assert can_execute is False
        assert reason == "Financial actions require approval"

    def test_can_execute_content_creation(self):
        """Test the can_execute method for content creation actions."""
        # Arrange
        category = DecisionCategory.CONTENT_CREATION
        action = "generate_content"
        context = {"content_type": "article", "topic": "Test Topic"}

        # Act
        can_execute, reason = self.autonomy_framework.can_execute(category, action, context)

        # Assert
        assert can_execute is True
        assert reason == "Notification required"

    def test_can_execute_platform_interaction(self):
        """Test the can_execute method for platform interaction actions."""
        # Arrange
        category = DecisionCategory.PLATFORM_INTERACTION
        action = "post_to_platform"
        context = {"platform": "Pinterest", "content_id": "123"}

        # Act
        can_execute, reason = self.autonomy_framework.can_execute(category, action, context)

        # Assert
        assert can_execute is True
        assert reason == "Notification required"

    def test_can_execute_system(self):
        """Test the can_execute method for system actions."""
        # Arrange
        category = DecisionCategory.SYSTEM
        action = "restart_service"
        context = {"service_name": "agent_core"}

        # Act
        can_execute, reason = self.autonomy_framework.can_execute(category, action, context)

        # Assert
        assert can_execute is True
        assert reason is None

    def test_can_execute_unknown(self):
        """Test the can_execute method for unknown actions."""
        # Arrange
        category = MagicMock()  # Not a valid DecisionCategory
        action = "unknown_action"
        context = {}

        # Act
        can_execute, reason = self.autonomy_framework.can_execute(category, action, context)

        # Assert
        assert can_execute is False
        assert reason == "Unknown action category requires approval"

    def test_get_approval_workflow(self):
        """Test the get_approval_workflow method."""
        # Act
        workflow = self.autonomy_framework.get_approval_workflow()

        # Assert
        assert workflow is self.autonomy_framework.approval_workflow


class TestNotificationSystem:
    """Test the Notification System."""

    def setup_method(self):
        """Set up the test environment."""
        self.notification_system = NotificationSystem()

    def test_init(self):
        """Test the initialization of the notification system."""
        assert self.notification_system.notifications == []

    def test_create_notification(self):
        """Test creating a notification."""
        # Arrange
        title = "Test Notification"
        message = "This is a test notification"
        notification_type = NotificationType.INFO
        priority = NotificationPriority.MEDIUM
        user_id = "test_user"

        # Act
        notification = self.notification_system.create_notification(
            title, message, notification_type, priority, user_id
        )

        # Assert
        assert notification is not None
        assert notification.title == title
        assert notification.message == message
        assert notification.notification_type == notification_type
        assert notification.priority == priority
        assert notification.user_id == user_id
        assert notification.read is False
        assert notification in self.notification_system.notifications

    def test_get_notifications_all(self):
        """Test getting all notifications."""
        # Arrange
        self.notification_system.create_notification(
            "Notification 1", "Message 1", NotificationType.INFO, NotificationPriority.LOW, "user1"
        )
        self.notification_system.create_notification(
            "Notification 2", "Message 2", NotificationType.WARNING, NotificationPriority.MEDIUM, "user2"
        )

        # Act
        notifications = self.notification_system.get_notifications()

        # Assert
        assert len(notifications) == 2

    def test_get_notifications_by_user(self):
        """Test getting notifications for a specific user."""
        # Arrange
        self.notification_system.create_notification(
            "Notification 1", "Message 1", NotificationType.INFO, NotificationPriority.LOW, "user1"
        )
        self.notification_system.create_notification(
            "Notification 2", "Message 2", NotificationType.WARNING, NotificationPriority.MEDIUM, "user2"
        )
        self.notification_system.create_notification(
            "Notification 3", "Message 3", NotificationType.ERROR, NotificationPriority.HIGH, "user1"
        )

        # Act
        notifications = self.notification_system.get_notifications("user1")

        # Assert
        assert len(notifications) == 2
        assert all(n.user_id == "user1" for n in notifications)


class TestApprovalWorkflow:
    """Test the Approval Workflow."""

    def setup_method(self):
        """Set up the test environment."""
        self.notification_system = NotificationSystem()
        self.approval_workflow = ApprovalWorkflow(self.notification_system)

    def test_init(self):
        """Test the initialization of the approval workflow."""
        assert self.approval_workflow.notification_system is self.notification_system
        assert self.approval_workflow.approval_requests == []

    def test_create_approval_request(self):
        """Test creating an approval request."""
        # Arrange
        title = "Test Approval"
        description = "This is a test approval request"
        category = DecisionCategory.FINANCIAL
        action = "make_payment"
        context = {"amount": 100.0, "recipient": "Test Recipient"}
        user_id = "test_user"
        callback = MagicMock()

        # Act
        request = self.approval_workflow.create_approval_request(
            title, description, category, action, context, user_id, callback
        )

        # Assert
        assert request is not None
        assert request.title == title
        assert request.description == description
        assert request.category == category
        assert request.action == action
        assert request.context == context
        assert request.user_id == user_id
        assert request.callback == callback
        assert request.status == ApprovalStatus.PENDING
        assert request in self.approval_workflow.approval_requests

        # Verify a notification was created
        notifications = self.notification_system.get_notifications(user_id)
        assert len(notifications) == 1
        assert "Approval Required" in notifications[0].title
        assert description in notifications[0].message

    def test_process_approval_approved(self):
        """Test processing an approval request with approval."""
        # Arrange
        request = self.approval_workflow.create_approval_request(
            "Test Approval",
            "This is a test approval request",
            DecisionCategory.FINANCIAL,
            "make_payment",
            {"amount": 100.0, "recipient": "Test Recipient"},
            "test_user",
            MagicMock()
        )

        # Act
        result = self.approval_workflow.process_approval(request.id, True, "Approved by test")

        # Assert
        assert result is True
        assert request.status == ApprovalStatus.APPROVED
        assert request.response_details == "Approved by test"

        # Verify the callback was called
        request.callback.assert_called_once_with(request.id, ApprovalStatus.APPROVED, "Approved by test")

        # Verify a notification was created
        notifications = self.notification_system.get_notifications("test_user")
        assert len(notifications) == 2  # Initial request notification + approval notification
        assert "Approval Granted" in notifications[1].title

    def test_process_approval_rejected(self):
        """Test processing an approval request with rejection."""
        # Arrange
        request = self.approval_workflow.create_approval_request(
            "Test Approval",
            "This is a test approval request",
            DecisionCategory.FINANCIAL,
            "make_payment",
            {"amount": 100.0, "recipient": "Test Recipient"},
            "test_user",
            MagicMock()
        )

        # Act
        result = self.approval_workflow.process_approval(request.id, False, "Rejected by test")

        # Assert
        assert result is True
        assert request.status == ApprovalStatus.REJECTED
        assert request.response_details == "Rejected by test"

        # Verify the callback was called
        request.callback.assert_called_once_with(request.id, ApprovalStatus.REJECTED, "Rejected by test")

        # Verify a notification was created
        notifications = self.notification_system.get_notifications("test_user")
        assert len(notifications) == 2  # Initial request notification + rejection notification
        assert "Approval Rejected" in notifications[1].title

    def test_process_approval_not_found(self):
        """Test processing a non-existent approval request."""
        # Act
        result = self.approval_workflow.process_approval("non-existent-id", True, "Approved by test")

        # Assert
        assert result is False

    def test_process_approval_already_processed(self):
        """Test processing an already processed approval request."""
        # Arrange
        request = self.approval_workflow.create_approval_request(
            "Test Approval",
            "This is a test approval request",
            DecisionCategory.FINANCIAL,
            "make_payment",
            {"amount": 100.0, "recipient": "Test Recipient"},
            "test_user"
        )

        # Process the request once
        self.approval_workflow.process_approval(request.id, True, "Approved by test")

        # Act - Try to process it again
        result = self.approval_workflow.process_approval(request.id, False, "Rejected by test")

        # Assert
        assert result is False
        assert request.status == ApprovalStatus.APPROVED  # Status should not change

    def test_get_pending_count(self):
        """Test getting the count of pending approval requests."""
        # Arrange
        # Create some approval requests
        self.approval_workflow.create_approval_request(
            "Test Approval 1",
            "This is a test approval request",
            DecisionCategory.FINANCIAL,
            "make_payment",
            {"amount": 100.0, "recipient": "Test Recipient"},
            "test_user"
        )

        request2 = self.approval_workflow.create_approval_request(
            "Test Approval 2",
            "This is another test approval request",
            DecisionCategory.FINANCIAL,
            "make_payment",
            {"amount": 200.0, "recipient": "Another Recipient"},
            "test_user"
        )

        self.approval_workflow.create_approval_request(
            "Test Approval 3",
            "This is a third test approval request",
            DecisionCategory.FINANCIAL,
            "make_payment",
            {"amount": 300.0, "recipient": "Third Recipient"},
            "test_user"
        )

        # Process one of the requests
        self.approval_workflow.process_approval(request2.id, True, "Approved by test")

        # Act
        pending_count = self.approval_workflow.get_pending_count()

        # Assert
        assert pending_count == 2
