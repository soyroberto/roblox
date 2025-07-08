from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime
from enum import Enum
import math

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="Roblox Architecture Explanation API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

class ComponentType(str, Enum):
    LOAD_BALANCER = "load_balancer"
    CDN = "cdn"
    API_GATEWAY = "api_gateway"
    GAME_SERVER = "game_server"
    DATABASE = "database"
    CACHE = "cache"
    MESSAGE_QUEUE = "message_queue"
    MONITORING = "monitoring"
    SECURITY = "security"
    STORAGE = "storage"

class DifficultyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class ArchitectureComponent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    type: ComponentType
    description: str
    detailed_explanation: str
    technologies: List[str]
    protocols: List[str]
    capacity_metrics: Dict[str, Any]
    position: Dict[str, int]  # x, y coordinates for diagram
    connections: List[str]  # IDs of connected components
    difficulty_level: DifficultyLevel
    step_order: int
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CapacityCalculationInput(BaseModel):
    component_id: str
    calculation_type: str
    inputs: Dict[str, Any]

class CapacityCalculation(BaseModel):
    component_id: str
    calculation_type: str
    inputs: Dict[str, Any]
    result: Dict[str, Any]
    explanation: str

class StepExplanation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    step_number: int
    title: str
    description: str
    components_involved: List[str]
    diagram_focus: List[str]
    technical_details: Dict[str, Any]
    beginner_explanation: str
    advanced_explanation: str

