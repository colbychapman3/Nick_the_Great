const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');
const logging = require('./logging'); // Assuming you have a logging module

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
const AGENT_CORE_PORT = process.env.AGENT_CORE_PORT || 50052;
const AGENT_CORE_ADDRESS = `${AGENT_CORE_HOST}:${AGENT_CORE_PORT}`;

// Create the gRPC client
let client;

function getClient() {
    if (!client) {
        client = new nickthegreat_proto.AgentService(AGENT_CORE_ADDRESS, grpc.credentials.createInsecure());
        logging.info(`gRPC client created, connecting to ${AGENT_CORE_ADDRESS}`);
    }
    return client;
}

// Function to get the agent status
function getAgentStatus() {
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

module.exports = {
    getAgentStatus,
};
