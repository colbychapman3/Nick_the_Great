const express = require('express');
const router = express.Router();
const { ObjectId } = require('mongodb');
const { connectToDatabase } = require('../db');

// Get all strategies for a user
router.get('/', async (req, res) => {
  try {
    const db = await connectToDatabase();
    const userId = req.user.id;

    // Find all strategies for the user
    const strategies = await db.collection('strategies')
      .find({ userId })
      .toArray();

    res.json(strategies);
  } catch (error) {
    console.error('Error fetching strategies:', error);
    res.status(500).json({ message: 'Error fetching strategies', error: error.message });
  }
});

// Get a specific strategy by ID
router.get('/:id', async (req, res) => {
  try {
    const db = await connectToDatabase();
    const userId = req.user.id;
    const strategyId = req.params.id;

    // Validate strategy ID
    if (!ObjectId.isValid(strategyId)) {
      return res.status(400).json({ message: 'Invalid strategy ID' });
    }

    // Find the specific strategy
    const strategy = await db.collection('strategies').findOne({
      _id: new ObjectId(strategyId),
      userId: userId
    });

    if (!strategy) {
      return res.status(404).json({ message: 'Strategy not found' });
    }

    res.json(strategy);
  } catch (error) {
    console.error('Error fetching strategy:', error);
    res.status(500).json({ message: 'Error fetching strategy', error: error.message });
  }
});

// Create a new strategy
router.post('/', async (req, res) => {
  try {
    const db = await connectToDatabase();
    const userId = req.user.id;
    
    // Validate request body
    const { name, description, status, criteria, parameters } = req.body;
    
    if (!name) {
      return res.status(400).json({ message: 'Strategy name is required' });
    }

    // Create new strategy document
    const newStrategy = {
      userId,
      name,
      description: description || '',
      status: status || 'draft',
      criteria: criteria || [],
      parameters: parameters || {},
      createdAt: new Date(),
      updatedAt: new Date()
    };

    // Insert into database
    const result = await db.collection('strategies').insertOne(newStrategy);
    
    // Return the created strategy with ID
    res.status(201).json({
      _id: result.insertedId,
      ...newStrategy
    });
  } catch (error) {
    console.error('Error creating strategy:', error);
    res.status(500).json({ message: 'Error creating strategy', error: error.message });
  }
});

// Update a strategy
router.put('/:id', async (req, res) => {
  try {
    const db = await connectToDatabase();
    const userId = req.user.id;
    const strategyId = req.params.id;

    // Validate strategy ID
    if (!ObjectId.isValid(strategyId)) {
      return res.status(400).json({ message: 'Invalid strategy ID' });
    }

    // Extract fields to update
    const { name, description, status, criteria, parameters } = req.body;
    
    // Create update object with only provided fields
    const updateData = { updatedAt: new Date() };
    if (name !== undefined) updateData.name = name;
    if (description !== undefined) updateData.description = description;
    if (status !== undefined) updateData.status = status;
    if (criteria !== undefined) updateData.criteria = criteria;
    if (parameters !== undefined) updateData.parameters = parameters;

    // Update the strategy
    const result = await db.collection('strategies').updateOne(
      { _id: new ObjectId(strategyId), userId },
      { $set: updateData }
    );

    if (result.matchedCount === 0) {
      return res.status(404).json({ message: 'Strategy not found or not authorized to update' });
    }

    // Return updated strategy
    const updatedStrategy = await db.collection('strategies').findOne({
      _id: new ObjectId(strategyId),
      userId
    });

    res.json(updatedStrategy);
  } catch (error) {
    console.error('Error updating strategy:', error);
    res.status(500).json({ message: 'Error updating strategy', error: error.message });
  }
});

// Delete a strategy
router.delete('/:id', async (req, res) => {
  try {
    const db = await connectToDatabase();
    const userId = req.user.id;
    const strategyId = req.params.id;

    // Validate strategy ID
    if (!ObjectId.isValid(strategyId)) {
      return res.status(400).json({ message: 'Invalid strategy ID' });
    }

    // Delete the strategy
    const result = await db.collection('strategies').deleteOne({
      _id: new ObjectId(strategyId),
      userId
    });

    if (result.deletedCount === 0) {
      return res.status(404).json({ message: 'Strategy not found or not authorized to delete' });
    }

    res.json({ message: 'Strategy deleted successfully' });
  } catch (error) {
    console.error('Error deleting strategy:', error);
    res.status(500).json({ message: 'Error deleting strategy', error: error.message });
  }
});

module.exports = router;
