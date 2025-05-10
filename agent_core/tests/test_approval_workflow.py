"""
Unit tests for the Approval Workflow.
"""

import os
import sys
import pytest
import time
from unittest.mock import MagicMock, patch

# Add the parent directory to the path so we can import the agent_core modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the modules to test
from autonomy_framework import (
    ApprovalWorkflow,
    ApprovalStatus,
    ApprovalRequest,
    NotificationSystem,
    NotificationType,
    NotificationPriority,
    DecisionCategory
)

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
            title=title,
            description=description,
            category=category,
            action=action,
            context=context,
            user_id=user_id,
            callback=callback
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
        assert request.created_time is not None
        assert request.response_time is None
        assert request.response_details is None
        assert request in self.approval_workflow.approval_requests
        
        # Verify a notification was created
        notifications = self.notification_system.get_notifications(user_id=user_id)
        assert len(notifications) == 1
        assert "Approval Required" in notifications[0].title
        assert description in notifications[0].message
        assert notifications[0].notification_type == NotificationType.REQUEST
        assert notifications[0].priority == NotificationPriority.HIGH
        assert notifications[0].related_entity_id == request.id
        assert notifications[0].related_entity_type == f"{category.value}_{action}"
    
    def test_create_approval_request_minimal(self):
        """Test creating an approval request with minimal parameters."""
        # Arrange
        title = "Test Approval"
        description = "This is a test approval request"
        category = DecisionCategory.FINANCIAL
        action = "make_payment"
        context = {"amount": 100.0, "recipient": "Test Recipient"}
        
        # Act
        request = self.approval_workflow.create_approval_request(
            title=title,
            description=description,
            category=category,
            action=action,
            context=context
        )
        
        # Assert
        assert request is not None
        assert request.title == title
        assert request.description == description
        assert request.category == category
        assert request.action == action
        assert request.context == context
        assert request.user_id is None
        assert request.callback is None
        assert request.status == ApprovalStatus.PENDING
        assert request in self.approval_workflow.approval_requests
        
        # Verify a notification was created (system-wide since no user_id)
        notifications = self.notification_system.get_notifications()
        assert len(notifications) == 1
        assert "Approval Required" in notifications[0].title
        assert description in notifications[0].message
    
    def test_get_approval_request(self):
        """Test getting an approval request by ID."""
        # Arrange
        request = self.approval_workflow.create_approval_request(
            title="Test Approval",
            description="This is a test approval request",
            category=DecisionCategory.FINANCIAL,
            action="make_payment",
            context={"amount": 100.0, "recipient": "Test Recipient"}
        )
        
        # Act
        retrieved_request = self.approval_workflow.get_approval_request(request.id)
        
        # Assert
        assert retrieved_request is request
    
    def test_get_approval_request_not_found(self):
        """Test getting a non-existent approval request."""
        # Act
        retrieved_request = self.approval_workflow.get_approval_request("non-existent-id")
        
        # Assert
        assert retrieved_request is None
    
    def test_get_approval_requests(self):
        """Test getting all approval requests."""
        # Arrange
        request1 = self.approval_workflow.create_approval_request(
            title="Test Approval 1",
            description="This is a test approval request",
            category=DecisionCategory.FINANCIAL,
            action="make_payment",
            context={"amount": 100.0, "recipient": "Test Recipient"},
            user_id="user1"
        )
        request2 = self.approval_workflow.create_approval_request(
            title="Test Approval 2",
            description="This is another test approval request",
            category=DecisionCategory.CONTENT_CREATION,
            action="publish_content",
            context={"content_id": "123"},
            user_id="user2"
        )
        
        # Act
        requests = self.approval_workflow.get_approval_requests()
        
        # Assert
        assert len(requests) == 2
        assert request1 in requests
        assert request2 in requests
    
    def test_get_approval_requests_by_user(self):
        """Test getting approval requests for a specific user."""
        # Arrange
        request1 = self.approval_workflow.create_approval_request(
            title="Test Approval 1",
            description="This is a test approval request",
            category=DecisionCategory.FINANCIAL,
            action="make_payment",
            context={"amount": 100.0, "recipient": "Test Recipient"},
            user_id="user1"
        )
        request2 = self.approval_workflow.create_approval_request(
            title="Test Approval 2",
            description="This is another test approval request",
            category=DecisionCategory.CONTENT_CREATION,
            action="publish_content",
            context={"content_id": "123"},
            user_id="user2"
        )
        request3 = self.approval_workflow.create_approval_request(
            title="Test Approval 3",
            description="This is a third test approval request",
            category=DecisionCategory.FINANCIAL,
            action="allocate_budget",
            context={"amount": 200.0, "project": "Test Project"},
            user_id="user1"
        )
        
        # Act
        requests = self.approval_workflow.get_approval_requests(user_id="user1")
        
        # Assert
        assert len(requests) == 2
        assert all(r.user_id == "user1" for r in requests)
        assert request1 in requests
        assert request3 in requests
    
    def test_get_approval_requests_by_status(self):
        """Test getting approval requests by status."""
        # Arrange
        request1 = self.approval_workflow.create_approval_request(
            title="Test Approval 1",
            description="This is a test approval request",
            category=DecisionCategory.FINANCIAL,
            action="make_payment",
            context={"amount": 100.0, "recipient": "Test Recipient"}
        )
        request2 = self.approval_workflow.create_approval_request(
            title="Test Approval 2",
            description="This is another test approval request",
            category=DecisionCategory.CONTENT_CREATION,
            action="publish_content",
            context={"content_id": "123"}
        )
        
        # Process one request
        self.approval_workflow.process_approval(request1.id, True, "Approved for testing")
        
        # Act
        pending_requests = self.approval_workflow.get_approval_requests(status=ApprovalStatus.PENDING)
        approved_requests = self.approval_workflow.get_approval_requests(status=ApprovalStatus.APPROVED)
        
        # Assert
        assert len(pending_requests) == 1
        assert pending_requests[0] is request2
        assert len(approved_requests) == 1
        assert approved_requests[0] is request1
    
    def test_process_approval_approved(self):
        """Test processing an approval request with approval."""
        # Arrange
        callback = MagicMock()
        request = self.approval_workflow.create_approval_request(
            title="Test Approval",
            description="This is a test approval request",
            category=DecisionCategory.FINANCIAL,
            action="make_payment",
            context={"amount": 100.0, "recipient": "Test Recipient"},
            user_id="test_user",
            callback=callback
        )
        
        # Act
        result = self.approval_workflow.process_approval(request.id, True, "Approved for testing")
        
        # Assert
        assert result is True
        assert request.status == ApprovalStatus.APPROVED
        assert request.response_details == "Approved for testing"
        assert request.response_time is not None
        
        # Verify the callback was called
        callback.assert_called_once_with(request.id, ApprovalStatus.APPROVED, "Approved for testing")
        
        # Verify a notification was created
        notifications = self.notification_system.get_notifications(user_id="test_user")
        assert len(notifications) == 2  # Initial request notification + approval notification
        assert "Approval Granted" in notifications[1].title
        assert notifications[1].notification_type == NotificationType.INFO
        assert notifications[1].priority == NotificationPriority.HIGH
    
    def test_process_approval_rejected(self):
        """Test processing an approval request with rejection."""
        # Arrange
        callback = MagicMock()
        request = self.approval_workflow.create_approval_request(
            title="Test Approval",
            description="This is a test approval request",
            category=DecisionCategory.FINANCIAL,
            action="make_payment",
            context={"amount": 100.0, "recipient": "Test Recipient"},
            user_id="test_user",
            callback=callback
        )
        
        # Act
        result = self.approval_workflow.process_approval(request.id, False, "Rejected for testing")
        
        # Assert
        assert result is True
        assert request.status == ApprovalStatus.REJECTED
        assert request.response_details == "Rejected for testing"
        assert request.response_time is not None
        
        # Verify the callback was called
        callback.assert_called_once_with(request.id, ApprovalStatus.REJECTED, "Rejected for testing")
        
        # Verify a notification was created
        notifications = self.notification_system.get_notifications(user_id="test_user")
        assert len(notifications) == 2  # Initial request notification + rejection notification
        assert "Approval Rejected" in notifications[1].title
        assert notifications[1].notification_type == NotificationType.INFO
        assert notifications[1].priority == NotificationPriority.HIGH
    
    def test_process_approval_not_found(self):
        """Test processing a non-existent approval request."""
        # Act
        result = self.approval_workflow.process_approval("non-existent-id", True, "Approved for testing")
        
        # Assert
        assert result is False
    
    def test_process_approval_already_processed(self):
        """Test processing an already processed approval request."""
        # Arrange
        request = self.approval_workflow.create_approval_request(
            title="Test Approval",
            description="This is a test approval request",
            category=DecisionCategory.FINANCIAL,
            action="make_payment",
            context={"amount": 100.0, "recipient": "Test Recipient"}
        )
        
        # Process the request once
        self.approval_workflow.process_approval(request.id, True, "Approved for testing")
        
        # Act - Try to process it again
        result = self.approval_workflow.process_approval(request.id, False, "Rejected for testing")
        
        # Assert
        assert result is False
        assert request.status == ApprovalStatus.APPROVED  # Status should not change
    
    def test_get_pending_count(self):
        """Test getting the count of pending approval requests."""
        # Arrange
        # Create some approval requests
        request1 = self.approval_workflow.create_approval_request(
            title="Test Approval 1",
            description="This is a test approval request",
            category=DecisionCategory.FINANCIAL,
            action="make_payment",
            context={"amount": 100.0, "recipient": "Test Recipient"}
        )
        
        request2 = self.approval_workflow.create_approval_request(
            title="Test Approval 2",
            description="This is another test approval request",
            category=DecisionCategory.CONTENT_CREATION,
            action="publish_content",
            context={"content_id": "123"}
        )
        
        request3 = self.approval_workflow.create_approval_request(
            title="Test Approval 3",
            description="This is a third test approval request",
            category=DecisionCategory.FINANCIAL,
            action="allocate_budget",
            context={"amount": 200.0, "project": "Test Project"}
        )
        
        # Process one of the requests
        self.approval_workflow.process_approval(request2.id, True, "Approved for testing")
        
        # Act
        pending_count = self.approval_workflow.get_pending_count()
        
        # Assert
        assert pending_count == 2
