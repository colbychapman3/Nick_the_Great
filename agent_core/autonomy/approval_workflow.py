"""
Approval Workflow for the Nick the Great Unified Agent.

This module implements the approval workflow that manages the process of requesting
and receiving approval for agent actions.
"""

import logging
import enum
import time
import uuid
import json
from typing import Dict, Any, List, Optional, Callable, Tuple
from datetime import datetime, timedelta

from .decision_matrix import DecisionCategory, ApprovalLevel
from .notification_system import NotificationSystem, NotificationType, NotificationPriority, NotificationStatus

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ApprovalStatus(enum.Enum):
    """Status of an approval request."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"
    CANCELLED = "cancelled"

class ApprovalRequest:
    """
    Represents a request for approval of an agent action.
    """
    
    def __init__(self, 
                 title: str,
                 description: str,
                 category: DecisionCategory,
                 action: str,
                 context: Dict[str, Any],
                 user_id: Optional[str] = None,
                 expiry_time: Optional[int] = None,
                 callback: Optional[Callable[[str, ApprovalStatus, Dict[str, Any]], None]] = None):
        """
        Initialize a new approval request.
        
        Args:
            title: The title of the approval request
            description: A detailed description of the action requiring approval
            category: The decision category
            action: The specific action
            context: The context in which the action is being performed
            user_id: The ID of the user to request approval from (None for any user)
            expiry_time: Unix timestamp when the approval request expires
            callback: Function to call when the approval status changes
        """
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.category = category
        self.action = action
        self.context = context
        self.user_id = user_id
        self.created_time = int(time.time())
        self.expiry_time = expiry_time
        self.status = ApprovalStatus.PENDING
        self.decision_time = None
        self.decision_user_id = None
        self.decision_reason = None
        self.notification_id = None
        self.callback = callback
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the approval request to a dictionary.
        
        Returns:
            Dict: The approval request as a dictionary
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category.value,
            "action": self.action,
            "context": self.context,
            "user_id": self.user_id,
            "created_time": self.created_time,
            "expiry_time": self.expiry_time,
            "status": self.status.value,
            "decision_time": self.decision_time,
            "decision_user_id": self.decision_user_id,
            "decision_reason": self.decision_reason,
            "notification_id": self.notification_id
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ApprovalRequest':
        """
        Create an approval request from a dictionary.
        
        Args:
            data: The dictionary containing approval request data
        
        Returns:
            ApprovalRequest: The created approval request
        """
        request = cls(
            title=data["title"],
            description=data["description"],
            category=DecisionCategory(data["category"]),
            action=data["action"],
            context=data["context"],
            user_id=data.get("user_id"),
            expiry_time=data.get("expiry_time")
        )
        request.id = data["id"]
        request.created_time = data["created_time"]
        request.status = ApprovalStatus(data["status"])
        request.decision_time = data.get("decision_time")
        request.decision_user_id = data.get("decision_user_id")
        request.decision_reason = data.get("decision_reason")
        request.notification_id = data.get("notification_id")
        return request
    
    def approve(self, user_id: str, reason: Optional[str] = None) -> bool:
        """
        Approve the request.
        
        Args:
            user_id: The ID of the user approving the request
            reason: The reason for approval
        
        Returns:
            bool: True if the approval was successful, False otherwise
        """
        if self.status != ApprovalStatus.PENDING:
            logger.warning(f"Attempted to approve request {self.id} with status {self.status.value}")
            return False
        
        self.status = ApprovalStatus.APPROVED
        self.decision_time = int(time.time())
        self.decision_user_id = user_id
        self.decision_reason = reason
        
        if self.callback:
            try:
                self.callback(self.id, self.status, {
                    "user_id": user_id,
                    "reason": reason
                })
            except Exception as e:
                logger.error(f"Error in approval callback for request {self.id}: {e}")
        
        return True
    
    def reject(self, user_id: str, reason: Optional[str] = None) -> bool:
        """
        Reject the request.
        
        Args:
            user_id: The ID of the user rejecting the request
            reason: The reason for rejection
        
        Returns:
            bool: True if the rejection was successful, False otherwise
        """
        if self.status != ApprovalStatus.PENDING:
            logger.warning(f"Attempted to reject request {self.id} with status {self.status.value}")
            return False
        
        self.status = ApprovalStatus.REJECTED
        self.decision_time = int(time.time())
        self.decision_user_id = user_id
        self.decision_reason = reason
        
        if self.callback:
            try:
                self.callback(self.id, self.status, {
                    "user_id": user_id,
                    "reason": reason
                })
            except Exception as e:
                logger.error(f"Error in rejection callback for request {self.id}: {e}")
        
        return True
    
    def cancel(self) -> bool:
        """
        Cancel the request.
        
        Returns:
            bool: True if the cancellation was successful, False otherwise
        """
        if self.status != ApprovalStatus.PENDING:
            logger.warning(f"Attempted to cancel request {self.id} with status {self.status.value}")
            return False
        
        self.status = ApprovalStatus.CANCELLED
        self.decision_time = int(time.time())
        
        if self.callback:
            try:
                self.callback(self.id, self.status, {})
            except Exception as e:
                logger.error(f"Error in cancellation callback for request {self.id}: {e}")
        
        return True
    
    def is_expired(self) -> bool:
        """
        Check if the approval request has expired.
        
        Returns:
            bool: True if the request has expired, False otherwise
        """
        if self.expiry_time is None:
            return False
        
        return time.time() > self.expiry_time
    
    def mark_as_expired(self) -> bool:
        """
        Mark the request as expired.
        
        Returns:
            bool: True if the operation was successful, False otherwise
        """
        if self.status != ApprovalStatus.PENDING:
            return False
        
        self.status = ApprovalStatus.EXPIRED
        self.decision_time = int(time.time())
        
        if self.callback:
            try:
                self.callback(self.id, self.status, {})
            except Exception as e:
                logger.error(f"Error in expiration callback for request {self.id}: {e}")
        
        return True

class ApprovalWorkflow:
    """
    Workflow for managing approval requests in the agent.
    """
    
    def __init__(self, notification_system: NotificationSystem):
        """
        Initialize the approval workflow.
        
        Args:
            notification_system: The notification system to use for sending approval requests
        """
        self.notification_system = notification_system
        self.approval_requests = {}  # Dictionary of request ID to ApprovalRequest
        logger.info("Approval Workflow initialized")
    
    def create_approval_request(self, 
                               title: str,
                               description: str,
                               category: DecisionCategory,
                               action: str,
                               context: Dict[str, Any],
                               user_id: Optional[str] = None,
                               expiry_hours: int = 24,
                               callback: Optional[Callable[[str, ApprovalStatus, Dict[str, Any]], None]] = None) -> ApprovalRequest:
        """
        Create a new approval request.
        
        Args:
            title: The title of the approval request
            description: A detailed description of the action requiring approval
            category: The decision category
            action: The specific action
            context: The context in which the action is being performed
            user_id: The ID of the user to request approval from (None for any user)
            expiry_hours: Number of hours until the request expires
            callback: Function to call when the approval status changes
        
        Returns:
            ApprovalRequest: The created approval request
        """
        # Calculate expiry time
        expiry_time = int(time.time() + expiry_hours * 3600)
        
        # Create approval request
        request = ApprovalRequest(
            title=title,
            description=description,
            category=category,
            action=action,
            context=context,
            user_id=user_id,
            expiry_time=expiry_time,
            callback=callback
        )
        
        # Store the request
        self.approval_requests[request.id] = request
        
        # Create a notification for the approval request
        notification = self.notification_system.create_notification(
            title=f"Approval Required: {title}",
            message=description,
            notification_type=NotificationType.APPROVAL_REQUEST,
            priority=NotificationPriority.HIGH,
            user_id=user_id,
            related_entity_id=request.id,
            related_entity_type="approval_request",
            action_required=True,
            action_options=["approve", "reject"],
            expiry_time=expiry_time
        )
        
        # Link the notification to the approval request
        request.notification_id = notification.id
        
        logger.info(f"Created approval request {request.id}: {title}")
        return request
    
    def get_approval_request(self, request_id: str) -> Optional[ApprovalRequest]:
        """
        Get an approval request by ID.
        
        Args:
            request_id: The ID of the approval request to get
        
        Returns:
            Optional[ApprovalRequest]: The approval request, or None if not found
        """
        return self.approval_requests.get(request_id)
    
    def get_approval_requests(self, 
                             user_id: Optional[str] = None, 
                             status: Optional[ApprovalStatus] = None,
                             category: Optional[DecisionCategory] = None) -> List[ApprovalRequest]:
        """
        Get approval requests matching the specified filters.
        
        Args:
            user_id: Filter by user ID
            status: Filter by approval status
            category: Filter by decision category
        
        Returns:
            List[ApprovalRequest]: The matching approval requests
        """
        result = []
        
        for request in self.approval_requests.values():
            # Apply filters
            if user_id is not None and request.user_id != user_id:
                continue
            
            if status is not None and request.status != status:
                continue
            
            if category is not None and request.category != category:
                continue
            
            result.append(request)
        
        return result
    
    def approve_request(self, request_id: str, user_id: str, reason: Optional[str] = None) -> bool:
        """
        Approve an approval request.
        
        Args:
            request_id: The ID of the approval request to approve
            user_id: The ID of the user approving the request
            reason: The reason for approval
        
        Returns:
            bool: True if the approval was successful, False otherwise
        """
        request = self.get_approval_request(request_id)
        if not request:
            logger.warning(f"Attempted to approve non-existent request: {request_id}")
            return False
        
        # Update the notification if it exists
        if request.notification_id:
            notification = self.notification_system.get_notification(request.notification_id)
            if notification:
                notification.take_action("approve")
        
        return request.approve(user_id, reason)
    
    def reject_request(self, request_id: str, user_id: str, reason: Optional[str] = None) -> bool:
        """
        Reject an approval request.
        
        Args:
            request_id: The ID of the approval request to reject
            user_id: The ID of the user rejecting the request
            reason: The reason for rejection
        
        Returns:
            bool: True if the rejection was successful, False otherwise
        """
        request = self.get_approval_request(request_id)
        if not request:
            logger.warning(f"Attempted to reject non-existent request: {request_id}")
            return False
        
        # Update the notification if it exists
        if request.notification_id:
            notification = self.notification_system.get_notification(request.notification_id)
            if notification:
                notification.take_action("reject")
        
        return request.reject(user_id, reason)
