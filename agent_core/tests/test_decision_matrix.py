"""
Unit tests for the Decision Matrix.
"""

import os
import sys
import pytest
from unittest.mock import MagicMock, patch

# Add the parent directory to the path so we can import the agent_core modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the modules to test
from autonomy_framework import DecisionMatrix, DecisionCategory, ApprovalLevel

class TestDecisionMatrix:
    """Test the Decision Matrix."""
    
    def setup_method(self):
        """Set up the test environment."""
        self.decision_matrix = DecisionMatrix()
    
    def test_init(self):
        """Test the initialization of the decision matrix."""
        assert self.decision_matrix.matrix is not None
        assert DecisionCategory.CONTENT_CREATION in self.decision_matrix.matrix
        assert DecisionCategory.FINANCIAL in self.decision_matrix.matrix
        assert DecisionCategory.PLATFORM_INTERACTION in self.decision_matrix.matrix
        assert DecisionCategory.EXPERIMENT_MANAGEMENT in self.decision_matrix.matrix
        assert DecisionCategory.RESOURCE_ALLOCATION in self.decision_matrix.matrix
        assert DecisionCategory.EXTERNAL_COMMUNICATION in self.decision_matrix.matrix
    
    def test_get_approval_level_content_creation(self):
        """Test getting approval level for content creation actions."""
        # Test default approval level
        approval_level = self.decision_matrix.get_approval_level(
            DecisionCategory.CONTENT_CREATION,
            "generate_ebook",
            {}
        )
        assert approval_level == ApprovalLevel.AUTONOMOUS
        
        # Test condition: word_count > 10000
        approval_level = self.decision_matrix.get_approval_level(
            DecisionCategory.CONTENT_CREATION,
            "generate_ebook",
            {"word_count": 15000}
        )
        assert approval_level == ApprovalLevel.NOTIFY
        
        # Test condition: contains_sensitive_topics
        approval_level = self.decision_matrix.get_approval_level(
            DecisionCategory.CONTENT_CREATION,
            "generate_ebook",
            {"contains_sensitive_topics": True}
        )
        assert approval_level == ApprovalLevel.APPROVAL_REQUIRED
    
    def test_get_approval_level_financial(self):
        """Test getting approval level for financial actions."""
        # Test default approval level
        approval_level = self.decision_matrix.get_approval_level(
            DecisionCategory.FINANCIAL,
            "spend_money",
            {}
        )
        assert approval_level == ApprovalLevel.APPROVAL_REQUIRED
        
        # Test condition: amount <= 5.0
        approval_level = self.decision_matrix.get_approval_level(
            DecisionCategory.FINANCIAL,
            "spend_money",
            {"amount": 3.0}
        )
        assert approval_level == ApprovalLevel.NOTIFY
        
        # Test condition: amount > 50.0
        approval_level = self.decision_matrix.get_approval_level(
            DecisionCategory.FINANCIAL,
            "spend_money",
            {"amount": 60.0}
        )
        assert approval_level == ApprovalLevel.PROHIBITED
    
    def test_get_approval_level_platform_interaction(self):
        """Test getting approval level for platform interaction actions."""
        # Test default approval level
        approval_level = self.decision_matrix.get_approval_level(
            DecisionCategory.PLATFORM_INTERACTION,
            "post_content",
            {}
        )
        assert approval_level == ApprovalLevel.NOTIFY
        
        # Test condition: platform in ['twitter', 'facebook']
        approval_level = self.decision_matrix.get_approval_level(
            DecisionCategory.PLATFORM_INTERACTION,
            "post_content",
            {"platform": "twitter"}
        )
        assert approval_level == ApprovalLevel.APPROVAL_REQUIRED
        
        # Test with a different platform
        approval_level = self.decision_matrix.get_approval_level(
            DecisionCategory.PLATFORM_INTERACTION,
            "post_content",
            {"platform": "pinterest"}
        )
        assert approval_level == ApprovalLevel.NOTIFY
    
    def test_get_approval_level_experiment_management(self):
        """Test getting approval level for experiment management actions."""
        # Test default approval level
        approval_level = self.decision_matrix.get_approval_level(
            DecisionCategory.EXPERIMENT_MANAGEMENT,
            "create_experiment",
            {}
        )
        assert approval_level == ApprovalLevel.AUTONOMOUS
        
        # Test condition: estimated_cost > 20.0
        approval_level = self.decision_matrix.get_approval_level(
            DecisionCategory.EXPERIMENT_MANAGEMENT,
            "create_experiment",
            {"estimated_cost": 25.0}
        )
        assert approval_level == ApprovalLevel.APPROVAL_REQUIRED
        
        # Test with cost below threshold
        approval_level = self.decision_matrix.get_approval_level(
            DecisionCategory.EXPERIMENT_MANAGEMENT,
            "create_experiment",
            {"estimated_cost": 15.0}
        )
        assert approval_level == ApprovalLevel.AUTONOMOUS
    
    def test_get_approval_level_unknown_category(self):
        """Test getting approval level for an unknown category."""
        # Create a mock category that's not in the matrix
        mock_category = MagicMock()
        mock_category.value = "unknown_category"
        
        approval_level = self.decision_matrix.get_approval_level(
            mock_category,
            "some_action",
            {}
        )
        assert approval_level == ApprovalLevel.APPROVAL_REQUIRED
    
    def test_get_approval_level_unknown_action(self):
        """Test getting approval level for an unknown action."""
        approval_level = self.decision_matrix.get_approval_level(
            DecisionCategory.CONTENT_CREATION,
            "unknown_action",
            {}
        )
        assert approval_level == ApprovalLevel.APPROVAL_REQUIRED
    
    def test_update_matrix(self):
        """Test updating the decision matrix."""
        # Update an existing action
        result = self.decision_matrix.update_matrix(
            DecisionCategory.CONTENT_CREATION,
            "generate_ebook",
            {
                "default": ApprovalLevel.NOTIFY,
                "conditions": {
                    "word_count > 5000": ApprovalLevel.APPROVAL_REQUIRED
                }
            }
        )
        assert result is True
        
        # Verify the update
        approval_level = self.decision_matrix.get_approval_level(
            DecisionCategory.CONTENT_CREATION,
            "generate_ebook",
            {}
        )
        assert approval_level == ApprovalLevel.NOTIFY
        
        approval_level = self.decision_matrix.get_approval_level(
            DecisionCategory.CONTENT_CREATION,
            "generate_ebook",
            {"word_count": 6000}
        )
        assert approval_level == ApprovalLevel.APPROVAL_REQUIRED
        
        # Add a new action to an existing category
        result = self.decision_matrix.update_matrix(
            DecisionCategory.CONTENT_CREATION,
            "new_action",
            {
                "default": ApprovalLevel.AUTONOMOUS,
                "conditions": {
                    "is_public": ApprovalLevel.NOTIFY
                }
            }
        )
        assert result is True
        
        # Verify the new action
        approval_level = self.decision_matrix.get_approval_level(
            DecisionCategory.CONTENT_CREATION,
            "new_action",
            {}
        )
        assert approval_level == ApprovalLevel.AUTONOMOUS
        
        approval_level = self.decision_matrix.get_approval_level(
            DecisionCategory.CONTENT_CREATION,
            "new_action",
            {"is_public": True}
        )
        assert approval_level == ApprovalLevel.NOTIFY
        
        # Add a new category
        mock_category = MagicMock()
        mock_category.value = "test_category"
        
        result = self.decision_matrix.update_matrix(
            mock_category,
            "test_action",
            {
                "default": ApprovalLevel.AUTONOMOUS,
                "conditions": {}
            }
        )
        assert result is True
        
        # Verify the new category and action
        approval_level = self.decision_matrix.get_approval_level(
            mock_category,
            "test_action",
            {}
        )
        assert approval_level == ApprovalLevel.AUTONOMOUS
    
    def test_update_matrix_error(self):
        """Test error handling in update_matrix."""
        # Mock an exception during update
        with patch.object(self.decision_matrix.matrix, "__setitem__", side_effect=Exception("Test exception")):
            result = self.decision_matrix.update_matrix(
                DecisionCategory.CONTENT_CREATION,
                "generate_ebook",
                {"default": ApprovalLevel.NOTIFY}
            )
            assert result is False
    
    def test_condition_evaluation_error(self):
        """Test error handling in condition evaluation."""
        # Create a condition that will raise an exception when evaluated
        self.decision_matrix.matrix[DecisionCategory.CONTENT_CREATION]["generate_ebook"]["conditions"]["invalid_condition"] = ApprovalLevel.PROHIBITED
        
        # The default level should be returned when condition evaluation fails
        approval_level = self.decision_matrix.get_approval_level(
            DecisionCategory.CONTENT_CREATION,
            "generate_ebook",
            {}
        )
        assert approval_level == ApprovalLevel.AUTONOMOUS
