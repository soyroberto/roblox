# Roblox Architecture Explained 🎮

An interactive web application that explains how Roblox handles 26 million concurrent players through a comprehensive, educational interface covering distributed systems architecture.

![Roblox Architecture Overview](https://img.shields.io/badge/Architecture-Educational-blue) ![Tech Stack](https://img.shields.io/badge/Stack-FastAPI%20%2B%20React-green) ![License](https://img.shields.io/badge/License-MIT-yellow)

## 🎯 Project Overview

This educational platform breaks down Roblox's distributed systems architecture into digestible, visually engaging components suitable for:
- **Students** learning distributed systems
- **Developers** understanding scalable architecture
- **Architects** planning large-scale systems  
- **Engineers** implementing high-performance solutions

### Key Features
- **Interactive Architecture Diagram** with 10 clickable components
- **Step-by-Step Explanations** of the complete player journey
- **Capacity Calculators** for infrastructure planning
- **Progressive Difficulty** (Beginner → Intermediate → Advanced)
- **Modern UI/UX** with smooth animations and responsive design

## 🏗️ Architecture Components

The application covers 10 core distributed systems components:

1. **Global Load Balancer** - Geographic request distribution
2. **Content Delivery Network (CDN)** - Edge location caching
3. **API Gateway** - Microservice routing and management
4. **Game Server Cluster** - Container orchestration and scaling
5. **Distributed Database** - Sharding and replication strategies
6. **Caching Layer** - Multi-tier performance optimization
7. **Message Queue System** - Real-time event processing
8. **Monitoring & Observability** - System health and metrics
9. **Security & DDoS Protection** - Multi-layer threat mitigation
10. **Data Storage & Analytics** - Large-scale data processing

## 🚀 Quick Start

### Prerequisites

- **Node.js** (v18+ recommended)
- **Python** (v3.9+ recommended)
- **MongoDB** (v5.0+ recommended)
- **Git**

### Local Development Setup

#### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd roblox-architecture-explained
```

#### 2. Backend Setup (FastAPI)
```bash
# Navigate to backend directory
cd backend

# Create virtual environment (macOS/Linux)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your MongoDB connection string
```

#### 3. Frontend Setup (React)
```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies using Yarn
yarn install

# Set up environment variables
cp .env.example .env
# Edit .env with your backend URL
```

#### 4. Database Setup (MongoDB)

**Option A: Local MongoDB**
```bash
# Install MongoDB (macOS with Homebrew)
brew tap mongodb/brew
brew install mongodb-community

# Start MongoDB service
brew services start mongodb/brew/mongodb-community

# Default connection string for .env:
# MONGO_URL="mongodb://localhost:27017"
# DB_NAME="roblox_architecture"
```

**Option B: MongoDB Atlas (Cloud)**
1. Create account at [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create a new cluster
3. Get connection string and add to backend/.env

#### 5. Run the Application

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

The application will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8001
- **API Documentation**: http://localhost:8001/docs

## 📁 Project Structure

```
roblox-architecture-explained/
├── backend/                    # FastAPI backend
│   ├── server.py              # Main FastAPI application
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Environment variables
├── frontend/                  # React frontend
│   ├── src/
│   │   ├── App.js            # Main React component
│   │   ├── App.css           # Styles and animations
│   │   └── index.js          # React entry point
│   ├── package.json          # Node.js dependencies
│   └── .env                  # Environment variables
├── tests/                    # Test files
└── README.md                # This file
```

## 🔧 Development Workflow

### Making Changes

#### Backend Changes
1. Modify files in `backend/`
2. The development server will auto-reload
3. Test API endpoints at http://localhost:8001/docs

#### Frontend Changes  
1. Modify files in `frontend/src/`
2. Changes will hot-reload automatically
3. View changes at http://localhost:3000

#### Adding New Architecture Components
1. Update the `components` array in `backend/server.py`
2. Add corresponding UI elements in `frontend/src/App.js`
3. Update capacity calculations if needed

### Environment Variables

**Backend (.env):**
```env
MONGO_URL="mongodb://localhost:27017"
DB_NAME="roblox_architecture"
```

**Frontend (.env):**
```env
REACT_APP_BACKEND_URL="http://localhost:8001"
```

## 🌐 Deployment

### Deploy to Azure Static Web Apps

#### Prerequisites
- Azure account
- Azure CLI installed
- Static Web Apps CLI (`npm install -g @azure/static-web-apps-cli`)

#### Option A: GitHub Actions (Recommended)

1. **Push to GitHub:**
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Create Azure Static Web App:**
```bash
# Install Azure CLI (macOS)
brew install azure-cli

# Login to Azure
az login

# Create resource group
az group create --name roblox-architecture-rg --location "East US"

# Create static web app with GitHub integration
az staticwebapp create \
  --name roblox-architecture-app \
  --resource-group roblox-architecture-rg \
  --source https://github.com/YOUR_USERNAME/YOUR_REPO \
  --location "East US" \
  --branch main \
  --app-location "/frontend" \
  --api-location "/backend" \
  --build-location "build"
```

#### Option B: Manual Deployment

1. **Build Frontend:**
```bash
cd frontend
yarn build
```

2. **Deploy to Azure Storage:**
```bash
# Create storage account
az storage account create \
  --name robloxarchitecturestorage \
  --resource-group roblox-architecture-rg \
  --location "East US" \
  --sku Standard_LRS

# Enable static website hosting
az storage blob service-properties update \
  --account-name robloxarchitecturestorage \
  --static-website \
  --index-document index.html \
  --404-document index.html

# Upload build files
az storage blob upload-batch \
  --account-name robloxarchitecturestorage \
  --source frontend/build \
  --destination '$web'
```

3. **Deploy Backend to Azure Functions:**
```bash
# Install Azure Functions Core Tools
brew tap azure/functions
brew install azure-functions-core-tools@4

# Create Function App
cd backend
func init --python
func new --name roblox-api --template "HTTP trigger"

# Deploy
func azure functionapp publish roblox-architecture-functions
```

### Environment Variables for Production

Update your frontend `.env` for production:
```env
REACT_APP_BACKEND_URL="https://your-function-app.azurewebsites.net"
```

## 🧪 Testing

### Run Backend Tests
```bash
cd backend
python -m pytest
```

### Run Frontend Tests
```bash
cd frontend
yarn test
```

### API Testing
```bash
# Test all endpoints
curl http://localhost:8001/api/components
curl http://localhost:8001/api/steps
curl http://localhost:8001/api/overview

# Test capacity calculator
curl -X POST http://localhost:8001/api/calculate-capacity \
  -H "Content-Type: application/json" \
  -d '{"component_id": "...", "calculation_type": "basic", "inputs": {...}}'
```

## 🎨 Customization

### Adding New Components
```python
# In backend/server.py, add to components array:
{
    "name": "Your Component",
    "type": ComponentType.YOUR_TYPE,
    "description": "Component description",
    "detailed_explanation": "Detailed technical explanation",
    "technologies": ["Tech1", "Tech2"],
    "protocols": ["Protocol1", "Protocol2"],
    "capacity_metrics": {...},
    "position": {"x": 100, "y": 200},
    "connections": ["other_component"],
    "difficulty_level": DifficultyLevel.INTERMEDIATE,
    "step_order": 11
}
```

### Modifying UI Components
```javascript
// In frontend/src/App.js, modify:
- ArchitectureDiagram component for visual changes
- ComponentDetails component for information display
- CapacityCalculator for new calculation types
```

### Custom Styling
```css
/* In frontend/src/App.css, customize: */
- Color schemes
- Animations
- Layout responsive breakpoints
```

## 📊 Monitoring & Analytics

### Application Insights (Azure)
```bash
# Add Application Insights to track usage
npm install applicationinsights
```

### Custom Metrics
The application tracks:
- Component interaction rates
- Step completion rates  
- Capacity calculator usage
- User difficulty preferences

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow existing code style
- Add tests for new features
- Update documentation
- Ensure responsive design
- Test across different browsers

## 📚 Educational Use

This project is designed for educational purposes. Feel free to:
- Use in computer science courses
- Adapt for different architectural examples
- Extend with additional components
- Modify difficulty levels
- Add new calculation types

## 🔗 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://reactjs.org/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [Azure Static Web Apps](https://docs.microsoft.com/azure/static-web-apps/)
- [Distributed Systems Patterns](https://martinfowler.com/articles/patterns-of-distributed-systems/)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by Roblox's actual distributed systems architecture
- Educational content suitable for all skill levels
- Modern web development best practices
- Accessibility and responsive design principles

---

**Built with ❤️ for education and learning**

For questions or support, please open an issue or reach out through the repository.
