const express = require('express');
const cors = require('cors');
const jwt = require('jsonwebtoken');
const dotenv = require('dotenv');
const { Configuration, OpenAIApi } = require('openai');
const { connectToDatabase, getClient } = require('./db');

// Load environment variables
dotenv.config();

// Initialize Express app
const app = express();
app.use(cors());
app.use(express.json());

// MongoDB connection
let db;

// OpenAI configuration
const configuration = new Configuration({
  apiKey: process.env.OPENAI_API_KEY,
});
const openai = new OpenAIApi(configuration);

// Authentication middleware
function authenticateToken(req, res, next) {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];
  
  if (!token) {
    return res.status(401).json({ message: 'Authentication required' });
  }
  
  jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
    if (err) {
      return res.status(403).json({ message: 'Invalid or expired token' });
    }
    
    req.user = user;
    next();
  });
}

// API Routes

// Agent configuration endpoints
app.get('/api/agent/config', authenticateToken, async (req, res) => {
  try {
    const config = await db.collection('configurations').findOne({ userId: req.user.id });
    res.json(config || {});
  } catch (error) {
    res.status(500).json({ message: 'Error fetching agent configuration', error: error.message });
  }
});

app.put('/api/agent/config', authenticateToken, async (req, res) => {
  try {
    const result = await db.collection('configurations').updateOne(
      { userId: req.user.id },
      { $set: req.body },
      { upsert: true }
    );
    res.json({ message: 'Configuration updated', result });
  } catch (error) {
    res.status(500).json({ message: 'Error updating agent configuration', error: error.message });
  }
});

// Strategy endpoints
app.get('/api/strategies', authenticateToken, async (req, res) => {
  try {
    const strategies = await db.collection('strategies')
      .find({ userId: req.user.id })
      .toArray();
    res.json(strategies);
  } catch (error) {
    res.status(500).json({ message: 'Error fetching strategies', error: error.message });
  }
});

app.get('/api/strategies/:id', authenticateToken, async (req, res) => {
  try {
    const strategy = await db.collection('strategies').findOne({
      _id: req.params.id,
      userId: req.user.id
    });
    
    if (!strategy) {
      return res.status(404).json({ message: 'Strategy not found' });
    }
    
    res.json(strategy);
  } catch (error) {
    res.status(500).json({ message: 'Error fetching strategy', error: error.message });
  }
});

app.post('/api/strategies', authenticateToken, async (req, res) => {
  try {
    const strategy = {
      ...req.body,
      userId: req.user.id,
      createdAt: new Date(),
      updatedAt: new Date()
    };
    
    const result = await db.collection('strategies').insertOne(strategy);
    res.status(201).json({ ...strategy, _id: result.insertedId });
  } catch (error) {
    res.status(500).json({ message: 'Error creating strategy', error: error.message });
  }
});

app.put('/api/strategies/:id', authenticateToken, async (req, res) => {
  try {
    const strategy = await db.collection('strategies').findOne({
      _id: req.params.id,
      userId: req.user.id
    });
    
    if (!strategy) {
      return res.status(404).json({ message: 'Strategy not found' });
    }
    
    const updatedStrategy = {
      ...req.body,
      userId: req.user.id,
      updatedAt: new Date()
    };
    
    await db.collection('strategies').updateOne(
      { _id: req.params.id, userId: req.user.id },
      { $set: updatedStrategy }
    );
    
    res.json({ ...updatedStrategy, _id: req.params.id });
  } catch (error) {
    res.status(500).json({ message: 'Error updating strategy', error: error.message });
  }
});

app.delete('/api/strategies/:id', authenticateToken, async (req, res) => {
  try {
    const result = await db.collection('strategies').deleteOne({
      _id: req.params.id,
      userId: req.user.id
    });
    
    if (result.deletedCount === 0) {
      return res.status(404).json({ message: 'Strategy not found' });
    }
    
    res.json({ message: 'Strategy deleted' });
  } catch (error) {
    res.status(500).json({ message: 'Error deleting strategy', error: error.message });
  }
});

app.post('/api/strategies/:id/execute', authenticateToken, async (req, res) => {
  try {
    const strategy = await db.collection('strategies').findOne({
      _id: req.params.id,
      userId: req.user.id
    });
    
    if (!strategy) {
      return res.status(404).json({ message: 'Strategy not found' });
    }
    
    // Execute strategy logic would go here
    // For now, just create an execution record
    const execution = {
      strategyId: req.params.id,
      userId: req.user.id,
      status: 'in_progress',
      startedAt: new Date(),
      logs: ['Strategy execution started']
    };
    
    const result = await db.collection('executions').insertOne(execution);
    
    res.json({ 
      message: 'Strategy execution started', 
      executionId: result.insertedId 
    });
  } catch (error) {
    res.status(500).json({ message: 'Error executing strategy', error: error.message });
  }
});

