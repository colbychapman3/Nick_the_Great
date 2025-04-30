const { connectToDatabase, closeConnection } = require('./db');

async function testDatabaseConnection() {
  try {
    console.log('Attempting to connect to MongoDB...');
    const db = await connectToDatabase();
    
    console.log('Successfully connected to MongoDB!');
    console.log('Database name:', db.databaseName);
    
    // Test a simple database operation
    const collections = await db.collections();
    console.log('Collections in database:', collections.map(c => c.collectionName));
    
    // Ping the database
    const pingResult = await db.command({ ping: 1 });
    console.log('Ping result:', pingResult);
    
    // Close the connection
    await closeConnection();
    console.log('Connection closed successfully');
  } catch (error) {
    console.error('Error testing MongoDB connection:', error);
  }
}

// Run the test
testDatabaseConnection()
  .then(() => console.log('Test complete'))
  .catch(console.error);
