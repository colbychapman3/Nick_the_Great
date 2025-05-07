# Nick the Great Environment Variables

This document provides a comprehensive list of all environment variables used across the Nick the Great project components. It serves as a standardized reference to ensure consistent naming and usage across the backend, frontend, and mobile app.

## Backend Environment Variables

### Server Configuration
- `NODE_ENV`: Environment mode (development/production)
- `PORT`: Port number for the server (default: 10000)

### Authentication
- `JWT_SECRET`: Secret key for JWT authentication

### Database
- `MONGODB_URI`: MongoDB connection string

### API Keys
- `GEMINI_API_KEY`: API key for Google Gemini services
- `ABACUS_API_KEY`: API key for Abacus service
- `GOOGLE_CLOUD_API_KEY`: API key for Google Cloud services

### gRPC Configuration
- `BACKEND_IP`: IP address for the gRPC server
- `GRPC_PORT`: Port number for the gRPC server (default: 50051)

## Frontend Environment Variables (Vercel)

### API Configuration
- `NEXT_PUBLIC_API_URL`: URL of the backend API (e.g., "https://nick-the-great-api.onrender.com")
- `NEXT_PUBLIC_AUTH_API_URL`: URL of the authentication API (e.g., "https://nick-the-great-api.onrender.com/auth")

### Feature Flags
- `NEXT_PUBLIC_ENABLE_GRPC`: Enable gRPC functionality (true/false)

## Mobile App Environment Variables (React Native Config)

### API Configuration
- `API_URL`: URL of the backend API (same as frontend)
- `AUTH_API_URL`: URL of the authentication API (same as frontend)

### App Configuration
- `APP_ENV`: Environment mode (development/production)
- `ENABLE_ANALYTICS`: Enable analytics functionality (true/false)

## Usage Guidelines

1. **Naming Conventions**:
   - Use `NEXT_PUBLIC_` prefix for frontend environment variables that need to be accessible in the browser
   - Use uppercase letters and underscores for all environment variables
   - Use descriptive names that clearly indicate the purpose of the variable

2. **Security**:
   - Never commit sensitive environment variables to version control
   - Use `.env.example` files to document required variables without their values
   - Use environment variable management systems provided by deployment platforms (Vercel, Render)

3. **Cross-Component Consistency**:
   - Ensure that variables with the same purpose have the same name across components
   - For example, the backend API URL should be consistently referenced as `API_URL` in both frontend and mobile

4. **Documentation**:
   - Document all new environment variables in this file
   - Include a brief description of the purpose and expected format/values

## Examples

### Backend (.env)
```
NODE_ENV=production
PORT=10000
JWT_SECRET=your_jwt_secret_here
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/nick_agent
GEMINI_API_KEY=your_gemini_api_key_here
```

### Frontend (Vercel Environment Variables)
```
NEXT_PUBLIC_API_URL=https://nick-the-great.onrender.com
NEXT_PUBLIC_AUTH_API_URL=https://nick-the-great.onrender.com/auth
NEXT_PUBLIC_ENABLE_GRPC=false
```

### Mobile App (.env)
```
API_URL=https://nick-the-great-api.onrender.com
AUTH_API_URL=https://nick-the-great-api.onrender.com/auth
APP_ENV=production
ENABLE_ANALYTICS=true
