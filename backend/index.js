const express = require("express");
const cors = require("cors");
const jwt = require("jsonwebtoken");
const dotenv = require("dotenv");
const bcrypt = require("bcryptjs");
const { connectToDatabase, getClient } = require("./db");
const {
  createExperiment,
  startExperiment,
  stopExperiment,
  getExperimentStatus,
  getAgentStatus,
  listExperiments,
  getLogs,
  approveDecision,
  stopAgent,
  ExperimentType, // Import enums/types
  Struct // Import Struct
} = require('./src/agent_client');
const experimentService = require('./src/services/experimentService');
const syncService = require('./src/services/syncService');
const grpcServer = require('./src/grpc_server');
const logger = require('./src/utils/logger');

// Load environment variables
dotenv.config();

// Initialize Express app
const app = express();

// --- Logging Middleware ---
// Log all incoming requests (method, URL, headers)
app.use((req, res, next) => {
  console.log(`Request Method: ${req.method}`);
  console.log(`Request URL: ${req.url}`);
  console.log(`Request Headers: ${JSON.stringify(req.headers)}`);
  next();
});
// --- End Logging Middleware ---

// --- CORS Configuration ---
// Simplify CORS for development/testing
const corsOptions = {
  origin: '*', // Allow all origins
  credentials: true, // Still allow credentials (cookies, auth headers)
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'], // Allow common HTTP methods
  allowedHeaders: ['Content-Type', 'Authorization', 'X-Requested-With'], // Allow necessary headers
  optionsSuccessStatus: 200 // Compatibility for preflight requests
};

app.use(cors(corsOptions));
// --- End CORS Configuration ---

// Handle OPTIONS requests (preflight) explicitly for all routes
// This should come BEFORE other routes or general CORS middleware for other methods
app.options('*', cors(corsOptions));

// Apply CORS middleware for all other requests (GET, POST, etc.)
app.use(cors(corsOptions));
// --- End CORS Configuration ---

app.use(express.json());

// MongoDB connection variable
let db;

// Authentication middleware (remains the same)
function authenticateToken(req, res, next) {
  const authHeader = req.headers["authorization"];
  const token = authHeader && authHeader.split(" ")[1];

  if (!token) {
    return res.status(401).json({ message: "Authentication required" });
  }

  // Use a default secret for verification if not set, but log a warning
  const secret = process.env.JWT_SECRET;
  if (!secret) {
      console.warn("Warning: JWT_SECRET environment variable is not set. Using default for verification.");
  }

  jwt.verify(token, secret || "fallback_secret_for_verification_only", (err, user) => {
    if (err) {
      console.error("JWT Verification Error:", err.message);
      return res.status(403).json({ message: "Invalid or expired token" });
    }
    req.user = user; // Add user payload to request object
    next();
  });
}

// --- Middleware ---
const ensureDbConnected = require('./src/middleware/ensureDbConnected');

// --- API Routes ---

// --- Authentication Endpoints (Changed path from /api/auth to /auth) ---
app.post("/auth/register", async (req, res) => {
  try {
    const { email, password, name } = req.body;

    if (!email || !password || !name) {
      return res.status(400).json({ message: "Email, password, and name are required" });
    }

    // Ensure db is connected
    if (!db) {
        return res.status(500).json({ message: "Database not connected" });
    }

    // Check if user already exists
    const existingUser = await db.collection("users").findOne({ email });
    if (existingUser) {
      return res.status(409).json({ message: "User already exists with this email" });
    }

    // Hash password
    const salt = await bcrypt.genSalt(10);
    const hashedPassword = await bcrypt.hash(password, salt);

    // Create user document
    const newUser = {
      email,
      password: hashedPassword,
      name,
      role: "user", // Default role
      createdAt: new Date(),
      updatedAt: new Date(),
      // Add any default settings if needed
    };

    const result = await db.collection("users").insertOne(newUser);

    // Don't send password back
    const userForToken = {
        id: result.insertedId.toString(),
        email: newUser.email,
        name: newUser.name,
        role: newUser.role
    };

    // Generate JWT token
    const secret = process.env.JWT_SECRET;
    if (!secret) {
        console.error("Error: JWT_SECRET environment variable is not set for token signing.");
        return res.status(500).json({ message: "Internal server error: JWT secret not configured." });
    }
    const token = jwt.sign(userForToken, secret, { expiresIn: "24h" });

    res.status(201).json({
      message: "Registration successful",
      token,
      user: userForToken // Send user info (without password)
    });

  } catch (error) {
    console.error("Registration Error:", error);
    res.status(500).json({ message: "Error during registration", error: error.message });
  }
});

