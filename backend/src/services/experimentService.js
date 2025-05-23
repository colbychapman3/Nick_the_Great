const Experiment = require('../models/experiment');
const ExperimentLog = require('../models/experimentLog');
const ExperimentMetrics = require('../models/experimentMetrics');
const { connectToDatabase } = require('../db');
const { getClient } = require('../agent_client');
const logger = require('../utils/logger');

/**
 * Service for handling experiment-related operations
 */
class ExperimentService {
  /**
   * Create a new experiment in the database
   * @param {Object} experimentData - Experiment data from gRPC
   * @param {String} userId - User ID who created the experiment
   * @returns {Promise<Object>} Created experiment
   */
  async createExperiment(experimentData, userId) {
    try {
      // Create a new experiment document
      const experiment = new Experiment({
        _id: experimentData.id.id,
        userId,
        name: experimentData.name,
        type: experimentData.type,
        description: experimentData.definition?.description || '',
        // NOTE ON PARAMETER SOURCE (for experiment definition parameters):
        // The 'experimentData' object, which is a gRPC ExperimentStatus message
        // from Agent Core, contains the original ExperimentDefinition (including
        // its 'parameters' Struct) as an embedded 'definition' field.
        // This service directly accesses 'experimentData.definition.parameters'
        // to populate the Mongoose 'Experiment' model's 'parameters' field.
        //
        // Agent Core does NOT flatten definition parameters into the 'metrics' field
        // of the ExperimentStatus message for persistence. The 'metrics' field is
        // reserved for dynamic operational metrics.
        parameters: experimentData.definition?.parameters || {},
        state: experimentData.state,
        statusMessage: experimentData.status_message,
        metrics: experimentData.metrics || {},
        startTime: experimentData.start_time ? new Date(experimentData.start_time.seconds * 1000) : null,
        lastUpdateTime: experimentData.last_update_time ? new Date(experimentData.last_update_time.seconds * 1000) : new Date(),
        estimatedCompletionTime: experimentData.estimated_completion_time ? new Date(experimentData.estimated_completion_time.seconds * 1000) : null
      });

      // Save the experiment to the database
      await experiment.save();

      // Create initial metrics snapshot if metrics exist
      if (experimentData.metrics && Object.keys(experimentData.metrics).length > 0) {
        const metricsSnapshot = ExperimentMetrics.fromGrpc(experimentData.id.id, experimentData.metrics);
        await metricsSnapshot.save();
      }

      return experiment;
    } catch (error) {
      logger.error(`Error creating experiment in database: ${error.message}`);
      throw error;
    }
  }

  /**
   * Update an existing experiment in the database
   * @param {Object} experimentData - Experiment data from gRPC
   * @returns {Promise<Object>} Updated experiment
   */
  async updateExperiment(experimentData) {
    try {
      // Find the experiment by ID
      const experiment = await Experiment.findById(experimentData.id.id);

      if (!experiment) {
        throw new Error(`Experiment with ID ${experimentData.id.id} not found`);
      }

      // Update the experiment with new data
      experiment.name = experimentData.name;
      experiment.type = experimentData.type;
      experiment.state = experimentData.state;
      experiment.statusMessage = experimentData.status_message;
      experiment.metrics = experimentData.metrics || {};

      if (experimentData.start_time) {
        experiment.startTime = new Date(experimentData.start_time.seconds * 1000);
      }

      experiment.lastUpdateTime = experimentData.last_update_time ?
        new Date(experimentData.last_update_time.seconds * 1000) : new Date();

      if (experimentData.estimated_completion_time) {
        experiment.estimatedCompletionTime = new Date(experimentData.estimated_completion_time.seconds * 1000);
      }

      // Save the updated experiment
      await experiment.save();

      // Create metrics snapshot if metrics exist and have changed
      if (experimentData.metrics && Object.keys(experimentData.metrics).length > 0) {
        const metricsSnapshot = ExperimentMetrics.fromGrpc(experimentData.id.id, experimentData.metrics);
        await metricsSnapshot.save();
      }

      return experiment;
    } catch (error) {
      logger.error(`Error updating experiment in database: ${error.message}`);
      throw error;
    }
  }

