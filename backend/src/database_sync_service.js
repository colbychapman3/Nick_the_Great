/**
 * Implementation of the DatabaseSyncService for gRPC
 * This service handles synchronization of experiment data between Agent Core and Backend
 */

const experimentService = require('./services/experimentService');
const logger = require('./utils/logger');

/**
 * Restore experiments from the database to the Agent Core
 * @param {Object} call - gRPC call object
 * @param {Function} callback - gRPC callback function
 */
async function restoreExperiments(call, callback) {
  try {
    logger.info('Received RestoreExperiments request');
    
    // Extract filters from request
    const userId = call.request.user_id || null;
    const experimentType = call.request.experiment_type || null;
    const experimentState = call.request.experiment_state || null;
    const limit = call.request.limit || 100;
    
    // Build filters
    const filters = {};
    if (userId) {
      filters.userId = userId;
    }
    if (experimentType) {
      filters.type = experimentType;
    }
    if (experimentState) {
      filters.state = experimentState;
    }
    
    // Get experiments from database
    const result = await experimentService.listExperiments(filters, 1, limit);
    
    // Convert experiments to gRPC format
    const experiments = result.experiments.map(experiment => experiment.toGrpcFormat());
    
    // Return response
    callback(null, {
      success: true,
      message: `Restored ${experiments.length} experiments`,
      experiments: experiments
    });
  } catch (error) {
    logger.error(`Error in RestoreExperiments: ${error.message}`);
    callback(null, {
      success: false,
      message: `Error restoring experiments: ${error.message}`,
      experiments: []
    });
  }
}

/**
 * Sync experiment status from Agent Core to the database
 * @param {Object} call - gRPC call object
 * @param {Function} callback - gRPC callback function
 */
async function syncExperimentStatus(call, callback) {
  try {
    const experimentStatus = call.request.experiment_status;
    
    if (!experimentStatus || !experimentStatus.id || !experimentStatus.id.id) {
      callback(null, {
        success: false,
        message: 'Invalid experiment status: missing ID'
      });
      return;
    }
    
    const experimentId = experimentStatus.id.id;
    logger.debug(`Received SyncExperimentStatus request for experiment ${experimentId}`);
    
    // Check if experiment exists in database
    const existingExperiment = await experimentService.getExperimentById(experimentId);
    
    if (existingExperiment) {
      // Update existing experiment
      await experimentService.updateExperiment(experimentStatus);
      logger.debug(`Updated experiment ${experimentId} in database`);
    } else {
      // Create new experiment with system user ID
      const systemUserId = process.env.SYSTEM_USER_ID || 'system';
      await experimentService.createExperiment(experimentStatus, systemUserId);
      logger.debug(`Created new experiment ${experimentId} in database`);
    }
    
    callback(null, {
      success: true,
      message: `Successfully synced experiment ${experimentId}`
    });
  } catch (error) {
    logger.error(`Error in SyncExperimentStatus: ${error.message}`);
    callback(null, {
      success: false,
      message: `Error syncing experiment status: ${error.message}`
    });
  }
}

/**
 * Sync log entry from Agent Core to the database
 * @param {Object} call - gRPC call object
 * @param {Function} callback - gRPC callback function
 */
async function syncLogEntry(call, callback) {
  try {
    const logEntry = call.request.log_entry;
    
    if (!logEntry || !logEntry.experiment_id || !logEntry.experiment_id.id) {
      callback(null, {
        success: false,
        message: 'Invalid log entry: missing experiment ID'
      });
      return;
    }
    
    const experimentId = logEntry.experiment_id.id;
    logger.debug(`Received SyncLogEntry request for experiment ${experimentId}`);
    
    // Add log entry to database
    await experimentService.addLogEntry(logEntry);
    
    callback(null, {
      success: true,
      message: `Successfully synced log entry for experiment ${experimentId}`
    });
  } catch (error) {
    logger.error(`Error in SyncLogEntry: ${error.message}`);
    callback(null, {
      success: false,
      message: `Error syncing log entry: ${error.message}`
    });
  }
}

/**
 * Sync metrics from Agent Core to the database
 * @param {Object} call - gRPC call object
 * @param {Function} callback - gRPC callback function
 */
async function syncMetrics(call, callback) {
  try {
    const experimentId = call.request.experiment_id.id;
    const metrics = call.request.metrics;
    
    if (!experimentId) {
      callback(null, {
        success: false,
        message: 'Invalid metrics request: missing experiment ID'
      });
      return;
    }
    
    logger.debug(`Received SyncMetrics request for experiment ${experimentId}`);
    
    // Create metrics snapshot
    const metricsSnapshot = experimentService.createMetricsSnapshot(experimentId, metrics);
    
    callback(null, {
      success: true,
      message: `Successfully synced metrics for experiment ${experimentId}`
    });
  } catch (error) {
    logger.error(`Error in SyncMetrics: ${error.message}`);
    callback(null, {
      success: false,
      message: `Error syncing metrics: ${error.message}`
    });
  }
}

module.exports = {
  restoreExperiments,
  syncExperimentStatus,
  syncLogEntry,
  syncMetrics
};
