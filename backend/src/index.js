const express = require("express");
const cors = require("cors");
const jwt = require("jsonwebtoken");
const dotenv = require("dotenv");
const bcrypt = require("bcryptjs"); // Ensure this is installed and in package.json
// const { Configuration, OpenAIApi } = require("openai"); // Removed OpenAI
const { connectToDatabase, getClient } = require("./db"); // Use the corrected db.js

// Load environment variables
dotenv.config();

// --- JWT Secret Check ---
const JWT_SECRET = process.env.JWT_SECRET;
if (!JWT_SECRET) {
    console.error("FATAL ERROR: JWT_SECRET environment variable is not set.");
    process.exit(1); // Exit if JWT secret is not configured
}
// --- End JWT Secret Check ---

// Initialize Express app
const app = express();

// --- CORS Configuration ---
const allowedOrigins = [
  "https://nick-the-great.vercel.app", // Primary Vercel deployment
  "https://nick-the-great-git-main-colby-chapmans-projects.vercel.app", // Current Vercel preview URL
  "https://nick-the-great-auneyxzhz-colby-chapmans-projects.vercel.app", // Previous preview URL
  "https://nick-the-great-5wvgfpnbc-colby-chapmans-projects.vercel.app", // Latest preview URL
  "http://localhost:3000" // For local development
];

app.use(cors({
  origin: function (origin, callback) {
    if (!origin || allowedOrigins.indexOf(origin) !== -1) {
      callback(null, true);
    } else {
      const msg = `The CORS policy for this site does not allow access from the specified Origin: ${origin}`;
      console.error(msg);
      callback(new Error(msg), false);
    }
  }
}));
// --- End CORS Configuration ---

app.use(express.json());

// MongoDB connection variable
let db;

// --- Google Gemini Configuration Placeholder ---
// const { GoogleGenerativeAI } = require("@google/generative-ai");
// const GEMINI_API_KEY = process.env.GEMINI_API_KEY;
// if (!GEMINI_API_KEY) {
//     console.warn("Warning: GEMINI_API_KEY environment variable is not set. AI features may not work.");
// }
// const genAI = new GoogleGenerativeAI(GEMINI_API_KEY);
// Add functions here to interact with Gemini API
// --- End Google Gemini Configuration ---

// --- Middleware ---

// Authentication middleware
function authenticateToken(req, res, next) {
  const authHeader = req.headers["authorization"];
  const token = authHeader && authHeader.split(" ")[1];

  if (!token) {
    return res.status(401).json({ message: "Authentication required" });
  }

  jwt.verify(token, JWT_SECRET, (err, user) => { // Use the validated JWT_SECRET
    if (err) {
      console.error("JWT Verification Error:", err.message);
      return res.status(403).json({ message: "Invalid or expired token" });
    }
    req.user = user; // Add user payload to request object
    next();
  });
}

// Database connection check middleware
function ensureDbConnected(req, res, next) {
  if (!db) {
    console.error("Database connection not available for request:", req.path);
    return res.status(500).json({ message: "Database not connected" });
  }
  next();
}

// --- End Middleware ---


// --- API Routes ---

// --- Authentication Endpoints (/auth/...) ---
app.post("/auth/register", async (req, res) => {
  // Added ensureDbConnected here as it's needed before auth middleware
  if (!db) {
    console.error("Database connection not available for /auth/register");
    return res.status(500).json({ message: "Database not connected" });
  }
  try {
    const { email, password, name } = req.body;
    if (!email || !password || !name) {
      return res.status(400).json({ message: "Email, password, and name are required" });
    }
    const existingUser = await db.collection("users").findOne({ email });
    if (existingUser) {
      return res.status(409).json({ message: "User already exists with this email" });
    }
    const salt = await bcrypt.genSalt(10);
    const hashedPassword = await bcrypt.hash(password, salt);
    const newUser = {
      email,
      password: hashedPassword,
      name,
      role: "user",
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    const result = await db.collection("users").insertOne(newUser);
    const userForToken = {
        id: result.insertedId.toString(),
        email: newUser.email,
        name: newUser.name,
        role: newUser.role
    };
    const token = jwt.sign(userForToken, JWT_SECRET, { expiresIn: "24h" });
    res.status(201).json({
      message: "Registration successful",
      token,
      user: userForToken
    });
  } catch (error) {
    console.error("Registration Error:", error);
    res.status(500).json({ message: "Error during registration", error: error.message });
  }
});

app.post("/auth/login", async (req, res) => {
  // Added ensureDbConnected here as it's needed before auth middleware
  if (!db) {
    console.error("Database connection not available for /auth/login");
    return res.status(500).json({ message: "Database not connected" });
  }
  try {
    const { email, password } = req.body;
    if (!email || !password) {
      return res.status(400).json({ message: "Email and password are required" });
    }
    const user = await db.collection("users").findOne({ email });
    if (!user) {
      return res.status(401).json({ message: "Invalid credentials" });
    }
    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) {
      return res.status(401).json({ message: "Invalid credentials" });
    }
    const userForToken = {
        id: user._id.toString(),
        email: user.email,
        name: user.name,
        role: user.role
    };
    const token = jwt.sign(userForToken, JWT_SECRET, { expiresIn: "24h" });
    res.json({
      message: "Login successful",
      token,
      user: userForToken
    });
  } catch (error) {
    console.error("Login Error:", error);
    res.status(500).json({ message: "Error during login", error: error.message });
  }
});

// --- Other API Routes (/api/...) ---
// Apply authentication and DB check middleware

app.get("/api/agent/config", authenticateToken, ensureDbConnected, async (req, res) => {
  try {
    const config = await db.collection("configurations").findOne({ userId: req.user.id });
    res.json(config || {});
  } catch (error) {
    res.status(500).json({ message: "Error fetching agent configuration", error: error.message });
  }
});

app.put("/api/agent/config", authenticateToken, ensureDbConnected, async (req, res) => {
  try {
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

app.get("/api/strategies", authenticateToken, ensureDbConnected, async (req, res) => {
  try {
    const strategies = await db.collection("strategies")
      .find({ userId: req.user.id })
      .toArray();
    res.json(strategies);
  } catch (error) {
    res.status(500).json({ message: "Error fetching strategies", error: error.message });
  }
});

// ... (Apply authenticateToken and ensureDbConnected to other /api routes as needed)

// --- Start the server ---
const PORT = process.env.PORT || 10000; // Use 10000 as default for Render

async function startServer() {
  try {
    const database = await connectToDatabase();
    db = database; // Make db instance available globally

    app.listen(PORT, "0.0.0.0", () => {
      console.log(`Server running on port ${PORT}`);
    });
  } catch (error) {
      console.error("Failed to start server:", error);
      process.exit(1);
  }
}

// For standalone Node.js environment (Used by Render)
// Removed check for require.main === module as it's less common with modern practices
// Render's build process typically runs the start command directly.
startServer();

// Removed Cloudflare Workers specific export:
// module.exports = app;
