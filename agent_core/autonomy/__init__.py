"""
Autonomy Framework for the Nick the Great Unified Agent.

This package implements the autonomy framework that determines when the agent can act
autonomously and when it needs human approval.
"""

from .decision_matrix import DecisionMatrix, DecisionCategory, ApprovalLevel
from .notification_system import NotificationSystem, NotificationType, NotificationPriority, NotificationStatus, Notification
from .approval_workflow import ApprovalWorkflow, ApprovalStatus, ApprovalRequest
from .autonomy_framework import AutonomyFramework

__all__ = [
    'DecisionMatrix',
    'DecisionCategory',
    'ApprovalLevel',
    'NotificationSystem',
    'NotificationType',
    'NotificationPriority',
    'NotificationStatus',
    'Notification',
    'ApprovalWorkflow',
    'ApprovalStatus',
    'ApprovalRequest',
    'AutonomyFramework'
]