// Resource endpoints
app.get('/api/resources', authenticateToken, async (req, res) => {
  try {
    const resources = await db.collection('resources')
      .find({ userId: req.user.id })
      .toArray();
    res.json(resources);
  } catch (error) {
    res.status(500).json({ message: 'Error fetching resources', error: error.message });
  }
});

app.post('/api/resources/allocate', authenticateToken, async (req, res) => {
  try {
    const allocation = {
      ...req.body,
      userId: req.user.id,
      createdAt: new Date()
    };
    
    const result = await db.collection('allocations').insertOne(allocation);
    
    // Update resource balances
    // This would involve more complex logic in a real implementation
    
    res.status(201).json({ 
      message: 'Resources allocated', 
      allocationId: result.insertedId 
    });
  } catch (error) {
    res.status(500).json({ message: 'Error allocating resources', error: error.message });
  }
});

// Approval endpoints
app.get('/api/approvals', authenticateToken, async (req, res) => {
  try {
    const approvals = await db.collection('approvals')
      .find({ userId: req.user.id })
      .toArray();
    res.json(approvals);
  } catch (error) {
    res.status(500).json({ message: 'Error fetching approvals', error: error.message });
  }
});

app.post('/api/approvals/:id/respond', authenticateToken, async (req, res) => {
  try {
    const approval = await db.collection('approvals').findOne({
      _id: req.params.id,
      userId: req.user.id
    });
    
    if (!approval) {
      return res.status(404).json({ message: 'Approval request not found' });
    }
    
    const { approved, notes } = req.body;
    
    await db.collection('approvals').updateOne(
      { _id: req.params.id, userId: req.user.id },
      { 
        $set: { 
          status: approved ? 'approved' : 'rejected',
          respondedAt: new Date(),
          notes
        } 
      }
    );
    
    res.json({ message: `Approval request ${approved ? 'approved' : 'rejected'}` });
  } catch (error) {
    res.status(500).json({ message: 'Error responding to approval request', error: error.message });
  }
});

// Platform endpoints
app.get('/api/platforms', authenticateToken, async (req, res) => {
  try {
    const platforms = await db.collection('platforms')
      .find({})
      .toArray();
    res.json(platforms);
  } catch (error) {
    res.status(500).json({ message: 'Error fetching platforms', error: error.message });
  }
});

// Recommendation endpoints
app.post('/api/recommendations/strategies', authenticateToken, async (req, res) => {
  try {
    const { budget, riskTolerance, skills, timeHorizon } = req.body;
    
    // In a real implementation, this would use OpenAI to generate recommendations
    // For now, return some mock recommendations
    const recommendations = [
      {
        name: 'Content Creation Strategy',
        description: 'Create and monetize content on Medium',
        estimatedRoi: 120,
        timeToProfit: 30,
        riskLevel: 'low',
        platforms: ['medium'],
        initialInvestment: 0
      },
      {
        name: 'Digital Products Strategy',
        description: 'Create and sell digital products on Etsy',
        estimatedRoi: 200,
        timeToProfit: 45,
        riskLevel: 'medium',
        platforms: ['etsy'],
        initialInvestment: 50
      },
      {
        name: 'Affiliate Marketing Strategy',
        description: 'Promote products through Amazon Associates',
        estimatedRoi: 150,
        timeToProfit: 30,
        riskLevel: 'low',
        platforms: ['amazon_associates'],
        initialInvestment: 20
      }
    ];
    
    res.json(recommendations);
  } catch (error) {
    res.status(500).json({ message: 'Error generating recommendations', error: error.message });
  }
});

// Simulation endpoints
app.post('/api/simulation/run', authenticateToken, async (req, res) => {
  try {
    const { strategyType, platform, resourceAllocation, timeline } = req.body;
    
    // In a real implementation, this would run a simulation based on the parameters
    // For now, return some mock results
    const results = {
      metrics: {
        estimatedRoi: 127,
        monthlyIncome: 42,
        timeToProfit: 18,
        riskScore: 'medium'
      },
      analysis: {
        strengths: 'Low initial investment, leverages existing skills, scalable over time.',
        weaknesses: 'Requires consistent content creation, competitive market.',
        opportunities: 'Potential for viral growth, cross-platform expansion.',
        threats: 'Platform algorithm changes, market saturation.'
      },
      implementationPlan: [
        {
          phase: 'Initial Setup',
          duration: '1-3 days',
          description: 'Create accounts, set up profiles, prepare content templates.'
        },
        {
          phase: 'Content Creation',
          duration: '4-10 days',
          description: 'Develop initial content pieces, optimize for platform algorithms.'
        },
        {
          phase: 'Promotion & Optimization',
          duration: '11-20 days',
          description: 'Implement promotion strategies, analyze performance, optimize approach.'
        },
        {
          phase: 'Scaling & Reinvestment',
          duration: '21-30 days',
          description: 'Reinvest initial earnings, expand content library, implement automation.'
        }
      ]
    };
    
    res.json(results);
  } catch (error) {
    res.status(500).json({ message: 'Error running simulation', error: error.message });
  }
});

