"""
Unit tests for the Risk Tolerance Framework.
"""

import os
import sys
import pytest
from unittest.mock import MagicMock, patch

# Add the parent directory to the path so we can import the agent_core modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the modules to test
from autonomy_framework.risk_tolerance import (
    RiskLevel,
    RiskCategory,
    RiskToleranceProfile,
    RiskAssessment,
    create_default_profiles
)

class TestRiskToleranceProfile:
    """Test the RiskToleranceProfile class."""
    
    def setup_method(self):
        """Set up the test environment."""
        self.tolerance_levels = {
            RiskCategory.FINANCIAL: RiskLevel.MEDIUM,
            RiskCategory.REPUTATION: RiskLevel.LOW,
            RiskCategory.OPERATIONAL: RiskLevel.HIGH,
            RiskCategory.COMPLIANCE: RiskLevel.MINIMAL,
            RiskCategory.SECURITY: RiskLevel.LOW,
            RiskCategory.PERFORMANCE: RiskLevel.MEDIUM
        }
        
        self.profile = RiskToleranceProfile(
            name="Test Profile",
            description="A test risk profile",
            tolerance_levels=self.tolerance_levels
        )
    
    def test_init(self):
        """Test the initialization of the risk tolerance profile."""
        assert self.profile.name == "Test Profile"
        assert self.profile.description == "A test risk profile"
        assert self.profile.tolerance_levels == self.tolerance_levels
    
    def test_get_tolerance_level(self):
        """Test getting the tolerance level for a specific risk category."""
        assert self.profile.get_tolerance_level(RiskCategory.FINANCIAL) == RiskLevel.MEDIUM
        assert self.profile.get_tolerance_level(RiskCategory.REPUTATION) == RiskLevel.LOW
        assert self.profile.get_tolerance_level(RiskCategory.OPERATIONAL) == RiskLevel.HIGH
        assert self.profile.get_tolerance_level(RiskCategory.COMPLIANCE) == RiskLevel.MINIMAL
        assert self.profile.get_tolerance_level(RiskCategory.SECURITY) == RiskLevel.LOW
        assert self.profile.get_tolerance_level(RiskCategory.PERFORMANCE) == RiskLevel.MEDIUM
    
    def test_get_tolerance_level_unknown_category(self):
        """Test getting the tolerance level for an unknown risk category."""
        # Create a mock category that's not in the profile
        mock_category = MagicMock()
        mock_category.value = "unknown_category"
        
        # Should return MINIMAL risk level for unknown categories
        assert self.profile.get_tolerance_level(mock_category) == RiskLevel.MINIMAL
    
    def test_update_tolerance_level(self):
        """Test updating the tolerance level for a specific risk category."""
        # Update an existing category
        self.profile.update_tolerance_level(RiskCategory.FINANCIAL, RiskLevel.HIGH)
        assert self.profile.get_tolerance_level(RiskCategory.FINANCIAL) == RiskLevel.HIGH
        
        # Update a new category
        mock_category = MagicMock()
        mock_category.value = "test_category"
        self.profile.update_tolerance_level(mock_category, RiskLevel.MEDIUM)
        assert self.profile.get_tolerance_level(mock_category) == RiskLevel.MEDIUM
    
    def test_to_dict(self):
        """Test converting the profile to a dictionary."""
        profile_dict = self.profile.to_dict()
        
        assert profile_dict["name"] == "Test Profile"
        assert profile_dict["description"] == "A test risk profile"
        assert "tolerance_levels" in profile_dict
        
        # Check that the tolerance levels are correctly converted
        tolerance_levels = profile_dict["tolerance_levels"]
        assert tolerance_levels["financial"] == "medium"
        assert tolerance_levels["reputation"] == "low"
        assert tolerance_levels["operational"] == "high"
        assert tolerance_levels["compliance"] == "minimal"
        assert tolerance_levels["security"] == "low"
        assert tolerance_levels["performance"] == "medium"
    
    def test_from_dict(self):
        """Test creating a profile from a dictionary."""
        profile_dict = {
            "name": "Test Profile",
            "description": "A test risk profile",
            "tolerance_levels": {
                "financial": "medium",
                "reputation": "low",
                "operational": "high",
                "compliance": "minimal",
                "security": "low",
                "performance": "medium"
            }
        }
        
        profile = RiskToleranceProfile.from_dict(profile_dict)
        
        assert profile.name == "Test Profile"
        assert profile.description == "A test risk profile"
        assert profile.get_tolerance_level(RiskCategory.FINANCIAL) == RiskLevel.MEDIUM
        assert profile.get_tolerance_level(RiskCategory.REPUTATION) == RiskLevel.LOW
        assert profile.get_tolerance_level(RiskCategory.OPERATIONAL) == RiskLevel.HIGH
        assert profile.get_tolerance_level(RiskCategory.COMPLIANCE) == RiskLevel.MINIMAL
        assert profile.get_tolerance_level(RiskCategory.SECURITY) == RiskLevel.LOW
        assert profile.get_tolerance_level(RiskCategory.PERFORMANCE) == RiskLevel.MEDIUM

