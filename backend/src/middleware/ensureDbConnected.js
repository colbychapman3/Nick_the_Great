/**
 * Middleware to ensure database connection is established before handling requests
 */

const { connectToDatabase } = require('../db');
const logger = require('../utils/logger');

/**
 * Middleware that ensures the database is connected before proceeding to the next middleware
 * @param {Object} req - Express request object
 * @param {Object} res - Express response object
 * @param {Function} next - Express next function
 */
async function ensureDbConnected(req, res, next) {
  try {
    // Try to connect to the database
    await connectToDatabase();
    
    // If we get here, the connection was successful
    next();
  } catch (error) {
    // Log the error
    logger.error(`Database connection error in middleware: ${error.message}`);
    
    // Send an error response
    res.status(500).json({
      message: 'Database connection error',
      error: process.env.NODE_ENV === 'production' ? 'Internal server error' : error.message
    });
  }
}

module.exports = ensureDbConnected;
