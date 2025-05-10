/**
 * Pinterest Strategy API Routes
 * Handles Pinterest authentication and strategy execution
 */

const express = require('express');
const router = express.Router();
const { spawn } = require('child_process');
const path = require('path');
const { ObjectId } = require('mongodb');
const logger = require('../utils/logger');

// Get database instance
let db;
const setDb = (database) => {
  db = database;
};

/**
 * @route GET /api/pinterest/auth-url
 * @desc Get Pinterest OAuth authorization URL
 * @access Private (requires authentication)
 */
router.get('/auth-url', async (req, res) => {
  try {
    const userId = req.user.id;
    
    // Generate a state parameter to prevent CSRF attacks
    // This should be stored in the database and verified when the user returns
    const state = Buffer.from(JSON.stringify({
      userId,
      timestamp: Date.now()
    })).toString('base64');
    
    // Store the state in the database
    await db.collection('pinterestAuth').updateOne(
      { userId },
      { 
        $set: { 
          state,
          stateCreatedAt: new Date()
        }
      },
      { upsert: true }
    );
    
    // Call the Python script to get the authorization URL
    const pythonProcess = spawn('python', [
      path.join(process.cwd(), '../pinterest_automation/src/get_auth_url.py'),
      '--redirect_uri', process.env.PINTEREST_REDIRECT_URI || 'http://localhost:3000/pinterest/callback',
      '--state', state
    ]);
    
    let authUrl = '';
    
    pythonProcess.stdout.on('data', (data) => {
      authUrl += data.toString();
    });
    
    pythonProcess.stderr.on('data', (data) => {
      logger.error(`Pinterest Auth URL Error: ${data}`);
    });
    
    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        return res.status(500).json({ 
          message: 'Failed to generate Pinterest authorization URL',
          error: `Process exited with code ${code}`
        });
      }
      
      res.json({ authUrl: authUrl.trim() });
    });
  } catch (error) {
    logger.error(`Pinterest Auth URL Error: ${error.message}`);
    res.status(500).json({ 
      message: 'Error generating Pinterest authorization URL',
      error: error.message
    });
  }
});

/**
 * @route POST /api/pinterest/callback
 * @desc Handle Pinterest OAuth callback
 * @access Public (callback from Pinterest)
 */
router.post('/callback', async (req, res) => {
  try {
    const { code, state } = req.body;
    
    if (!code || !state) {
      return res.status(400).json({ message: 'Missing code or state parameter' });
    }
    
    // Verify the state parameter
    let stateData;
    try {
      stateData = JSON.parse(Buffer.from(state, 'base64').toString());
    } catch (error) {
      return res.status(400).json({ message: 'Invalid state parameter' });
    }
    
    const { userId, timestamp } = stateData;
    
    // Check if the state exists in the database
    const storedState = await db.collection('pinterestAuth').findOne({ 
      userId,
      state
    });
    
    if (!storedState) {
      return res.status(400).json({ message: 'Invalid state parameter' });
    }
    
    // Check if the state is expired (10 minutes)
    const stateAge = Date.now() - timestamp;
    if (stateAge > 10 * 60 * 1000) {
      return res.status(400).json({ message: 'State parameter expired' });
    }
    
    // Call the Python script to exchange the code for tokens
    const pythonProcess = spawn('python', [
      path.join(process.cwd(), '../pinterest_automation/src/exchange_code.py'),
      '--code', code,
      '--redirect_uri', process.env.PINTEREST_REDIRECT_URI || 'http://localhost:3000/pinterest/callback'
    ]);
    
    let result = '';
    
    pythonProcess.stdout.on('data', (data) => {
      result += data.toString();
    });
    
    pythonProcess.stderr.on('data', (data) => {
      logger.error(`Pinterest Token Exchange Error: ${data}`);
    });
    
    pythonProcess.on('close', async (code) => {
      if (code !== 0) {
        return res.status(500).json({ 
          message: 'Failed to exchange code for tokens',
          error: `Process exited with code ${code}`
        });
      }
      
      try {
        // Parse the result
        const tokens = JSON.parse(result.trim());
        
        // Store the tokens in the database
        await db.collection('pinterestAuth').updateOne(
          { userId },
          { 
            $set: { 
              accessToken: tokens.access_token,
              refreshToken: tokens.refresh_token,
              expiresAt: new Date(Date.now() + tokens.expires_in * 1000),
              authenticated: true,
              authenticatedAt: new Date()
            },
            $unset: { state: "", stateCreatedAt: "" }
          }
        );
        
        res.json({ success: true });
      } catch (error) {
        logger.error(`Pinterest Token Storage Error: ${error.message}`);
        res.status(500).json({ 
          message: 'Error storing Pinterest tokens',
          error: error.message
        });
      }
    });
  } catch (error) {
    logger.error(`Pinterest Callback Error: ${error.message}`);
    res.status(500).json({ 
      message: 'Error handling Pinterest callback',
      error: error.message
    });
  }
});