class TestRiskAssessment:
    """Test the RiskAssessment class."""
    
    def setup_method(self):
        """Set up the test environment."""
        self.tolerance_levels = {
            RiskCategory.FINANCIAL: RiskLevel.MEDIUM,
            RiskCategory.REPUTATION: RiskLevel.LOW,
            RiskCategory.OPERATIONAL: RiskLevel.HIGH,
            RiskCategory.COMPLIANCE: RiskLevel.MINIMAL,
            RiskCategory.SECURITY: RiskLevel.LOW,
            RiskCategory.PERFORMANCE: RiskLevel.MEDIUM
        }
        
        self.profile = RiskToleranceProfile(
            name="Test Profile",
            description="A test risk profile",
            tolerance_levels=self.tolerance_levels
        )
        
        self.risk_assessment = RiskAssessment(self.profile)
    
    def test_init(self):
        """Test the initialization of the risk assessment."""
        assert self.risk_assessment.profile == self.profile
    
    def test_assess_risk(self):
        """Test assessing the risk of an action."""
        # Test with minimal context
        context = {}
        assessment = self.risk_assessment.assess_risk("test_action", context)
        
        # All categories should have minimal risk
        for category in RiskCategory:
            assert assessment[category] == RiskLevel.MINIMAL
        
        # Test with financial risk
        context = {"amount": 1500}
        assessment = self.risk_assessment.assess_risk("test_action", context)
        assert assessment[RiskCategory.FINANCIAL] == RiskLevel.CRITICAL
        
        # Test with reputation risk
        context = {"public": True}
        assessment = self.risk_assessment.assess_risk("test_action", context)
        assert assessment[RiskCategory.REPUTATION] == RiskLevel.MEDIUM
        
        # Test with compliance risk
        context = {"regulated": True}
        assessment = self.risk_assessment.assess_risk("test_action", context)
        assert assessment[RiskCategory.COMPLIANCE] == RiskLevel.HIGH
        
        # Test with security risk
        context = {"sensitive_data": True}
        assessment = self.risk_assessment.assess_risk("test_action", context)
        assert assessment[RiskCategory.SECURITY] == RiskLevel.HIGH
        
        # Test with operational risk
        context = {"critical_system": True}
        assessment = self.risk_assessment.assess_risk("test_action", context)
        assert assessment[RiskCategory.OPERATIONAL] == RiskLevel.HIGH
        
        # Test with performance risk
        context = {"resource_intensive": True}
        assessment = self.risk_assessment.assess_risk("test_action", context)
        assert assessment[RiskCategory.PERFORMANCE] == RiskLevel.MEDIUM
        
        # Test with multiple risk factors
        context = {
            "amount": 600,
            "public": True,
            "regulated": True,
            "sensitive_data": True,
            "critical_system": True,
            "resource_intensive": True
        }
        assessment = self.risk_assessment.assess_risk("test_action", context)
        assert assessment[RiskCategory.FINANCIAL] == RiskLevel.HIGH
        assert assessment[RiskCategory.REPUTATION] == RiskLevel.MEDIUM
        assert assessment[RiskCategory.COMPLIANCE] == RiskLevel.HIGH
        assert assessment[RiskCategory.SECURITY] == RiskLevel.HIGH
        assert assessment[RiskCategory.OPERATIONAL] == RiskLevel.HIGH
        assert assessment[RiskCategory.PERFORMANCE] == RiskLevel.MEDIUM
    
    def test_is_within_tolerance(self):
        """Test determining if a risk assessment is within tolerance levels."""
        # Test with all risks within tolerance
        assessment = {
            RiskCategory.FINANCIAL: RiskLevel.LOW,
            RiskCategory.REPUTATION: RiskLevel.LOW,
            RiskCategory.OPERATIONAL: RiskLevel.MEDIUM,
            RiskCategory.COMPLIANCE: RiskLevel.MINIMAL,
            RiskCategory.SECURITY: RiskLevel.LOW,
            RiskCategory.PERFORMANCE: RiskLevel.LOW
        }
        
        within_tolerance, reason = self.risk_assessment.is_within_tolerance(assessment)
        assert within_tolerance is True
        assert reason is None
        
        # Test with one risk exceeding tolerance
        assessment[RiskCategory.FINANCIAL] = RiskLevel.HIGH
        within_tolerance, reason = self.risk_assessment.is_within_tolerance(assessment)
        assert within_tolerance is False
        assert "Risk level high for financial exceeds tolerance level medium" in reason
        
        # Test with multiple risks exceeding tolerance
        assessment[RiskCategory.REPUTATION] = RiskLevel.MEDIUM
        assessment[RiskCategory.COMPLIANCE] = RiskLevel.LOW
        within_tolerance, reason = self.risk_assessment.is_within_tolerance(assessment)
        assert within_tolerance is False
        # The reason should mention the first category that exceeds tolerance
        assert "Risk level high for financial exceeds tolerance level medium" in reason

