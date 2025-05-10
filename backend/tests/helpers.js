/**
 * Test helpers for the backend
 */

const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');
const { v4: uuidv4 } = require('uuid');
const mongoose = require('mongoose');

/**
 * Create a test user in the database
 * @param {Object} db - MongoDB database instance
 * @param {Object} userData - User data to create
 * @returns {Object} Created user object
 */
async function createTestUser(db, userData = {}) {
  const defaultUserData = {
    username: `testuser_${Date.now()}`,
    email: `test_${Date.now()}@example.com`,
    password: await bcrypt.hash('password123', 10),
    firstName: 'Test',
    lastName: 'User',
    role: 'user',
  };
  
  const mergedUserData = { ...defaultUserData, ...userData };
  
  const result = await db.collection('users').insertOne(mergedUserData);
  return { ...mergedUserData, _id: result.insertedId };
}

/**
 * Generate a JWT token for a user
 * @param {Object} user - User object
 * @returns {String} JWT token
 */
function generateToken(user) {
  return jwt.sign(
    { 
      id: user._id.toString(), 
      username: user.username,
      role: user.role 
    },
    process.env.JWT_SECRET,
    { expiresIn: '1h' }
  );
}

/**
 * Create a test experiment in the database
 * @param {Object} db - MongoDB database instance
 * @param {String} userId - User ID who owns the experiment
 * @param {Object} experimentData - Experiment data to create
 * @returns {Object} Created experiment object
 */
async function createTestExperiment(db, userId, experimentData = {}) {
  const experimentId = experimentData._id || uuidv4();
  
  const defaultExperimentData = {
    _id: experimentId,
    userId: userId,
    name: `Test Experiment ${Date.now()}`,
    type: 'AI_DRIVEN_EBOOKS',
    description: 'A test experiment',
    parameters: {
      topic: 'Test Topic',
      target_audience: 'Test Audience',
      length: '1000 words'
    },
    state: 'STATE_DEFINED',
    statusMessage: 'Experiment defined',
    metrics: {
      progress_percent: 0,
      elapsed_time_seconds: 0,
      estimated_remaining_seconds: 0,
      cpu_usage_percent: 0,
      memory_usage_mb: 0,
      error_count: 0
    },
    startTime: null,
    lastUpdateTime: new Date(),
    estimatedCompletionTime: null,
    createdAt: new Date(),
    updatedAt: new Date()
  };
  
  const mergedExperimentData = { ...defaultExperimentData, ...experimentData };
  
  const result = await db.collection('experiments').insertOne(mergedExperimentData);
  return { ...mergedExperimentData, _id: experimentId };
}

/**
 * Create a test log entry in the database
 * @param {Object} db - MongoDB database instance
 * @param {String} experimentId - Experiment ID
 * @param {Object} logData - Log data to create
 * @returns {Object} Created log object
 */
async function createTestLogEntry(db, experimentId, logData = {}) {
  const defaultLogData = {
    experimentId: experimentId,
    timestamp: new Date(),
    level: 'INFO',
    message: `Test log message ${Date.now()}`,
    sourceComponent: 'TestComponent',
    createdAt: new Date(),
    updatedAt: new Date()
  };
  
  const mergedLogData = { ...defaultLogData, ...logData };
  
  const result = await db.collection('experimentlogs').insertOne(mergedLogData);
  return { ...mergedLogData, _id: result.insertedId };
}

/**
 * Create a test metrics snapshot in the database
 * @param {Object} db - MongoDB database instance
 * @param {String} experimentId - Experiment ID
 * @param {Object} metricsData - Metrics data to create
 * @returns {Object} Created metrics object
 */
async function createTestMetricsSnapshot(db, experimentId, metricsData = {}) {
  const defaultMetricsData = {
    experimentId: experimentId,
    timestamp: new Date(),
    progressPercent: 50,
    elapsedTimeSeconds: 300,
    estimatedRemainingSeconds: 300,
    cpuUsagePercent: 25,
    memoryUsageMb: 100,
    errorCount: 0,
    additionalMetrics: {
      custom_metric: 'test value'
    },
    createdAt: new Date(),
    updatedAt: new Date()
  };
  
  const mergedMetricsData = { ...defaultMetricsData, ...metricsData };
  
  const result = await db.collection('experimentmetrics').insertOne(mergedMetricsData);
  return { ...mergedMetricsData, _id: result.insertedId };
}

module.exports = {
  createTestUser,
  generateToken,
  createTestExperiment,
  createTestLogEntry,
  createTestMetricsSnapshot
};
