#!/usr/bin/env python3
"""
Script to generate a Pinterest OAuth authorization URL.
"""

import os
import sys
import argparse
import logging
from dotenv import load_dotenv
from api.auth import PinterestAuth

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Generate and print a Pinterest OAuth authorization URL."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Generate Pinterest OAuth authorization URL')
    parser.add_argument('--redirect_uri', required=True, help='Redirect URI for OAuth callback')
    parser.add_argument('--state', required=True, help='State parameter for CSRF protection')
    parser.add_argument('--scope', help='Comma-separated list of scopes')
    args = parser.parse_args()
    
    try:
        # Load environment variables
        load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', '.env'))
        
        # Initialize Pinterest auth
        auth = PinterestAuth()
        
        # Get authorization URL
        auth_url = auth.get_authorization_url(
            redirect_uri=args.redirect_uri,
            scope=args.scope,
            state=args.state
        )
        
        # Print the URL to stdout
        print(auth_url, end='')
        
        return 0
    except Exception as e:
        logger.error(f"Error generating authorization URL: {e}", exc_info=True)
        return 1

if __name__ == '__main__':
    sys.exit(main())
