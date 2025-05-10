#!/usr/bin/env python3
"""
Script to exchange an authorization code for Pinterest OAuth tokens.
"""

import os
import sys
import json
import argparse
import logging
from dotenv import load_dotenv
from api.auth import PinterestAuth

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Exchange an authorization code for Pinterest OAuth tokens."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Exchange authorization code for Pinterest OAuth tokens')
    parser.add_argument('--code', required=True, help='Authorization code from Pinterest')
    parser.add_argument('--redirect_uri', required=True, help='Redirect URI used for authorization')
    args = parser.parse_args()
    
    try:
        # Load environment variables
        load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', '.env'))
        
        # Initialize Pinterest auth
        auth = PinterestAuth()
        
        # Exchange code for tokens
        tokens = auth.exchange_code_for_tokens(
            code=args.code,
            redirect_uri=args.redirect_uri
        )
        
        # Print the tokens as JSON to stdout
        print(json.dumps(tokens), end='')
        
        return 0
    except Exception as e:
        logger.error(f"Error exchanging code for tokens: {e}", exc_info=True)
        return 1

if __name__ == '__main__':
    sys.exit(main())
