/**
 * Integration tests for the experiment API endpoints
 */

const request = require('supertest');
const express = require('express');
const mongoose = require('mongoose');
const { MongoMemoryServer } = require('mongodb-memory-server');
const jwt = require('jsonwebtoken');
const { v4: uuidv4 } = require('uuid');

// Import test helpers
const { createTestUser, generateToken, createTestExperiment } = require('../helpers');

// Mock the agent_client module
jest.mock('../../src/agent_client', () => ({
  createExperiment: jest.fn().mockResolvedValue({
    id: { id: 'mock-experiment-id' },
    status: { success: true, message: 'Experiment created successfully' }
  }),
  startExperiment: jest.fn().mockResolvedValue({
    success: true,
    message: 'Experiment started successfully'
  }),
  stopExperiment: jest.fn().mockResolvedValue({
    success: true,
    message: 'Experiment stopped successfully'
  }),
  getExperimentStatus: jest.fn().mockResolvedValue({
    id: { id: 'mock-experiment-id' },
    name: 'Mock Experiment',
    type: 'AI_DRIVEN_EBOOKS',
    state: 'STATE_RUNNING',
    status_message: 'Experiment running',
    metrics: {
      progress_percent: 50,
      elapsed_time_seconds: 300,
      estimated_remaining_seconds: 300
    },
    start_time: { seconds: Math.floor(Date.now() / 1000) - 300 },
    last_update_time: { seconds: Math.floor(Date.now() / 1000) },
    estimated_completion_time: { seconds: Math.floor(Date.now() / 1000) + 300 }
  }),
  listExperiments: jest.fn().mockResolvedValue([
    {
      id: { id: 'mock-experiment-id-1' },
      name: 'Mock Experiment 1',
      type: 'AI_DRIVEN_EBOOKS',
      state: 'STATE_RUNNING'
    },
    {
      id: { id: 'mock-experiment-id-2' },
      name: 'Mock Experiment 2',
      type: 'PINTEREST_STRATEGY',
      state: 'STATE_COMPLETED'
    }
  ]),
  ExperimentType: {
    AI_DRIVEN_EBOOKS: 'AI_DRIVEN_EBOOKS',
    FREELANCE_WRITING: 'FREELANCE_WRITING',
    NICHE_AFFILIATE_WEBSITE: 'NICHE_AFFILIATE_WEBSITE',
    PINTEREST_STRATEGY: 'PINTEREST_STRATEGY'
  },
  Struct: {
    fromJavaScript: jest.fn().mockReturnValue({})
  }
}));

// Create a test app
let app;
let server;
let db;
let mongoServer;
let testUser;
let authToken;

describe('Experiment API Endpoints', () => {
  beforeAll(async () => {
    // Create an in-memory MongoDB server
    mongoServer = await MongoMemoryServer.create();
    const mongoUri = mongoServer.getUri();

    // Connect to the in-memory database
    await mongoose.connect(mongoUri);

    // Get the database instance
    db = mongoose.connection.db;

    // Create a test user
    testUser = await createTestUser(db);

    // Generate an auth token
    authToken = generateToken(testUser);

    // Create the Express app
    app = express();

    // Apply middleware
    app.use(express.json());

    // Mock the authenticateToken middleware
    app.use((req, res, next) => {
      req.user = { id: testUser._id.toString(), username: testUser.username };
      next();
    });

    // Import the routes
    const indexRoutes = require('../../index');

    // Start the server
    server = app.listen(3001);
  });

  afterAll(async () => {
    // Close the server
    await server.close();

    // Close the MongoDB connection and stop the server
    await mongoose.connection.close();
    await mongoServer.stop();
  });

  beforeEach(async () => {
    // Clear all collections before each test
    const collections = mongoose.connection.collections;

    for (const key in collections) {
      const collection = collections[key];
      await collection.deleteMany({});
    }

    // Reset all mocks
    jest.clearAllMocks();
  });

  describe('GET /api/agent/experiments', () => {
    it('should return a list of experiments', async () => {
      // Arrange
      const userId = testUser._id.toString();

      // Create some test experiments
      await createTestExperiment(db, userId, { _id: 'test-exp-1', name: 'Test Experiment 1' });
      await createTestExperiment(db, userId, { _id: 'test-exp-2', name: 'Test Experiment 2' });

      // Act
      const response = await request(app)
        .get('/api/agent/experiments')
        .set('Authorization', `Bearer ${authToken}`);

      // Assert
      expect(response.status).toBe(200);
      expect(response.body.experiments).toHaveLength(2);
      expect(response.body.pagination).toBeDefined();
      expect(response.body.pagination.total).toBe(2);
    });

    it('should filter experiments by type', async () => {
      // Arrange
      const userId = testUser._id.toString();

      // Create some test experiments with different types
      await createTestExperiment(db, userId, {
        _id: 'test-exp-1',
        name: 'Test Experiment 1',
        type: 'AI_DRIVEN_EBOOKS'
      });
      await createTestExperiment(db, userId, {
        _id: 'test-exp-2',
        name: 'Test Experiment 2',
        type: 'PINTEREST_STRATEGY'
      });

      // Act
      const response = await request(app)
        .get('/api/agent/experiments?type=AI_DRIVEN_EBOOKS')
        .set('Authorization', `Bearer ${authToken}`);

      // Assert
      expect(response.status).toBe(200);
      expect(response.body.experiments).toHaveLength(1);
      expect(response.body.experiments[0].type).toBe('AI_DRIVEN_EBOOKS');
    });
  });
});