# Initialize architecture data
@app.on_event("startup")
async def initialize_architecture_data():
    """Initialize the database with Roblox architecture components"""
    
    # Clear existing data
    await db.components.delete_many({})
    await db.steps.delete_many({})
    
    # Define architecture components
    components = [
        {
            "name": "Global Load Balancer",
            "type": ComponentType.LOAD_BALANCER,
            "description": "Distributes 26M concurrent players across global regions",
            "detailed_explanation": "Roblox uses a multi-tier load balancing system with geographic distribution. The global load balancer uses DNS-based routing and anycast to direct players to the nearest regional data center. It handles health checks, failover, and capacity-based routing.",
            "technologies": ["HAProxy", "NGINX", "AWS ELB", "Cloudflare"],
            "protocols": ["HTTP/2", "TCP", "DNS", "Anycast"],
            "capacity_metrics": {
                "requests_per_second": 2000000,
                "concurrent_connections": 26000000,
                "latency_ms": 50,
                "availability": 99.99
            },
            "position": {"x": 100, "y": 100},
            "connections": ["cdn", "api_gateway"],
            "difficulty_level": DifficultyLevel.INTERMEDIATE,
            "step_order": 1
        },
        {
            "name": "Content Delivery Network (CDN)",
            "type": ComponentType.CDN,
            "description": "Caches game assets and reduces latency globally",
            "detailed_explanation": "Roblox's CDN network spans 200+ edge locations worldwide, caching game assets, avatars, and static content. It uses intelligent routing, content optimization, and edge computing to minimize latency for players.",
            "technologies": ["CloudFront", "Cloudflare", "Akamai", "Custom Edge Servers"],
            "protocols": ["HTTP/2", "HTTP/3", "WebRTC", "UDP"],
            "capacity_metrics": {
                "edge_locations": 200,
                "cache_hit_ratio": 95,
                "bandwidth_tbps": 100,
                "asset_requests_per_second": 5000000
            },
            "position": {"x": 300, "y": 100},
            "connections": ["load_balancer", "storage"],
            "difficulty_level": DifficultyLevel.BEGINNER,
            "step_order": 2
        },
        {
            "name": "API Gateway",
            "type": ComponentType.API_GATEWAY,
            "description": "Routes requests to appropriate microservices",
            "detailed_explanation": "The API Gateway acts as a single entry point for all client requests, handling authentication, rate limiting, request routing, and protocol translation. It implements circuit breakers and retries for fault tolerance.",
            "technologies": ["Kong", "Envoy", "AWS API Gateway", "Custom Service Mesh"],
            "protocols": ["HTTP/2", "gRPC", "WebSocket", "TCP"],
            "capacity_metrics": {
                "requests_per_second": 10000000,
                "services_managed": 500,
                "rate_limit_per_user": 1000,
                "response_time_ms": 10
            },
            "position": {"x": 200, "y": 250},
            "connections": ["load_balancer", "game_server", "database"],
            "difficulty_level": DifficultyLevel.INTERMEDIATE,
            "step_order": 3
        },
        {
            "name": "Game Server Cluster",
            "type": ComponentType.GAME_SERVER,
            "description": "Hosts individual game instances and player sessions",
            "detailed_explanation": "Roblox runs thousands of game servers across multiple regions. Each server can handle 50-100 concurrent players per game instance. The system uses container orchestration, auto-scaling, and intelligent placement to optimize performance.",
            "technologies": ["Kubernetes", "Docker", "Custom Game Engine", "Lua Runtime"],
            "protocols": ["UDP", "TCP", "WebSocket", "Custom Protocol"],
            "capacity_metrics": {
                "servers_count": 50000,
                "players_per_server": 100,
                "games_hosted": 1000000,
                "cpu_utilization": 70
            },
            "position": {"x": 400, "y": 350},
            "connections": ["api_gateway", "database", "cache", "message_queue"],
            "difficulty_level": DifficultyLevel.ADVANCED,
            "step_order": 4
        },
        {
            "name": "Distributed Database",
            "type": ComponentType.DATABASE,
            "description": "Stores player data, game state, and metadata",
            "detailed_explanation": "Roblox uses a combination of SQL and NoSQL databases with horizontal sharding. Player data is partitioned geographically, with read replicas for performance and master-slave replication for consistency.",
            "technologies": ["MySQL", "MongoDB", "Redis", "Cassandra"],
            "protocols": ["MySQL Protocol", "MongoDB Wire Protocol", "Redis Protocol"],
            "capacity_metrics": {
                "shards_count": 1000,
                "read_replicas": 5000,
                "writes_per_second": 500000,
                "reads_per_second": 2000000
            },
            "position": {"x": 100, "y": 450},
            "connections": ["api_gateway", "game_server", "cache"],
            "difficulty_level": DifficultyLevel.ADVANCED,
            "step_order": 5
        },
        {
            "name": "Caching Layer",
            "type": ComponentType.CACHE,
            "description": "High-speed data access for frequent operations",
            "detailed_explanation": "Multi-tier caching system with L1 (application), L2 (Redis), and L3 (CDN) caches. Implements cache warming, invalidation strategies, and consistent hashing for optimal performance.",
            "technologies": ["Redis Cluster", "Memcached", "Application Cache", "CDN Cache"],
            "protocols": ["Redis Protocol", "Memcached Protocol", "HTTP"],
            "capacity_metrics": {
                "cache_nodes": 5000,
                "hit_ratio": 95,
                "operations_per_second": 10000000,
                "memory_tb": 100
            },
            "position": {"x": 200, "y": 450},
            "connections": ["game_server", "database", "api_gateway"],
            "difficulty_level": DifficultyLevel.INTERMEDIATE,
            "step_order": 6
        },
        {
            "name": "Message Queue System",
            "type": ComponentType.MESSAGE_QUEUE,
            "description": "Handles real-time events and cross-service communication",
            "detailed_explanation": "Event-driven architecture using message queues for decoupled communication. Handles player actions, game events, and system notifications with guaranteed delivery and ordering.",
            "technologies": ["Apache Kafka", "RabbitMQ", "AWS SQS", "Custom Event Bus"],
            "protocols": ["Kafka Protocol", "AMQP", "WebSocket", "Server-Sent Events"],
            "capacity_metrics": {
                "messages_per_second": 50000000,
                "topics": 10000,
                "partitions": 100000,
                "retention_hours": 168
            },
            "position": {"x": 500, "y": 350},
            "connections": ["game_server", "monitoring", "api_gateway"],
            "difficulty_level": DifficultyLevel.ADVANCED,
            "step_order": 7
        },
        {
            "name": "Monitoring & Observability",
            "type": ComponentType.MONITORING,
            "description": "Tracks system health and performance metrics",
            "detailed_explanation": "Comprehensive monitoring stack with metrics collection, distributed tracing, log aggregation, and alerting. Provides real-time visibility into system performance and user experience.",
            "technologies": ["Prometheus", "Grafana", "ELK Stack", "Jaeger", "DataDog"],
            "protocols": ["HTTP", "gRPC", "StatsD", "OpenTelemetry"],
            "capacity_metrics": {
                "metrics_per_second": 100000000,
                "log_entries_per_second": 10000000,
                "alerts_per_day": 1000,
                "dashboards": 5000
            },
            "position": {"x": 600, "y": 250},
            "connections": ["message_queue", "game_server", "database"],
            "difficulty_level": DifficultyLevel.INTERMEDIATE,
            "step_order": 8
        },
        {
            "name": "Security & DDoS Protection",
            "type": ComponentType.SECURITY,
            "description": "Protects against attacks and unauthorized access",
            "detailed_explanation": "Multi-layered security including DDoS protection, Web Application Firewall, intrusion detection, and rate limiting. Implements OAuth, JWT tokens, and encryption for secure communication.",
            "technologies": ["Cloudflare", "AWS Shield", "WAF", "OAuth 2.0", "JWT"],
            "protocols": ["HTTPS", "OAuth", "JWT", "TLS 1.3"],
            "capacity_metrics": {
                "requests_filtered_per_second": 1000000,
                "attack_mitigation_time_ms": 100,
                "false_positive_rate": 0.1,
                "security_events_per_day": 100000
            },
            "position": {"x": 50, "y": 250},
            "connections": ["load_balancer", "api_gateway"],
            "difficulty_level": DifficultyLevel.ADVANCED,
            "step_order": 9
        },
        {
            "name": "Data Storage & Analytics",
            "type": ComponentType.STORAGE,
            "description": "Stores game assets, logs, and analytics data",
            "detailed_explanation": "Distributed storage system for game assets, player data, and analytics. Uses object storage, data lakes, and real-time analytics for business intelligence and game optimization.",
            "technologies": ["AWS S3", "HDFS", "Snowflake", "Apache Spark", "BigQuery"],
            "protocols": ["HTTP", "HDFS Protocol", "SQL", "Parquet"],
            "capacity_metrics": {
                "storage_pb": 100,
                "files_count": 1000000000,
                "analytics_queries_per_day": 1000000,
                "data_processing_tb_per_day": 1000
            },
            "position": {"x": 400, "y": 100},
            "connections": ["cdn", "game_server", "monitoring"],
            "difficulty_level": DifficultyLevel.INTERMEDIATE,
            "step_order": 10
        }
    ]
    
    # Insert components
    for comp_data in components:
        component = ArchitectureComponent(**comp_data)
        await db.components.insert_one(component.dict())
    
    # Define step explanations
    steps = [
        {
            "step_number": 1,
            "title": "Player Request Arrives",
            "description": "A player opens Roblox and makes a request to join a game",
            "components_involved": ["load_balancer", "security"],
            "diagram_focus": ["load_balancer"],
            "technical_details": {
                "request_flow": "Client → DNS → Global Load Balancer → Regional Load Balancer",
                "protocols": ["DNS", "HTTP/2", "TLS 1.3"],
                "latency_target": "< 50ms"
            },
            "beginner_explanation": "When you click 'Play' on a Roblox game, your request first goes to a load balancer that decides which server should handle your request based on your location and server capacity.",
            "advanced_explanation": "The global load balancer uses GeoDNS and anycast routing to direct the request to the optimal regional cluster. It performs health checks, capacity assessment, and implements sticky sessions for connection persistence."
        },
        {
            "step_number": 2,
            "title": "Security & DDoS Protection",
            "description": "Request passes through security layers and DDoS protection",
            "components_involved": ["security", "load_balancer"],
            "diagram_focus": ["security"],
            "technical_details": {
                "security_layers": ["Rate Limiting", "WAF", "DDoS Protection", "IP Reputation"],
                "processing_time": "< 5ms",
                "blocked_requests_per_second": 100000
            },
            "beginner_explanation": "Before your request reaches the game servers, it passes through security systems that block malicious traffic and protect against attacks.",
            "advanced_explanation": "Multi-layered security including L3/L4 DDoS protection, L7 WAF rules, behavioral analysis, and machine learning-based threat detection. Implements challenge-response for suspicious traffic."
        },
        {
            "step_number": 3,
            "title": "CDN Asset Delivery",
            "description": "Game assets are served from the nearest CDN edge location",
            "components_involved": ["cdn", "storage"],
            "diagram_focus": ["cdn"],
            "technical_details": {
                "cache_strategy": "LRU with TTL",
                "edge_locations": 200,
                "cache_hit_ratio": 95
            },
            "beginner_explanation": "Game graphics, sounds, and other files are loaded from servers close to your location for faster loading times.",
            "advanced_explanation": "Intelligent edge caching with dynamic content optimization, image compression, and prefetching. Uses HTTP/2 push and service workers for optimal asset delivery."
        },
        {
            "step_number": 4,
            "title": "API Gateway Routing",
            "description": "Request is routed to appropriate microservices",
            "components_involved": ["api_gateway", "game_server"],
            "diagram_focus": ["api_gateway"],
            "technical_details": {
                "routing_algorithm": "Weighted Round Robin",
                "circuit_breaker": "Enabled",
                "retry_policy": "Exponential Backoff"
            },
            "beginner_explanation": "The API Gateway acts like a smart router that sends different types of requests to the right services that can handle them.",
            "advanced_explanation": "Service mesh with intelligent routing, load balancing, circuit breaking, and distributed tracing. Implements canary deployments and A/B testing capabilities."
        },
        {
            "step_number": 5,
            "title": "Game Server Assignment",
            "description": "Player is assigned to an optimal game server instance",
            "components_involved": ["game_server", "database", "cache"],
            "diagram_focus": ["game_server"],
            "technical_details": {
                "placement_algorithm": "Proximity + Capacity",
                "server_capacity": 100,
                "scaling_strategy": "Horizontal Auto-scaling"
            },
            "beginner_explanation": "You're connected to a game server that has space and is close to your location for the best gaming experience.",
            "advanced_explanation": "Kubernetes-based orchestration with custom scheduler considering latency, resource utilization, and game-specific requirements. Implements predictive scaling and resource quotas."
        },
        {
            "step_number": 6,
            "title": "Database Operations",
            "description": "Player data and game state are retrieved from distributed databases",
            "components_involved": ["database", "cache"],
            "diagram_focus": ["database"],
            "technical_details": {
                "sharding_strategy": "Consistent Hashing",
                "replication_factor": 3,
                "consistency_model": "Eventually Consistent"
            },
            "beginner_explanation": "Your player profile, inventory, and game progress are loaded from databases that store millions of players' information.",
            "advanced_explanation": "Horizontally partitioned databases with read replicas, write-through caching, and conflict-free replicated data types (CRDTs) for distributed consistency."
        },
        {
            "step_number": 7,
            "title": "Real-time Communication",
            "description": "WebSocket connections established for real-time gameplay",
            "components_involved": ["message_queue", "game_server"],
            "diagram_focus": ["message_queue"],
            "technical_details": {
                "protocol": "WebSocket + Custom Binary",
                "message_rate": "30 FPS",
                "compression": "LZ4"
            },
            "beginner_explanation": "A fast, continuous connection is established so you can see other players' actions in real-time as you play.",
            "advanced_explanation": "Event-driven architecture with message queues, event sourcing, and CQRS pattern. Implements delta compression and client-side prediction for smooth gameplay."
        },
        {
            "step_number": 8,
            "title": "Monitoring & Analytics",
            "description": "System continuously monitors performance and player behavior",
            "components_involved": ["monitoring", "storage"],
            "diagram_focus": ["monitoring"],
            "technical_details": {
                "metrics_collection": "Prometheus + Custom Collectors",
                "log_aggregation": "ELK Stack",
                "alerting": "PagerDuty Integration"
            },
            "beginner_explanation": "Behind the scenes, systems constantly check that everything is working properly and collect data to improve the game.",
            "advanced_explanation": "Distributed tracing with OpenTelemetry, real-time anomaly detection, and machine learning-based capacity planning. Implements SLI/SLO monitoring and automated remediation."
        }
    ]
    
    # Insert steps
    for step_data in steps:
        step = StepExplanation(**step_data)
        await db.steps.insert_one(step.dict())
    
    logger.info("Architecture data initialized successfully")

