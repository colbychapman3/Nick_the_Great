#!/bin/bash

# Script to generate gRPC code from proto files
# This script should be run from the project root directory

# Create directories for generated code if they don't exist
mkdir -p agent_core/generated
mkdir -p backend/src/generated

# Generate Python code for agent.proto
python -m grpc_tools.protoc \
  -I. \
  --python_out=agent_core/generated \
  --grpc_python_out=agent_core/generated \
  proto/agent.proto

# Generate Python code for database_sync.proto
python -m grpc_tools.protoc \
  -I. \
  --python_out=agent_core/generated \
  --grpc_python_out=agent_core/generated \
  proto/database_sync.proto

# Generate JavaScript code for agent.proto
npx grpc_tools_node_protoc \
  --js_out=import_style=commonjs,binary:backend/src/generated \
  --grpc_out=grpc_js:backend/src/generated \
  --proto_path=. \
  proto/agent.proto

# Generate JavaScript code for database_sync.proto
npx grpc_tools_node_protoc \
  --js_out=import_style=commonjs,binary:backend/src/generated \
  --grpc_out=grpc_js:backend/src/generated \
  --proto_path=. \
  proto/database_sync.proto

# Fix Python imports in generated code
# This is needed because the generated code uses relative imports
# but we want to use absolute imports
sed -i 's/import agent_pb2/from agent_core.generated import agent_pb2/g' agent_core/generated/agent_pb2_grpc.py
sed -i 's/import database_sync_pb2/from agent_core.generated import database_sync_pb2/g' agent_core/generated/database_sync_pb2_grpc.py

# Create __init__.py files to make the generated code importable
touch agent_core/generated/__init__.py

echo "Proto code generation complete!"
