const express = require('express');
const router = express.Router();
const { ObjectId } = require('mongodb');
const { getClient } = require('../db');

// Get all resources for a user
router.get('/', async (req, res) => {
  try {
    const db = getClient();
    const userId = req.user.id;

    // Find all resources for the user
    const resources = await db.collection('resources')
      .find({ userId })
      .toArray();

    res.json(resources);
  } catch (error) {
    console.error('Error fetching resources:', error);
    res.status(500).json({ message: 'Error fetching resources', error: error.message });
  }
});

// Get a specific resource by ID
router.get('/:id', async (req, res) => {
  try {
    const db = getClient();
    const userId = req.user.id;
    const resourceId = req.params.id;

    // Validate resource ID
    if (!ObjectId.isValid(resourceId)) {
      return res.status(400).json({ message: 'Invalid resource ID' });
    }

    // Find the specific resource
    const resource = await db.collection('resources').findOne({
      _id: new ObjectId(resourceId),
      userId: userId
    });

    if (!resource) {
      return res.status(404).json({ message: 'Resource not found' });
    }

    res.json(resource);
  } catch (error) {
    console.error('Error fetching resource:', error);
    res.status(500).json({ message: 'Error fetching resource', error: error.message });
  }
});

// Create a new resource
router.post('/', async (req, res) => {
  try {
    const db = getClient();
    const userId = req.user.id;
    
    // Validate request body
    const { title, description, url, category, tags } = req.body;
    
    if (!title) {
      return res.status(400).json({ message: 'Resource title is required' });
    }

    if (!url) {
      return res.status(400).json({ message: 'Resource URL is required' });
    }

    // Create new resource document
    const newResource = {
      userId,
      title,
      description: description || '',
      url,
      category: category || 'General',
      tags: tags || [],
      createdAt: new Date(),
      updatedAt: new Date()
    };

    // Insert into database
    const result = await db.collection('resources').insertOne(newResource);
    
    // Return the created resource with ID
    res.status(201).json({
      _id: result.insertedId,
      ...newResource
    });
  } catch (error) {
    console.error('Error creating resource:', error);
    res.status(500).json({ message: 'Error creating resource', error: error.message });
  }
});

// Update a resource
router.put('/:id', async (req, res) => {
  try {
    const db = getClient();
    const userId = req.user.id;
    const resourceId = req.params.id;

    // Validate resource ID
    if (!ObjectId.isValid(resourceId)) {
      return res.status(400).json({ message: 'Invalid resource ID' });
    }

    // Extract fields to update
    const { title, description, url, category, tags } = req.body;
    
    // Create update object with only provided fields
    const updateData = { updatedAt: new Date() };
    if (title !== undefined) updateData.title = title;
    if (description !== undefined) updateData.description = description;
    if (url !== undefined) updateData.url = url;
    if (category !== undefined) updateData.category = category;
    if (tags !== undefined) updateData.tags = tags;

    // Update the resource
    const result = await db.collection('resources').updateOne(
      { _id: new ObjectId(resourceId), userId },
      { $set: updateData }
    );

    if (result.matchedCount === 0) {
      return res.status(404).json({ message: 'Resource not found or not authorized to update' });
    }

    // Return updated resource
    const updatedResource = await db.collection('resources').findOne({
      _id: new ObjectId(resourceId),
      userId
    });

    res.json(updatedResource);
  } catch (error) {
    console.error('Error updating resource:', error);
    res.status(500).json({ message: 'Error updating resource', error: error.message });
  }
});

// Delete a resource
router.delete('/:id', async (req, res) => {
  try {
    const db = getClient();
    const userId = req.user.id;
    const resourceId = req.params.id;

    // Validate resource ID
    if (!ObjectId.isValid(resourceId)) {
      return res.status(400).json({ message: 'Invalid resource ID' });
    }

    // Delete the resource
    const result = await db.collection('resources').deleteOne({
      _id: new ObjectId(resourceId),
      userId
    });

    if (result.deletedCount === 0) {
      return res.status(404).json({ message: 'Resource not found or not authorized to delete' });
    }

    res.json({ message: 'Resource deleted successfully' });
  } catch (error) {
    console.error('Error deleting resource:', error);
    res.status(500).json({ message: 'Error deleting resource', error: error.message });
  }
});

module.exports = router;
