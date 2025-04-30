```javascript
const { MongoClient, ServerApiVersion } = require("mongodb");
require("dotenv").config();

// Get MongoDB connection URI from environment variables
const uri = process.env.MONGODB_URI;

if (!uri) {
  console.error("Error: MONGODB_URI environment variable not set.");
  process.exit(1);
}

// Create a MongoClient with a MongoClientOptions object to set the Stable API version
// Add keepAlive options
const client = new MongoClient(uri, {
  serverApi: {
    version: ServerApiVersion.v1,
    strict: true,
    deprecationErrors: true,
  },
  // Recommended options for long-running applications
  keepAlive: true,
  keepAliveInitialDelay: 300000, // 5 minutes
  connectTimeoutMS: 30000, // 30 seconds
  socketTimeoutMS: 45000, // 45 seconds
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
  client.on("close", () => {
    console.warn("MongoDB connection closed.");
    db = null; // Mark db as null
    // Optionally attempt reconnection here or let the next request trigger it
    // connectToDatabase().catch(err => console.error("Reconnect attempt failed:", err));
  });
  client.on("error", (error) => {
    console.error("MongoDB connection error:", error);
    db = null;
    // Consider specific error handling or reconnection attempts
  });
  client.on("timeout", () => {
    console.warn("MongoDB connection timeout.");
    db = null;
  });
  client.on("serverHeartbeatFailed", (event) => {
    console.warn("MongoDB server heartbeat failed:", event);
  });
  // Note: The node driver handles reconnection attempts automatically by default
  // for certain types of errors. These listeners help log and potentially react
  // to specific states.
}

/**
 * Close the MongoDB connection
 */
async function closeConnection() {
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
```
