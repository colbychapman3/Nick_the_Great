"""
Initialize the autonomy and experimentation frameworks.

This script initializes the autonomy and experimentation frameworks and sets up
the circular references between them.
"""

import logging
from autonomy_framework import AutonomyFramework
from experimentation_framework import ExperimentationFramework

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def initialize_frameworks():
    """
    Initialize the autonomy and experimentation frameworks.
    
    Returns:
        Tuple[AutonomyFramework, ExperimentationFramework]: The initialized frameworks
    """
    # Initialize the autonomy framework
    autonomy_framework = AutonomyFramework()
    
    # Initialize the experimentation framework with the autonomy framework
    experimentation_framework = ExperimentationFramework(autonomy_framework)
    
    # Set the experimentation framework in the autonomy framework
    autonomy_framework.set_experimentation_framework(experimentation_framework)
    
    logger.info("Initialized autonomy and experimentation frameworks")
    
    return autonomy_framework, experimentation_framework

# If this script is run directly, initialize the frameworks
if __name__ == "__main__":
    autonomy_framework, experimentation_framework = initialize_frameworks()
