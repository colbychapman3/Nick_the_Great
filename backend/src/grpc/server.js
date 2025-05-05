const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');
const memory = require('../memory/memory');

const PROTO_PATH = path.join(__dirname, '../../proto/agent.proto');
const packageDefinition = protoLoader.loadSync(PROTO_PATH);
const { agent } = grpc.loadPackageDefinition(packageDefinition);

class AgentService {
  async ExecuteCommand(call, callback) {
    const { command_text, source } = call.request;
    await memory.saveEntry({
      content: command_text,
      source: source,
      priority: source === 'cli' ? 30 : 10
    });
    callback(null, { success: true, message: `Processed "${command_text}"` });
  }

  StreamState(call) {
    setInterval(async () => {
      call.write({
        current_tasks: [],
        status_message: "Operational",
        recent_memory: await memory.getRecentEntries(3)
      });
    }, 2000);
  }
}

const server = new grpc.Server();
server.addService(agent.AgentService.service, new AgentService());
server.bindAsync(
  '0.0.0.0:50051',
  grpc.ServerCredentials.createInsecure(),
  () => server.start()
);
