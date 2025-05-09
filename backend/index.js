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
  getLogs,
  approveDecision,
  stopAgent,
  ExperimentType, // Import enums/types
  Struct // Import Struct
} = require('./src/agent_client');

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

// New endpoint to create an experiment
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

        const response = await createExperiment(experimentDefinition);

        if (response.status.success) {
            // Optionally save experiment details to MongoDB here if needed for persistence beyond Agent Core's memory
            // const dbResult = await db.collection("experiments").insertOne({
            //     _id: response.id.id, // Use the ID generated by Agent Core
            //     userId: req.user.id,
            //     ...experimentDefinition,
            //     state: 'STATE_DEFINED', // Initial state
            //     createdAt: new Date(),
            //     updatedAt: new Date()
            // });
            res.status(201).json(response);
        } else {
            res.status(500).json(response.status);
        }

    } catch (error) {
        console.error("Create Experiment Error:", error);
        res.status(500).json({ message: "Error creating experiment", error: error.message });
    }
});

// New endpoint to start an experiment
app.post("/api/agent/experiments/:experimentId/start", authenticateToken, async (req, res) => {
    try {
        const experimentId = req.params.experimentId;
        const response = await startExperiment(experimentId);
        res.json(response);
    } catch (error) {
        console.error("Start Experiment Error:", error);
        res.status(500).json({ message: "Error starting experiment", error: error.message });
    }
});

// New endpoint to stop an experiment
app.post("/api/agent/experiments/:experimentId/stop", authenticateToken, async (req, res) => {
    try {
        const experimentId = req.params.experimentId;
        const response = await stopExperiment(experimentId);
        res.json(response);
    } catch (error) {
        console.error("Stop Experiment Error:", error);
        res.status(500).json({ message: "Error stopping experiment", error: error.message });
    }
});

// New endpoint to get the status of a specific experiment
app.get("/api/agent/experiments/:experimentId/status", authenticateToken, async (req, res) => {
    try {
        const experimentId = req.params.experimentId;
        const status = await getExperimentStatus(experimentId);
        res.json(status);
    } catch (error) {
        console.error("Get Experiment Status Error:", error);
        res.status(500).json({ message: "Error fetching experiment status", error: error.message });
    }
});


app.get("/api/agent/status", authenticateToken, async (req, res) => {
  try {
    const agentStatus = await getAgentStatus();
    res.json(agentStatus);
  } catch (error) {
    console.error("Get Agent Status Error:", error);
    res.status(500).json({ message: "Error fetching agent status", error: error.message });
  }
});

// New endpoint to stream logs (using server-sent events or websockets if needed, for now just a basic request)
app.get("/api/agent/logs", authenticateToken, async (req, res) => {
    // This is a basic implementation. For true streaming, consider
    // Server-Sent Events (SSE) or WebSockets.
    // For now, we'll just make a single gRPC call and return logs if available
    // The gRPC GetLogs is a stream, so a direct mapping here is complex.
    // A simple approach for now is to perhaps get recent logs if the Agent Core
    // stores them temporarily, or indicate that streaming is needed.

    // As per design, GetLogs is a stream. A simple REST endpoint can't directly
    // map to a gRPC stream response in a single request-response cycle.
    // We'll leave this as a placeholder or return a message indicating streaming is required.
    res.status(501).json({ message: "Log streaming requires a different connection type (e.g., WebSockets or SSE)" });

    // TODO: Implement log streaming using SSE or WebSockets if needed for the frontend
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

// Example: Strategy endpoint modification
app.get("/api/strategies", authenticateToken, async (req, res) => {
  // Ensure db is connected
  if (!db) return res.status(500).json({ message: "Database not connected" });
  try {
    const strategies = await db.collection("strategies")
      .find({ userId: req.user.id })
      .toArray();
    res.json(strategies);
  } catch (error) {
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

    app.listen(PORT, "0.0.0.0", () => { // Ensure listening on 0.0.0.0
      console.log(`Server running on port ${PORT}`);
    });
  } catch (error) {
      console.error("Failed to start server:", error);
      process.exit(1);
  }
}

// For Cloudflare Workers environment (Keep if needed, but likely not used for Render deployment)
// module.exports = app;

// For standalone Node.js environment (This is used by Render)
if (require.main === module) {
  startServer();
}
