#!/usr/bin/env python3
"""
MoodMate Backend API Testing Suite
Tests all backend endpoints for functionality, AI integration, and data persistence.
"""

import asyncio
import aiohttp
import json
import os
from datetime import datetime
from typing import Dict, List, Any

# Get backend URL from frontend environment
BACKEND_URL = "https://mood-lifter-12.preview.emergentagent.com/api"

class MoodMateAPITester:
    def __init__(self):
        self.session = None
        self.test_results = []
        self.saved_message_ids = []
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def log_test(self, test_name: str, success: bool, details: str, response_data: Any = None):
        """Log test results"""
        result = {
            'test': test_name,
            'success': success,
            'details': details,
            'timestamp': datetime.utcnow().isoformat(),
            'response_data': response_data
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {details}")
        if response_data and not success:
            print(f"   Response: {response_data}")
    
    async def test_health_check(self):
        """Test GET /api/ endpoint"""
        try:
            async with self.session.get(f"{BACKEND_URL}/") as response:
                if response.status == 200:
                    data = await response.json()
                    if "message" in data and "MoodMate" in data["message"]:
                        self.log_test("Health Check", True, f"API is running: {data['message']}", data)
                        return True
                    else:
                        self.log_test("Health Check", False, f"Unexpected response format", data)
                        return False
                else:
                    text = await response.text()
                    self.log_test("Health Check", False, f"HTTP {response.status}: {text}")
                    return False
        except Exception as e:
            self.log_test("Health Check", False, f"Connection error: {str(e)}")
            return False
    
    async def test_generate_message(self, emotion: str, language: str, test_name: str = None):
        """Test POST /api/generate-message endpoint"""
        if not test_name:
            test_name = f"Generate Message ({emotion}, {language})"
            
        try:
            payload = {
                "emotion": emotion,
                "language": language
            }
            
            async with self.session.post(
                f"{BACKEND_URL}/generate-message",
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    
                    # Verify response structure
                    required_fields = ["message", "emotion", "language", "timestamp"]
                    missing_fields = [field for field in required_fields if field not in data]
                    
                    if missing_fields:
                        self.log_test(test_name, False, f"Missing fields: {missing_fields}", data)
                        return False, None
                    
                    # Verify emotion and language match request
                    if data["emotion"] != emotion or data["language"] != language:
                        self.log_test(test_name, False, f"Emotion/language mismatch. Expected: {emotion}/{language}, Got: {data['emotion']}/{data['language']}", data)
                        return False, None
                    
                    # Verify message is not empty and seems contextual
                    message = data["message"].strip()
                    if not message:
                        self.log_test(test_name, False, "Empty message returned", data)
                        return False, None
                    
                    # Check if message seems generic/hardcoded (basic heuristics)
                    generic_phrases = ["hello", "test", "dummy", "placeholder", "lorem ipsum"]
                    is_generic = any(phrase in message.lower() for phrase in generic_phrases)
                    
                    if is_generic:
                        self.log_test(test_name, False, f"Message appears generic/hardcoded: {message}", data)
                        return False, None
                    
                    # Verify message length is reasonable (not too short/long)
                    if len(message) < 10:
                        self.log_test(test_name, False, f"Message too short ({len(message)} chars): {message}", data)
                        return False, None
                    
                    if len(message) > 500:
                        self.log_test(test_name, False, f"Message too long ({len(message)} chars)", data)
                        return False, None
                    
                    self.log_test(test_name, True, f"Generated contextual message ({len(message)} chars): {message[:100]}...", data)
                    return True, data
                    
                else:
                    text = await response.text()
                    self.log_test(test_name, False, f"HTTP {response.status}: {text}")
                    return False, None
                    
        except Exception as e:
            self.log_test(test_name, False, f"Request error: {str(e)}")
            return False, None
    
    async def test_save_message(self, emotion: str, language: str, message: str):
        """Test POST /api/save-message endpoint"""
        test_name = f"Save Message ({emotion})"
        
        try:
            payload = {
                "emotion": emotion,
                "language": language,
                "message": message
            }
            
            async with self.session.post(
                f"{BACKEND_URL}/save-message",
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    
                    # Verify response structure
                    if "id" not in data or "message" not in data:
                        self.log_test(test_name, False, "Missing id or message in response", data)
                        return False, None
                    
                    # Verify success message
                    if "success" not in data["message"].lower():
                        self.log_test(test_name, False, f"Unexpected response message: {data['message']}", data)
                        return False, None
                    
                    # Store ID for later retrieval test
                    message_id = data["id"]
                    self.saved_message_ids.append(message_id)
                    
                    self.log_test(test_name, True, f"Message saved with ID: {message_id}", data)
                    return True, data
                    
                else:
                    text = await response.text()
                    self.log_test(test_name, False, f"HTTP {response.status}: {text}")
                    return False, None
                    
        except Exception as e:
            self.log_test(test_name, False, f"Request error: {str(e)}")
            return False, None
    
    async def test_get_saved_messages(self):
        """Test GET /api/saved-messages endpoint"""
        test_name = "Get Saved Messages"
        
        try:
            async with self.session.get(f"{BACKEND_URL}/saved-messages") as response:
                
                if response.status == 200:
                    data = await response.json()
                    
                    # Verify response structure
                    if "messages" not in data:
                        self.log_test(test_name, False, "Missing 'messages' field in response", data)
                        return False
                    
                    messages = data["messages"]
                    if not isinstance(messages, list):
                        self.log_test(test_name, False, "'messages' field is not a list", data)
                        return False
                    
                    # Verify each message has required fields
                    required_fields = ["id", "emotion", "language", "text", "timestamp"]
                    
                    for i, msg in enumerate(messages):
                        missing_fields = [field for field in required_fields if field not in msg]
                        if missing_fields:
                            self.log_test(test_name, False, f"Message {i} missing fields: {missing_fields}", msg)
                            return False
                    
                    # Check if we can find our saved messages
                    found_saved_messages = 0
                    for saved_id in self.saved_message_ids:
                        if any(msg["id"] == saved_id for msg in messages):
                            found_saved_messages += 1
                    
                    self.log_test(test_name, True, f"Retrieved {len(messages)} messages, found {found_saved_messages}/{len(self.saved_message_ids)} saved messages", data)
                    return True
                    
                else:
                    text = await response.text()
                    self.log_test(test_name, False, f"HTTP {response.status}: {text}")
                    return False
                    
        except Exception as e:
            self.log_test(test_name, False, f"Request error: {str(e)}")
            return False
    
    async def run_comprehensive_tests(self):
        """Run all API tests"""
        print(f"🚀 Starting MoodMate Backend API Tests")
        print(f"📡 Backend URL: {BACKEND_URL}")
        print("=" * 60)
        
        # Test 1: Health Check
        health_ok = await self.test_health_check()
        
        if not health_ok:
            print("\n❌ Health check failed - stopping tests")
            return False
        
        # Test 2: Message Generation Tests
        test_cases = [
            ("Happy", "English"),
            ("Sad", "Turkish"), 
            ("Anxious", "Spanish"),
            ("Excited", "English"),
            ("Stressed", "German")
        ]
        
        generated_messages = []
        generation_success = True
        
        for emotion, language in test_cases:
            success, response_data = await self.test_generate_message(emotion, language)
            if success and response_data:
                generated_messages.append((emotion, language, response_data["message"]))
            else:
                generation_success = False
        
        # Test uniqueness of generated messages
        if generated_messages:
            messages_text = [msg[2] for msg in generated_messages]
            unique_messages = set(messages_text)
            
            if len(unique_messages) < len(messages_text):
                self.log_test("Message Uniqueness", False, f"Generated {len(messages_text)} messages but only {len(unique_messages)} unique")
            else:
                self.log_test("Message Uniqueness", True, f"All {len(messages_text)} generated messages are unique")
        
        # Test 3: Save Messages
        save_success = True
        for emotion, language, message in generated_messages[:3]:  # Save first 3 messages
            success, _ = await self.test_save_message(emotion, language, message)
            if not success:
                save_success = False
        
        # Test 4: Retrieve Saved Messages
        retrieval_success = await self.test_get_saved_messages()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        # Show failed tests
        failed_tests = [result for result in self.test_results if not result['success']]
        if failed_tests:
            print(f"\n❌ FAILED TESTS:")
            for test in failed_tests:
                print(f"   • {test['test']}: {test['details']}")
        
        overall_success = health_ok and generation_success and save_success and retrieval_success
        
        if overall_success:
            print(f"\n🎉 ALL CORE FUNCTIONALITY WORKING!")
        else:
            print(f"\n⚠️  SOME TESTS FAILED - CHECK DETAILS ABOVE")
        
        return overall_success

async def main():
    """Main test runner"""
    async with MoodMateAPITester() as tester:
        success = await tester.run_comprehensive_tests()
        return success

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)