  /**
   * Get an experiment by ID
   * @param {String} experimentId - Experiment ID
   * @returns {Promise<Object>} Experiment document
   */
  async getExperimentById(experimentId) {
    try {
      return await Experiment.findById(experimentId);
    } catch (error) {
      logger.error(`Error getting experiment from database: ${error.message}`);
      throw error;
    }
  }

  /**
   * List experiments with optional filtering
   * @param {Object} filters - Filter criteria
   * @param {Number} page - Page number (1-based)
   * @param {Number} limit - Number of items per page
   * @returns {Promise<Object>} Paginated experiments
   */
  async listExperiments(filters = {}, page = 1, limit = 10) {
    try {
      const skip = (page - 1) * limit;
      const query = { ...filters };

      // Execute the query with pagination
      const experiments = await Experiment.find(query)
        .sort({ lastUpdateTime: -1 })
        .skip(skip)
        .limit(limit);

      // Get total count for pagination
      const total = await Experiment.countDocuments(query);

      return {
        experiments,
        pagination: {
          total,
          page,
          limit,
          pages: Math.ceil(total / limit)
        }
      };
    } catch (error) {
      logger.error(`Error listing experiments from database: ${error.message}`);
      throw error;
    }
  }

  /**
   * Add a log entry for an experiment
   * @param {Object} logEntry - Log entry data
   * @returns {Promise<Object>} Created log entry
   */
  async addLogEntry(logEntry) {
    try {
      const log = ExperimentLog.fromGrpc(logEntry);
      return await log.save();
    } catch (error) {
      logger.error(`Error adding log entry to database: ${error.message}`);
      throw error;
    }
  }

  /**
   * Get logs for an experiment
   * @param {String} experimentId - Experiment ID
   * @param {Object} filters - Filter criteria
   * @param {Number} limit - Number of logs to retrieve
   * @returns {Promise<Array>} Log entries
   */
  async getExperimentLogs(experimentId, filters = {}, limit = 100) {
    try {
      const query = { experimentId, ...filters };

      return await ExperimentLog.find(query)
        .sort({ timestamp: -1 })
        .limit(limit);
    } catch (error) {
      logger.error(`Error getting experiment logs from database: ${error.message}`);
      throw error;
    }
  }

  /**
   * Get metrics history for an experiment
   * @param {String} experimentId - Experiment ID
   * @param {Number} timeRangeMinutes - Time range in minutes (0 for all)
   * @param {Number} limit - Number of metrics points to retrieve
   * @returns {Promise<Array>} Metrics history
   */
  async getExperimentMetricsHistory(experimentId, timeRangeMinutes = 0, limit = 100) {
    try {
      const query = { experimentId };

      // Add time range filter if specified
      if (timeRangeMinutes > 0) {
        const startTime = new Date();
        startTime.setMinutes(startTime.getMinutes() - timeRangeMinutes);
        query.timestamp = { $gte: startTime };
      }

      return await ExperimentMetrics.find(query)
        .sort({ timestamp: -1 })
        .limit(limit);
    } catch (error) {
      logger.error(`Error getting experiment metrics history from database: ${error.message}`);
      throw error;
    }
  }

  /**
   * Create a metrics snapshot for an experiment
   * @param {String} experimentId - Experiment ID
   * @param {Object} metrics - Metrics data
   * @returns {Promise<Object>} Created metrics snapshot
   */
  async createMetricsSnapshot(experimentId, metrics) {
    try {
      // Create metrics snapshot
      const metricsSnapshot = ExperimentMetrics.fromGrpc(experimentId, metrics);

      // Save to database
      await metricsSnapshot.save();

      // Update experiment with latest metrics
      const experiment = await this.getExperimentById(experimentId);
      if (experiment) {
        experiment.metrics = metrics;
        experiment.lastUpdateTime = new Date();
        await experiment.save();
      }

      return metricsSnapshot;
    } catch (error) {
      logger.error(`Error creating metrics snapshot in database: ${error.message}`);
      throw error;
    }
  }
}

module.exports = new ExperimentService();
