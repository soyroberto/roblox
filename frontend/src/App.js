import React, { useState, useEffect } from 'react';
import './App.css';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Components
const Header = () => (
  <header className="bg-gradient-to-r from-blue-900 via-purple-900 to-indigo-900 text-white py-6">
    <div className="container mx-auto px-6">
      <h1 className="text-4xl font-bold text-center mb-2">
        How Roblox Handles 26 Million Concurrent Players
      </h1>
      <p className="text-xl text-center text-blue-200">
        A deep dive into distributed systems architecture
      </p>
    </div>
  </header>
);

const Overview = ({ overview }) => (
  <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
    <h2 className="text-2xl font-bold text-gray-800 mb-4">System Overview</h2>
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div className="bg-blue-50 rounded-lg p-4 text-center">
        <div className="text-3xl font-bold text-blue-600">{overview.total_concurrent_players?.toLocaleString() || 'Loading...'}</div>
        <div className="text-sm text-gray-600">Concurrent Players</div>
      </div>
      <div className="bg-green-50 rounded-lg p-4 text-center">
        <div className="text-3xl font-bold text-green-600">{overview.total_game_servers?.toLocaleString() || 'Loading...'}</div>
        <div className="text-sm text-gray-600">Game Servers</div>
      </div>
      <div className="bg-purple-50 rounded-lg p-4 text-center">
        <div className="text-3xl font-bold text-purple-600">{overview.requests_per_second?.toLocaleString() || 'Loading...'}</div>
        <div className="text-sm text-gray-600">Requests/Second</div>
      </div>
      <div className="bg-orange-50 rounded-lg p-4 text-center">
        <div className="text-3xl font-bold text-orange-600">{overview.uptime_percentage || 'Loading...'}%</div>
        <div className="text-sm text-gray-600">Uptime</div>
      </div>
    </div>
  </div>
);

const ArchitectureDiagram = ({ components, selectedComponent, onComponentClick }) => {
  const svgWidth = 800;
  const svgHeight = 600;
  
  const getComponentColor = (type) => {
    const colors = {
      load_balancer: '#3B82F6',
      cdn: '#10B981',
      api_gateway: '#8B5CF6',
      game_server: '#F59E0B',
      database: '#EF4444',
      cache: '#06B6D4',
      message_queue: '#84CC16',
      monitoring: '#F97316',
      security: '#EC4899',
      storage: '#6366F1'
    };
    return colors[type] || '#6B7280';
  };

  const renderConnections = () => {
    return components.flatMap(component => 
      component.connections.map(connectionId => {
        const targetComponent = components.find(c => c.type === connectionId);
        if (!targetComponent) return null;
        
        return (
          <line
            key={`${component.id}-${connectionId}`}
            x1={component.position.x}
            y1={component.position.y}
            x2={targetComponent.position.x}
            y2={targetComponent.position.y}
            stroke="#E5E7EB"
            strokeWidth="2"
            className="animate-pulse"
          />
        );
      })
    ).filter(Boolean);
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">Architecture Overview</h2>
      <div className="overflow-x-auto">
        <svg width={svgWidth} height={svgHeight} className="border border-gray-200 rounded">
          {/* Background Grid */}
          <defs>
            <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
              <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#F3F4F6" strokeWidth="1"/>
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid)" />
          
          {/* Connections */}
          {renderConnections()}
          
          {/* Components */}
          {components.map(component => (
            <g key={component.id}>
              <circle
                cx={component.position.x}
                cy={component.position.y}
                r={selectedComponent?.id === component.id ? 35 : 25}
                fill={getComponentColor(component.type)}
                stroke={selectedComponent?.id === component.id ? '#1F2937' : '#FFFFFF'}
                strokeWidth={selectedComponent?.id === component.id ? 3 : 2}
                className="cursor-pointer hover:stroke-gray-700 transition-all duration-300"
                onClick={() => onComponentClick(component)}
              />
              <text
                x={component.position.x}
                y={component.position.y + 50}
                textAnchor="middle"
                className="text-xs font-medium fill-gray-700"
              >
                {component.name}
              </text>
            </g>
          ))}
          
          {/* Data Flow Animation */}
          {selectedComponent && (
            <circle
              r="3"
              fill="#EF4444"
              className="animate-ping"
            >
              <animateMotion
                dur="3s"
                repeatCount="indefinite"
                path="M100,100 Q200,50 300,100 T500,100"
              />
            </circle>
          )}
        </svg>
      </div>
    </div>
  );
};

