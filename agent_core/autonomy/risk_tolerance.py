"""
Risk Tolerance Framework for the Nick the Great Unified Agent.

This module implements the risk tolerance framework that determines the level of risk
the agent is willing to take in different contexts.
"""

import logging
import enum
from typing import Dict, Any, Optional, List, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RiskLevel(enum.Enum):
    """Risk levels for agent actions."""
    MINIMAL = "minimal"  # Very low risk, almost no chance of negative outcomes
    LOW = "low"  # Low risk, small chance of minor negative outcomes
    MEDIUM = "medium"  # Medium risk, moderate chance of negative outcomes
    HIGH = "high"  # High risk, significant chance of negative outcomes
    CRITICAL = "critical"  # Critical risk, high chance of severe negative outcomes

class RiskCategory(enum.Enum):
    """Categories of risk that the agent can encounter."""
    FINANCIAL = "financial"  # Risk related to financial losses
    REPUTATION = "reputation"  # Risk related to reputation damage
    OPERATIONAL = "operational"  # Risk related to operational disruptions
    COMPLIANCE = "compliance"  # Risk related to regulatory compliance
    SECURITY = "security"  # Risk related to security breaches
    PERFORMANCE = "performance"  # Risk related to performance degradation

class RiskToleranceProfile:
    """
    Risk tolerance profile for the agent.
    
    This class defines the risk tolerance levels for different risk categories.
    """
    
    def __init__(self, name: str, description: str, tolerance_levels: Dict[RiskCategory, RiskLevel]):
        """
        Initialize the risk tolerance profile.
        
        Args:
            name: The name of the profile
            description: A description of the profile
            tolerance_levels: A dictionary mapping risk categories to risk levels
        """
        self.name = name
        self.description = description
        self.tolerance_levels = tolerance_levels
        logger.info(f"Created risk tolerance profile: {name}")
    
    def get_tolerance_level(self, category: RiskCategory) -> RiskLevel:
        """
        Get the tolerance level for a specific risk category.
        
        Args:
            category: The risk category
        
        Returns:
            RiskLevel: The tolerance level for the category
        """
        if category not in self.tolerance_levels:
            logger.warning(f"Unknown risk category: {category}. Using MINIMAL risk tolerance.")
            return RiskLevel.MINIMAL
        
        return self.tolerance_levels[category]
    
    def update_tolerance_level(self, category: RiskCategory, level: RiskLevel) -> None:
        """
        Update the tolerance level for a specific risk category.
        
        Args:
            category: The risk category
            level: The new tolerance level
        """
        self.tolerance_levels[category] = level
        logger.info(f"Updated risk tolerance for {category.value} to {level.value}")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the profile to a dictionary.
        
        Returns:
            Dict: The profile as a dictionary
        """
        return {
            "name": self.name,
            "description": self.description,
            "tolerance_levels": {category.value: level.value for category, level in self.tolerance_levels.items()}
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RiskToleranceProfile':
        """
        Create a profile from a dictionary.
        
        Args:
            data: The dictionary containing the profile data
        
        Returns:
            RiskToleranceProfile: The created profile
        """
        tolerance_levels = {
            RiskCategory(category): RiskLevel(level)
            for category, level in data.get("tolerance_levels", {}).items()
        }
        
        return cls(
            name=data.get("name", "Unknown"),
            description=data.get("description", ""),
            tolerance_levels=tolerance_levels
        )

class RiskAssessment:
    """
    Risk assessment for agent actions.
    
    This class provides methods for assessing the risk of agent actions.
    """
    
    def __init__(self, profile: RiskToleranceProfile):
        """
        Initialize the risk assessment.
        
        Args:
            profile: The risk tolerance profile to use
        """
        self.profile = profile
        logger.info(f"Initialized risk assessment with profile: {profile.name}")
    
    def assess_risk(self, action: str, context: Dict[str, Any]) -> Dict[RiskCategory, RiskLevel]:
        """
        Assess the risk of an action in a specific context.
        
        Args:
            action: The action to assess
            context: The context in which the action is being performed
        
        Returns:
            Dict[RiskCategory, RiskLevel]: The risk assessment for each category
        """
        # This is a simplified implementation. In a real system, this would use
        # more sophisticated risk assessment algorithms.
        
        # Default to minimal risk for all categories
        assessment = {category: RiskLevel.MINIMAL for category in RiskCategory}
        
        # Assess financial risk
        if "amount" in context:
            amount = context["amount"]
            if amount > 1000:
                assessment[RiskCategory.FINANCIAL] = RiskLevel.CRITICAL
            elif amount > 500:
                assessment[RiskCategory.FINANCIAL] = RiskLevel.HIGH
            elif amount > 100:
                assessment[RiskCategory.FINANCIAL] = RiskLevel.MEDIUM
            elif amount > 10:
                assessment[RiskCategory.FINANCIAL] = RiskLevel.LOW
        
        # Assess reputation risk
        if "public" in context and context["public"]:
            assessment[RiskCategory.REPUTATION] = RiskLevel.MEDIUM
        
        # Assess compliance risk
        if "regulated" in context and context["regulated"]:
            assessment[RiskCategory.COMPLIANCE] = RiskLevel.HIGH
        
        # Assess security risk
        if "sensitive_data" in context and context["sensitive_data"]:
            assessment[RiskCategory.SECURITY] = RiskLevel.HIGH
        
        # Assess operational risk
        if "critical_system" in context and context["critical_system"]:
            assessment[RiskCategory.OPERATIONAL] = RiskLevel.HIGH
        
        # Assess performance risk
        if "resource_intensive" in context and context["resource_intensive"]:
            assessment[RiskCategory.PERFORMANCE] = RiskLevel.MEDIUM
        
        logger.info(f"Risk assessment for action '{action}': {assessment}")
        return assessment
    
    def is_within_tolerance(self, assessment: Dict[RiskCategory, RiskLevel]) -> Tuple[bool, Optional[str]]:
        """
        Determine if a risk assessment is within the tolerance levels.
        
        Args:
            assessment: The risk assessment
        
        Returns:
            Tuple[bool, Optional[str]]: (within_tolerance, reason)
        """
        for category, level in assessment.items():
            tolerance = self.profile.get_tolerance_level(category)
            
            if self._risk_level_to_value(level) > self._risk_level_to_value(tolerance):
                reason = f"Risk level {level.value} for {category.value} exceeds tolerance level {tolerance.value}"
                logger.warning(reason)
                return False, reason
        
        return True, None
    
    def _risk_level_to_value(self, level: RiskLevel) -> int:
        """
        Convert a risk level to a numeric value for comparison.
        
        Args:
            level: The risk level
        
        Returns:
            int: The numeric value
        """
        values = {
            RiskLevel.MINIMAL: 1,
            RiskLevel.LOW: 2,
            RiskLevel.MEDIUM: 3,
            RiskLevel.HIGH: 4,
            RiskLevel.CRITICAL: 5
        }
        return values.get(level, 0)

# Create default risk tolerance profiles
def create_default_profiles() -> Dict[str, RiskToleranceProfile]:
    """
    Create default risk tolerance profiles.
    
    Returns:
        Dict[str, RiskToleranceProfile]: The default profiles
    """
    conservative = RiskToleranceProfile(
        name="Conservative",
        description="A conservative risk profile that minimizes risk across all categories",
        tolerance_levels={
            RiskCategory.FINANCIAL: RiskLevel.LOW,
            RiskCategory.REPUTATION: RiskLevel.LOW,
            RiskCategory.OPERATIONAL: RiskLevel.LOW,
            RiskCategory.COMPLIANCE: RiskLevel.MINIMAL,
            RiskCategory.SECURITY: RiskLevel.MINIMAL,
            RiskCategory.PERFORMANCE: RiskLevel.MEDIUM
        }
    )
    
    balanced = RiskToleranceProfile(
        name="Balanced",
        description="A balanced risk profile with moderate risk tolerance",
        tolerance_levels={
            RiskCategory.FINANCIAL: RiskLevel.MEDIUM,
            RiskCategory.REPUTATION: RiskLevel.MEDIUM,
            RiskCategory.OPERATIONAL: RiskLevel.MEDIUM,
            RiskCategory.COMPLIANCE: RiskLevel.LOW,
            RiskCategory.SECURITY: RiskLevel.LOW,
            RiskCategory.PERFORMANCE: RiskLevel.MEDIUM
        }
    )
    
    aggressive = RiskToleranceProfile(
        name="Aggressive",
        description="An aggressive risk profile with high risk tolerance",
        tolerance_levels={
            RiskCategory.FINANCIAL: RiskLevel.HIGH,
            RiskCategory.REPUTATION: RiskLevel.HIGH,
            RiskCategory.OPERATIONAL: RiskLevel.HIGH,
            RiskCategory.COMPLIANCE: RiskLevel.MEDIUM,
            RiskCategory.SECURITY: RiskLevel.MEDIUM,
            RiskCategory.PERFORMANCE: RiskLevel.HIGH
        }
    )
    
    return {
        "conservative": conservative,
        "balanced": balanced,
        "aggressive": aggressive
    }
