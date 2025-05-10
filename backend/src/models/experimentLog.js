const mongoose = require('mongoose');
const Schema = mongoose.Schema;

/**
 * Experiment Log Schema
 * Represents a log entry for an experiment
 */
const ExperimentLogSchema = new Schema({
  // Associated experiment ID
  experimentId: {
    type: String,
    required: true,
    index: true
  },
  // Timestamp of the log entry
  timestamp: {
    type: Date,
    required: true,
    default: Date.now,
    index: true
  },
  // Log level (maps to LogLevel enum in proto)
  level: {
    type: String,
    required: true,
    enum: ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
    default: 'INFO',
    index: true
  },
  // Log message
  message: {
    type: String,
    required: true
  },
  // Source component that generated the log
  sourceComponent: {
    type: String,
    default: 'AgentCore'
  }
}, {
  timestamps: true // Automatically manage createdAt and updatedAt
});

// Add compound index for efficient querying
ExperimentLogSchema.index({ experimentId: 1, timestamp: -1 });
ExperimentLogSchema.index({ experimentId: 1, level: 1, timestamp: -1 });

/**
 * Convert MongoDB document to gRPC LogEntry message format
 * @returns {Object} Object formatted for gRPC LogEntry
 */
ExperimentLogSchema.methods.toGrpcFormat = function() {
  return {
    timestamp: { seconds: Math.floor(this.timestamp.getTime() / 1000) },
    level: this.level,
    message: this.message,
    experiment_id: { id: this.experimentId },
    source_component: this.sourceComponent
  };
};

/**
 * Create a log entry from gRPC LogEntry message
 * @param {Object} logEntry - gRPC LogEntry message
 * @returns {Object} New ExperimentLog document
 */
ExperimentLogSchema.statics.fromGrpc = function(logEntry) {
  return new this({
    experimentId: logEntry.experiment_id.id,
    timestamp: new Date(logEntry.timestamp.seconds * 1000),
    level: logEntry.level,
    message: logEntry.message,
    sourceComponent: logEntry.source_component
  });
};

// Create and export the model
const ExperimentLog = mongoose.model('ExperimentLog', ExperimentLogSchema);
module.exports = ExperimentLog;
