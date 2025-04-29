const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');
const { MongoClient, ObjectId } = require('mongodb');

// MongoDB connection
let db;
const mongoUri = process.env.MONGODB_URI || 'mongodb://mongo:27017/nick_agent';
const client = new MongoClient(mongoUri);

// Connect to MongoDB
async function connectToDatabase() {
  try {
    await client.connect();
    db = client.db();
    console.log('Connected to MongoDB');
    
    // Create indexes for user collection
    await db.collection('users').createIndex({ email: 1 }, { unique: true });
    
    return db;
  } catch (error) {
    console.error('MongoDB connection error:', error);
    throw error;
  }
}

// User registration
async function registerUser(userData) {
  try {
    const { email, password, name } = userData;
    
    // Check if user already exists
    const existingUser = await db.collection('users').findOne({ email });
    if (existingUser) {
      throw new Error('User already exists with this email');
    }
    
    // Hash password
    const salt = await bcrypt.genSalt(10);
    const hashedPassword = await bcrypt.hash(password, salt);
    
    // Create user
    const user = {
      email,
      password: hashedPassword,
      name,
      role: 'user',
      createdAt: new Date(),
      updatedAt: new Date(),
      settings: {
        theme: 'light',
        notifications: true
      }
    };
    
    const result = await db.collection('users').insertOne(user);
    
    // Create initial agent configuration
    await db.collection('configurations').insertOne({
      userId: result.insertedId.toString(),
      budget: 50,
      riskTolerance: 'medium',
      timeHorizon: 'short',
      createdAt: new Date(),
      updatedAt: new Date()
    });
    
    // Remove password from response
    const { password: _, ...userWithoutPassword } = user;
    return { ...userWithoutPassword, _id: result.insertedId };
  } catch (error) {
    console.error('Registration error:', error);
    throw error;
  }
}

// User login
async function loginUser(credentials) {
  try {
    const { email, password } = credentials;
    
    // Find user
    const user = await db.collection('users').findOne({ email });
    if (!user) {
      throw new Error('Invalid credentials');
    }
    
    // Verify password
    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) {
      throw new Error('Invalid credentials');
    }
    
    // Generate JWT token
    const payload = {
      id: user._id.toString(),
      email: user.email,
      name: user.name,
      role: user.role
    };
    
    const token = jwt.sign(payload, process.env.JWT_SECRET || 'local_development_secret', {
      expiresIn: '24h'
    });
    
    // Remove password from response
    const { password: _, ...userWithoutPassword } = user;
    return { token, user: userWithoutPassword };
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
}

// Get user profile
async function getUserProfile(userId) {
  try {
    const user = await db.collection('users').findOne({ _id: new ObjectId(userId) });
    if (!user) {
      throw new Error('User not found');
    }
    
    // Remove password from response
    const { password, ...userWithoutPassword } = user;
    return userWithoutPassword;
  } catch (error) {
    console.error('Get user profile error:', error);
    throw error;
  }
}

// Update user profile
async function updateUserProfile(userId, userData) {
  try {
    const { name, settings } = userData;
    
    const updateData = {
      updatedAt: new Date()
    };
    
    if (name) updateData.name = name;
    if (settings) updateData.settings = settings;
    
    const result = await db.collection('users').updateOne(
      { _id: new ObjectId(userId) },
      { $set: updateData }
    );
    
    if (result.matchedCount === 0) {
      throw new Error('User not found');
    }
    
    return await getUserProfile(userId);
  } catch (error) {
    console.error('Update user profile error:', error);
    throw error;
  }
}

// Change password
async function changePassword(userId, passwordData) {
  try {
    const { currentPassword, newPassword } = passwordData;
    
    // Find user
    const user = await db.collection('users').findOne({ _id: new ObjectId(userId) });
    if (!user) {
      throw new Error('User not found');
    }
    
    // Verify current password
    const isMatch = await bcrypt.compare(currentPassword, user.password);
    if (!isMatch) {
      throw new Error('Current password is incorrect');
    }
    
    // Hash new password
    const salt = await bcrypt.genSalt(10);
    const hashedPassword = await bcrypt.hash(newPassword, salt);
    
    // Update password
    await db.collection('users').updateOne(
      { _id: new ObjectId(userId) },
      { 
        $set: { 
          password: hashedPassword,
          updatedAt: new Date()
        } 
      }
    );
    
    return { message: 'Password updated successfully' };
  } catch (error) {
    console.error('Change password error:', error);
    throw error;
  }
}

// Authentication middleware
function authenticateToken(req, res, next) {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];
  
  if (!token) {
    return res.status(401).json({ message: 'Authentication required' });
  }
  
  jwt.verify(token, process.env.JWT_SECRET || 'local_development_secret', (err, user) => {
    if (err) {
      return res.status(403).json({ message: 'Invalid or expired token' });
    }
    
    req.user = user;
    next();
  });
}

module.exports = {
  connectToDatabase,
  registerUser,
  loginUser,
  getUserProfile,
  updateUserProfile,
  changePassword,
  authenticateToken
};