# API Endpoints
@api_router.get("/components", response_model=List[ArchitectureComponent])
async def get_components(difficulty: Optional[DifficultyLevel] = None):
    """Get all architecture components, optionally filtered by difficulty"""
    query = {}
    if difficulty:
        query["difficulty_level"] = difficulty
    
    components = await db.components.find(query).sort("step_order", 1).to_list(100)
    return [ArchitectureComponent(**comp) for comp in components]

@api_router.get("/components/{component_id}", response_model=ArchitectureComponent)
async def get_component(component_id: str):
    """Get a specific component by ID"""
    component = await db.components.find_one({"id": component_id})
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")
    return ArchitectureComponent(**component)

@api_router.get("/steps", response_model=List[StepExplanation])
async def get_steps():
    """Get all step explanations in order"""
    steps = await db.steps.find().sort("step_number", 1).to_list(100)
    return [StepExplanation(**step) for step in steps]

@api_router.get("/steps/{step_number}", response_model=StepExplanation)
async def get_step(step_number: int):
    """Get a specific step explanation"""
    step = await db.steps.find_one({"step_number": step_number})
    if not step:
        raise HTTPException(status_code=404, detail="Step not found")
    return StepExplanation(**step)

@api_router.post("/calculate-capacity")
async def calculate_capacity(calculation: CapacityCalculationInput):
    """Calculate capacity metrics for a component"""
    component = await db.components.find_one({"id": calculation.component_id})
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")
    
    # Capacity calculation logic based on component type
    if component["type"] == ComponentType.GAME_SERVER:
        players = calculation.inputs.get("concurrent_players", 26000000)
        players_per_server = calculation.inputs.get("players_per_server", 100)
        servers_needed = math.ceil(players / players_per_server)
        
        result = {
            "servers_needed": servers_needed,
            "cpu_cores_total": servers_needed * 4,
            "memory_gb_total": servers_needed * 8,
            "network_gbps": servers_needed * 0.1
        }
        explanation = f"For {players:,} concurrent players with {players_per_server} players per server, you need {servers_needed:,} game servers."
    
    elif component["type"] == ComponentType.DATABASE:
        reads_per_second = calculation.inputs.get("reads_per_second", 2000000)
        writes_per_second = calculation.inputs.get("writes_per_second", 500000)
        
        result = {
            "read_replicas_needed": max(1, int(reads_per_second / 10000)),
            "write_masters_needed": max(1, int(writes_per_second / 5000)),
            "storage_tb_needed": int((reads_per_second + writes_per_second) * 0.001),
            "shards_needed": max(1, int((reads_per_second + writes_per_second) / 50000))
        }
        explanation = f"For {reads_per_second:,} reads/sec and {writes_per_second:,} writes/sec, you need {result['read_replicas_needed']} read replicas and {result['shards_needed']} shards."
    
    elif component["type"] == ComponentType.LOAD_BALANCER:
        requests_per_second = calculation.inputs.get("requests_per_second", 2000000)
        
        result = {
            "load_balancers_needed": max(1, int(requests_per_second / 100000)),
            "bandwidth_gbps": int(requests_per_second * 0.01),
            "ssl_termination_capacity": int(requests_per_second * 0.8),
            "health_checks_per_second": int(requests_per_second * 0.1)
        }
        explanation = f"For {requests_per_second:,} requests/sec, you need {result['load_balancers_needed']} load balancers with {result['bandwidth_gbps']} Gbps bandwidth."
    
    else:
        result = {"message": "Capacity calculation not implemented for this component type"}
        explanation = "Capacity calculation not available for this component."
    
    return {
        "component_id": calculation.component_id,
        "calculation_type": calculation.calculation_type,
        "inputs": calculation.inputs,
        "result": result,
        "explanation": explanation
    }

@api_router.get("/overview")
async def get_overview():
    """Get system overview metrics"""
    return {
        "total_concurrent_players": 26000000,
        "total_game_servers": 50000,
        "total_games": 1000000,
        "global_regions": 12,
        "edge_locations": 200,
        "requests_per_second": 10000000,
        "data_processed_per_day_tb": 1000,
        "uptime_percentage": 99.99
    }

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()