// Debug endpoints
app.post('/api/debug/validate', authenticateToken, async (req, res) => {
  try {
    const config = req.body;
    
    // In a real implementation, this would validate the configuration
    // For now, return some mock validation results
    const validationResults = {
      issues: [
        {
          type: 'warning',
          message: 'Limited Platform Access',
          details: 'Your configuration includes Gumroad but no API key is provided.'
        },
        {
          type: 'error',
          message: 'Resource Allocation',
          details: 'Total allocated resources exceed available budget by $15.'
        },
        {
          type: 'success',
          message: 'Strategy Compatibility',
          details: 'Selected strategies are compatible with your skills and platforms.'
        }
      ],
      suggestions: [
        {
          type: 'resource',
          message: 'Resource Reallocation',
          details: 'Consider reducing affiliate marketing budget by $15 to match available resources.'
        },
        {
          type: 'platform',
          message: 'Platform Prioritization',
          details: 'Medium has higher ROI potential than Etsy for your selected content strategy.'
        },
        {
          type: 'timeline',
          message: 'Timeline Adjustment',
          details: 'Extending timeline from 30 to 45 days could improve ROI by approximately 22%.'
        }
      ]
    };
    
    res.json(validationResults);
  } catch (error) {
    res.status(500).json({ message: 'Error validating configuration', error: error.message });
  }
});

app.get('/api/debug/health', async (req, res) => {
  try {
    const health = {
      status: 'healthy',
      components: [
        {
          name: 'API Connection',
          status: 'operational',
          lastCheck: new Date(),
          details: 'Response time: 124ms'
        },
        {
          name: 'Database',
          status: 'operational',
          lastCheck: new Date(),
          details: 'Query time: 45ms'
        },
        {
          name: 'Medium Integration',
          status: 'degraded',
          lastCheck: new Date(Date.now() - 300000), // 5 minutes ago
          details: 'API rate limiting active'
        },
        {
          name: 'Amazon Associates',
          status: 'operational',
          lastCheck: new Date(Date.now() - 300000), // 5 minutes ago
          details: 'All services available'
        }
      ]
    };
    
    res.json(health);
  } catch (error) {
    res.status(500).json({ message: 'Error checking system health', error: error.message });
  }
});

// Authentication endpoints
app.post('/api/auth/login', async (req, res) => {
  try {
    const { email, password } = req.body;
    
    // In a real implementation, this would validate credentials against the database
    // For now, just check for a demo account
    if (email === 'demo@example.com' && password === 'password') {
      const user = {
        id: '1',
        email: 'demo@example.com',
        name: 'Demo User'
      };
      
      const token = jwt.sign(user, process.env.JWT_SECRET, { expiresIn: '24h' });
      
      res.json({
        message: 'Login successful',
        token,
        user
      });
    } else {
      res.status(401).json({ message: 'Invalid credentials' });
    }
  } catch (error) {
    res.status(500).json({ message: 'Error during login', error: error.message });
  }
});

app.post('/api/auth/register', async (req, res) => {
  try {
    const { email, password, name } = req.body;
    
    // In a real implementation, this would create a new user in the database
    // For now, just return a success message
    const user = {
      id: Date.now().toString(),
      email,
      name
    };
    
    const token = jwt.sign(user, process.env.JWT_SECRET, { expiresIn: '24h' });
    
    res.status(201).json({
      message: 'Registration successful',
      token,
      user
    });
  } catch (error) {
    res.status(500).json({ message: 'Error during registration', error: error.message });
  }
});

// Start the server
const PORT = process.env.PORT || 10000;

async function startServer() {
  try {
    db = await connectToDatabase();
    
    app.listen(PORT, () => {
      console.log(`Server running on port ${PORT}`);
    });
  } catch (error) {
    console.error('Failed to start server:', error);
    process.exit(1);
  }
}

// For Cloudflare Workers environment
module.exports = app;

// For standalone Node.js environment
if (require.main === module) {
  startServer().catch(console.error);
}
