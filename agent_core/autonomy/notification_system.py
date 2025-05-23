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
                 system: 'NotificationSystem', # Added reference to the system
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
            system: The NotificationSystem instance creating this notification.
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
        self._system = system # Store reference to the system
    
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
    def from_dict(cls, system: 'NotificationSystem', data: Dict[str, Any]) -> 'Notification':
        """
        Create a notification from a dictionary.
        
        Args:
            system: The NotificationSystem instance that will own this notification.
            data: The dictionary containing notification data
        
        Returns:
            Notification: The created notification
        """
        notification = cls(
            system=system, # Pass the system instance
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
        if self.status == NotificationStatus.READ:
            return # Already read
        self.status = NotificationStatus.READ
        self.read_time = int(time.time())
        if self._system:
            self._system._notify_notification_updated(self)
    
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
        if self._system:
            self._system._notify_notification_updated(self)
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
    
    def __init__(self, db_client: Optional[Any] = None):
        """
        Initialize the notification system.
        
        Args:
            db_client: The database client for persistence.
        """
        self.db_client = db_client
        self.notifications: Dict[str, Notification] = {}  # Dictionary of notification ID to Notification
        
        if self.db_client:
            self._restore_unsynced_notifications()
            
        logger.info("Notification System initialized")

    def _restore_unsynced_notifications(self):
        """
        Restore notifications from the database that might need further interaction or were not synced.
        """
        if not self.db_client:
            return

        logger.info("Attempting to restore notifications from database...")
        try:
            # TODO: Implement self.db_client.restore_notifications() in db_client.py
            # This method should fetch notifications, potentially those that are not yet EXPIRED or ACTIONED.
            # Example expected return: List[Dict[str, Any]]
            restored_notifications_data = self.db_client.restore_notifications()
            
            if restored_notifications_data:
                for notif_data in restored_notifications_data:
                    try:
                        # Pass 'self' as the system when reconstructing
                        notification = Notification.from_dict(self, notif_data)
                        
                        # Only restore if not already handled or expired
                        if notification.status not in [NotificationStatus.ACTIONED, NotificationStatus.EXPIRED] and \
                           not notification.is_expired():
                            self.notifications[notification.id] = notification
                            logger.info(f"Restored notification {notification.id}")
                        elif notification.status != NotificationStatus.EXPIRED and notification.is_expired():
                            notification.status = NotificationStatus.EXPIRED # Mark as expired
                            # And update in DB
                            # TODO: Implement self.db_client.update_notification() in db_client.py
                            self.db_client.update_notification(notification.id, notification.to_dict())
                            logger.info(f"Restored and marked notification {notification.id} as EXPIRED.")
                            
                    except Exception as e:
                        logger.error(f"Error reconstructing notification from data '{notif_data}': {e}")
                logger.info(f"Successfully processed {len(restored_notifications_data)} restored notifications.")
            else:
                logger.info("No notifications found in database to restore.")
        except AttributeError:
            logger.warning("db_client does not have 'restore_notifications' method. Skipping restore.")
        except Exception as e:
            logger.error(f"Error restoring notifications from database: {e}")

    def _notify_notification_updated(self, notification: Notification):
        """
        Called by a Notification object when its state changes, to sync to DB.
        """
        if self.db_client:
            try:
                # TODO: Implement self.db_client.update_notification(notification_id, notification_data) in db_client.py
                self.db_client.update_notification(notification.id, notification.to_dict())
                logger.info(f"Notification {notification.id} update synced with database.")
            except AttributeError:
                logger.warning(f"db_client does not have 'update_notification' method. Notification {notification.id} update not synced.")
            except Exception as e:
                logger.error(f"Error syncing notification {notification.id} update to database: {e}")
            
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
        
        # Persist the notification if db_client is available
        if self.db_client:
            try:
                # TODO: Implement self.db_client.sync_notification(notification_data) in db_client.py
                # This method should save the new notification to the database.
                self.db_client.sync_notification(notification.to_dict())
                logger.info(f"Notification {notification.id} synced with database.")
            except AttributeError:
                logger.warning(f"db_client does not have 'sync_notification' method. Notification {notification.id} not synced.")
            except Exception as e:
                logger.error(f"Error syncing notification {notification.id} to database: {e}")
        
        # TODO: Send notification to backend for delivery to users (this part remains)
        
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
