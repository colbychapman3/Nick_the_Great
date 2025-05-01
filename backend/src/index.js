const express = require('express');
const cors = require('cors');
const jwt = require('jsonwebtoken');
const dotenv = require('dotenv');
const bcrypt = require('bcryptjs'); // Import bcrypt
const { connectToDatabase } = require('./db'); // Use the corrected db.js

// Load environment variables
dotenv.config();

// Initialize Express app
const app = express();

// --- CORS Configuration ---
// Define allowed origins
const allowedOrigins = [
  'https://nick-the-great.vercel.app', // Your primary Vercel deployment
  'https://nick-the-great-auneyxzhz-colby-chapmans-projects.vercel.app', // The specific preview URL from logs
  // Add any other frontend URLs if needed (e.g., localhost for development)
  'http://localhost:3000'
];

app.use(cors({
  origin: function (origin, callback) {
    // Allow requests with no origin (like mobile apps or curl requests)
    if (!origin) return callback(null, true);
    if (allowedOrigins.indexOf(origin) === -1) {
      const msg = 'The CORS policy for this site does not allow access from the specified Origin.';
      return callback(new Error(msg), false);
    }
    return callback(null, true);
  }
}));
// --- End CORS Configuration ---

app.use(express.json());

// MongoDB connection variable
let db;

// Authentication middleware (remains the same)
function authenticateToken(req, res, next) {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return res.status(401).json({ message: 'Authentication required' });
  }

  // Use a default secret for verification if not set, but log a warning
  const secret = process.env.JWT_SECRET;
  if (!secret) {
      console.warn('Warning: JWT_SECRET environment variable is not set. Using default for verification.');
  }

  jwt.verify(token, secret || 'fallback_secret_for_verification_only', (err, user) => {
    if (err) {
      console.error('JWT Verification Error:', err.message);
      return res.status(403).json({ message: 'Invalid or expired token' });
    }
    req.user = user; // Add user payload to request object
    next();
  });
}

// --- API Routes ---

// --- Authentication Endpoints ---
app.post('/api/auth/register', async (req, res) => {
  try {
    const { email, password, name } = req.body;

    if (!email || !password || !name) {
      return res.status(400).json({ message: 'Email, password, and name are required' });
    }

    // Ensure db is connected
    if (!db) {
        return res.status(500).json({ message: 'Database not connected' });
    }

    // Check if user already exists
    const existingUser = await db.collection('users').findOne({ email });
    if (existingUser) {
      return res.status(409).json({ message: 'User already exists with this email' });
    }

    // Hash password
    const salt = await bcrypt.genSalt(10);
    const hashedPassword = await bcrypt.hash(password, salt);

    // Create user document
    const newUser = {
      email,
      password: hashedPassword,
      name,
      role: 'user', // Default role
      createdAt: new Date(),
      updatedAt: new Date(),
      // Add any default settings if needed
    };

    const result = await db.collection('users').insertOne(newUser);

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
        console.error('Error: JWT_SECRET environment variable is not set for token signing.');
        return res.status(500).json({ message: 'Internal server error: JWT secret not configured.' });
    }
    const token = jwt.sign(userForToken, secret, { expiresIn: '24h' });

    res.status(201).json({
      message: 'Registration successful',
      token,
      user: userForToken // Send user info (without password)
    });

  } catch (error) {
    console.error('Registration Error:', error);
    res.status(500).json({ message: 'Error during registration', error: error.message });
  }
});

app.post('/api/auth/login', async (req, res) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ message: 'Email and password are required' });
    }

    // Ensure db is connected
    if (!db) {
        return res.status(500).json({ message: 'Database not connected' });
    }

    // Find user
    const user = await db.collection('users').findOne({ email });
    if (!user) {
      return res.status(401).json({ message: 'Invalid credentials' });
    }

    // Verify password
    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) {
      return res.status(401).json({ message: 'Invalid credentials' });
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
        console.error('Error: JWT_SECRET environment variable is not set for token signing.');
        return res.status(500).json({ message: 'Internal server error: JWT secret not configured.' });
    }
    const token = jwt.sign(userForToken, secret, { expiresIn: '24h' });

    res.json({
      message: 'Login successful',
      token,
      user: userForToken // Send user info (without password)
    });

  } catch (error) {
    console.error('Login Error:', error);
    res.status(500).json({ message: 'Error during login', error: error.message });
  }
});

// --- Other API Routes (Agent config, Strategies, etc.) ---
// These routes use the authenticateToken middleware

app.get('/api/agent/config', authenticateToken, async (req, res) => {
  // Ensure db is connected
  if (!db) return res.status(500).json({ message: 'Database not connected' });
  try {
    // Use req.user.id from the verified token payload
    const config = await db.collection('configurations').findOne({ userId: req.user.id });
    res.json(config || {});
  } catch (error) {
    res.status(500).json({ message: 'Error fetching agent configuration', error: error.message });
  }
});

app.put('/api/agent/config', authenticateToken, async (req, res) => {
  // Ensure db is connected
  if (!db) return res.status(500).json({ message: 'Database not connected' });
  try {
    // Use req.user.id from the verified token payload
    const result = await db.collection('configurations').updateOne(
      { userId: req.user.id },
      { $set: req.body },
      { upsert: true }
    );
    res.json({ message: 'Configuration updated', result });
  } catch (error) {
    res.status(500).json({ message: 'Error updating agent configuration', error: error.message });
  }
});

// Example: Strategy endpoint modification
app.get('/api/strategies', authenticateToken, async (req, res) => {
  // Ensure db is connected
  if (!db) return res.status(500).json({ message: 'Database not connected' });
  try {
    const strategies = await db.collection('strategies')
      .find({ userId: req.user.id })
      .toArray();
    res.json(strategies);
  } catch (error) {
    res.status(500).json({ message: 'Error fetching strategies', error: error.message });
  }
});

// --- Start the server ---
const PORT = process.env.PORT || 10000; // Use 10000 as default for Render

async function startServer() {
  try {
    // Connect to DB and assign to the outer 'db' variable
    const database = await connectToDatabase();
    db = database; // Make db instance available to routes

    app.listen(PORT, '0.0.0.0', () => { // Ensure listening on 0.0.0.0
      console.log(`Server running on port ${PORT}`);
    });
  } catch (error) {
      console.error('Failed to start server:', error);
      process.exit(1);
  }
}

// For standalone Node.js environment (This is used by Render)
if (require.main === module) {
  startServer();
}
