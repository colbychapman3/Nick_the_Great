const mongoose = require('mongoose');

const MemorySchema = new mongoose.Schema({
  timestamp: { type: Date, default: Date.now },
  content: String,
  source: String,
  priority: Number
});

module.exports = {
  saveEntry: async (entry) => {
    const Memory = mongoose.model('Memory', MemorySchema);
    await Memory.create(entry);
  },
  getRecentEntries: async (limit = 5) => {
    const Memory = mongoose.model('Memory', MemorySchema);
    return Memory.find().sort({ timestamp: -1 }).limit(limit);
  }
};
