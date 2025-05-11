/**
 * Mock Pinterest Strategy API Routes for testing
 */

const express = require('express');
const router = express.Router();
const logger = require('../utils/logger');

// Mock database instance
let db = null;
const setDb = (database) => {
  db = database;
};

// Mock Pinterest auth data
const mockPinterestAuth = {
  authenticated: true,
  tokenStatus: 'valid',
  authenticatedAt: new Date().toISOString()
};

// Mock Pinterest strategy
const mockStrategy = {
  _id: 'mock-strategy-id',
  userId: 'mock-user-id',
  type: 'pinterest',
  niche: 'Digital Marketing',
  targetAudience: 'Small Business Owners',
  businessGoal: 'Increase brand awareness',
  numPins: 5,
  status: 'completed',
  createdAt: new Date().toISOString(),
  updatedAt: new Date().toISOString(),
  result: {
    pinterestStrategy: {
      overview: 'This Pinterest strategy focuses on creating visually appealing pins that showcase your digital marketing expertise.',
      target_audience_analysis: 'Small business owners on Pinterest are looking for actionable tips and strategies they can implement quickly.',
      content_strategy: 'Create a mix of infographics, quote pins, and step-by-step guides that provide immediate value.',
      board_structure: {
        'Digital Marketing Tips': 'General marketing advice and trends',
        'SEO Strategies': 'Search engine optimization techniques',
        'Social Media Marketing': 'Platform-specific strategies and tips'
      }
    },
    pinIdeas: [
      {
        title: '5 SEO Tips for Small Businesses',
        description: 'Boost your website traffic with these simple SEO strategies any small business can implement.',
        type: 'Infographic',
        target_board: 'SEO Strategies'
      },
      {
        title: 'Social Media Checklist for Entrepreneurs',
        description: 'Daily, weekly, and monthly tasks to keep your social media presence strong.',
        type: 'Checklist',
        target_board: 'Social Media Marketing'
      },
      {
        title: 'How to Create a Marketing Plan in 7 Steps',
        description: 'A step-by-step guide to creating an effective marketing plan for your small business.',
        type: 'Step-by-Step Guide',
        target_board: 'Digital Marketing Tips'
      },
      {
        title: 'Content Marketing ROI Calculator',
        description: 'Use this formula to calculate the return on investment for your content marketing efforts.',
        type: 'Infographic',
        target_board: 'Digital Marketing Tips'
      },
      {
        title: 'Email Marketing Subject Lines That Convert',
        description: '10 proven email subject line templates to improve your open rates.',
        type: 'List',
        target_board: 'Digital Marketing Tips'
      }
    ]
  }
};

/**
 * @route GET /api/pinterest/auth-url
 * @desc Get Pinterest OAuth authorization URL
 * @access Private (requires authentication)
 */
router.get('/auth-url', async (req, res) => {
  try {
    logger.info('Mock Pinterest auth-url endpoint called');
    
    // Return a mock authorization URL
    res.json({ 
      authUrl: 'https://www.pinterest.com/oauth/authorize?client_id=1518892&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Fpinterest%2Fcallback&response_type=code&scope=pins%3Aread%2Cpins%3Awrite%2Cboards%3Aread%2Cboards%3Awrite%2Cuser_accounts%3Aread&state=mock-state'
    });
  } catch (error) {
    logger.error(`Mock Pinterest Auth URL Error: ${error.message}`);
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
    
    logger.info('Mock Pinterest callback endpoint called', { code, state });
    
    // Return success response
    res.json({ success: true });
  } catch (error) {
    logger.error(`Mock Pinterest Callback Error: ${error.message}`);
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
    logger.info('Mock Pinterest status endpoint called');
    
    // Return mock authentication status
    res.json(mockPinterestAuth);
  } catch (error) {
    logger.error(`Mock Pinterest Status Error: ${error.message}`);
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
    const { niche, targetAudience, businessGoal, numPins = 5 } = req.body;
    
    if (!niche || !targetAudience || !businessGoal) {
      return res.status(400).json({ message: 'Missing required parameters' });
    }
    
    logger.info('Mock Pinterest strategy endpoint called', { niche, targetAudience, businessGoal, numPins });
    
    // Return mock strategy ID
    res.json({ 
      message: 'Pinterest strategy generation started',
      strategyId: 'mock-strategy-id'
    });
  } catch (error) {
    logger.error(`Mock Pinterest Strategy Error: ${error.message}`);
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
    const strategyId = req.params.id;
    
    logger.info('Mock Pinterest strategy/:id endpoint called', { strategyId });
    
    // Return mock strategy
    res.json(mockStrategy);
  } catch (error) {
    logger.error(`Mock Pinterest Strategy Retrieval Error: ${error.message}`);
    res.status(500).json({ 
      message: 'Error retrieving Pinterest strategy',
      error: error.message
    });
  }
});

module.exports = { router, setDb };
