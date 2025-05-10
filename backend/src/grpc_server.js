/**
 * gRPC Server for the Backend
 * Handles communication with the Agent Core
 */

const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');
const logger = require('./utils/logger');
const databaseSyncService = require('./database_sync_service');

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

// Create gRPC server
const server = new grpc.Server();

// Add the DatabaseSyncService to the server
server.addService(dbSyncProto.DatabaseSyncService.service, {
  restoreExperiments: databaseSyncService.restoreExperiments,
  syncExperimentStatus: databaseSyncService.syncExperimentStatus,
  syncLogEntry: databaseSyncService.syncLogEntry,
  syncMetrics: databaseSyncService.syncMetrics
});

/**
 * Start the gRPC server
 * @param {Number} port - Port to listen on
 * @returns {Promise<void>} Promise that resolves when the server is started
 */
function startServer(port = 50052) {
  return new Promise((resolve, reject) => {
    server.bindAsync(`0.0.0.0:${port}`, grpc.ServerCredentials.createInsecure(), (error, actualPort) => {
      if (error) {
        logger.error(`Failed to start gRPC server: ${error.message}`);
        reject(error);
        return;
      }
      
      server.start();
      logger.info(`gRPC server started on port ${actualPort}`);
      resolve(actualPort);
    });
  });
}

/**
 * Stop the gRPC server
 * @returns {Promise<void>} Promise that resolves when the server is stopped
 */
function stopServer() {
  return new Promise((resolve) => {
    server.tryShutdown(() => {
      logger.info('gRPC server stopped');
      resolve();
    });
  });
}

module.exports = {
  startServer,
  stopServer
};