app.post("/auth/login", async (req, res) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ message: "Email and password are required" });
    }

    // Ensure db is connected
    if (!db) {
        return res.status(500).json({ message: "Database not connected" });
    }

    // Find user
    const user = await db.collection("users").findOne({ email });
    if (!user) {
      return res.status(401).json({ message: "Invalid credentials" });
    }

    // Verify password
    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) {
      return res.status(401).json({ message: "Invalid credentials" });
    }

    // Prepare user payload for token (exclude password)
    const userForToken = {
        id: user._id.toString(),
        email: user.email,
        name: user.name,
        role: user.role
    };

    // Generate JWT token
    const secret = process.env.JWT_SECRET;
    if (!secret) {
        console.error("Error: JWT_SECRET environment variable is not set for token signing.");
        return res.status(500).json({ message: "Internal server error: JWT secret not configured." });
    }
    const token = jwt.sign(userForToken, secret, { expiresIn: "24h" });

    res.json({
      message: "Login successful",
      token,
      user: userForToken // Send user info (without password)
    });

  } catch (error) {
    console.error("Login Error:", error);
    res.status(500).json({ message: "Error during login", error: error.message });
  }
});

// --- Other API Routes (Agent config, Strategies, etc.) ---
// These routes use the authenticateToken middleware and retain the /api prefix

app.get("/api/agent/config", authenticateToken, async (req, res) => {
  // Ensure db is connected
  if (!db) return res.status(500).json({ message: "Database not connected" });
  try {
    // Use req.user.id from the verified token payload
    const config = await db.collection("configurations").findOne({ userId: req.user.id });
    res.json(config || {});
  } catch (error) {
    res.status(500).json({ message: "Error fetching agent configuration", error: error.message });
  }
});

app.put("/api/agent/config", authenticateToken, async (req, res) => {
  // Ensure db is connected
  if (!db) return res.status(500).json({ message: "Database not connected" });
  try {
    // Use req.user.id from the verified token payload
    const result = await db.collection("configurations").updateOne(
      { userId: req.user.id },
      { $set: req.body },
      { upsert: true }
    );
    res.json({ message: "Configuration updated", result });
  } catch (error) {
    res.status(500).json({ message: "Error updating agent configuration", error: error.message });
  }
});

// Endpoint to list all experiments
app.get("/api/agent/experiments", authenticateToken, async (req, res) => {
    try {
        // Get page and limit from query parameters
        const page = parseInt(req.query.page) || 1;
        const limit = parseInt(req.query.limit) || 10;

        // Build filters based on query parameters
        const filters = { userId: req.user.id };

        // Add type filter if provided
        if (req.query.type) {
            filters.type = req.query.type;
        }

        // Add state filter if provided
        if (req.query.state) {
            filters.state = req.query.state;
        }

        // Get experiments from database with pagination
        const result = await experimentService.listExperiments(filters, page, limit);

        res.json(result);
    } catch (error) {
        logger.error("List Experiments Error:", error);
        res.status(500).json({ message: "Error listing experiments", error: error.message });
    }
});

