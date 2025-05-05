/**
 * Deployment Verification Script
 *
 * This script verifies that all critical endpoints of the Nick the Great API
 * are functioning correctly. It tests authentication, database connections,
 * and API functionality.
 *
 * Dependencies:
 * - Requires `node-fetch`: Run `npm install node-fetch` in the backend directory.
 *
 * Usage:
 * - Local testing: node deployment-verification.js
 * - Remote testing: node deployment-verification.js https://nick-the-great.onrender.com
 *
 * Note: This script creates test data (user, strategy, resource) and attempts
 * to clean up the strategy and resource afterwards. The test user needs to be
 * deleted manually. It also uses a hardcoded password for the test user, which
 * is acceptable for this internal script but should be handled carefully.
 */

const fetch = require('node-fetch');
global.fetch = require('node-fetch'); // Make fetch global
const { promisify } = require('util');
const { exec } = require('child_process');
const execAsync = promisify(exec);
const readline = require('readline');

// Default to localhost if no URL provided
const BASE_URL = process.argv[2] || 'http://localhost:10000';

// Create interactive console interface
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

const question = (query) => new Promise((resolve) => rl.question(query, resolve));

// Helper function to make HTTP requests
async function makeRequest(endpoint, options = {}) {
  const url = `${BASE_URL}${endpoint}`;
  console.log(`Making request to: ${url}`);

  try {
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      ...options
    });

    let data;
    try {
      data = await response.json();
    } catch (jsonError) {
      // Log the actual response text when JSON parsing fails
      const rawText = await response.text().catch(() => "Could not extract response text");
      console.error(`JSON parsing error: ${jsonError.message}`);
      console.error(`Raw response: ${rawText}`);
      return {
        status: response.status,
        data: null,
        ok: false,
        error: jsonError.message,
        rawResponse: rawText
      };
    }

    return {
      status: response.status,
      data,
      ok: response.ok,
      response
    };
  } catch (error) {
    console.error(`Error requesting ${url}:`, error.message);
    return {
      status: 0,
      data: null,
      ok: false,
      error: error.message
    };
  }
}

