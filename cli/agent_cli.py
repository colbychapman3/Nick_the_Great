import grpc
import agent_pb2
import agent_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')
stub = agent_pb2_grpc.AgentServiceStub(channel)

def execute_command(command):
    response = stub.ExecuteCommand(
        agent_pb2.CommandRequest(
            command_text=command,
            source="cli"
        )
    )
    print(f"Response: {response.message}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        execute_command(' '.join(sys.argv[1:]))
    else:
        print("Usage: python agent_cli.py <command_text>")
