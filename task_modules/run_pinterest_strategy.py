#!/usr/bin/env python3
"""
Script to run the Pinterest strategy task.
"""

import os
import sys
import json
import argparse
import logging
import pymongo
from bson import ObjectId
from datetime import datetime
from dotenv import load_dotenv
from pinterest_strategy_task import PinterestStrategyTask

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def connect_to_mongodb():
    """Connect to MongoDB and return the database instance."""
    # Load MongoDB connection string from environment variables
    mongo_uri = os.getenv('MONGODB_URI')
    if not mongo_uri:
        raise ValueError("MONGODB_URI environment variable is not set")

    # Connect to MongoDB
    client = pymongo.MongoClient(mongo_uri)
    db_name = os.getenv('MONGODB_DB_NAME', 'nick_the_great')
    db = client[db_name]

    return db

def main():
    """Run the Pinterest strategy task."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run Pinterest strategy task')
    parser.add_argument('--strategy_id', required=True, help='Strategy ID from MongoDB')
    parser.add_argument('--niche', required=True, help='Business niche')
    parser.add_argument('--target_audience', required=True, help='Target audience')
    parser.add_argument('--business_goal', required=True, help='Business goal')
    parser.add_argument('--num_pins', type=int, default=5, help='Number of pins to generate')
    args = parser.parse_args()

    try:
        # Load environment variables
        load_dotenv()

        # Connect to MongoDB
        db = connect_to_mongodb()

        # Update strategy status to 'processing'
        db.strategies.update_one(
            {'_id': ObjectId(args.strategy_id)},
            {'$set': {'status': 'processing', 'processingStartedAt': datetime.now()}}
        )

        # Initialize and run the Pinterest strategy task
        task = PinterestStrategyTask()
        result = task.execute(
            niche=args.niche,
            target_audience=args.target_audience,
            business_goal=args.business_goal,
            num_pins=args.num_pins
        )

        # Update the strategy document with the result
        update_data = {
            'status': 'completed' if result.get('status') == 'success' else 'failed',
            'completedAt': datetime.now(),
            'result': result
        }

        db.strategies.update_one(
            {'_id': ObjectId(args.strategy_id)},
            {'$set': update_data}
        )

        logger.info(f"Pinterest strategy task completed for strategy {args.strategy_id}")
        return 0
    except Exception as e:
        logger.error(f"Error running Pinterest strategy task: {e}", exc_info=True)

        # Update strategy status to 'failed'
        try:
            db.strategies.update_one(
                {'_id': ObjectId(args.strategy_id)},
                {
                    '$set': {
                        'status': 'failed',
                        'error': str(e),
                        'completedAt': datetime.now()
                    }
                }
            )
        except Exception as update_error:
            logger.error(f"Error updating strategy status: {update_error}")

        return 1

if __name__ == '__main__':
    sys.exit(main())
