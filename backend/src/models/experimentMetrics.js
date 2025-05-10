const mongoose = require('mongoose');
const Schema = mongoose.Schema;

/**
 * Experiment Metrics Schema
 * Represents historical metrics data for an experiment
 */
const ExperimentMetricsSchema = new Schema({
  // Associated experiment ID
  experimentId: {
    type: String,
    required: true,
    index: true
  },
  // Timestamp of the metrics snapshot
  timestamp: {
    type: Date,
    required: true,
    default: Date.now,
    index: true
  },
  // Progress percentage (0-100)
  progressPercent: {
    type: Number,
    min: 0,
    max: 100,
    default: 0
  },
  // Elapsed time in seconds
  elapsedTimeSeconds: {
    type: Number,
    min: 0,
    default: 0
  },
  // Estimated remaining time in seconds
  estimatedRemainingSeconds: {
    type: Number,
    min: 0,
    default: 0
  },
  // CPU usage percentage
  cpuUsagePercent: {
    type: Number,
    min: 0,
    max: 100,
    default: 0
  },
  // Memory usage in MB
  memoryUsageMb: {
    type: Number,
    min: 0,
    default: 0
  },
  // Error count
  errorCount: {
    type: Number,
    min: 0,
    default: 0
  },
  // Additional metrics specific to experiment type
  additionalMetrics: {
    type: Schema.Types.Mixed,
    default: {}
  }
}, {
  timestamps: true // Automatically manage createdAt and updatedAt
});

// Add compound index for efficient querying
ExperimentMetricsSchema.index({ experimentId: 1, timestamp: -1 });

/**
 * Create metrics entry from gRPC metrics Struct
 * @param {String} experimentId - Experiment ID
 * @param {Object} metricsStruct - gRPC metrics Struct
 * @returns {Object} New ExperimentMetrics document
 */
ExperimentMetricsSchema.statics.fromGrpc = function(experimentId, metricsStruct) {
  // Extract standard metrics
  const standardMetrics = {
    experimentId,
    timestamp: new Date(),
    progressPercent: metricsStruct.progress_percent || 0,
    elapsedTimeSeconds: metricsStruct.elapsed_time_seconds || 0,
    estimatedRemainingSeconds: metricsStruct.estimated_remaining_seconds || 0,
    cpuUsagePercent: metricsStruct.cpu_usage_percent || 0,
    memoryUsageMb: metricsStruct.memory_usage_mb || 0,
    errorCount: metricsStruct.error_count || 0
  };

  // Extract additional metrics (anything not in the standard set)
  const additionalMetrics = {};
  for (const key in metricsStruct) {
    if (!['progress_percent', 'elapsed_time_seconds', 'estimated_remaining_seconds', 
          'cpu_usage_percent', 'memory_usage_mb', 'error_count'].includes(key)) {
      additionalMetrics[key] = metricsStruct[key];
    }
  }

  return new this({
    ...standardMetrics,
    additionalMetrics
  });
};

// Create and export the model
const ExperimentMetrics = mongoose.model('ExperimentMetrics', ExperimentMetricsSchema);
module.exports = ExperimentMetrics;