class TestDefaultProfiles:
    """Test the default risk tolerance profiles."""
    
    def test_create_default_profiles(self):
        """Test creating the default risk tolerance profiles."""
        profiles = create_default_profiles()
        
        assert "conservative" in profiles
        assert "balanced" in profiles
        assert "aggressive" in profiles
        
        # Test the conservative profile
        conservative = profiles["conservative"]
        assert conservative.name == "Conservative"
        assert conservative.get_tolerance_level(RiskCategory.FINANCIAL) == RiskLevel.LOW
        assert conservative.get_tolerance_level(RiskCategory.REPUTATION) == RiskLevel.LOW
        assert conservative.get_tolerance_level(RiskCategory.OPERATIONAL) == RiskLevel.LOW
        assert conservative.get_tolerance_level(RiskCategory.COMPLIANCE) == RiskLevel.MINIMAL
        assert conservative.get_tolerance_level(RiskCategory.SECURITY) == RiskLevel.MINIMAL
        assert conservative.get_tolerance_level(RiskCategory.PERFORMANCE) == RiskLevel.MEDIUM
        
        # Test the balanced profile
        balanced = profiles["balanced"]
        assert balanced.name == "Balanced"
        assert balanced.get_tolerance_level(RiskCategory.FINANCIAL) == RiskLevel.MEDIUM
        assert balanced.get_tolerance_level(RiskCategory.REPUTATION) == RiskLevel.MEDIUM
        assert balanced.get_tolerance_level(RiskCategory.OPERATIONAL) == RiskLevel.MEDIUM
        assert balanced.get_tolerance_level(RiskCategory.COMPLIANCE) == RiskLevel.LOW
        assert balanced.get_tolerance_level(RiskCategory.SECURITY) == RiskLevel.LOW
        assert balanced.get_tolerance_level(RiskCategory.PERFORMANCE) == RiskLevel.MEDIUM
        
        # Test the aggressive profile
        aggressive = profiles["aggressive"]
        assert aggressive.name == "Aggressive"
        assert aggressive.get_tolerance_level(RiskCategory.FINANCIAL) == RiskLevel.HIGH
        assert aggressive.get_tolerance_level(RiskCategory.REPUTATION) == RiskLevel.HIGH
        assert aggressive.get_tolerance_level(RiskCategory.OPERATIONAL) == RiskLevel.HIGH
        assert aggressive.get_tolerance_level(RiskCategory.COMPLIANCE) == RiskLevel.MEDIUM
        assert aggressive.get_tolerance_level(RiskCategory.SECURITY) == RiskLevel.MEDIUM
        assert aggressive.get_tolerance_level(RiskCategory.PERFORMANCE) == RiskLevel.HIGH
