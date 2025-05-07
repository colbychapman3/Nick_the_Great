# Nick the Great Deployment Checklist

This document provides a comprehensive checklist for deploying the Nick the Great application, ensuring all components are properly configured and working together.

## Frontend Deployment (Vercel)

### Environment Variables
- [ ] Set `NEXT_PUBLIC_API_URL` to `https://nick-the-great.onrender.com`
- [ ] Set `NEXT_PUBLIC_AUTH_API_URL` to `https://nick-the-great.onrender.com/auth`
- [ ] Set `NEXT_PUBLIC_ENABLE_GRPC` to `false` (if applicable)

### Build Configuration
- [ ] Node.js version set to 16.x or later
- [ ] Build command: `npm run build`
- [ ] Install command: `npm install`
- [ ] Output directory: `.next`

### Domain Configuration
- [ ] Set up custom domain (if applicable)
- [ ] Configure SSL certificates

## Backend Deployment (Render)

### Environment Variables
- [x] `NODE_ENV` set to `production`
- [x] `PORT` set to `10000`
- [x] `JWT_SECRET` configured with secure random value
- [x] `MONGODB_URI` set to MongoDB connection string
- [x] `GEMINI_API_KEY` configured (if using Google Gemini)

### Build Configuration
- [x] Node.js runtime selected
- [x] Build command: `cd backend && npm install`
- [x] Start command: `cd backend && node src/index.js`

### Database
- [ ] Verify MongoDB database is provisioned
- [ ] Ensure MongoDB connection string is correct
- [ ] Check that database user has appropriate permissions
- [ ] Verify network access rules to allow connections from Render IP ranges

## Post-Deployment Verification

### Frontend
- [ ] Homepage loads properly
- [ ] Registration form works
- [ ] Login form works
- [ ] Dashboard loads after authentication
- [ ] Strategies page loads
- [ ] Resources page loads
- [ ] Logout works correctly

### Backend
- [ ] Health check endpoint (`https://nick-the-great.onrender.com/health`) returns 200 OK
- [ ] Authentication endpoints work (`/auth/login`, `/auth/register`)
- [ ] API endpoints return expected data when authenticated
- [ ] Check logs for any errors or warnings

### Security
- [ ] Verify CORS is properly configured
- [ ] Ensure JWT authentication is working
- [ ] Check that sensitive routes are protected
- [ ] Verify environment variables are properly protected

## Deployment Verification

### Automated Verification Script
- [ ] Run the API verification script to test all endpoints
  ```bash
  cd backend && node src/deployment-verification.js https://nick-the-great.onrender.com
  ```
- [ ] Verify all test cases pass
- [ ] Check the detailed output for any issues that need attention

This script automatically tests:
- Health check endpoint functionality
- User registration and login flows
- Authentication token generation
- Protected API endpoints
- Data creation capabilities
- Database connection verification

### Manual Verification Checklist

#### Frontend
- [ ] Homepage loads properly
- [ ] Registration form works
- [ ] Login form works
- [ ] Dashboard loads after authentication
- [ ] Strategies page loads
- [ ] Resources page loads
- [ ] Logout works correctly

#### Backend
- [ ] Health check endpoint (`https://nick-the-great.onrender.com/health`) returns 200 OK
- [ ] Authentication endpoints work (`/auth/login`, `/auth/register`)
- [ ] API endpoints return expected data when authenticated
- [ ] Check logs for any errors or warnings

## Troubleshooting

### Common Frontend Issues
- **Failed to fetch errors**: Check CORS configuration and ensure backend is running
- **Authentication issues**: Verify JWT token handling in frontend and backend
- **Rendering problems**: Check for TypeScript or React component errors

### Common Backend Issues
- **Database connection failures**: Check MongoDB connection string and network rules
- **Authentication failures**: Verify JWT secret is properly set
- **API response issues**: Look for JSON parsing or null reference errors
- **"db.collection is not a function" error**: Make sure route handlers use `await connectToDatabase()` instead of `getClient()`

### Recent Fixes
- [x] Fixed incorrect database connection in route handlers (2025-05-05)
  - Changed `getClient()` to `await connectToDatabase()` in strategies.js and resources.js
  - The `getClient()` function returns the MongoDB client, while routes need the database instance

- [x] Removed unused OpenAI dependency with high severity vulnerabilities (2025-05-05)
  - The openai package (v3.2.1) was depending on a vulnerable version of axios
  - Since the package wasn't being actively used in the codebase, it was removed entirely
  - This eliminated the 2 high severity vulnerabilities reported during build

## Monitoring & Maintenance

- [ ] Set up uptime monitoring for both frontend and backend
- [ ] Configure alerts for server health issues
- [ ] Set up regular database backups
- [ ] Document deployment process for future updates

## Next Steps

- [ ] Set up CI/CD pipeline for automated deployments
- [ ] Implement analytics to track user behavior
- [ ] Configure error tracking and reporting
- [ ] Plan for scaling if user base grows
