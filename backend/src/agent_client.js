const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');
const logging = require('./logging'); // Assuming you have a logging module
const { Struct } = require('google-protobuf/google/protobuf/struct_pb'); // Import Struct

// Load environment variables
require('dotenv').config();

// Define the path to the proto file
const PROTO_PATH = path.resolve(__dirname, '../../proto/agent.proto');

// Load the proto definition
const packageDefinition = protoLoader.loadSync(
    PROTO_PATH,
    {
        keepCase: true,
        longs: String,
        enums: String,
        defaults: true,
        oneofs: true
    });

// Load the gRPC package
const nickthegreat_proto = grpc.loadPackageDefinition(packageDefinition).nickthegreat;

// Get the Agent Core Service address from environment variables
const AGENT_CORE_HOST = process.env.AGENT_CORE_HOST || 'localhost';
const AGENT_CORE_PORT = process.env.AGENT_CORE_PORT || 50051; // Corrected default port based on agent_core/main.py
const AGENT_CORE_ADDRESS = `${AGENT_CORE_HOST}:${AGENT_CORE_PORT}`;

// Create the gRPC client
let client;

function getClient() {
    if (!client) {
        // TODO: Implement TLS for production
        client = new nickthegreat_proto.AgentService(AGENT_CORE_ADDRESS, grpc.credentials.createInsecure());
        logging.info(`gRPC client created, connecting to ${AGENT_CORE_ADDRESS}`);
    }
    return client;
}

// Function to create a new experiment
function createExperiment(experimentDefinition) {
    return new Promise((resolve, reject) => {
        const request = {
            definition: experimentDefinition
        };
        getClient().CreateExperiment(request, (err, response) => {
            if (err) {
                logging.error(`Error creating experiment: ${err}`);
                reject(err);
            } else {
                logging.info(`CreateExperiment response: ${JSON.stringify(response)}`);
                resolve(response);
            }
        });
    });
}

// Function to start a specific experiment
function startExperiment(experimentId) {
    return new Promise((resolve, reject) => {
        const request = {
            id: { id: experimentId }
        };
        getClient().StartExperiment(request, (err, response) => {
            if (err) {
                logging.error(`Error starting experiment: ${err}`);
                reject(err);
            } else {
                logging.info(`StartExperiment response: ${JSON.stringify(response)}`);
                resolve(response);
            }
        });
    });
}

// Function to stop a specific experiment
function stopExperiment(experimentId) {
    return new Promise((resolve, reject) => {
        const request = {
            id: { id: experimentId }
        };
        getClient().StopExperiment(request, (err, response) => {
            if (err) {
                logging.error(`Error stopping experiment: ${err}`);
                reject(err);
            } else {
                logging.info(`StopExperiment response: ${JSON.stringify(response)}`);
                resolve(response);
            }
        });
    });
}

// Function to get the status of a specific experiment
function getExperimentStatus(experimentId) {
    return new Promise((resolve, reject) => {
        const request = {
            id: { id: experimentId }
        };
        getClient().GetExperimentStatus(request, (err, response) => {
            if (err) {
                logging.error(`Error getting experiment status: ${err}`);
                reject(err);
            } else {
                logging.info(`Experiment status for ${experimentId}: ${JSON.stringify(response)}`);
                resolve(response);
            }
        });
    });
}


// Function to get the overall agent status
function getAgentStatus(userId) {
  return new Promise((resolve, reject) => {
    getClient().GetAgentStatus({}, (err, response) => {
      if (err) {
        logging.error(`Error getting agent status: ${err}`);
        reject(err);
      } else {
        logging.info(`Agent status: ${JSON.stringify(response)}`);
        resolve(response);
      }
    });
  });
}

// Function to list all experiments (this is a backend-only function since there's no gRPC endpoint for it)
// It uses the existing experiment statuses stored in the Agent Core
function listExperiments() {
    return new Promise((resolve, reject) => {
        // We'll use a workaround by getting the agent status first
        getAgentStatus()
            .then(() => {
                // Now we'll try to get the status of some experiments
                // This is a temporary solution until we implement a proper ListExperiments gRPC method
                // For now, we'll maintain a list of experiment IDs in the backend
                const experimentIds = global.experimentIds || [];

                // If we have no experiment IDs, return an empty array
                if (experimentIds.length === 0) {
                    return resolve([]);
                }

                // Get the status of each experiment
                const promises = experimentIds.map(id => getExperimentStatus(id));
                Promise.all(promises)
                    .then(statuses => {
                        // Filter out any null or undefined statuses
                        const validStatuses = statuses.filter(status => status && status.id);
                        resolve(validStatuses);
                    })
                    .catch(err => {
                        logging.error(`Error getting experiment statuses: ${err}`);
                        reject(err);
                    });
            })
            .catch(err => {
                logging.error(`Error getting agent status: ${err}`);
                reject(err);
            });
    });
}

// Function to stream logs from the agent
function getLogs(experimentId, minimumLevel) {
    const request = {
        experiment_id: experimentId ? { id: experimentId } : null,
        minimum_level: minimumLevel || nickthegreat_proto.LogLevel.LOG_LEVEL_UNSPECIFIED
    };
    const call = getClient().GetLogs(request);
    logging.info(`Streaming logs with request: ${JSON.stringify(request)}`);
    return call; // Return the readable stream
}

// Function to approve or reject a pending agent decision
function approveDecision(decisionId, userId, approved, comment) {
    return new Promise((resolve, reject) => {
        const request = {
            decision_id: { id: decisionId },
            user_id: userId,
            approved: approved,
            comment: comment
        };
        getClient().ApproveDecision(request, (err, response) => {
            if (err) {
                logging.error(`Error approving decision: ${err}`);
                reject(err);
            } else {
                logging.info(`ApproveDecision response: ${JSON.stringify(response)}`);
                resolve(response);
            }
        });
    });
}

// Function to immediately stop all agent activities (kill switch)
function stopAgent(reason) {
    return new Promise((resolve, reject) => {
        const request = {
            reason: reason || ""
        };
        getClient().StopAgent(request, (err, response) => {
            if (err) {
                logging.error(`Error stopping agent: ${err}`);
                reject(err);
            } else {
                logging.info(`StopAgent response: ${JSON.stringify(response)}`);
                resolve(response);
            }
        });
    });
}


module.exports = {
    getClient,
    createExperiment,
    startExperiment,
    stopExperiment,
    getExperimentStatus,
    getAgentStatus,
    listExperiments,
    getLogs,
    approveDecision,
    stopAgent,
    // Expose proto enums and types if needed in backend routes
    ExperimentType: nickthegreat_proto.ExperimentType,
    ExperimentState: nickthegreat_proto.ExperimentState,
    LogLevel: nickthegreat_proto.LogLevel,
    ExperimentDefinition: nickthegreat_proto.ExperimentDefinition,
    ExperimentId: nickthegreat_proto.ExperimentId,
    DecisionId: nickthegreat_proto.DecisionId,
    StatusResponse: nickthegreat_proto.StatusResponse,
    AgentStatus: nickthegreat_proto.AgentStatus,
    ExperimentStatus: nickthegreat_proto.ExperimentStatus,
    LogEntry: nickthegreat_proto.LogEntry,
    Struct: Struct // Export Struct for creating parameters
};
