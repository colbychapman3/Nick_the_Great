/**
 * Test script for experiment database functionality
 * 
 * This script tests the MongoDB connection and experiment persistence
 * by creating, retrieving, and updating experiment data.
 */

const mongoose = require('mongoose');
const { connectToDatabase, closeConnection } = require('./db');
const Experiment = require('./models/experiment');
const ExperimentLog = require('./models/experimentLog');
const ExperimentMetrics = require('./models/experimentMetrics');
const experimentService = require('./services/experimentService');
const logger = require('./utils/logger');
const { v4: uuidv4 } = require('uuid');

async function testExperimentDatabase() {
  try {
    logger.info('Starting experiment database test');
    
    // Connect to MongoDB
    logger.info('Connecting to MongoDB...');
    const db = await connectToDatabase();
    logger.info(`Connected to database: ${db.databaseName}`);
    
    // Test creating an experiment
    const experimentId = uuidv4();
    const userId = 'test-user-' + Date.now();
    
    logger.info(`Creating test experiment with ID: ${experimentId}`);
    
    // Create experiment data
    const experimentData = {
      id: { id: experimentId },
      name: 'Test Experiment',
      type: 'AI_DRIVEN_EBOOKS',
      state: 'STATE_DEFINED',
      status_message: 'Test experiment created',
      metrics: {
        progress_percent: 0.0,
        elapsed_time_seconds: 0.0,
        estimated_remaining_seconds: 0.0,
        cpu_usage_percent: 0.0,
        memory_usage_mb: 0.0,
        error_count: 0
      },
      start_time: null,
      last_update_time: { seconds: Math.floor(Date.now() / 1000) },
      estimated_completion_time: null,
      definition: {
        type: 'AI_DRIVEN_EBOOKS',
        name: 'Test Experiment',
        description: 'A test experiment for database functionality',
        parameters: {
          topic: 'MongoDB Testing',
          target_audience: 'Developers',
          length: '5000 words'
        }
      }
    };
    
    // Create experiment in database
    const experiment = await experimentService.createExperiment(experimentData, userId);
    logger.info(`Created experiment in database with ID: ${experiment._id}`);
    
    // Test retrieving the experiment
    logger.info(`Retrieving experiment with ID: ${experimentId}`);
    const retrievedExperiment = await experimentService.getExperimentById(experimentId);
    
    if (retrievedExperiment) {
      logger.info(`Retrieved experiment: ${retrievedExperiment.name}`);
    } else {
      logger.error(`Failed to retrieve experiment with ID: ${experimentId}`);
    }
    
    // Test updating the experiment
    logger.info(`Updating experiment with ID: ${experimentId}`);
    
    // Update experiment data
    experimentData.state = 'STATE_RUNNING';
    experimentData.status_message = 'Test experiment running';
    experimentData.start_time = { seconds: Math.floor(Date.now() / 1000) };
    experimentData.metrics.progress_percent = 25.0;
    
    // Update experiment in database
    const updatedExperiment = await experimentService.updateExperiment(experimentData);
    logger.info(`Updated experiment in database: ${updatedExperiment.statusMessage}`);
    
    // Test adding a log entry
    logger.info(`Adding log entry for experiment with ID: ${experimentId}`);
    
    // Create log entry data
    const logEntryData = {
      timestamp: { seconds: Math.floor(Date.now() / 1000) },
      level: 'INFO',
      message: 'Test log entry',
      experiment_id: { id: experimentId },
      source_component: 'TestScript'
    };
    
    // Add log entry to database
    await experimentService.addLogEntry(logEntryData);
    logger.info('Added log entry to database');
    
    // Test retrieving logs
    logger.info(`Retrieving logs for experiment with ID: ${experimentId}`);
    const logs = await experimentService.getExperimentLogs(experimentId);
    logger.info(`Retrieved ${logs.length} log entries`);
    
    // Test adding metrics
    logger.info(`Adding metrics for experiment with ID: ${experimentId}`);
    
    // Create metrics data
    const metricsData = {
      progress_percent: 50.0,
      elapsed_time_seconds: 300.0,
      estimated_remaining_seconds: 300.0,
      cpu_usage_percent: 25.0,
      memory_usage_mb: 100.0,
      error_count: 0,
      custom_metric: 'test value'
    };
    
    // Create metrics snapshot
    const metricsSnapshot = ExperimentMetrics.fromGrpc(experimentId, metricsData);
    await metricsSnapshot.save();
    logger.info('Added metrics snapshot to database');
    
    // Test retrieving metrics history
    logger.info(`Retrieving metrics history for experiment with ID: ${experimentId}`);
    const metricsHistory = await experimentService.getExperimentMetricsHistory(experimentId);
    logger.info(`Retrieved ${metricsHistory.length} metrics snapshots`);
    
    // Test listing experiments
    logger.info('Listing experiments');
    const result = await experimentService.listExperiments({ userId });
    logger.info(`Listed ${result.experiments.length} experiments`);
    
    // Clean up test data
    logger.info('Cleaning up test data');
    await Experiment.deleteOne({ _id: experimentId });
    await ExperimentLog.deleteMany({ experimentId });
    await ExperimentMetrics.deleteMany({ experimentId });
    logger.info('Test data cleaned up');
    
    // Close database connection
    await closeConnection();
    logger.info('Database connection closed');
    
    logger.info('Experiment database test completed successfully');
  } catch (error) {
    logger.error(`Error testing experiment database: ${error.message}`);
    logger.error(error.stack);
    
    // Try to close the connection
    try {
      await closeConnection();
    } catch (closeError) {
      logger.error(`Error closing database connection: ${closeError.message}`);
    }
  }
}

// Run the test
testExperimentDatabase();