// Endpoint to get a specific experiment by ID
app.get("/api/agent/experiments/:experimentId", authenticateToken, async (req, res) => {
    try {
        const experimentId = req.params.experimentId;

        // Check if experiment exists in database
        const experiment = await experimentService.getExperimentById(experimentId);
        if (!experiment) {
            return res.status(404).json({ message: `Experiment with ID ${experimentId} not found` });
        }

        // Check if user owns this experiment
        if (experiment.userId !== req.user.id) {
            return res.status(403).json({ message: "You don't have permission to view this experiment" });
        }

        // Get status from Agent Core to ensure we have the latest data
        try {
            const agentCoreStatus = await getExperimentStatus(experimentId);

            // If Agent Core has updated status, update our database
            if (agentCoreStatus && agentCoreStatus.id && agentCoreStatus.id.id === experimentId) {
                await experimentService.updateExperiment(agentCoreStatus);

                // Get fresh experiment data from database
                const updatedExperiment = await experimentService.getExperimentById(experimentId);
                return res.json(updatedExperiment);
            }
        } catch (error) {
            // If we can't get status from Agent Core, just return the database version
            logger.warn(`Could not get experiment status from Agent Core: ${error.message}`);
        }

        // Return the experiment from database
        res.json(experiment);
    } catch (error) {
        logger.error("Get Experiment Error:", error);
        res.status(500).json({ message: "Error fetching experiment", error: error.message });
    }
});

// Endpoint to create an experiment
app.post("/api/agent/experiments", authenticateToken, async (req, res) => {
    try {
        const { type, name, description, parameters } = req.body;

        if (type === undefined || !name || !description || !parameters) {
            return res.status(400).json({ message: "Experiment type, name, description, and parameters are required" });
        }

        // Map string type to enum value
        const experimentTypeEnum = ExperimentType[type];
        if (experimentTypeEnum === undefined) {
             return res.status(400).json({ message: `Invalid experiment type: ${type}` });
        }

        // Convert parameters object to protobuf Struct
        const parametersStruct = Struct.fromJavaScript(parameters);

        const experimentDefinition = {
            type: experimentTypeEnum,
            name: name,
            description: description,
            parameters: parametersStruct
        };

        // Create experiment in Agent Core
        const response = await createExperiment(experimentDefinition);

        if (response.status.success) {
            // Get the experiment status from Agent Core
            const experimentStatus = await getExperimentStatus(response.id.id);

            // Store experiment in MongoDB
            await experimentService.createExperiment(experimentStatus, req.user.id);

            // Store the experiment ID in the global list for backward compatibility
            if (!global.experimentIds) {
                global.experimentIds = [];
            }
            global.experimentIds.push(response.id.id);

            res.status(201).json(response);
        } else {
            res.status(500).json(response.status);
        }

    } catch (error) {
        logger.error("Create Experiment Error:", error);
        res.status(500).json({ message: "Error creating experiment", error: error.message });
    }
});

// Endpoint to start an experiment
app.post("/api/agent/experiments/:experimentId/start", authenticateToken, async (req, res) => {
    try {
        const experimentId = req.params.experimentId;

        // Check if experiment exists in database
        const experiment = await experimentService.getExperimentById(experimentId);
        if (!experiment) {
            return res.status(404).json({ message: `Experiment with ID ${experimentId} not found` });
        }

        // Check if user owns this experiment
        if (experiment.userId !== req.user.id) {
            return res.status(403).json({ message: "You don't have permission to start this experiment" });
        }

        // Start experiment in Agent Core
        const response = await startExperiment(experimentId);

        if (response.success) {
            // Get updated status from Agent Core
            const experimentStatus = await getExperimentStatus(experimentId);

            // Update experiment in database
            await experimentService.updateExperiment(experimentStatus);
        }

        res.json(response);
    } catch (error) {
        logger.error("Start Experiment Error:", error);
        res.status(500).json({ message: "Error starting experiment", error: error.message });
    }
});

// Endpoint to stop an experiment
app.post("/api/agent/experiments/:experimentId/stop", authenticateToken, async (req, res) => {
    try {
        const experimentId = req.params.experimentId;

        // Check if experiment exists in database
        const experiment = await experimentService.getExperimentById(experimentId);
        if (!experiment) {
            return res.status(404).json({ message: `Experiment with ID ${experimentId} not found` });
        }

        // Check if user owns this experiment
        if (experiment.userId !== req.user.id) {
            return res.status(403).json({ message: "You don't have permission to stop this experiment" });
        }

        // Stop experiment in Agent Core
        const response = await stopExperiment(experimentId);

        if (response.success) {
            // Get updated status from Agent Core
            const experimentStatus = await getExperimentStatus(experimentId);

            // Update experiment in database
            await experimentService.updateExperiment(experimentStatus);
        }

        res.json(response);
    } catch (error) {
        logger.error("Stop Experiment Error:", error);
        res.status(500).json({ message: "Error stopping experiment", error: error.message });
    }
});

