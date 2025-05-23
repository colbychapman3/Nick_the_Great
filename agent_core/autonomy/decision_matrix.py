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

    # NOTE ON SOURCE OF TRUTH:
    # The default decision rules defined in the `_create_default_matrix()` method
    # are the definitive source of truth for the agent's behavior.
    # There is a corresponding Markdown document at `autonomy/autonomous_decision_matrix.md`
    # which provides a human-readable overview of these rules.
    #
    # **Synchronization Process:**
    # Currently, synchronization between this Python definition and the Markdown
    # document is a manual process. If changes are made to the rules in this
    # Python file (especially the structure or logic of conditions), the
    # `autonomy/autonomous_decision_matrix.md` document **must be updated manually**
    # to reflect these changes accurately.
    # Future consideration: Develop a script to auto-generate the Markdown
    # tables from this Python definition to ensure consistency.
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
                    "conditions": [ # Conditions are now a list of rule objects
                        {"if": {"field": "word_count", "operator": ">", "value": 10000}, "then": ApprovalLevel.NOTIFY},
                        {"if": {"field": "contains_sensitive_topics", "operator": "is_true"}, "then": ApprovalLevel.APPROVAL_REQUIRED}
                    ]
                },
                "create_blog_post": {
                    "default": ApprovalLevel.AUTONOMOUS,
                    "conditions": [
                        {"if": {"field": "contains_sensitive_topics", "operator": "is_true"}, "then": ApprovalLevel.APPROVAL_REQUIRED}
                    ]
                },
                "create_social_media_post": {
                    "default": ApprovalLevel.NOTIFY,
                    "conditions": [
                        {"if": {"field": "platform", "operator": "==", "value": "twitter"}, "then": ApprovalLevel.APPROVAL_REQUIRED},
                        {"if": {"field": "contains_sensitive_topics", "operator": "is_true"}, "then": ApprovalLevel.APPROVAL_REQUIRED}
                    ]
                }
            },
            DecisionCategory.FINANCIAL: {
                "spend_money": {
                    "default": ApprovalLevel.APPROVAL_REQUIRED,
                    "conditions": [
                        {"if": {"field": "amount", "operator": "<=", "value": 5.0}, "then": ApprovalLevel.NOTIFY},
                        {"if": {"field": "amount", "operator": ">", "value": 50.0}, "then": ApprovalLevel.PROHIBITED}
                    ]
                },
                "allocate_budget": {
                    "default": ApprovalLevel.APPROVAL_REQUIRED,
                    "conditions": [
                        {"if": [ # Represents AND condition: list of condition objects
                            {"field": "amount", "operator": "<=", "value": 10.0},
                            {"field": "experiment_has_positive_roi", "operator": "is_true"}
                        ], "then": ApprovalLevel.NOTIFY}
                    ]
                }
            },
            DecisionCategory.PLATFORM_INTERACTION: {
                "create_account": {
                    "default": ApprovalLevel.APPROVAL_REQUIRED,
                    "conditions": [] # No specific conditions, always default
                },
                "post_content": {
                    "default": ApprovalLevel.NOTIFY,
                    "conditions": [
                        {"if": {"field": "platform", "operator": "in", "value": ["twitter", "facebook"]}, "then": ApprovalLevel.APPROVAL_REQUIRED}
                    ]
                },
                "interact_with_users": {
                    "default": ApprovalLevel.APPROVAL_REQUIRED,
                    "conditions": [
                        {"if": {"field": "interaction_type", "operator": "==", "value": "like"}, "then": ApprovalLevel.NOTIFY}
                    ]
                }
            },
            DecisionCategory.EXPERIMENT_MANAGEMENT: {
                "create_experiment": {
                    "default": ApprovalLevel.AUTONOMOUS,
                    "conditions": [
                        {"if": {"field": "estimated_cost", "operator": ">", "value": 20.0}, "then": ApprovalLevel.APPROVAL_REQUIRED}
                    ]
                },
                "start_experiment": {
                    "default": ApprovalLevel.AUTONOMOUS,
                    "conditions": [
                        {"if": {"field": "estimated_cost", "operator": ">", "value": 20.0}, "then": ApprovalLevel.APPROVAL_REQUIRED}
                    ]
                },
                "stop_experiment": {
                    "default": ApprovalLevel.AUTONOMOUS,
                    "conditions": []
                },
                "modify_experiment": {
                    "default": ApprovalLevel.NOTIFY,
                    "conditions": [
                        {"if": {"field": "changes_estimated_cost_by", "operator": ">", "value": 10.0}, "then": ApprovalLevel.APPROVAL_REQUIRED}
                    ]
                }
            },
            DecisionCategory.RESOURCE_ALLOCATION: {
                "allocate_resources": {
                    "default": ApprovalLevel.AUTONOMOUS,
                    "conditions": [
                        {"if": {"field": "resource_type", "operator": "==", "value": "financial"}, "then": ApprovalLevel.APPROVAL_REQUIRED}
                    ]
                },
                "reallocate_resources": {
                    "default": ApprovalLevel.NOTIFY,
                    "conditions": [
                        {"if": {"field": "resource_type", "operator": "==", "value": "financial"}, "then": ApprovalLevel.APPROVAL_REQUIRED},
                        {"if": {"field": "amount_change", "operator": ">", "value": 20.0}, "then": ApprovalLevel.APPROVAL_REQUIRED}
                    ]
                }
            },
            DecisionCategory.EXTERNAL_COMMUNICATION: {
                "send_email": {
                    "default": ApprovalLevel.APPROVAL_REQUIRED,
                    "conditions": [
                        {"if": {"field": "template", "operator": "==", "value": "status_update"}, "then": ApprovalLevel.NOTIFY}
                    ]
                },
                "contact_freelancer": {
                    "default": ApprovalLevel.APPROVAL_REQUIRED,
                    "conditions": [
                         {"if": [ # Represents AND condition
                            {"field": "is_existing_relationship", "operator": "is_true"},
                            {"field": "message_type", "operator": "==", "value": "status_request"}
                        ], "then": ApprovalLevel.NOTIFY}
                    ]
                }
            }
        }
        return matrix

    def _evaluate_condition(self, condition_group: Any, context: Dict[str, Any]) -> bool:
        """
        Evaluate a single condition or a group of conditions (for AND logic).

        Args:
            condition_group: A single condition dictionary `{"field":..., "operator":..., "value":...}`
                             or a list of such dictionaries (implicitly ANDed).
            context: The context for evaluation.

        Returns:
            bool: True if the condition(s) are met, False otherwise.
        """
        if isinstance(condition_group, list): # AND group
            if not condition_group: # Empty list of conditions
                return True # Or False, depending on desired logic for empty AND group. Let's assume True.
            return all(self._evaluate_single_condition(cond, context) for cond in condition_group)
        elif isinstance(condition_group, dict): # Single condition
            return self._evaluate_single_condition(condition_group, context)
        else:
            logger.warning(f"Invalid condition format encountered: {condition_group}")
            return False

    def _evaluate_single_condition(self, condition: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """
        Evaluate a single structured condition.
        A condition is a dictionary like: {"field": "name", "operator": "op", "value": "val"}
        or {"field": "name", "operator": "is_true"}
        """
        field = condition.get("field")
        operator = condition.get("operator")
        # Value is not required for operators like 'is_true', 'is_false'
        value = condition.get("value") 

        if not field or not operator:
            logger.warning(f"Invalid condition structure: {condition}. Missing 'field' or 'operator'.")
            return False

        context_value = context.get(field)

        # Handle cases where context_value might be None
        if operator == "is_true":
            return bool(context_value) is True
        elif operator == "is_false": # Add is_false for completeness
            return bool(context_value) is False
        
        # For other operators, if context_value is None, the condition generally cannot be met.
        if context_value is None:
            logger.debug(f"Field '{field}' not found in context or is None for condition: {condition}")
            return False
            
        try:
            if operator == "==":
                return context_value == value
            elif operator == "!=":
                return context_value != value
            elif operator == ">":
                return isinstance(context_value, (int, float)) and isinstance(value, (int, float)) and context_value > value
            elif operator == "<":
                return isinstance(context_value, (int, float)) and isinstance(value, (int, float)) and context_value < value
            elif operator == ">=":
                return isinstance(context_value, (int, float)) and isinstance(value, (int, float)) and context_value >= value
            elif operator == "<=":
                return isinstance(context_value, (int, float)) and isinstance(value, (int, float)) and context_value <= value
            elif operator == "in":
                return isinstance(value, list) and context_value in value
            elif operator == "not in": # Add "not in" for completeness
                return isinstance(value, list) and context_value not in value
            else:
                logger.warning(f"Unsupported operator '{operator}' in condition: {condition}")
                return False
        except TypeError as e:
            # This can happen if context_value and value are of incompatible types for comparison
            logger.error(f"Type error evaluating condition '{condition}' with context value {context_value} ({type(context_value)}) and condition value {value} ({type(value)}): {e}")
            return False
        except Exception as e: # Catch any other unexpected errors during evaluation
            logger.error(f"Unexpected error evaluating condition '{condition}': {e}")
            return False

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
            logger.warning(f"Unknown decision category: {category.value if isinstance(category, DecisionCategory) else category}")
            return ApprovalLevel.APPROVAL_REQUIRED
        
        category_actions = self.matrix.get(category)
        if not category_actions or action not in category_actions:
            logger.warning(f"Unknown action '{action}' in category {category.value if isinstance(category, DecisionCategory) else category}")
            return ApprovalLevel.APPROVAL_REQUIRED
        
        action_rules = category_actions[action]
        default_level = action_rules.get("default", ApprovalLevel.APPROVAL_REQUIRED) # Default to approval if not specified
        
        # Conditions are now a list of {"if": <condition_obj_or_list_of_condition_obj>, "then": ApprovalLevel}
        for rule in action_rules.get("conditions", []):
            condition_group = rule.get("if")
            approval_level_for_condition = rule.get("then")

            if condition_group is None or approval_level_for_condition is None:
                logger.warning(f"Malformed rule for {category.value}.{action}: {rule}. Missing 'if' or 'then'.")
                continue

            try:
                condition_met = self._evaluate_condition(condition_group, context)
                if condition_met:
                    logger.info(f"Condition group met for {category.value}.{action} (Context: {context}). Condition: {condition_group}. Setting approval level to {approval_level_for_condition.value}")
                    return approval_level_for_condition
            except Exception as e: # Should ideally be caught by _evaluate_condition, but as a safeguard
                logger.error(f"Error evaluating condition group '{condition_group}' for {category.value}.{action}: {e}")
        
        logger.info(f"No specific condition met for {category.value}.{action} (Context: {context}). Using default approval level {default_level.value}")
        return default_level
    
    def update_matrix(self, category: DecisionCategory, action: str, 
                     updates: Dict[str, Any]) -> bool:
        """
        Update the decision matrix for a specific category and action.
        
        Args:
            category: The decision category to update
            action: The specific action to update
            updates: The updates to apply. 'default' should be an ApprovalLevel enum.
                     'conditions' should be a list of rule dictionaries in the new structured format:
                     e.g., `[{"if": {"field": "amount", "operator": ">", "value": 100}, "then": ApprovalLevel.NOTIFY}, ...]`
        
        Returns:
            bool: True if the update was successful, False otherwise
        """
        try:
            if category not in self.matrix:
                self.matrix[category] = {} # Initialize if category does not exist
            
            if action not in self.matrix[category]:
                # Initialize with a restrictive default if action is new
                self.matrix[category][action] = {"default": ApprovalLevel.APPROVAL_REQUIRED, "conditions": []} 
            
            # Update default approval level if provided and is a valid ApprovalLevel
            if "default" in updates:
                if isinstance(updates["default"], ApprovalLevel):
                    self.matrix[category][action]["default"] = updates["default"]
                else:
                    logger.warning(f"Invalid type for 'default' in update_matrix: {type(updates['default'])}. Must be ApprovalLevel enum.")
            
            # Update conditions if provided and is a list
            if "conditions" in updates:
                if isinstance(updates["conditions"], list):
                    # Add validation for the structure of each condition in the list
                    valid_conditions = []
                    for rule in updates["conditions"]:
                        if isinstance(rule, dict) and "if" in rule and "then" in rule and isinstance(rule["then"], ApprovalLevel):
                            # Further validation of the "if" part can be added here (e.g. checking field, operator)
                            valid_conditions.append(rule)
                        else:
                            logger.warning(f"Skipping invalid rule in update_matrix for {category.value}.{action}: {rule}")
                    self.matrix[category][action]["conditions"] = valid_conditions
                else:
                    logger.warning(f"Invalid type for 'conditions' in update_matrix: {type(updates['conditions'])}. Must be a list of rule dicts.")
            
            logger.info(f"Updated decision matrix for {category.value}.{action}")
            return True
        except Exception as e:
            logger.error(f"Error updating decision matrix for {category.value}.{action}: {e}")
            return False
