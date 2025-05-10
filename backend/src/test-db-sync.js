/**
 * Test script for database sync service
 * 
 * This script tests the database sync service by creating a mock gRPC client
 * and calling the service methods.
 */

const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');
const { v4: uuidv4 } = require('uuid');
const { connectToDatabase, closeConnection } = require('./db');
const logger = require('./utils/logger');

// Path to proto files
const AGENT_PROTO_PATH = path.join(__dirname, '../../proto/agent.proto');
const DB_SYNC_PROTO_PATH = path.join(__dirname, '../../proto/database_sync.proto');

// Load proto files
const agentPackageDefinition = protoLoader.loadSync(AGENT_PROTO_PATH, {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true
});

const dbSyncPackageDefinition = protoLoader.loadSync(DB_SYNC_PROTO_PATH, {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true
});

// Load proto descriptors
const agentProto = grpc.loadPackageDefinition(agentPackageDefinition).nickthegreat;
const dbSyncProto = grpc.loadPackageDefinition(dbSyncPackageDefinition).nickthegreat.database;

// Import the database sync service
const databaseSyncService = require('./database_sync_service');

// Create a mock context
const mockContext = {
  callback: (error, response) => {
    if (error) {
      logger.error(`Error: ${error.message}`);
      return;
    }
    logger.info(`Response: ${JSON.stringify(response)}`);
  }
};

// Create a mock experiment status
function createMockExperimentStatus() {
  const experimentId = uuidv4();
  return {
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
      description: 'A test experiment for database sync service',
      parameters: {
        topic: 'MongoDB Testing',
        target_audience: 'Developers',
        length: '5000 words'
      }
    }
  };
}

// Create a mock log entry
function createMockLogEntry(experimentId) {
  return {
    timestamp: { seconds: Math.floor(Date.now() / 1000) },
    level: 'INFO',
    message: 'Test log entry',
    experiment_id: { id: experimentId },
    source_component: 'TestScript'
  };
}

// Create a mock metrics struct
function createMockMetrics() {
  return {
    progress_percent: 50.0,
    elapsed_time_seconds: 300.0,
    estimated_remaining_seconds: 300.0,
    cpu_usage_percent: 25.0,
    memory_usage_mb: 100.0,
    error_count: 0,
    custom_metric: 'test value'
  };
}

// Test the database sync service
async function testDatabaseSyncService() {
  try {
    logger.info('Starting database sync service test');
    
    // Connect to MongoDB
    logger.info('Connecting to MongoDB...');
    const db = await connectToDatabase();
    logger.info(`Connected to database: ${db.databaseName}`);
    
    // Test restoreExperiments
    logger.info('Testing restoreExperiments...');
    const restoreRequest = {
      limit: 10
    };
    await new Promise((resolve) => {
      databaseSyncService.restoreExperiments({ request: restoreRequest }, (error, response) => {
        if (error) {
          logger.error(`Error in restoreExperiments: ${error.message}`);
        } else {
          logger.info(`Restored ${response.experiments ? response.experiments.length : 0} experiments`);
        }
        resolve();
      });
    });
    
    // Test syncExperimentStatus
    logger.info('Testing syncExperimentStatus...');
    const experimentStatus = createMockExperimentStatus();
    const syncStatusRequest = {
      experiment_status: experimentStatus
    };
    await new Promise((resolve) => {
      databaseSyncService.syncExperimentStatus({ request: syncStatusRequest }, (error, response) => {
        if (error) {
          logger.error(`Error in syncExperimentStatus: ${error.message}`);
        } else {
          logger.info(`Synced experiment status: ${response.success ? 'Success' : 'Failed'} - ${response.message}`);
        }
        resolve();
      });
    });
    
    // Test syncLogEntry
    logger.info('Testing syncLogEntry...');
    const logEntry = createMockLogEntry(experimentStatus.id.id);
    const syncLogRequest = {
      log_entry: logEntry
    };
    await new Promise((resolve) => {
      databaseSyncService.syncLogEntry({ request: syncLogRequest }, (error, response) => {
        if (error) {
          logger.error(`Error in syncLogEntry: ${error.message}`);
        } else {
          logger.info(`Synced log entry: ${response.success ? 'Success' : 'Failed'} - ${response.message}`);
        }
        resolve();
      });
    });
    
    // Test syncMetrics
    logger.info('Testing syncMetrics...');
    const metrics = createMockMetrics();
    const syncMetricsRequest = {
      experiment_id: { id: experimentStatus.id.id },
      metrics: metrics,
      timestamp: { seconds: Math.floor(Date.now() / 1000) }
    };
    await new Promise((resolve) => {
      databaseSyncService.syncMetrics({ request: syncMetricsRequest }, (error, response) => {
        if (error) {
          logger.error(`Error in syncMetrics: ${error.message}`);
        } else {
          logger.info(`Synced metrics: ${response.success ? 'Success' : 'Failed'} - ${response.message}`);
        }
        resolve();
      });
    });
    
    // Close database connection
    await closeConnection();
    logger.info('Database connection closed');
    
    logger.info('Database sync service test completed successfully');
  } catch (error) {
    logger.error(`Error testing database sync service: ${error.message}`);
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
testDatabaseSyncService();
