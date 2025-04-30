# Nick the Great

Nick the Great is an autonomous passive income agent management system.

## Project Structure

```
nick-the-great/
├── backend/              # Node.js API server
│   ├── src/              # Backend source code
│   │   ├── db.js         # MongoDB connection module
│   │   └── index.js      # Main server file
│   ├── .env              # Environment variables (not committed to git)
│   ├── package.json      # Backend dependencies
│   └── run.js            # Server startup script
├── frontend/             # Next.js frontend
│   ├── src/              # Frontend source code
│   │   ├── app/          # Next.js app directory
│   │   ├── components/   # React components
│   │   └── lib/          # Frontend utilities
│   └── package.json      # Frontend dependencies
├── docker-compose.yml    # Docker Compose configuration
└── README.md             # This file
```

## Prerequisites

- Node.js v18 or higher
- MongoDB Atlas account (or local MongoDB installation)

## Setup

1. Clone the repository
2. Install backend dependencies:
   ```
   cd backend
   npm install
   ```
3. Install frontend dependencies:
   ```
   cd frontend
   npm install
   ```
4. Set up environment variables:
   ```
   cp .env.example backend/.env
   ```
5. Update the MongoDB connection string in `backend/.env`

## Development

### Backend
```bash
cd backend
npm run dev
```

### Frontend
```bash
cd frontend
npm run dev
```

## Testing

### Test MongoDB Connection
```bash
cd backend
npm test
```

## Deployment

### Backend (Render.com)
- Set up environment variables on Render.com
- Deploy with the following settings:
  - Build command: `cd backend && npm install`
  - Start command: `cd backend && npm start`

### Frontend (Cloudflare Pages)
- Deploy with the following settings:
  - Build command: `cd frontend && npm install && npm run build`
  - Output directory: `frontend/.next`

## MongoDB Integration

The application uses MongoDB Atlas as its database. The connection is configured in `backend/src/db.js`. The database connection URI is stored in the `MONGODB_URI` environment variable.

To configure the database connection:

1. Create a MongoDB Atlas account and cluster
2. Obtain a connection string in the format:
   ```
   mongodb+srv://username:password@cluster.mongodb.net/database
   ```
3. Add the connection string to the `MONGODB_URI` variable in your `backend/.env` file

The MongoDB driver uses the stable API version 1 to ensure forward compatibility.