// Main verification function
async function verifyDeployment() {
  console.log('\n=== NICK THE GREAT API DEPLOYMENT VERIFICATION ===');
  console.log(`Testing API at: ${BASE_URL}`);

  let token = null;
  let userId = null;

  // Step 1: Check health endpoint
  console.log('\n--- Step 1: Health Check ---');
  const healthCheck = await makeRequest('/health');

  if (healthCheck.ok && healthCheck.data.message === 'OK') {
    console.log('✅ Health check endpoint is working');
    console.log(`   Server uptime: ${healthCheck.data.uptime} seconds`);
  } else {
    console.log('❌ Health check endpoint failed');
    console.log('   This indicates a basic server connectivity issue');
    await askToContinue();
  }

  // Step 2: Test registration
  console.log('\n--- Step 2: User Registration ---');
  console.log('Creating a test user for verification...');

  // Generate a unique email for testing
  const testEmail = `test-${Date.now()}@example.com`;
  const testPassword = 'Password123!';
  const testName = 'Test User';

  const registrationResult = await makeRequest('/auth/register', {
    method: 'POST',
    body: JSON.stringify({
      email: testEmail,
      password: testPassword,
      name: testName
    })
  });

  if (registrationResult.ok) {
    console.log('✅ Registration endpoint is working');
    token = registrationResult.data.token;
    userId = registrationResult.data.user.id;
    console.log(`   Created test user: ${testEmail}`);
  } else {
    console.log('❌ Registration endpoint failed');
    console.log(`   Error: ${JSON.stringify(registrationResult.data)}`);
    await askToContinue();
  }

  // Step 3: Test login
  console.log('\n--- Step 3: User Login ---');

  const loginResult = await makeRequest('/auth/login', {
    method: 'POST',
    body: JSON.stringify({
      email: testEmail,
      password: testPassword
    })
  });

  if (loginResult.ok) {
    console.log('✅ Login endpoint is working');
    // Update token in case registration didn't work but login did
    token = loginResult.data.token || token;
    userId = loginResult.data.user.id || userId;
  } else {
    console.log('❌ Login endpoint failed');
    console.log(`   Error: ${JSON.stringify(loginResult.data)}`);
    await askToContinue();
  }

  if (!token) {
    console.log('\n⚠️ Unable to obtain authentication token. Cannot test authenticated endpoints.');
    return;
  }

  // Step 4: Test authenticated API endpoints
  console.log('\n--- Step 4: Testing Authenticated Endpoints ---');

  // Test strategies endpoint
  const strategiesResult = await makeRequest('/api/strategies', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });

  if (strategiesResult.ok) {
    console.log('✅ Strategies endpoint is working');
    console.log(`   Retrieved ${strategiesResult.data.length || 0} strategies`);
  } else {
    console.log('❌ Strategies endpoint failed');
    console.log(`   Error: ${JSON.stringify(strategiesResult.data)}`);
  }

  // Test resources endpoint
  const resourcesResult = await makeRequest('/api/resources', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });

  if (resourcesResult.ok) {
    console.log('✅ Resources endpoint is working');
    console.log(`   Retrieved ${resourcesResult.data.length || 0} resources`);
  } else {
    console.log('❌ Resources endpoint failed');
    console.log(`   Error: ${JSON.stringify(resourcesResult.data)}`);
  }

  // Test agent configuration endpoint
  const configResult = await makeRequest('/api/agent/config', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });

  if (configResult.ok) {
    console.log('✅ Agent configuration endpoint is working');
  } else {
    console.log('❌ Agent configuration endpoint failed');
    console.log(`   Error: ${JSON.stringify(configResult.data)}`);
  }

  // Step 5: Test creating data
  console.log('\n--- Step 5: Testing Data Creation ---');

  // Create a test strategy
  let strategyId;
  const testStrategy = {
    name: 'Test Strategy',
    description: 'Created by deployment verification script',
    status: 'draft'
  };

  const createStrategyResult = await makeRequest('/api/strategies', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(testStrategy)
  });

  if (createStrategyResult.ok) {
    console.log('✅ Strategy creation is working');
    strategyId = createStrategyResult.data._id;
    console.log(`   Created strategy with ID: ${strategyId}`);
  } else {
    console.log('❌ Strategy creation failed');
    console.log(`   Error: ${JSON.stringify(createStrategyResult.data)}`);
  }

  // Create a test resource
  let resourceId;
  const testResource = {
    title: 'Test Resource',
    description: 'Created by deployment verification script',
    url: 'https://example.com/test-resource',
    category: 'Test'
  };

  const createResourceResult = await makeRequest('/api/resources', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(testResource)
  });

  if (createResourceResult.ok) {
    console.log('✅ Resource creation is working');
    resourceId = createResourceResult.data._id;
    console.log(`   Created resource with ID: ${resourceId}`);
  } else {
    console.log('❌ Resource creation failed');
    console.log(`   Error: ${JSON.stringify(createResourceResult.data)}`);
  }

  // Step 6: Check MongoDB connection
  console.log('\n--- Step 6: MongoDB Connection Check ---');
  console.log('This test will check if MongoDB is properly connected by analyzing API responses...');

  if (strategiesResult.ok && resourcesResult.ok && configResult.ok) {
    console.log('✅ MongoDB connection appears to be working');
    console.log('   All database-dependent endpoints are responding correctly');
  } else {
    console.log('❌ MongoDB connection issues detected');
    console.log('   One or more database-dependent endpoints failed');
  }

  // Step 7: Cleanup test data
  console.log('\n--- Step 7: Cleaning Up Test Data ---');

  // Delete the created strategy
  if (createStrategyResult.ok) {
    const deleteStrategyResult = await makeRequest(`/api/strategies/${strategyId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (deleteStrategyResult.ok) {
      console.log('✅ Successfully deleted test strategy');
    } else {
      console.log('❌ Failed to delete test strategy');
      console.log(`   Error: ${JSON.stringify(deleteStrategyResult.data)}`);
    }
  }

  // Delete the created resource
  if (createResourceResult.ok) {
    const deleteResourceResult = await makeRequest(`/api/resources/${resourceId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (deleteResourceResult.ok) {
      console.log('✅ Successfully deleted test resource');
    } else {
      console.log('❌ Failed to delete test resource');
      console.log(`   Error: ${JSON.stringify(deleteResourceResult.data)}`);
    }
  }

  // Step 8: Delete the test user
  console.log('\n--- Step 8: Deleting Test User ---');
  console.log('⚠️  Deleting the test user requires an admin endpoint.  ⚠️');
  console.log('⚠️  This step is not automated in this script.             ⚠️');
  console.log('⚠️  Please manually delete the test user from the database. ⚠️');

  // Final results
  console.log('\n=== VERIFICATION SUMMARY ===');
  const testsPassed = [
    healthCheck.ok,
    registrationResult.ok,
    loginResult.ok,
    strategiesResult.ok,
    resourcesResult.ok,
    configResult.ok,
    createStrategyResult.ok,
    createResourceResult.ok
  ].filter(Boolean).length;

  const totalTests = 8;

  console.log(`Tests passed: ${testsPassed}/${totalTests} (${Math.round(testsPassed / totalTests * 100)}%)`);

  if (testsPassed === totalTests) {
    console.log('\n✅ ALL TESTS PASSED! The API deployment appears to be working correctly.');
  } else {
    console.log(`\n⚠️ ${totalTests - testsPassed} tests failed. Review the logs above for details.`);
  }

  console.log('\nDeployment verification completed.');
  rl.close();
}

// Utility function to ask for confirmation to continue
async function askToContinue() {
  const answer = await question('Do you want to continue with the tests anyway? (y/n): ');
  if (answer.toLowerCase() !== 'y') {
    console.log('Verification aborted by user.');
    rl.close();
    process.exit(0);
  }
}

// Run the verification
verifyDeployment().catch(error => {
  console.error('An unexpected error occurred during verification:', error);
  rl.close();
});
