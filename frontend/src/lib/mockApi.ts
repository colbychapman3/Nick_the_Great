// Mock API service to use during development while backend is not deployed

interface User {
  id: string;
  name: string;
  email: string;
}

interface AuthResponse {
  token: string;
  user: User;
  message: string;
}

// Simulated database
const users: User[] = [
  { id: '1', name: 'Demo User', email: 'demo@example.com' }
];

// Simple token generation
const generateToken = (userId: string): string => {
  return `mock-token-${userId}-${Date.now()}`;
};

// Simulate API delay
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

// Mock API functions
export const mockApi = {
  // User authentication
  register: async (userData: { name: string; email: string; password: string }): Promise<AuthResponse> => {
    await delay(800); // Simulate network delay
    
    // Check if user already exists
    const existingUser = users.find(user => user.email === userData.email);
    if (existingUser) {
      throw new Error('User with this email already exists');
    }
    
    // Create new user
    const newUser: User = {
      id: Date.now().toString(),
      name: userData.name,
      email: userData.email
    };
    
    users.push(newUser);
    
    // Generate token
    const token = generateToken(newUser.id);
    
    return {
      token,
      user: newUser,
      message: 'Registration successful'
    };
  },
  
  login: async (credentials: { email: string; password: string }): Promise<AuthResponse> => {
    await delay(800); // Simulate network delay
    
    // Find user
    const user = users.find(user => user.email === credentials.email);
    
    if (!user) {
      throw new Error('Invalid credentials');
    }
    
    // Generate token
    const token = generateToken(user.id);
    
    return {
      token,
      user,
      message: 'Login successful'
    };
  },
  
  // Health check
  getHealth: async () => {
    await delay(300);
    
    return {
      status: 'healthy',
      components: [
        {
          name: 'API Connection',
          status: 'operational',
          lastCheck: new Date(),
          details: 'Mock API is active'
        },
        {
          name: 'Database',
          status: 'operational',
          lastCheck: new Date(),
          details: 'Mock database available'
        }
      ]
    };
  }
};
