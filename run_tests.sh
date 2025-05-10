#!/bin/bash

# Run tests for the Nick the Great project

# Set environment variables for testing
export ABACUSAI_API_KEY="test-api-key"
export AGENT_CORE_PORT="50051"
export BACKEND_HOST="localhost"
export BACKEND_PORT="3001"
export BACKEND_GRPC_PORT="50052"
export DB_SYNC_ENABLED="false"
export MONGODB_URI="mongodb://localhost:27017/nick_agent_test"
export JWT_SECRET="test-jwt-secret"

# Function to run tests with a header
run_tests() {
    echo "============================================================"
    echo "Running $1 tests"
    echo "============================================================"
    $2
    if [ $? -ne 0 ]; then
        echo "❌ $1 tests failed"
        exit 1
    else
        echo "✅ $1 tests passed"
    fi
    echo ""
}

# Check if a specific component was specified
if [ "$1" == "agent" ]; then
    # Run Agent Core tests
    cd agent_core
    run_tests "Agent Core" "python -m pytest"
elif [ "$1" == "backend" ]; then
    # Run Backend tests
    cd backend
    run_tests "Backend" "npm test"
elif [ "$1" == "frontend" ]; then
    # Run Frontend tests
    cd frontend
    run_tests "Frontend" "npm test"
elif [ "$1" == "mobile" ]; then
    # Run Mobile tests
    cd mobile
    run_tests "Mobile" "npm test"
else
    # Run all tests
    
    # Run Agent Core tests
    cd agent_core
    run_tests "Agent Core" "python -m pytest"
    cd ..
    
    # Run Backend tests
    cd backend
    run_tests "Backend" "npm test"
    cd ..
    
    # Run Frontend tests
    cd frontend
    run_tests "Frontend" "npm test"
    cd ..
    
    # Run Mobile tests
    cd mobile
    run_tests "Mobile" "npm test"
    cd ..
fi

echo "============================================================"
echo "All tests completed successfully! 🎉"
echo "============================================================"