// Endpoint to get the status of a specific experiment
app.get("/api/agent/experiments/:experimentId/status", authenticateToken, async (req, res) => {
    try {
        const experimentId = req.params.experimentId;

        // Check if experiment exists in database
        const experiment = await experimentService.getExperimentById(experimentId);
        if (!experiment) {
            return res.status(404).json({ message: `Experiment with ID ${experimentId} not found` });
        }

        // Check if user owns this experiment
        if (experiment.userId !== req.user.id) {
            return res.status(403).json({ message: "You don't have permission to view this experiment" });
        }

        // Get status from Agent Core
        const agentCoreStatus = await getExperimentStatus(experimentId);

        // If Agent Core has updated status, update our database
        if (agentCoreStatus && agentCoreStatus.id && agentCoreStatus.id.id === experimentId) {
            // Update experiment in database
            await experimentService.updateExperiment(agentCoreStatus);

            // Get fresh experiment data from database
            const updatedExperiment = await experimentService.getExperimentById(experimentId);

            // Return the updated experiment with additional database fields
            res.json({
                ...agentCoreStatus,
                createdAt: updatedExperiment.createdAt,
                updatedAt: updatedExperiment.updatedAt,
                results: updatedExperiment.results
            });
        } else {
            // If Agent Core doesn't have the experiment, return database version
            res.json(experiment.toGrpcFormat());
        }
    } catch (error) {
        logger.error("Get Experiment Status Error:", error);
        res.status(500).json({ message: "Error fetching experiment status", error: error.message });
    }
});


// Endpoint to get experiment metrics history
app.get("/api/agent/experiments/:experimentId/metrics", authenticateToken, async (req, res) => {
    try {
        const experimentId = req.params.experimentId;
        const timeRangeMinutes = parseInt(req.query.timeRange) || 0;
        const limit = parseInt(req.query.limit) || 100;

        // Check if experiment exists in database
        const experiment = await experimentService.getExperimentById(experimentId);
        if (!experiment) {
            return res.status(404).json({ message: `Experiment with ID ${experimentId} not found` });
        }

        // Check if user owns this experiment
        if (experiment.userId !== req.user.id) {
            return res.status(403).json({ message: "You don't have permission to view metrics for this experiment" });
        }

        // Get metrics history from database
        const metrics = await experimentService.getExperimentMetricsHistory(experimentId, timeRangeMinutes, limit);

        res.json(metrics);
    } catch (error) {
        logger.error("Get Experiment Metrics Error:", error);
        res.status(500).json({ message: "Error fetching experiment metrics", error: error.message });
    }
});

app.get("/api/agent/status", authenticateToken, async (_, res) => {
  try {
    const agentStatus = await getAgentStatus();
    res.json(agentStatus);
  } catch (error) {
    logger.error("Get Agent Status Error:", error);
    res.status(500).json({ message: "Error fetching agent status", error: error.message });
  }
});

// Endpoint to get experiment logs
app.get("/api/agent/experiments/:experimentId/logs", authenticateToken, async (req, res) => {
    try {
        const experimentId = req.params.experimentId;
        const limit = parseInt(req.query.limit) || 100;

        // Check if experiment exists in database
        const experiment = await experimentService.getExperimentById(experimentId);
        if (!experiment) {
            return res.status(404).json({ message: `Experiment with ID ${experimentId} not found` });
        }

        // Check if user owns this experiment
        if (experiment.userId !== req.user.id) {
            return res.status(403).json({ message: "You don't have permission to view logs for this experiment" });
        }

        // Build filters based on query parameters
        const filters = {};

        // Add level filter if provided
        if (req.query.level) {
            filters.level = req.query.level;
        }

        // Get logs from database
        const logs = await experimentService.getExperimentLogs(experimentId, filters, limit);

        res.json(logs);
    } catch (error) {
        logger.error("Get Experiment Logs Error:", error);
        res.status(500).json({ message: "Error fetching experiment logs", error: error.message });
    }
});


