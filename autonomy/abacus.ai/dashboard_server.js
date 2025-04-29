const express = require('express');
const path = require('path');
const http = require('http');
const axios = require('axios');
const socketIo = require('socket.io');

// Load environment variables
require('dotenv').config();

// Initialize Express app
const app = express();
const server = http.createServer(app);
const io = socketIo(server);

// API Gateway URL
const API_GATEWAY_URL = process.env.API_GATEWAY_URL || 'http://api-gateway:8080';

// Middleware
app.use(express.json());
app.use(express.static(path.join(__dirname, 'build')));

// API proxy middleware
app.use('/api', async (req, res) => {
  try {
    // Forward request to API Gateway
    const response = await axios({
      method: req.method,
      url: `${API_GATEWAY_URL}${req.url}`,
      data: req.method !== 'GET' ? req.body : undefined,
      headers: {
        'X-API-Key': req.headers['x-api-key'],
        'Authorization': req.headers['authorization']
      },
      params: req.query
    });
    
    // Return response
    res.status(response.status).json(response.data);
  } catch (error) {
    console.error(`Error proxying request to ${req.url}:`, error.message);
    
    // Return error response
    if (error.response) {
      res.status(error.response.status).json(error.response.data);
    } else {
      res.status(500).json({
        status: 'error',
        message: error.message,
        timestamp: new Date().toISOString()
      });
    }
  }
});

// Serve React app
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'build', 'index.html'));
});

// Socket.io connection
io.on('connection', (socket) => {
  console.log('New client connected');
  
  // Subscribe to Redis channels for real-time updates
  const redis = require('redis');
  const redisClient = redis.createClient({
    url: process.env.REDIS_URI || 'redis://redis:6379'
  });
  
  // Subscribe to events
  const channels = [
    'events:opportunity_scan_complete',
    'events:allocation_updated',
    'events:profits_reinvested'
  ];
  
  // Handle Redis messages
  channels.forEach(channel => {
    redisClient.subscribe(channel, (message) => {
      try {
        const data = JSON.parse(message);
        socket.emit(channel, data);
      } catch (error) {
        console.error(`Error parsing Redis message from ${channel}:`, error);
      }
    });
  });
  
  // Handle disconnect
  socket.on('disconnect', () => {
    console.log('Client disconnected');
    redisClient.quit();
  });
});

// Start server
const PORT = process.env.PORT || 80;
server.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

// Fetch system status periodically and broadcast to clients
const fetchSystemStatus = async () => {
  try {
    const response = await axios.get(`${API_GATEWAY_URL}/system/status`, {
      headers: {
        'X-API-Key': process.env.DASHBOARD_API_KEY
      }
    });
    
    io.emit('system:status', response.data);
  } catch (error) {
    console.error('Error fetching system status:', error.message);
  }
};

// Fetch system status every 30 seconds
setInterval(fetchSystemStatus, 30000);

// Handle process termination
process.on('SIGINT', () => {
  console.log('Shutting down server...');
  server.close(() => {
    console.log('Server shut down');
    process.exit(0);
  });
});