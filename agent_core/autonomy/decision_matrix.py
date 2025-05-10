"""
Decision Matrix for the Nick the Great Unified Agent.

This module implements the decision matrix that determines when the agent can act autonomously
and when it needs human approval.
"""

import logging
import enum
from typing import Dict, Any, Optional, List, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DecisionCategory(enum.Enum):
    """Categories of decisions that the agent can make."""
    CONTENT_CREATION = "content_creation"
    FINANCIAL = "financial"
    PLATFORM_INTERACTION = "platform_interaction"
    EXPERIMENT_MANAGEMENT = "experiment_management"
    RESOURCE_ALLOCATION = "resource_allocation"
    EXTERNAL_COMMUNICATION = "external_communication"

class ApprovalLevel(enum.Enum):
    """Levels of approval required for decisions."""
    AUTONOMOUS = "autonomous"  # Agent can act without human approval
    NOTIFY = "notify"  # Agent can act but must notify humans
    APPROVAL_REQUIRED = "approval_required"  # Agent must get human approval before acting
    PROHIBITED = "prohibited"  # Agent cannot perform this action

class DecisionMatrix:
    """
    Decision Matrix for determining when the agent can act autonomously.
    
    The matrix is structured as a nested dictionary:
    - First level: Decision category (e.g., CONTENT_CREATION)
    - Second level: Action type (e.g., "generate_ebook")
    - Third level: Conditions and approval levels
    """
    
    def __init__(self):
        """Initialize the decision matrix with default values."""
        self.matrix = self._create_default_matrix()
        logger.info("Decision Matrix initialized with default values")
    
    def _create_default_matrix(self) -> Dict[DecisionCategory, Dict[str, Dict[str, Any]]]:
        """
        Create the default decision matrix.
        
        Returns:
            Dict: The default decision matrix
        """
        matrix = {
            DecisionCategory.CONTENT_CREATION: {
                "generate_ebook": {
                    "default": ApprovalLevel.AUTONOMOUS,
                    "conditions": {
                        "word_count > 10000": ApprovalLevel.NOTIFY,
                        "contains_sensitive_topics": ApprovalLevel.APPROVAL_REQUIRED
                    }
                },
                "create_blog_post": {
                    "default": ApprovalLevel.AUTONOMOUS,
                    "conditions": {
                        "contains_sensitive_topics": ApprovalLevel.APPROVAL_REQUIRED
                    }
                },
                "create_social_media_post": {
                    "default": ApprovalLevel.NOTIFY,
                    "conditions": {
                        "platform == 'twitter'": ApprovalLevel.APPROVAL_REQUIRED,
                        "contains_sensitive_topics": ApprovalLevel.APPROVAL_REQUIRED
                    }
                }
            },
            DecisionCategory.FINANCIAL: {
                "spend_money": {
                    "default": ApprovalLevel.APPROVAL_REQUIRED,
                    "conditions": {
                        "amount <= 5.0": ApprovalLevel.NOTIFY,
                        "amount > 50.0": ApprovalLevel.PROHIBITED
                    }
                },
                "allocate_budget": {
                    "default": ApprovalLevel.APPROVAL_REQUIRED,
                    "conditions": {
                        "amount <= 10.0 and experiment_has_positive_roi": ApprovalLevel.NOTIFY
                    }
                }
            },
            DecisionCategory.PLATFORM_INTERACTION: {
                "create_account": {
                    "default": ApprovalLevel.APPROVAL_REQUIRED,
                    "conditions": {}
                },
                "post_content": {
                    "default": ApprovalLevel.NOTIFY,
                    "conditions": {
                        "platform in ['twitter', 'facebook']": ApprovalLevel.APPROVAL_REQUIRED
                    }
                },
                "interact_with_users": {
                    "default": ApprovalLevel.APPROVAL_REQUIRED,
                    "conditions": {
                        "interaction_type == 'like'": ApprovalLevel.NOTIFY
                    }
                }
            },
            DecisionCategory.EXPERIMENT_MANAGEMENT: {
                "create_experiment": {
                    "default": ApprovalLevel.AUTONOMOUS,
                    "conditions": {
                        "estimated_cost > 20.0": ApprovalLevel.APPROVAL_REQUIRED
                    }
                },
                "start_experiment": {
                    "default": ApprovalLevel.AUTONOMOUS,
                    "conditions": {
                        "estimated_cost > 20.0": ApprovalLevel.APPROVAL_REQUIRED
                    }
                },
                "stop_experiment": {
                    "default": ApprovalLevel.AUTONOMOUS,
                    "conditions": {}
                },
                "modify_experiment": {
                    "default": ApprovalLevel.NOTIFY,
                    "conditions": {
                        "changes_estimated_cost_by > 10.0": ApprovalLevel.APPROVAL_REQUIRED
                    }
                }
            },
            DecisionCategory.RESOURCE_ALLOCATION: {
                "allocate_resources": {
                    "default": ApprovalLevel.AUTONOMOUS,
                    "conditions": {
                        "resource_type == 'financial'": ApprovalLevel.APPROVAL_REQUIRED
                    }
                },
                "reallocate_resources": {
                    "default": ApprovalLevel.NOTIFY,
                    "conditions": {
                        "resource_type == 'financial'": ApprovalLevel.APPROVAL_REQUIRED,
                        "amount_change > 20.0": ApprovalLevel.APPROVAL_REQUIRED
                    }
                }
            },
            DecisionCategory.EXTERNAL_COMMUNICATION: {
                "send_email": {
                    "default": ApprovalLevel.APPROVAL_REQUIRED,
                    "conditions": {
                        "template == 'status_update'": ApprovalLevel.NOTIFY
                    }
                },
                "contact_freelancer": {
                    "default": ApprovalLevel.APPROVAL_REQUIRED,
                    "conditions": {
                        "is_existing_relationship and message_type == 'status_request'": ApprovalLevel.NOTIFY
                    }
                }
            }
        }
        return matrix
    
    def get_approval_level(self, category: DecisionCategory, action: str, context: Dict[str, Any]) -> ApprovalLevel:
        """
        Determine the approval level required for a given action in a specific context.
        
        Args:
            category: The decision category
            action: The specific action
            context: The context in which the action is being performed
        
        Returns:
            ApprovalLevel: The required approval level
        """
        if category not in self.matrix:
            logger.warning(f"Unknown decision category: {category}")
            return ApprovalLevel.APPROVAL_REQUIRED
        
        if action not in self.matrix[category]:
            logger.warning(f"Unknown action '{action}' in category {category}")
            return ApprovalLevel.APPROVAL_REQUIRED
        
        action_rules = self.matrix[category][action]
        default_level = action_rules["default"]
        
        # Check conditions
        for condition_str, level in action_rules.get("conditions", {}).items():
            try:
                # Simple condition evaluation (not secure, but functional for prototype)
                # In production, use a proper expression evaluator
                condition_met = eval(condition_str, {"__builtins__": {}}, context)
                if condition_met:
                    logger.info(f"Condition '{condition_str}' met for {category.value}.{action}, setting approval level to {level.value}")
                    return level
            except Exception as e:
                logger.error(f"Error evaluating condition '{condition_str}': {e}")
        
        logger.info(f"Using default approval level {default_level.value} for {category.value}.{action}")
        return default_level
    
    def update_matrix(self, category: DecisionCategory, action: str, 
                     updates: Dict[str, Any]) -> bool:
        """
        Update the decision matrix for a specific category and action.
        
        Args:
            category: The decision category to update
            action: The specific action to update
            updates: The updates to apply
        
        Returns:
            bool: True if the update was successful, False otherwise
        """
        try:
            if category not in self.matrix:
                self.matrix[category] = {}
            
            if action not in self.matrix[category]:
                self.matrix[category][action] = {"default": ApprovalLevel.APPROVAL_REQUIRED, "conditions": {}}
            
            # Update default approval level if provided
            if "default" in updates:
                self.matrix[category][action]["default"] = updates["default"]
            
            # Update conditions if provided
            if "conditions" in updates:
                if "conditions" not in self.matrix[category][action]:
                    self.matrix[category][action]["conditions"] = {}
                
                for condition, level in updates["conditions"].items():
                    self.matrix[category][action]["conditions"][condition] = level
            
            logger.info(f"Updated decision matrix for {category.value}.{action}")
            return True
        except Exception as e:
            logger.error(f"Error updating decision matrix: {e}")
            return False
