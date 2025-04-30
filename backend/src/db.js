const { MongoClient, ServerApiVersion } = require('mongodb');
require('dotenv').config();

// Get MongoDB connection URI from environment variables
const uri = process.env.MONGODB_URI;

// Create a MongoClient with a MongoClientOptions object to set the Stable API version
const client = new MongoClient(uri, {
  serverApi: {
    version: ServerApiVersion.v1,
    strict: true,
    deprecationErrors: true,
  }
});

let db;

/**
 * Connect to MongoDB
 * @returns {Promise<object>} MongoDB database instance
 */
async function connectToDatabase() {
  if (db) return db;
  
  try {
    // Connect to the MongoDB cluster
    await client.connect();
    
    // Verify connection with a ping
    await client.db("admin").command({ ping: 1 });
    console.log("Successfully connected to MongoDB!");
    
    // Get the database instance
    db = client.db("nick_agent");
    return db;
  } catch (error) {
    console.error("Failed to connect to MongoDB:", error);
    throw error;
  }
}

/**
 * Close the MongoDB connection
 */
async function closeConnection() {
  if (client) {
    await client.close();
    console.log("MongoDB connection closed.");
  }
}

// Process terminate handlers
process.on('SIGINT', async () => {
  await closeConnection();
  process.exit(0);
});

process.on('SIGTERM', async () => {
  await closeConnection();
  process.exit(0);
});

module.exports = {
  connectToDatabase,
  closeConnection,
  getClient: () => client
};
