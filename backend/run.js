// Simple startup script for our backend server
const { spawn } = require('child_process');
const path = require('path');

// Define colors for log output
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  dim: '\x1b[2m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
};

console.log(`${colors.bright}${colors.blue}Starting Nick the Great API Server${colors.reset}`);
console.log(`${colors.dim}Press Ctrl+C to stop${colors.reset}`);

// Path to the server entry point
const serverPath = path.join(__dirname, 'src', 'index.js');

// Spawn the server process
const server = spawn('node', [serverPath], {
  stdio: 'inherit',
  env: { ...process.env }
});

// Handle server process events
server.on('error', (error) => {
  console.error(`${colors.red}Failed to start server:${colors.reset}`, error);
});

server.on('close', (code) => {
  if (code !== 0) {
    console.log(`${colors.red}Server process exited with code ${code}${colors.reset}`);
  } else {
    console.log(`${colors.yellow}Server stopped${colors.reset}`);
  }
});

// Handle termination signals
process.on('SIGINT', () => {
  console.log(`\n${colors.cyan}Shutting down server...${colors.reset}`);
  server.kill('SIGINT');
});

process.on('SIGTERM', () => {
  console.log(`\n${colors.cyan}Shutting down server...${colors.reset}`);
  server.kill('SIGTERM');
});
