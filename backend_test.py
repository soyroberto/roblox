import requests
import unittest
import json
import os
import sys

# Get the backend URL from the frontend .env file
BACKEND_URL = "https://0d186e34-9eb0-4f64-a901-d9734ba38586.preview.emergentagent.com"
API_URL = f"{BACKEND_URL}/api"

class RobloxArchitectureAPITest(unittest.TestCase):
    """Test suite for the Roblox Architecture Explanation API"""

    def test_components_endpoint(self):
        """Test the /api/components endpoint"""
        print("\n🔍 Testing /api/components endpoint...")
        
        # Test getting all components
        response = requests.get(f"{API_URL}/components")
        self.assertEqual(response.status_code, 200, "Should return 200 OK")
        
        components = response.json()
        self.assertEqual(len(components), 10, "Should return 10 architecture components")
        
        # Check required fields in each component
        required_fields = ["id", "name", "type", "description", "technologies", 
                          "protocols", "capacity_metrics", "difficulty_level"]
        
        for component in components:
            for field in required_fields:
                self.assertIn(field, component, f"Component should have '{field}' field")
        
        # Test filtering by difficulty level
        for difficulty in ["beginner", "intermediate", "advanced"]:
            response = requests.get(f"{API_URL}/components?difficulty={difficulty}")
            self.assertEqual(response.status_code, 200, f"Should return 200 OK for difficulty={difficulty}")
            
            filtered_components = response.json()
            self.assertTrue(len(filtered_components) > 0, f"Should return components with difficulty={difficulty}")
            
            # Verify all returned components have the correct difficulty level
            for component in filtered_components:
                self.assertEqual(component["difficulty_level"], difficulty, 
                                f"Component difficulty should match filter: {difficulty}")
        
        print("✅ /api/components endpoint tests passed")

    def test_steps_endpoint(self):
        """Test the /api/steps endpoint"""
        print("\n🔍 Testing /api/steps endpoint...")
        
        response = requests.get(f"{API_URL}/steps")
        self.assertEqual(response.status_code, 200, "Should return 200 OK")
        
        steps = response.json()
        self.assertEqual(len(steps), 8, "Should return 8 step explanations")
        
        # Check steps are in correct order
        for i, step in enumerate(steps):
            self.assertEqual(step["step_number"], i+1, "Steps should be in correct order")
            
            # Check each step has beginner and advanced explanations
            self.assertIn("beginner_explanation", step, "Step should have beginner explanation")
            self.assertIn("advanced_explanation", step, "Step should have advanced explanation")
            self.assertTrue(len(step["beginner_explanation"]) > 0, "Beginner explanation should not be empty")
            self.assertTrue(len(step["advanced_explanation"]) > 0, "Advanced explanation should not be empty")
            
            # Verify technical details are present
            self.assertIn("technical_details", step, "Step should have technical details")
            self.assertTrue(len(step["technical_details"]) > 0, "Technical details should not be empty")
        
        print("✅ /api/steps endpoint tests passed")

    def test_overview_endpoint(self):
        """Test the /api/overview endpoint"""
        print("\n🔍 Testing /api/overview endpoint...")
        
        response = requests.get(f"{API_URL}/overview")
        self.assertEqual(response.status_code, 200, "Should return 200 OK")
        
        overview = response.json()
        
        # Check required metrics
        required_metrics = ["total_concurrent_players", "total_game_servers", 
                           "requests_per_second", "uptime_percentage"]
        
        for metric in required_metrics:
            self.assertIn(metric, overview, f"Overview should include '{metric}'")
        
        # Verify specific values
        self.assertEqual(overview["total_concurrent_players"], 26000000, 
                        "Should report 26M concurrent players")
        self.assertEqual(overview["total_game_servers"], 50000, 
                        "Should report 50K game servers")
        
        print("✅ /api/overview endpoint tests passed")

    def test_capacity_calculator_endpoint(self):
        """Test the /api/calculate-capacity endpoint"""
        print("\n🔍 Testing /api/calculate-capacity endpoint...")
        
        # First, get a component ID for each type we want to test
        response = requests.get(f"{API_URL}/components")
        components = response.json()
        
        component_ids = {
            "game_server": next((c["id"] for c in components if c["type"] == "game_server"), None),
            "database": next((c["id"] for c in components if c["type"] == "database"), None),
            "load_balancer": next((c["id"] for c in components if c["type"] == "load_balancer"), None)
        }
        
        # Test game server capacity calculation
        if component_ids["game_server"]:
            data = {
                "component_id": component_ids["game_server"],
                "calculation_type": "basic",
                "inputs": {
                    "concurrent_players": 30000000,
                    "players_per_server": 80
                }
            }
            
            response = requests.post(f"{API_URL}/calculate-capacity", json=data)
            self.assertEqual(response.status_code, 200, "Should return 200 OK")
            
            result = response.json()
            self.assertIn("result", result, "Response should include calculation result")
            self.assertIn("servers_needed", result["result"], "Result should include servers_needed")
            
            # Verify calculation is mathematically correct
            expected_servers = 30000000 / 80
            self.assertEqual(result["result"]["servers_needed"], 375000, 
                            "Calculation should be mathematically correct")
        
        # Test database capacity calculation
        if component_ids["database"]:
            data = {
                "component_id": component_ids["database"],
                "calculation_type": "basic",
                "inputs": {
                    "reads_per_second": 2000000,
                    "writes_per_second": 500000
                }
            }
            
            response = requests.post(f"{API_URL}/calculate-capacity", json=data)
            self.assertEqual(response.status_code, 200, "Should return 200 OK")
            
            result = response.json()
            self.assertIn("result", result, "Response should include calculation result")
            self.assertIn("read_replicas_needed", result["result"], "Result should include read_replicas_needed")
            self.assertIn("shards_needed", result["result"], "Result should include shards_needed")
        
        # Test load balancer capacity calculation
        if component_ids["load_balancer"]:
            data = {
                "component_id": component_ids["load_balancer"],
                "calculation_type": "basic",
                "inputs": {
                    "requests_per_second": 2000000
                }
            }
            
            response = requests.post(f"{API_URL}/calculate-capacity", json=data)
            self.assertEqual(response.status_code, 200, "Should return 200 OK")
            
            result = response.json()
            self.assertIn("result", result, "Response should include calculation result")
            self.assertIn("load_balancers_needed", result["result"], "Result should include load_balancers_needed")
            self.assertIn("bandwidth_gbps", result["result"], "Result should include bandwidth_gbps")
        
        print("✅ /api/calculate-capacity endpoint tests passed")

if __name__ == "__main__":
    print(f"🧪 Running Roblox Architecture API Tests against {API_URL}")
    unittest.main(argv=['first-arg-is-ignored'], exit=False)