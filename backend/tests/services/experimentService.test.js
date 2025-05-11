/**
 * Unit tests for the experiment service
 */

const mongoose = require('mongoose');
const { MongoMemoryServer } = require('mongodb-memory-server');
const { v4: uuidv4 } = require('uuid');

// Import the service to test
const experimentService = require('../../src/services/experimentService');

// Import models
const Experiment = require('../../src/models/experiment');
const ExperimentLog = require('../../src/models/experimentLog');
const ExperimentMetrics = require('../../src/models/experimentMetrics');

// Import test helpers
const { createTestExperiment, createTestLogEntry, createTestMetricsSnapshot } = require('../helpers');

// Mock the logger
jest.mock('../../src/utils/logger', () => ({
  info: jest.fn(),
  error: jest.fn(),
  warn: jest.fn(),
  debug: jest.fn(),
}));

describe('Experiment Service', () => {
  let db;
  let mongoServer;

  beforeAll(async () => {
    // Create an in-memory MongoDB server
    mongoServer = await MongoMemoryServer.create();
    const mongoUri = mongoServer.getUri();

    // Connect to the in-memory database
    await mongoose.connect(mongoUri);

    // Get the database instance
    db = mongoose.connection.db;
  });

  afterAll(async () => {
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
  });

  describe('createExperiment', () => {
    it('should create a new experiment in the database', async () => {
      // Arrange
      const userId = 'test-user-id';
      const experimentId = uuidv4();
      const experimentData = {
        id: { id: experimentId },
        name: 'Test Experiment',
        type: 'AI_DRIVEN_EBOOKS',
        state: 'STATE_DEFINED',
        status_message: 'Experiment defined',
        metrics: {
          progress_percent: 0,
          elapsed_time_seconds: 0,
          estimated_remaining_seconds: 0
        },
        start_time: null,
        last_update_time: { seconds: Math.floor(Date.now() / 1000) },
        estimated_completion_time: null,
        definition: {
          description: 'Test description',
          parameters: {
            topic: 'Test Topic'
          }
        }
      };

      // Act
      const result = await experimentService.createExperiment(experimentData, userId);

      // Assert
      expect(result).toBeDefined();
      expect(result._id).toBe(experimentId);
      expect(result.userId).toBe(userId);
      expect(result.name).toBe(experimentData.name);
      expect(result.type).toBe(experimentData.type);
      expect(result.state).toBe(experimentData.state);

      // Verify it was saved to the database
      const savedExperiment = await Experiment.findById(experimentId);
      expect(savedExperiment).toBeDefined();
      expect(savedExperiment.name).toBe(experimentData.name);
    });

    it('should create metrics snapshot if metrics exist', async () => {
      // Arrange
      const userId = 'test-user-id';
      const experimentId = uuidv4();
      const experimentData = {
        id: { id: experimentId },
        name: 'Test Experiment',
        type: 'AI_DRIVEN_EBOOKS',
        state: 'STATE_RUNNING',
        status_message: 'Experiment running',
        metrics: {
          progress_percent: 50,
          elapsed_time_seconds: 300,
          estimated_remaining_seconds: 300,
          cpu_usage_percent: 25,
          memory_usage_mb: 100
        },
        start_time: { seconds: Math.floor(Date.now() / 1000) - 300 },
        last_update_time: { seconds: Math.floor(Date.now() / 1000) },
        estimated_completion_time: { seconds: Math.floor(Date.now() / 1000) + 300 }
      };

      // Act
      await experimentService.createExperiment(experimentData, userId);

      // Assert
      const metricsSnapshots = await ExperimentMetrics.find({ experimentId });
      expect(metricsSnapshots).toHaveLength(1);
      expect(metricsSnapshots[0].progressPercent).toBe(50);
      expect(metricsSnapshots[0].elapsedTimeSeconds).toBe(300);
    });
  });

  describe('updateExperiment', () => {
    it('should update an existing experiment in the database', async () => {
      // Arrange
      const userId = 'test-user-id';
      const experimentId = uuidv4();

      // Create an experiment first
      await createTestExperiment(db, userId, { _id: experimentId, name: 'Original Name' });

      const updatedData = {
        id: { id: experimentId },
        name: 'Updated Name',
        type: 'AI_DRIVEN_EBOOKS',
        state: 'STATE_RUNNING',
        status_message: 'Experiment running',
        metrics: {
          progress_percent: 25,
          elapsed_time_seconds: 150,
          estimated_remaining_seconds: 450
        },
        start_time: { seconds: Math.floor(Date.now() / 1000) - 150 },
        last_update_time: { seconds: Math.floor(Date.now() / 1000) },
        estimated_completion_time: { seconds: Math.floor(Date.now() / 1000) + 450 }
      };

      // Act
      const result = await experimentService.updateExperiment(updatedData);

      // Assert
      expect(result).toBeDefined();
      expect(result.name).toBe('Updated Name');
      expect(result.state).toBe('STATE_RUNNING');

      // Verify it was updated in the database
      const updatedExperiment = await Experiment.findById(experimentId);
      expect(updatedExperiment).toBeDefined();
      expect(updatedExperiment.name).toBe('Updated Name');
      expect(updatedExperiment.state).toBe('STATE_RUNNING');
    });

    it('should throw an error if experiment does not exist', async () => {
      // Arrange
      const nonExistentId = uuidv4();
      const updatedData = {
        id: { id: nonExistentId },
        name: 'Updated Name',
        type: 'AI_DRIVEN_EBOOKS',
        state: 'STATE_RUNNING'
      };

      // Act & Assert
      await expect(experimentService.updateExperiment(updatedData))
        .rejects.toThrow(`Experiment with ID ${nonExistentId} not found`);
    });
  });
});