const ComponentDetails = ({ component, onCalculateCapacity }) => {
  const [capacityInputs, setCapacityInputs] = useState({});
  const [capacityResult, setCapacityResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleCapacityCalculation = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API}/calculate-capacity`, {
        component_id: component.id,
        calculation_type: 'basic',
        inputs: capacityInputs
      });
      setCapacityResult(response.data);
    } catch (error) {
      console.error('Capacity calculation failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const getDifficultyColor = (level) => {
    const colors = {
      beginner: 'bg-green-100 text-green-800',
      intermediate: 'bg-yellow-100 text-yellow-800',
      advanced: 'bg-red-100 text-red-800'
    };
    return colors[level] || 'bg-gray-100 text-gray-800';
  };

  const getCapacityInputs = () => {
    switch (component.type) {
      case 'game_server':
        return [
          { key: 'concurrent_players', label: 'Concurrent Players', default: 26000000 },
          { key: 'players_per_server', label: 'Players per Server', default: 100 }
        ];
      case 'database':
        return [
          { key: 'reads_per_second', label: 'Reads per Second', default: 2000000 },
          { key: 'writes_per_second', label: 'Writes per Second', default: 500000 }
        ];
      case 'load_balancer':
        return [
          { key: 'requests_per_second', label: 'Requests per Second', default: 2000000 }
        ];
      default:
        return [];
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
      <div className="flex justify-between items-start mb-4">
        <h2 className="text-2xl font-bold text-gray-800">{component.name}</h2>
        <span className={`px-3 py-1 rounded-full text-sm font-medium ${getDifficultyColor(component.difficulty_level)}`}>
          {component.difficulty_level}
        </span>
      </div>
      
      <p className="text-gray-600 mb-4">{component.description}</p>
      
      <div className="grid md:grid-cols-2 gap-6">
        <div>
          <h3 className="text-lg font-semibold text-gray-800 mb-3">Technical Details</h3>
          <div className="space-y-3">
            <div>
              <h4 className="font-medium text-gray-700">Technologies:</h4>
              <div className="flex flex-wrap gap-2 mt-1">
                {component.technologies.map(tech => (
                  <span key={tech} className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-sm">
                    {tech}
                  </span>
                ))}
              </div>
            </div>
            
            <div>
              <h4 className="font-medium text-gray-700">Protocols:</h4>
              <div className="flex flex-wrap gap-2 mt-1">
                {component.protocols.map(protocol => (
                  <span key={protocol} className="px-2 py-1 bg-purple-100 text-purple-800 rounded text-sm">
                    {protocol}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
        
        <div>
          <h3 className="text-lg font-semibold text-gray-800 mb-3">Capacity Metrics</h3>
          <div className="space-y-2">
            {Object.entries(component.capacity_metrics).map(([key, value]) => (
              <div key={key} className="flex justify-between">
                <span className="text-gray-600 capitalize">{key.replace(/_/g, ' ')}:</span>
                <span className="font-medium">{typeof value === 'number' ? value.toLocaleString() : value}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
      
      <div className="mt-6 border-t pt-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-3">Detailed Explanation</h3>
        <p className="text-gray-700 leading-relaxed">{component.detailed_explanation}</p>
      </div>
      
      {getCapacityInputs().length > 0 && (
        <div className="mt-6 border-t pt-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-3">Capacity Calculator</h3>
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              {getCapacityInputs().map(input => (
                <div key={input.key} className="mb-3">
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    {input.label}
                  </label>
                  <input
                    type="number"
                    value={capacityInputs[input.key] || input.default}
                    onChange={(e) => setCapacityInputs({
                      ...capacityInputs,
                      [input.key]: parseInt(e.target.value)
                    })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              ))}
              <button
                onClick={handleCapacityCalculation}
                disabled={loading}
                className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50 transition-colors"
              >
                {loading ? 'Calculating...' : 'Calculate Capacity'}
              </button>
            </div>
            
            {capacityResult && (
              <div className="bg-gray-50 rounded-lg p-4">
                <h4 className="font-medium text-gray-800 mb-2">Calculation Result</h4>
                <div className="space-y-2 text-sm">
                  {Object.entries(capacityResult.result).map(([key, value]) => (
                    <div key={key} className="flex justify-between">
                      <span className="text-gray-600 capitalize">{key.replace(/_/g, ' ')}:</span>
                      <span className="font-medium">{typeof value === 'number' ? value.toLocaleString() : value}</span>
                    </div>
                  ))}
                </div>
                <p className="mt-3 text-sm text-gray-600 italic">{capacityResult.explanation}</p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

const StepByStep = ({ steps, currentStep, onStepChange }) => (
  <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
    <h2 className="text-2xl font-bold text-gray-800 mb-4">Step-by-Step Flow</h2>
    
    <div className="flex overflow-x-auto space-x-4 mb-6">
      {steps.map((step, index) => (
        <button
          key={step.step_number}
          onClick={() => onStepChange(index)}
          className={`flex-shrink-0 px-4 py-2 rounded-lg font-medium transition-colors ${
            currentStep === index
              ? 'bg-blue-600 text-white'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
        >
          {step.step_number}. {step.title}
        </button>
      ))}
    </div>
    
    {steps[currentStep] && (
      <div className="space-y-4">
        <div>
          <h3 className="text-xl font-semibold text-gray-800">{steps[currentStep].title}</h3>
          <p className="text-gray-600 mt-2">{steps[currentStep].description}</p>
        </div>
        
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-medium text-gray-800 mb-2">For Beginners:</h4>
            <p className="text-gray-700 bg-green-50 p-3 rounded-lg">
              {steps[currentStep].beginner_explanation}
            </p>
          </div>
          
          <div>
            <h4 className="font-medium text-gray-800 mb-2">For Advanced Users:</h4>
            <p className="text-gray-700 bg-blue-50 p-3 rounded-lg">
              {steps[currentStep].advanced_explanation}
            </p>
          </div>
        </div>
        
        <div>
          <h4 className="font-medium text-gray-800 mb-2">Technical Details:</h4>
          <div className="bg-gray-50 p-4 rounded-lg">
            {Object.entries(steps[currentStep].technical_details).map(([key, value]) => (
              <div key={key} className="flex justify-between items-center py-1">
                <span className="text-gray-600 capitalize">{key.replace(/_/g, ' ')}:</span>
                <span className="font-medium">{Array.isArray(value) ? value.join(', ') : value}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    )}
  </div>
);

const DifficultyFilter = ({ selectedDifficulty, onDifficultyChange }) => (
  <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
    <h2 className="text-2xl font-bold text-gray-800 mb-4">Difficulty Level</h2>
    <div className="flex space-x-4">
      {['beginner', 'intermediate', 'advanced'].map(level => (
        <button
          key={level}
          onClick={() => onDifficultyChange(level === selectedDifficulty ? null : level)}
          className={`px-4 py-2 rounded-lg font-medium transition-colors capitalize ${
            selectedDifficulty === level
              ? 'bg-blue-600 text-white'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
        >
          {level}
        </button>
      ))}
    </div>
  </div>
);

// Main App Component
function App() {
  const [components, setComponents] = useState([]);
  const [steps, setSteps] = useState([]);
  const [selectedComponent, setSelectedComponent] = useState(null);
  const [currentStep, setCurrentStep] = useState(0);
  const [overview, setOverview] = useState({});
  const [selectedDifficulty, setSelectedDifficulty] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [componentsRes, stepsRes, overviewRes] = await Promise.all([
          axios.get(`${API}/components${selectedDifficulty ? `?difficulty=${selectedDifficulty}` : ''}`),
          axios.get(`${API}/steps`),
          axios.get(`${API}/overview`)
        ]);
        
        setComponents(componentsRes.data);
        setSteps(stepsRes.data);
        setOverview(overviewRes.data);
      } catch (error) {
        console.error('Failed to fetch data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [selectedDifficulty]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-xl text-gray-600">Loading Roblox architecture data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="container mx-auto px-6 py-8">
        <Overview overview={overview} />
        
        <DifficultyFilter 
          selectedDifficulty={selectedDifficulty}
          onDifficultyChange={setSelectedDifficulty}
        />
        
        <ArchitectureDiagram
          components={components}
          selectedComponent={selectedComponent}
          onComponentClick={setSelectedComponent}
        />
        
        {selectedComponent && (
          <ComponentDetails component={selectedComponent} />
        )}
        
        <StepByStep
          steps={steps}
          currentStep={currentStep}
          onStepChange={setCurrentStep}
        />
      </main>
      
      <footer className="bg-gray-800 text-white py-6">
        <div className="container mx-auto px-6 text-center">
          <p>&copy; 2025 Roblox Architecture Explained - Educational Purpose</p>
        </div>
      </footer>
    </div>
  );
}

export default App;