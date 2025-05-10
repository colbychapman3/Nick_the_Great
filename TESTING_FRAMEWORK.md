# Testing Framework for Nick the Great

This document describes the testing framework for the Nick the Great project, which includes unit tests, integration tests, and end-to-end tests for all components of the system.

## Overview

The testing framework is designed to ensure the reliability and correctness of the Nick the Great system. It includes:

1. **Backend Tests**: Unit and integration tests for the Node.js/Express API server.
2. **Agent Core Tests**: Unit and integration tests for the Python gRPC Agent Core Service.
3. **Frontend Tests**: Component and integration tests for the Next.js web application.
4. **Mobile Tests**: Component and integration tests for the React Native mobile application.

## Backend Testing

### Setup

The backend testing framework uses Jest as the test runner and assertion library. It also uses MongoDB Memory Server to create an in-memory MongoDB database for testing.

#### Running Tests

```bash
cd backend
npm install
npm test                # Run all tests
npm run test:watch      # Run tests in watch mode
npm run test:coverage   # Run tests with coverage report
npm run test:db         # Run database connection test
npm run test:experiment # Run experiment database test
npm run test:db-sync    # Run database sync service test
```

### Test Structure

- **Unit Tests**: Located in `backend/tests` directory, with a structure mirroring the `src` directory.
- **Integration Tests**: Located in `backend/tests/api` directory, testing API endpoints.
- **Test Helpers**: Located in `backend/tests/helpers.js`, providing utility functions for tests.

### Key Features

- **In-Memory Database**: Tests use MongoDB Memory Server to create an isolated database for each test run.
- **Mocking**: External services and dependencies are mocked to isolate tests.
- **Coverage Reports**: Test coverage reports are generated to identify untested code.

## Agent Core Testing

### Setup

The Agent Core testing framework uses pytest as the test runner and assertion library.

#### Running Tests

```bash
cd agent_core
pip install -r requirements.txt
pytest                  # Run all tests
pytest -xvs             # Run tests with verbose output
pytest --cov=.          # Run tests with coverage report
pytest tests/test_db_sync.py  # Run specific test file
```

### Test Structure

- **Unit Tests**: Located in `agent_core/tests` directory.
- **Fixtures**: Defined in `agent_core/tests/conftest.py`, providing common test fixtures.

### Key Features

- **Mocking**: External services and dependencies are mocked to isolate tests.
- **Fixtures**: Common test fixtures are defined to reduce test setup code.
- **Coverage Reports**: Test coverage reports are generated to identify untested code.

## Frontend Testing

### Setup

The frontend testing framework uses Jest as the test runner and React Testing Library for testing React components.

#### Running Tests

```bash
cd frontend
npm install
npm test                # Run all tests
npm run test:watch      # Run tests in watch mode
npm run test:coverage   # Run tests with coverage report
```

### Test Structure

- **Component Tests**: Located alongside the components they test, with a `.test.tsx` extension.
- **Hook Tests**: Located alongside the hooks they test, with a `.test.tsx` extension.
- **Test Utilities**: Located in `frontend/src/utils/test-utils.tsx`, providing utility functions for tests.

### Key Features

- **Component Testing**: Tests focus on component behavior rather than implementation details.
- **Mocking**: External services and dependencies are mocked to isolate tests.
- **Coverage Reports**: Test coverage reports are generated to identify untested code.

## Mobile Testing

### Setup

The mobile testing framework uses Jest as the test runner and React Native Testing Library for testing React Native components.

#### Running Tests

```bash
cd mobile
npm install
npm test                # Run all tests
npm run test:watch      # Run tests in watch mode
npm run test:coverage   # Run tests with coverage report
```

### Test Structure

- **Component Tests**: Located alongside the components they test, with a `.test.tsx` extension.
- **Test Utilities**: Located in `mobile/src/utils/test-utils.tsx`, providing utility functions for tests.

### Key Features

- **Component Testing**: Tests focus on component behavior rather than implementation details.
- **Mocking**: External services and dependencies are mocked to isolate tests.
- **Coverage Reports**: Test coverage reports are generated to identify untested code.

