# Technical Context: Nick the Great

## Technologies Used

1. **Frontend**
   - Next.js (React framework)
   - TypeScript
   - Tailwind CSS

2. **Backend**
   - Node.js
   - Express.js
   - MongoDB

3. **Mobile App**
   - React Native

## Development Setup

1. **Frontend**
   - Deployed on Vercel
   - Using Vercel environment variables

2. **Backend**
   - Deployed on Render.com
   - Using environment variables for configuration

3. **Mobile App**
   - Using React Native Config for environment variables

## Technical Constraints

1. **CORS Configuration**: Implemented to allow cross-origin requests
2. **Authentication**: JWT-based with development bypass mode
3. **gRPC**: Configured for future implementation

## Dependencies

1. **Frontend**
   - `@types/react`
   - `next`
   - `react`

2. **Backend**
   - `express`
   - `mongodb`
   - `jsonwebtoken`

3. **Mobile App**
   - `react-native`
   - `react-native-config`

## Tool Usage Patterns

1. **Environment Variables**: Used extensively across all components. 
   - Standardized documentation available in `env-variables.md`
   - The backend uses the following environment variables:
     - `MONGODB_URI`: MongoDB connection string
     - `JWT_SECRET`: Secret key for JWT authentication
     - `PORT`: Port number for the server
     - `NODE_ENV`: Environment mode (development/production)
     - `ABACUS_API_KEY`: API key for Abacus service
     - `GOOGLE_CLOUD_API_KEY`: API key for Google Cloud services
   - Frontend (Vercel) uses variables with `NEXT_PUBLIC_` prefix
   - Mobile app uses React Native Config for environment variables

2. **API Proxying**: Implemented in Next.js configuration
3. **gRPC Configuration**: Added to environment variables

## Current Technical Challenges

1. Backend API connectivity issues
2. Implementing gRPC functionality

## Next Technical Steps

1. Implement gRPC server and client
2. Connect mobile app to gRPC server
3. Enhance authentication flow
4. Implement dashboard functionality
5. Continue debugging backend API connectivity
