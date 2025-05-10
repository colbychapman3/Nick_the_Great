"""
Unit tests for the Notification System.
"""

import os
import sys
import pytest
import time
from unittest.mock import MagicMock, patch

# Add the parent directory to the path so we can import the agent_core modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the modules to test
from autonomy_framework import NotificationSystem, NotificationType, NotificationPriority, Notification

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
        related_entity_id = "test_entity_123"
        related_entity_type = "test_entity_type"
        
        # Act
        notification = self.notification_system.create_notification(
            title=title,
            message=message,
            notification_type=notification_type,
            priority=priority,
            user_id=user_id,
            related_entity_id=related_entity_id,
            related_entity_type=related_entity_type
        )
        
        # Assert
        assert notification is not None
        assert notification.title == title
        assert notification.message == message
        assert notification.notification_type == notification_type
        assert notification.priority == priority
        assert notification.user_id == user_id
        assert notification.related_entity_id == related_entity_id
        assert notification.related_entity_type == related_entity_type
        assert notification.read is False
        assert notification.created_time is not None
        assert notification in self.notification_system.notifications
    
    def test_create_notification_minimal(self):
        """Test creating a notification with minimal parameters."""
        # Arrange
        title = "Test Notification"
        message = "This is a test notification"
        notification_type = NotificationType.INFO
        priority = NotificationPriority.MEDIUM
        
        # Act
        notification = self.notification_system.create_notification(
            title=title,
            message=message,
            notification_type=notification_type,
            priority=priority
        )
        
        # Assert
        assert notification is not None
        assert notification.title == title
        assert notification.message == message
        assert notification.notification_type == notification_type
        assert notification.priority == priority
        assert notification.user_id is None
        assert notification.related_entity_id is None
        assert notification.related_entity_type is None
        assert notification.read is False
        assert notification in self.notification_system.notifications
    
    def test_get_notifications_all(self):
        """Test getting all notifications."""
        # Arrange
        self.notification_system.create_notification(
            title="Notification 1",
            message="Message 1",
            notification_type=NotificationType.INFO,
            priority=NotificationPriority.LOW,
            user_id="user1"
        )
        self.notification_system.create_notification(
            title="Notification 2",
            message="Message 2",
            notification_type=NotificationType.WARNING,
            priority=NotificationPriority.MEDIUM,
            user_id="user2"
        )
        
        # Act
        notifications = self.notification_system.get_notifications()
        
        # Assert
        assert len(notifications) == 2
        assert notifications[0].title == "Notification 1"
        assert notifications[1].title == "Notification 2"
    
    def test_get_notifications_by_user(self):
        """Test getting notifications for a specific user."""
        # Arrange
        self.notification_system.create_notification(
            title="Notification 1",
            message="Message 1",
            notification_type=NotificationType.INFO,
            priority=NotificationPriority.LOW,
            user_id="user1"
        )
        self.notification_system.create_notification(
            title="Notification 2",
            message="Message 2",
            notification_type=NotificationType.WARNING,
            priority=NotificationPriority.MEDIUM,
            user_id="user2"
        )
        self.notification_system.create_notification(
            title="Notification 3",
            message="Message 3",
            notification_type=NotificationType.ERROR,
            priority=NotificationPriority.HIGH,
            user_id="user1"
        )
        
        # Act
        notifications = self.notification_system.get_notifications(user_id="user1")
        
        # Assert
        assert len(notifications) == 2
        assert all(n.user_id == "user1" for n in notifications)
        assert notifications[0].title == "Notification 1"
        assert notifications[1].title == "Notification 3"
    
    def test_get_notifications_by_type(self):
        """Test getting notifications of a specific type."""
        # Arrange
        self.notification_system.create_notification(
            title="Notification 1",
            message="Message 1",
            notification_type=NotificationType.INFO,
            priority=NotificationPriority.LOW
        )
        self.notification_system.create_notification(
            title="Notification 2",
            message="Message 2",
            notification_type=NotificationType.WARNING,
            priority=NotificationPriority.MEDIUM
        )
        self.notification_system.create_notification(
            title="Notification 3",
            message="Message 3",
            notification_type=NotificationType.INFO,
            priority=NotificationPriority.HIGH
        )
        
        # Act
        notifications = self.notification_system.get_notifications(notification_type=NotificationType.INFO)
        
        # Assert
        assert len(notifications) == 2
        assert all(n.notification_type == NotificationType.INFO for n in notifications)
        assert notifications[0].title == "Notification 1"
        assert notifications[1].title == "Notification 3"
    
    def test_get_notifications_by_priority(self):
        """Test getting notifications of a specific priority."""
        # Arrange
        self.notification_system.create_notification(
            title="Notification 1",
            message="Message 1",
            notification_type=NotificationType.INFO,
            priority=NotificationPriority.LOW
        )
        self.notification_system.create_notification(
            title="Notification 2",
            message="Message 2",
            notification_type=NotificationType.WARNING,
            priority=NotificationPriority.MEDIUM
        )
        self.notification_system.create_notification(
            title="Notification 3",
            message="Message 3",
            notification_type=NotificationType.ERROR,
            priority=NotificationPriority.HIGH
        )
        
        # Act
        notifications = self.notification_system.get_notifications(priority=NotificationPriority.HIGH)
        
        # Assert
        assert len(notifications) == 1
        assert notifications[0].priority == NotificationPriority.HIGH
        assert notifications[0].title == "Notification 3"
    
    def test_get_notifications_by_read_status(self):
        """Test getting notifications by read status."""
        # Arrange
        notification1 = self.notification_system.create_notification(
            title="Notification 1",
            message="Message 1",
            notification_type=NotificationType.INFO,
            priority=NotificationPriority.LOW
        )
        notification2 = self.notification_system.create_notification(
            title="Notification 2",
            message="Message 2",
            notification_type=NotificationType.WARNING,
            priority=NotificationPriority.MEDIUM
        )
        
        # Mark one notification as read
        notification1.read = True
        
        # Act
        unread_notifications = self.notification_system.get_notifications(read=False)
        read_notifications = self.notification_system.get_notifications(read=True)
        
        # Assert
        assert len(unread_notifications) == 1
        assert unread_notifications[0].title == "Notification 2"
        assert len(read_notifications) == 1
        assert read_notifications[0].title == "Notification 1"
    
    def test_get_notifications_by_entity(self):
        """Test getting notifications by related entity."""
        # Arrange
        self.notification_system.create_notification(
            title="Notification 1",
            message="Message 1",
            notification_type=NotificationType.INFO,
            priority=NotificationPriority.LOW,
            related_entity_id="entity1",
            related_entity_type="type1"
        )
        self.notification_system.create_notification(
            title="Notification 2",
            message="Message 2",
            notification_type=NotificationType.WARNING,
            priority=NotificationPriority.MEDIUM,
            related_entity_id="entity2",
            related_entity_type="type2"
        )
        
        # Act
        notifications = self.notification_system.get_notifications(related_entity_id="entity1")
        
        # Assert
        assert len(notifications) == 1
        assert notifications[0].related_entity_id == "entity1"
        assert notifications[0].title == "Notification 1"
    
    def test_get_notifications_combined_filters(self):
        """Test getting notifications with multiple filters."""
        # Arrange
        self.notification_system.create_notification(
            title="Notification 1",
            message="Message 1",
            notification_type=NotificationType.INFO,
            priority=NotificationPriority.LOW,
            user_id="user1",
            related_entity_id="entity1"
        )
        self.notification_system.create_notification(
            title="Notification 2",
            message="Message 2",
            notification_type=NotificationType.WARNING,
            priority=NotificationPriority.MEDIUM,
            user_id="user1",
            related_entity_id="entity2"
        )
        self.notification_system.create_notification(
            title="Notification 3",
            message="Message 3",
            notification_type=NotificationType.INFO,
            priority=NotificationPriority.HIGH,
            user_id="user2",
            related_entity_id="entity1"
        )
        
        # Act
        notifications = self.notification_system.get_notifications(
            user_id="user1",
            notification_type=NotificationType.INFO
        )
        
        # Assert
        assert len(notifications) == 1
        assert notifications[0].user_id == "user1"
        assert notifications[0].notification_type == NotificationType.INFO
        assert notifications[0].title == "Notification 1"
    
    def test_mark_as_read(self):
        """Test marking a notification as read."""
        # Arrange
        notification = self.notification_system.create_notification(
            title="Test Notification",
            message="This is a test notification",
            notification_type=NotificationType.INFO,
            priority=NotificationPriority.MEDIUM
        )
        assert notification.read is False
        
        # Act
        result = self.notification_system.mark_as_read(notification.id)
        
        # Assert
        assert result is True
        assert notification.read is True
    
    def test_mark_as_read_not_found(self):
        """Test marking a non-existent notification as read."""
        # Act
        result = self.notification_system.mark_as_read("non-existent-id")
        
        # Assert
        assert result is False
    
    def test_delete_notification(self):
        """Test deleting a notification."""
        # Arrange
        notification = self.notification_system.create_notification(
            title="Test Notification",
            message="This is a test notification",
            notification_type=NotificationType.INFO,
            priority=NotificationPriority.MEDIUM
        )
        assert notification in self.notification_system.notifications
        
        # Act
        result = self.notification_system.delete_notification(notification.id)
        
        # Assert
        assert result is True
        assert notification not in self.notification_system.notifications
    
    def test_delete_notification_not_found(self):
        """Test deleting a non-existent notification."""
        # Act
        result = self.notification_system.delete_notification("non-existent-id")
        
        # Assert
        assert result is False
