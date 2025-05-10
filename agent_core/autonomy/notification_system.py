"""
Notification System for the Nick the Great Unified Agent.

This module implements the notification system that sends notifications to users
about agent activities and decisions that require approval.
"""

import logging
import enum
import time
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NotificationType(enum.Enum):
    """Types of notifications that the agent can send."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    APPROVAL_REQUEST = "approval_request"
    STATUS_UPDATE = "status_update"

class NotificationPriority(enum.Enum):
    """Priority levels for notifications."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class NotificationStatus(enum.Enum):
    """Status of a notification."""
    PENDING = "pending"
    DELIVERED = "delivered"
    READ = "read"
    ACTIONED = "actioned"
    EXPIRED = "expired"

class Notification:
    """
    Represents a notification sent by the agent to a user.
    """
    
    def __init__(self, 
                 title: str, 
                 message: str, 
                 notification_type: NotificationType, 
                 priority: NotificationPriority = NotificationPriority.MEDIUM,
                 user_id: Optional[str] = None,
                 related_entity_id: Optional[str] = None,
                 related_entity_type: Optional[str] = None,
                 action_required: bool = False,
                 action_options: Optional[List[str]] = None,
                 expiry_time: Optional[int] = None):
        """
        Initialize a new notification.
        
        Args:
            title: The notification title
            message: The notification message
            notification_type: The type of notification
            priority: The priority level of the notification
            user_id: The ID of the user to notify (None for all users)
            related_entity_id: The ID of the entity related to this notification
            related_entity_type: The type of entity related to this notification
            action_required: Whether the notification requires user action
            action_options: List of possible actions the user can take
            expiry_time: Unix timestamp when the notification expires
        """
        self.id = str(uuid.uuid4())
        self.title = title
        self.message = message
        self.notification_type = notification_type
        self.priority = priority
        self.user_id = user_id
        self.related_entity_id = related_entity_id
        self.related_entity_type = related_entity_type
        self.action_required = action_required
        self.action_options = action_options or []
        self.created_time = int(time.time())
        self.expiry_time = expiry_time
        self.status = NotificationStatus.PENDING
        self.read_time = None
        self.action_taken = None
        self.action_time = None
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the notification to a dictionary.
        
        Returns:
            Dict: The notification as a dictionary
        """
        return {
            "id": self.id,
            "title": self.title,
            "message": self.message,
            "type": self.notification_type.value,
            "priority": self.priority.value,
            "user_id": self.user_id,
            "related_entity_id": self.related_entity_id,
            "related_entity_type": self.related_entity_type,
            "action_required": self.action_required,
            "action_options": self.action_options,
            "created_time": self.created_time,
            "expiry_time": self.expiry_time,
            "status": self.status.value,
            "read_time": self.read_time,
            "action_taken": self.action_taken,
            "action_time": self.action_time
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Notification':
        """
        Create a notification from a dictionary.
        
        Args:
            data: The dictionary containing notification data
        
        Returns:
            Notification: The created notification
        """
        notification = cls(
            title=data["title"],
            message=data["message"],
            notification_type=NotificationType(data["type"]),
            priority=NotificationPriority(data["priority"]),
            user_id=data.get("user_id"),
            related_entity_id=data.get("related_entity_id"),
            related_entity_type=data.get("related_entity_type"),
            action_required=data.get("action_required", False),
            action_options=data.get("action_options", []),
            expiry_time=data.get("expiry_time")
        )
        notification.id = data["id"]
        notification.created_time = data["created_time"]
        notification.status = NotificationStatus(data["status"])
        notification.read_time = data.get("read_time")
        notification.action_taken = data.get("action_taken")
        notification.action_time = data.get("action_time")
        return notification
    
    def mark_as_read(self) -> None:
        """Mark the notification as read."""
        self.status = NotificationStatus.READ
        self.read_time = int(time.time())
    
    def take_action(self, action: str) -> bool:
        """
        Take an action on the notification.
        
        Args:
            action: The action to take
        
        Returns:
            bool: True if the action was valid, False otherwise
        """
        if not self.action_required:
            logger.warning(f"Attempted to take action on notification {self.id} that doesn't require action")
            return False
        
        if self.status == NotificationStatus.EXPIRED:
            logger.warning(f"Attempted to take action on expired notification {self.id}")
            return False
        
        if self.action_options and action not in self.action_options:
            logger.warning(f"Invalid action '{action}' for notification {self.id}")
            return False
        
        self.action_taken = action
        self.action_time = int(time.time())
        self.status = NotificationStatus.ACTIONED
        return True
    
    def is_expired(self) -> bool:
        """
        Check if the notification has expired.
        
        Returns:
            bool: True if the notification has expired, False otherwise
        """
        if self.expiry_time is None:
            return False
        
        return time.time() > self.expiry_time

class NotificationSystem:
    """
    System for managing notifications in the agent.
    """
    
    def __init__(self):
        """Initialize the notification system."""
        self.notifications = {}  # Dictionary of notification ID to Notification
        logger.info("Notification System initialized")
    
    def create_notification(self, 
                           title: str, 
                           message: str, 
                           notification_type: NotificationType, 
                           priority: NotificationPriority = NotificationPriority.MEDIUM,
                           user_id: Optional[str] = None,
                           related_entity_id: Optional[str] = None,
                           related_entity_type: Optional[str] = None,
                           action_required: bool = False,
                           action_options: Optional[List[str]] = None,
                           expiry_time: Optional[int] = None) -> Notification:
        """
        Create a new notification.
        
        Args:
            title: The notification title
            message: The notification message
            notification_type: The type of notification
            priority: The priority level of the notification
            user_id: The ID of the user to notify (None for all users)
            related_entity_id: The ID of the entity related to this notification
            related_entity_type: The type of entity related to this notification
            action_required: Whether the notification requires user action
            action_options: List of possible actions the user can take
            expiry_time: Unix timestamp when the notification expires
        
        Returns:
            Notification: The created notification
        """
        notification = Notification(
            title=title,
            message=message,
            notification_type=notification_type,
            priority=priority,
            user_id=user_id,
            related_entity_id=related_entity_id,
            related_entity_type=related_entity_type,
            action_required=action_required,
            action_options=action_options,
            expiry_time=expiry_time
        )
        
        self.notifications[notification.id] = notification
        logger.info(f"Created notification {notification.id}: {title}")
        
        # TODO: Send notification to backend for delivery to users
        
        return notification
    
    def get_notification(self, notification_id: str) -> Optional[Notification]:
        """
        Get a notification by ID.
        
        Args:
            notification_id: The ID of the notification to get
        
        Returns:
            Optional[Notification]: The notification, or None if not found
        """
        return self.notifications.get(notification_id)
    
    def get_notifications(self, 
                         user_id: Optional[str] = None, 
                         status: Optional[NotificationStatus] = None,
                         notification_type: Optional[NotificationType] = None,
                         related_entity_id: Optional[str] = None,
                         related_entity_type: Optional[str] = None,
                         action_required: Optional[bool] = None) -> List[Notification]:
        """
        Get notifications matching the specified filters.
        
        Args:
            user_id: Filter by user ID
            status: Filter by notification status
            notification_type: Filter by notification type
            related_entity_id: Filter by related entity ID
            related_entity_type: Filter by related entity type
            action_required: Filter by whether action is required
        
        Returns:
            List[Notification]: The matching notifications
        """
        result = []
        
        for notification in self.notifications.values():
            # Apply filters
            if user_id is not None and notification.user_id != user_id:
                continue
            
            if status is not None and notification.status != status:
                continue
            
            if notification_type is not None and notification.notification_type != notification_type:
                continue
            
            if related_entity_id is not None and notification.related_entity_id != related_entity_id:
                continue
            
            if related_entity_type is not None and notification.related_entity_type != related_entity_type:
                continue
            
            if action_required is not None and notification.action_required != action_required:
                continue
            
            result.append(notification)
        
        return result
    
    def update_notification_status(self, notification_id: str, status: NotificationStatus) -> bool:
        """
        Update the status of a notification.
        
        Args:
            notification_id: The ID of the notification to update
            status: The new status
        
        Returns:
            bool: True if the update was successful, False otherwise
        """
        notification = self.get_notification(notification_id)
        if not notification:
            logger.warning(f"Attempted to update non-existent notification: {notification_id}")
            return False
        
        notification.status = status
        logger.info(f"Updated notification {notification_id} status to {status.value}")
        return True
    
    def take_action(self, notification_id: str, action: str) -> bool:
        """
        Take an action on a notification.
        
        Args:
            notification_id: The ID of the notification to act on
            action: The action to take
        
        Returns:
            bool: True if the action was successful, False otherwise
        """
        notification = self.get_notification(notification_id)
        if not notification:
            logger.warning(f"Attempted to take action on non-existent notification: {notification_id}")
            return False
        
        return notification.take_action(action)
