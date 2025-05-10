/**
 * Simple logging module for the backend.
 * Provides consistent logging format and levels.
 */

// Define log levels
const LOG_LEVELS = {
    DEBUG: 0,
    INFO: 1,
    WARN: 2,
    ERROR: 3,
    CRITICAL: 4
};

// Get log level from environment or default to INFO
const currentLevel = process.env.LOG_LEVEL ? 
    (LOG_LEVELS[process.env.LOG_LEVEL.toUpperCase()] || LOG_LEVELS.INFO) : 
    LOG_LEVELS.INFO;

/**
 * Format a log message with timestamp and level
 * @param {string} level - The log level
 * @param {string} message - The log message
 * @returns {string} - Formatted log message
 */
function formatLogMessage(level, message) {
    const timestamp = new Date().toISOString();
    return `${timestamp} - ${level.padEnd(7)} - ${message}`;
}

/**
 * Log a debug message
 * @param {string} message - The message to log
 */
function debug(message) {
    if (currentLevel <= LOG_LEVELS.DEBUG) {
        console.debug(formatLogMessage('DEBUG', message));
    }
}

/**
 * Log an info message
 * @param {string} message - The message to log
 */
function info(message) {
    if (currentLevel <= LOG_LEVELS.INFO) {
        console.info(formatLogMessage('INFO', message));
    }
}

/**
 * Log a warning message
 * @param {string} message - The message to log
 */
function warn(message) {
    if (currentLevel <= LOG_LEVELS.WARN) {
        console.warn(formatLogMessage('WARN', message));
    }
}

/**
 * Log an error message
 * @param {string} message - The message to log
 * @param {Error} [error] - Optional error object
 */
function error(message, error) {
    if (currentLevel <= LOG_LEVELS.ERROR) {
        console.error(formatLogMessage('ERROR', message));
        if (error && error.stack) {
            console.error(error.stack);
        }
    }
}

/**
 * Log a critical message
 * @param {string} message - The message to log
 * @param {Error} [error] - Optional error object
 */
function critical(message, error) {
    if (currentLevel <= LOG_LEVELS.CRITICAL) {
        console.error(formatLogMessage('CRITICAL', message));
        if (error && error.stack) {
            console.error(error.stack);
        }
    }
}

module.exports = {
    debug,
    info,
    warn,
    error,
    critical,
    LOG_LEVELS
};