/**
 * @route GET /api/pinterest/status
 * @desc Check if user is authenticated with Pinterest
 * @access Private (requires authentication)
 */
router.get('/status', async (req, res) => {
  try {
    const userId = req.user.id;
    
    const auth = await db.collection('pinterestAuth').findOne({ userId });
    
    if (!auth || !auth.authenticated) {
      return res.json({ authenticated: false });
    }
    
    // Check if the token is expired
    if (auth.expiresAt < new Date()) {
      return res.json({ 
        authenticated: true,
        tokenStatus: 'expired',
        authenticatedAt: auth.authenticatedAt
      });
    }
    
    res.json({ 
      authenticated: true,
      tokenStatus: 'valid',
      authenticatedAt: auth.authenticatedAt
    });
  } catch (error) {
    logger.error(`Pinterest Status Error: ${error.message}`);
    res.status(500).json({ 
      message: 'Error checking Pinterest authentication status',
      error: error.message
    });
  }
});

/**
 * @route POST /api/pinterest/strategy
 * @desc Generate a Pinterest strategy
 * @access Private (requires authentication)
 */
router.post('/strategy', async (req, res) => {
  try {
    const userId = req.user.id;
    const { niche, targetAudience, businessGoal, numPins = 5 } = req.body;
    
    if (!niche || !targetAudience || !businessGoal) {
      return res.status(400).json({ message: 'Missing required parameters' });
    }
    
    // Create a new strategy document
    const strategy = {
      userId,
      type: 'pinterest',
      niche,
      targetAudience,
      businessGoal,
      numPins,
      status: 'pending',
      createdAt: new Date()
    };
    
    const result = await db.collection('strategies').insertOne(strategy);
    const strategyId = result.insertedId;
    
    // Execute the strategy generation in the background
    const pythonProcess = spawn('python', [
      path.join(process.cwd(), '../task_modules/run_pinterest_strategy.py'),
      '--strategy_id', strategyId.toString(),
      '--niche', niche,
      '--target_audience', targetAudience,
      '--business_goal', businessGoal,
      '--num_pins', numPins.toString()
    ]);
    
    pythonProcess.stderr.on('data', (data) => {
      logger.error(`Pinterest Strategy Error: ${data}`);
    });
    
    // Return the strategy ID immediately
    res.json({ 
      message: 'Pinterest strategy generation started',
      strategyId: strategyId.toString()
    });
  } catch (error) {
    logger.error(`Pinterest Strategy Error: ${error.message}`);
    res.status(500).json({ 
      message: 'Error generating Pinterest strategy',
      error: error.message
    });
  }
});

/**
 * @route GET /api/pinterest/strategy/:id
 * @desc Get a Pinterest strategy by ID
 * @access Private (requires authentication)
 */
router.get('/strategy/:id', async (req, res) => {
  try {
    const userId = req.user.id;
    const strategyId = req.params.id;
    
    if (!ObjectId.isValid(strategyId)) {
      return res.status(400).json({ message: 'Invalid strategy ID' });
    }
    
    const strategy = await db.collection('strategies').findOne({
      _id: new ObjectId(strategyId),
      userId
    });
    
    if (!strategy) {
      return res.status(404).json({ message: 'Strategy not found' });
    }
    
    res.json(strategy);
  } catch (error) {
    logger.error(`Pinterest Strategy Retrieval Error: ${error.message}`);
    res.status(500).json({ 
      message: 'Error retrieving Pinterest strategy',
      error: error.message
    });
  }
});

module.exports = { router, setDb };