## Continuous Integration

The testing framework is integrated with the CI/CD pipeline to ensure that all tests pass before code is deployed to production.

### GitHub Actions Workflow

A GitHub Actions workflow is configured to run all tests on every push and pull request. The workflow includes:

1. **Backend Tests**: Runs all backend tests with coverage report.
2. **Agent Core Tests**: Runs all Agent Core tests with coverage report.
3. **Frontend Tests**: Runs all frontend tests with coverage report.
4. **Mobile Tests**: Runs all mobile tests with coverage report.

### Test Coverage Requirements

The CI/CD pipeline enforces minimum test coverage requirements:

- **Backend**: 70% coverage for branches, functions, lines, and statements.
- **Agent Core**: 70% coverage for branches, functions, lines, and statements.
- **Frontend**: 70% coverage for branches, functions, lines, and statements.
- **Mobile**: 70% coverage for branches, functions, lines, and statements.

## Best Practices

### Writing Tests

1. **Test Behavior, Not Implementation**: Focus on testing the behavior of the code, not the implementation details.
2. **Isolate Tests**: Each test should be independent of other tests.
3. **Mock External Dependencies**: Mock external services and dependencies to isolate tests.
4. **Use Descriptive Test Names**: Test names should describe what the test is testing.
5. **Follow AAA Pattern**: Arrange, Act, Assert pattern for organizing tests.

### Test Coverage

1. **Aim for High Coverage**: Aim for at least 70% coverage for all code.
2. **Focus on Critical Paths**: Ensure critical paths have 100% coverage.
3. **Don't Chase Coverage**: Don't write tests just to increase coverage.

## Recent Improvements

The testing framework has been enhanced with the following additions:

1. **Task Module Unit Tests**: Added comprehensive unit tests for task modules, including:
   - `test_ebook_generator_task.py`: Tests for the EbookGeneratorTask class
   - `test_freelance_writing_task.py`: Tests for the FreelanceWritingTask class
   - `test_niche_affiliate_website_task.py`: Tests for the NicheAffiliateWebsiteTask class
   - `test_pinterest_strategy_task.py`: Tests for the PinterestStrategyTask class

2. **Agent Core Integration Tests**: Added integration tests that test the interaction between Agent Core and task modules:
   - `test_agent_task_integration.py`: Tests the full experiment lifecycle
   - `test_task_modules_integration.py`: Tests the integration between the agent core and task modules
   - `test_agent_backend_integration.py`: Tests the integration between the agent core and backend API

3. **Autonomy Framework Tests**: Added comprehensive tests for the autonomy framework:
   - `test_autonomy_framework.py`: Tests the basic autonomy framework functionality
   - `test_enhanced_autonomy_framework.py`: Tests the enhanced autonomy framework with risk tolerance and experimentation
   - `test_autonomy_integration.py`: Tests the integration between the autonomy framework and the agent core
   - `test_decision_matrix.py`: Tests the decision matrix component
   - `test_notification_system.py`: Tests the notification system component
   - `test_approval_workflow.py`: Tests the approval workflow component
   - `test_risk_tolerance.py`: Tests the risk tolerance framework
   - `test_experimentation_framework.py`: Tests the experimentation framework

4. **Database Client Tests**: Enhanced tests for the database client:
   - `test_db_client.py`: Tests the database synchronization functionality
   - `test_db_sync.py`: Tests the database sync service integration

5. **Test Runner Script**: Added a script to run all tests:
   - `run_tests.sh`: Runs tests for all components with proper environment setup

## Future Improvements

1. **End-to-End Tests**: Add end-to-end tests that test the entire system.
2. **Performance Tests**: Add performance tests to ensure the system meets performance requirements.
3. **Load Tests**: Add load tests to ensure the system can handle expected load.
4. **Security Tests**: Add security tests to identify security vulnerabilities.
5. **Visual Regression Tests**: Add visual regression tests for the frontend and mobile app.
6. **Snapshot Tests**: Add snapshot tests for UI components.
7. **Contract Tests**: Add contract tests to ensure API compatibility.
8. **Mutation Tests**: Add mutation tests to ensure test quality.
