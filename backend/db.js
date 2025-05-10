/**
 * MongoDB connection module for the backend.
 * Provides functions to connect to the database and get the client.
 */

const { MongoClient } = require('mongodb');
const logging = require('./src/logging');

// MongoDB connection variables
let client = null;
let db = null;

/**
 * Connect to the MongoDB database
 * @returns {Promise<object>} - The database instance
 */
async function connectToDatabase() {
    try {
        // Get MongoDB connection string from environment variables
        const uri = process.env.MONGODB_URI;
        if (!uri) {
            throw new Error('MONGODB_URI environment variable is not set');
        }

        // Get database name from environment variables or use default
        const dbName = process.env.MONGODB_DB_NAME || 'nickthegreat';

        // Create a new MongoClient if not already created
        if (!client) {
            logging.info('Creating new MongoDB client');
            client = new MongoClient(uri, {
                useNewUrlParser: true,
                useUnifiedTopology: true,
            });
        }

        // Connect to the MongoDB server if not already connected
        if (!client.isConnected) {
            logging.info('Connecting to MongoDB server');
            await client.connect();
            logging.info('Connected to MongoDB server');
        }

        // Get the database instance
        db = client.db(dbName);
        logging.info(`Connected to database: ${dbName}`);

        return db;
    } catch (error) {
        logging.error('Error connecting to MongoDB:', error);
        throw error;
    }
}

/**
 * Get the MongoDB client instance
 * @returns {object} - The MongoDB client
 */
function getClient() {
    if (!client) {
        throw new Error('MongoDB client not initialized. Call connectToDatabase() first.');
    }
    return client;
}

/**
 * Close the MongoDB connection
 * @returns {Promise<void>}
 */
async function closeConnection() {
    if (client) {
        logging.info('Closing MongoDB connection');
        await client.close();
        client = null;
        db = null;
        logging.info('MongoDB connection closed');
    }
}

module.exports = {
    connectToDatabase,
    getClient,
    closeConnection
};
