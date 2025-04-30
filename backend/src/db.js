const { MongoClient, ServerApiVersion } = require("mongodb");
require("dotenv").config();

// Get MongoDB connection URI from environment variables
const uri = process.env.MONGODB_URI;

if (!uri) {
  console.error("Error: MONGODB_URI environment variable not set.");
  process.exit(1);
}

// Create a MongoClient with a MongoClientOptions object to set the Stable API version
// Use standard TCP keep-alive settings within socketOptions
const client = new MongoClient(uri, {
  serverApi: {
    version: ServerApiVersion.v1,
    strict: true,
    deprecationErrors: true,
  },
  // Standard TCP Keepalive options
  socketTimeoutMS: 45000, // Close sockets after 45 seconds of inactivity
  connectTimeoutMS: 30000, // Connection timeout
  // keepAlive: true, // This option is often implicitly handled or needs specific driver context
  // keepAliveInitialDelay: 300000, // This specific option is not standard
});

let db;
let isConnecting = false;
let connectionPromise = null;

/**
 * Connect to MongoDB with reconnection logic
 * @returns {Promise<object>} MongoDB database instance
 */
async function connectToDatabase() {
  // If already connected, return the db instance
  // Check topology status for a more reliable connection check
  if (db && client.topology && client.topology.isConnected()) {
    // console.log("Using existing MongoDB connection.");
    return db;
  }

  // If currently connecting, return the existing promise
  if (isConnecting && connectionPromise) {
    // console.log("Waiting for existing MongoDB connection attempt...");
    return connectionPromise;
  }

  // console.log("Attempting to connect to MongoDB...");
  isConnecting = true;
  connectionPromise = (async () => {
    try {
      // Connect to the MongoDB cluster
      await client.connect();
      console.log("Successfully connected to MongoDB!");

      // Get the database instance
      db = client.db("nick_agent"); // Ensure this matches your database name

      // Add listeners after successful connection
      addConnectionListeners();

      isConnecting = false;
      return db;
    } catch (error) {
      console.error("Failed to connect to MongoDB:", error);
      isConnecting = false;
      connectionPromise = null; // Reset promise on failure
      // Consider implementing a retry mechanism here if needed
      throw error; // Re-throw error to indicate connection failure
    }
  })();

  return connectionPromise;
}

/**
 * Add listeners to the MongoDB client connection
 */
function addConnectionListeners() {
  // Remove existing listeners to prevent duplicates if connectToDatabase is called again
  client.removeAllListeners("close");
  client.removeAllListeners("error");
  client.removeAllListeners("timeout");
  client.removeAllListeners("serverHeartbeatFailed");

  client.on("close", () => {
    console.warn("MongoDB connection closed.");
    db = null; // Mark db as null
    // The driver attempts reconnection automatically. Logging this event is useful.
  });
  client.on("error", (error) => {
    console.error("MongoDB connection error:", error);
    db = null;
    // Consider specific error handling based on the error type
  });
  client.on("timeout", () => {
    console.warn("MongoDB connection timeout.");
    db = null;
  });
  client.on("serverHeartbeatFailed", (event) => {
    console.warn("MongoDB server heartbeat failed:", event);
  });
}

/**
 * Close the MongoDB connection
 */
async function closeConnection() {
  // Check topology status before attempting to close
  if (client && client.topology && client.topology.isConnected()) {
    try {
      await client.close();
      console.log("MongoDB connection closed gracefully.");
      db = null;
    } catch (error) {
      console.error("Error closing MongoDB connection:", error);
    }
  }
}

// Process terminate handlers
process.on("SIGINT", async () => {
  console.log("Received SIGINT. Closing MongoDB connection...");
  await closeConnection();
  process.exit(0);
});

process.on("SIGTERM", async () => {
  console.log("Received SIGTERM. Closing MongoDB connection...");
  await closeConnection();
  process.exit(0);
});

// Handle unhandled promise rejections (optional but recommended)
process.on("unhandledRejection", (reason, promise) => {
  console.error("Unhandled Rejection at:", promise, "reason:", reason);
  // Application specific logging, throwing an error, or other logic here
});

module.exports = {
  connectToDatabase,
  closeConnection,
  getClient: () => client, // Expose client if needed elsewhere
};

