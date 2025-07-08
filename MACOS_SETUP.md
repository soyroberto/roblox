# macOS Development Setup Guide

This guide will help you set up the Roblox Architecture Explained application on macOS.

## Prerequisites Installation

### 1. Install Homebrew (if not already installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Install Node.js and Yarn
```bash
# Install Node.js (v18 recommended)
brew install node@18

# Install Yarn
brew install yarn

# Verify installations
node --version  # Should be v18.x.x
yarn --version  # Should be 1.22.x or higher
```

### 3. Install Python
```bash
# Install Python 3.9+
brew install python@3.9

# Verify installation
python3 --version  # Should be 3.9.x or higher
```

### 4. Install MongoDB
```bash
# Add MongoDB tap
brew tap mongodb/brew

# Install MongoDB Community Edition
brew install mongodb-community

# Start MongoDB service
brew services start mongodb/brew/mongodb-community

# Verify MongoDB is running
brew services list | grep mongodb
```

### 5. Install Git (if not already installed)
```bash
brew install git
```

## Project Setup

### 1. Clone and Setup Repository
```bash
# Clone the repository
git clone <your-repo-url>
cd roblox-architecture-explained

# Install root dependencies for convenience scripts
yarn install
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create Python virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit environment file (use nano, vim, or VS Code)
nano .env
```

**Update backend/.env:**
```env
MONGO_URL="mongodb://localhost:27017"
DB_NAME="roblox_architecture"
ENVIRONMENT="development"
DEBUG=true
```

### 3. Frontend Setup
```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install Node.js dependencies
yarn install

# Copy environment file
cp .env.example .env

# Edit environment file
nano .env
```

**Update frontend/.env:**
```env
REACT_APP_BACKEND_URL="http://localhost:8001"
REACT_APP_ENV="development"
WDS_SOCKET_PORT=3000
```

## Running the Application

### Option 1: Using Convenience Scripts (Recommended)
```bash
# From project root directory
# Install all dependencies
yarn install-all

# Start both backend and frontend simultaneously
yarn dev
```

### Option 2: Manual Startup

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
yarn start
```

### Option 3: Using Docker
```bash
# Build and run with Docker Compose
yarn docker:build
yarn docker:up

# Stop containers
yarn docker:down
```

## Accessing the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8001
- **API Documentation**: http://localhost:8001/docs
- **MongoDB**: mongodb://localhost:27017

## Development Workflow

### Making Changes

1. **Backend Changes**: Modify files in `backend/`, server auto-reloads
2. **Frontend Changes**: Modify files in `frontend/src/`, changes hot-reload
3. **Environment Variables**: Restart respective services after changes

### Testing
```bash
# Run all tests
yarn test

# Test only backend
cd backend && python -m pytest

# Test only frontend
cd frontend && yarn test
```

### Building for Production
```bash
# Build frontend
yarn build

# The build files will be in frontend/build/
```

## Common Issues and Solutions

### Issue: MongoDB Connection Failed
```bash
# Check if MongoDB is running
brew services list | grep mongodb

# Restart MongoDB
brew services restart mongodb/brew/mongodb-community

# Check MongoDB logs
tail -f /usr/local/var/log/mongodb/mongo.log
```

### Issue: Port Already in Use
```bash
# Kill process on port 8001 (backend)
lsof -ti:8001 | xargs kill -9

# Kill process on port 3000 (frontend)
lsof -ti:3000 | xargs kill -9
```

### Issue: Python Virtual Environment Issues
```bash
# Deactivate current environment
deactivate

# Remove and recreate virtual environment
rm -rf backend/venv
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Node Modules Issues
```bash
# Clear cache and reinstall
cd frontend
rm -rf node_modules yarn.lock
yarn install
```

## IDE Setup Recommendations

### VS Code Extensions
- Python
- JavaScript (ES6) code snippets
- ES7+ React/Redux/React-Native snippets
- MongoDB for VS Code
- REST Client (for API testing)

### VS Code Settings
```json
{
    "python.defaultInterpreterPath": "./backend/venv/bin/python",
    "python.terminal.activateEnvironment": true,
    "emmet.includeLanguages": {
        "javascript": "javascriptreact"
    }
}
```

## Environment Management

### Using Different Environments
```bash
# Development
export NODE_ENV=development
export REACT_APP_ENV=development

# Staging
export NODE_ENV=staging
export REACT_APP_ENV=staging

# Production
export NODE_ENV=production
export REACT_APP_ENV=production
```

### MongoDB Database Management
```bash
# Connect to MongoDB shell
mongosh

# List databases
show dbs

# Use project database
use roblox_architecture

# List collections
show collections

# Drop database (careful!)
db.dropDatabase()
```

## Performance Optimization

### Backend Optimization
- Use MongoDB indexes for better query performance
- Implement Redis caching for frequently accessed data
- Use async/await properly for non-blocking operations

### Frontend Optimization
- Use React.memo for expensive components
- Implement lazy loading for large datasets
- Optimize images and assets

## Deployment Preparation

### Environment Variables for Production
Create production environment files:

**backend/.env.production:**
```env
MONGO_URL="your-production-mongodb-url"
DB_NAME="roblox_architecture_prod"
ENVIRONMENT="production"
DEBUG=false
ALLOWED_ORIGINS="https://yourdomain.com"
```

**frontend/.env.production:**
```env
REACT_APP_BACKEND_URL="https://your-api-domain.com"
REACT_APP_ENV="production"
```

### Build and Test Production Build
```bash
# Build frontend for production
cd frontend
yarn build

# Serve production build locally for testing
npx serve -s build -l 3000
```

## Troubleshooting

### Reset Everything
```bash
# Stop all services
yarn docker:down
brew services stop mongodb/brew/mongodb-community

# Clean up
rm -rf backend/venv
rm -rf frontend/node_modules
rm -rf frontend/build

# Start fresh
yarn install-all
brew services start mongodb/brew/mongodb-community
yarn dev
```

### Check Logs
```bash
# Backend logs (if running manually)
tail -f backend/logs/app.log

# Frontend logs are in the terminal where you ran yarn start

# MongoDB logs
tail -f /usr/local/var/log/mongodb/mongo.log

# Docker logs (if using Docker)
docker-compose logs -f
```

For additional help, check the main README.md or open an issue in the repository.