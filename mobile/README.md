# Nick the Great - Mobile App

This is the React Native mobile application for Nick the Great.

## Setup

1. Install dependencies:
   ```
   cd mobile
   npm install
   ```

2. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Fill in the required API keys and configuration

3. Run the app:
   - For iOS: `npm run ios`
   - For Android: `npm run android`

## Environment Variables

The app uses the following environment variables:

- `API_URL`: The backend API URL
- `JWT_SECRET`: Secret key for JWT authentication
- `ABACUS_API_KEY`: API key for Abacus services
- `GOOGLE_CLOUD_API_KEY`: API key for Google Cloud services

## Project Structure

- `/src/components`: Reusable UI components
- `/src/screens`: Application screens
- `/src/navigation`: Navigation configuration

## Available Scripts

- `npm start`: Start the Metro bundler
- `npm run ios`: Run the app on iOS simulator
- `npm run android`: Run the app on Android emulator or device
- `npm test`: Run tests
- `npm run lint`: Run linting
