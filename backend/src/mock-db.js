const logger = require("./utils/logger");

// Mock database implementation
class MockCollection {
  constructor(name) {
    this.name = name;
    this.data = [];
  }

  async findOne(query) {
    logger.info(`Mock findOne on ${this.name} with query:`, query);
    return null;
  }

  async find(query) {
    logger.info(`Mock find on ${this.name} with query:`, query);
    return {
      toArray: async () => []
    };
  }

  async insertOne(doc) {
    logger.info(`Mock insertOne on ${this.name}:`, doc);
    return { insertedId: "mock-id-" + Date.now() };
  }

  async updateOne(query, update, options) {
    logger.info(`Mock updateOne on ${this.name} with query:`, query);
    logger.info(`Update:`, update);
    logger.info(`Options:`, options);
    return { modifiedCount: 1, upsertedId: options?.upsert ? "mock-id-" + Date.now() : null };
  }

  async deleteOne(query) {
    logger.info(`Mock deleteOne on ${this.name} with query:`, query);
    return { deletedCount: 1 };
  }
}

class MockDatabase {
  constructor() {
    this.collections = {};
  }

  collection(name) {
    if (!this.collections[name]) {
      this.collections[name] = new MockCollection(name);
    }
    return this.collections[name];
  }
}

// Mock client
const mockClient = {
  topology: {
    isConnected: () => true
  }
};

// Mock database instance
const mockDb = new MockDatabase();

/**
 * Connect to mock database
 * @returns {Promise<object>} Mock database instance
 */
async function connectToDatabase() {
  logger.info("Using mock database for testing");
  return mockDb;
}

/**
 * Close the mock database connection (no-op)
 */
async function closeConnection() {
  logger.info("Mock database connection closed");
}

module.exports = {
  connectToDatabase,
  closeConnection,
  getClient: () => mockClient,
};
