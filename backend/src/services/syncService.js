const { getExperimentStatus, listExperiments } = require('../agent_client');
const experimentService = require('./experimentService');
const logger = require('../utils/logger');

/**
 * Service for synchronizing experiment data between Agent Core and MongoDB
 */
class SyncService {
  constructor() {
    this.isRunning = false;
    this.syncInterval = null;
    this.syncIntervalMs = 30000; // 30 seconds by default
  }

  /**
   * Start the synchronization service
   * @param {Number} intervalMs - Sync interval in milliseconds (default: 30000)
   */
  start(intervalMs = 30000) {
    if (this.isRunning) {
      logger.warn('Sync service is already running');
      return;
    }

    this.syncIntervalMs = intervalMs;
    this.isRunning = true;
    
    // Run initial sync immediately
    this.syncExperiments();
    
    // Set up interval for regular syncing
    this.syncInterval = setInterval(() => {
      this.syncExperiments();
    }, this.syncIntervalMs);
    
    logger.info(`Sync service started with interval of ${this.syncIntervalMs}ms`);
  }

  /**
   * Stop the synchronization service
   */
  stop() {
    if (!this.isRunning) {
      logger.warn('Sync service is not running');
      return;
    }

    clearInterval(this.syncInterval);
    this.syncInterval = null;
    this.isRunning = false;
    
    logger.info('Sync service stopped');
  }

  /**
   * Synchronize experiments between Agent Core and MongoDB
   */
  async syncExperiments() {
    try {
      logger.info('Starting experiment synchronization');
      
      // Get all experiments from Agent Core
      const agentCoreExperiments = await listExperiments();
      
      if (!agentCoreExperiments || !Array.isArray(agentCoreExperiments)) {
        logger.warn('No experiments returned from Agent Core or invalid response');
        return;
      }
      
      logger.info(`Found ${agentCoreExperiments.length} experiments in Agent Core`);
      
      // Process each experiment
      for (const experiment of agentCoreExperiments) {
        try {
          // Get detailed status for this experiment
          const experimentStatus = await getExperimentStatus(experiment.id.id);
          
          // Check if experiment exists in database
          const existingExperiment = await experimentService.getExperimentById(experimentStatus.id.id);
          
          if (existingExperiment) {
            // Update existing experiment
            await experimentService.updateExperiment(experimentStatus);
            logger.info(`Updated experiment ${experimentStatus.id.id} in database`);
          } else {
            // This is an experiment we don't have in our database yet
            // We need a user ID to associate it with, but we don't have that information
            // For now, we'll associate it with a system user ID
            const systemUserId = process.env.SYSTEM_USER_ID || 'system';
            await experimentService.createExperiment(experimentStatus, systemUserId);
            logger.info(`Created new experiment ${experimentStatus.id.id} in database`);
          }
        } catch (error) {
          logger.error(`Error processing experiment ${experiment.id.id}: ${error.message}`);
          // Continue with next experiment
        }
      }
      
      logger.info('Experiment synchronization completed');
    } catch (error) {
      logger.error(`Error during experiment synchronization: ${error.message}`);
    }
  }

  /**
   * Synchronize a specific experiment
   * @param {String} experimentId - Experiment ID to synchronize
   */
  async syncExperiment(experimentId) {
    try {
      logger.info(`Synchronizing experiment ${experimentId}`);
      
      // Get experiment status from Agent Core
      const experimentStatus = await getExperimentStatus(experimentId);
      
      if (!experimentStatus || !experimentStatus.id) {
        logger.warn(`No valid status returned from Agent Core for experiment ${experimentId}`);
        return;
      }
      
      // Check if experiment exists in database
      const existingExperiment = await experimentService.getExperimentById(experimentId);
      
      if (existingExperiment) {
        // Update existing experiment
        await experimentService.updateExperiment(experimentStatus);
        logger.info(`Updated experiment ${experimentId} in database`);
      } else {
        // This is an experiment we don't have in our database yet
        // We need a user ID to associate it with, but we don't have that information
        // For now, we'll associate it with a system user ID
        const systemUserId = process.env.SYSTEM_USER_ID || 'system';
        await experimentService.createExperiment(experimentStatus, systemUserId);
        logger.info(`Created new experiment ${experimentId} in database`);
      }
      
      return true;
    } catch (error) {
      logger.error(`Error synchronizing experiment ${experimentId}: ${error.message}`);
      return false;
    }
  }
}

module.exports = new SyncService();
