"""
Main application file for Pinterest automation.
"""

import logging
from .utils.config import get_config
from .api.auth import PinterestAuth
from apscheduler.schedulers.background import BackgroundScheduler

logger = logging.getLogger(__name__)

def main():
    """Main function to run the Pinterest automation."""
    
    # Load configuration
    config = get_config(env_file=".env")
    
    # Validate configuration
    if not config.validate():
        logger.critical("Invalid configuration. Exiting.")
        return
    
    logger.info("Starting Pinterest automation...")
    logger.info(str(config))
    logger.debug("This is a test debug message")
    logger.info("This is a test info message")
    logger.warning("This is a test warning message")
    logger.error("This is a test error message")
    logger.critical("This is a test critical message")
    
    # Authenticate with Pinterest API
    auth = PinterestAuth()
    if not auth.is_authorized():
        logger.warning("Not authorized with Pinterest API. Please run the authorization flow.")
        
        # Get authorization URL
        auth_url = auth.get_authorization_url(redirect_uri="http://localhost:3000/callback")
        logger.info(f"Please visit the following URL to authorize the application:\n{auth_url}")
        
        # Get authorization code from user
        code = input("Enter the authorization code from the redirect URL: ")
        
        try:
            # Exchange code for tokens
            auth.exchange_code_for_tokens(code=code, redirect_uri="http://localhost:3000/callback")
            logger.info("Successfully obtained access and refresh tokens.")
        except ValueError as e:
            logger.error(f"Failed to obtain tokens: {e}")
            return
    else:
        logger.info("Successfully authorized with Pinterest API.")
    
    # Create a scheduler
    scheduler = BackgroundScheduler()
    
    # TODO: Schedule pin creation and analytics collection tasks
    
    # Start the scheduler
    scheduler.start()
    
    logger.info("Pinterest automation running...")
    
    try:
        # Keep the main thread alive
        while True:
            import time
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        logger.info("Shutting down scheduler...")
        scheduler.shutdown()
        logger.info("Scheduler shut down.")

if __name__ == "__main__":
    main()