// New endpoint to approve/reject a decision
app.post("/api/agent/decisions/:decisionId/approve", authenticateToken, async (req, res) => {
    try {
        const decisionId = req.params.decisionId;
        const { approved, comment } = req.body; // boolean approved, optional string comment
        const userId = req.user.id; // Get user ID from token

        if (approved === undefined) {
             return res.status(400).json({ message: "Approval status ('approved' boolean) is required" });
        }

        const response = await approveDecision(decisionId, userId, approved, comment);
        res.json(response);

    } catch (error) {
        console.error("Approve Decision Error:", error);
        res.status(500).json({ message: "Error processing decision approval", error: error.message });
    }
});

// New endpoint for the kill switch
app.post("/api/agent/stop", authenticateToken, async (req, res) => {
    try {
        const { reason } = req.body; // Optional reason
        const response = await stopAgent(reason);
        res.json(response);
    } catch (error) {
        console.error("Stop Agent Error:", error);
        res.status(500).json({ message: "Error stopping agent", error: error.message });
    }
});


// ... (Keep other existing endpoints like /api/strategies, /api/resources, etc.)
// Ensure they also check for db connection if they use it.

// Apply ensureDbConnected middleware to all API routes
app.use('/api', ensureDbConnected);

// Example: Strategy endpoint modification
app.get("/api/strategies", authenticateToken, async (req, res) => {
  try {
    const strategies = await db.collection("strategies")
      .find({ userId: req.user.id })
      .toArray();
    res.json(strategies);
  } catch (error) {
    logger.error(`Error fetching strategies: ${error.message}`);
    res.status(500).json({ message: "Error fetching strategies", error: error.message });
  }
});

// ... (Add similar db checks to other routes using the database)

// --- Start the server ---
// Check if we're running locally (not on Render)
const PORT = process.env.PORT || (process.env.NODE_ENV === 'development' ? 1000 : 10000);

async function startServer() {
  try {
    // Connect to DB and assign to the outer 'db' variable
    const database = await connectToDatabase();
    db = database; // Make db instance available to routes

    // Start the HTTP server
    app.listen(PORT, "0.0.0.0", () => { // Ensure listening on 0.0.0.0
      logger.info(`HTTP server running on port ${PORT}`);
    });

    // Start the gRPC server
    const grpcPort = parseInt(process.env.GRPC_PORT) || 50052;
    await grpcServer.startServer(grpcPort);
    logger.info(`gRPC server running on port ${grpcPort}`);

    // Start the sync service after a short delay to ensure server is up
    setTimeout(() => {
      // Get sync interval from environment variable or use default (30 seconds)
      const syncIntervalMs = parseInt(process.env.SYNC_INTERVAL_MS) || 30000;
      syncService.start(syncIntervalMs);
      logger.info(`Sync service started with interval of ${syncIntervalMs}ms`);
    }, 5000);
  } catch (error) {
      logger.error("Failed to start server:", error);
      process.exit(1);
  }

  // Handle graceful shutdown
  process.on('SIGTERM', gracefulShutdown);
  process.on('SIGINT', gracefulShutdown);
}

// Graceful shutdown function
async function gracefulShutdown() {
  logger.info('Received shutdown signal, closing connections...');

  // Stop the sync service
  syncService.stop();

  // Stop the gRPC server
  try {
    await grpcServer.stopServer();
    logger.info('gRPC server stopped');
  } catch (error) {
    logger.error(`Error stopping gRPC server: ${error.message}`);
  }

  // Close database connection
  try {
    getClient().close();
    logger.info('MongoDB connection closed');
  } catch (error) {
    logger.error(`Error closing MongoDB connection: ${error.message}`);
  }

  logger.info('Server shutdown complete');
  process.exit(0);
}

// For Cloudflare Workers environment (Keep if needed, but likely not used for Render deployment)
// module.exports = app;

// For standalone Node.js environment (This is used by Render)
if (require.main === module) {
  startServer();
}
