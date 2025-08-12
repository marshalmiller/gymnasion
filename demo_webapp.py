#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Demo script for the Gymnasion Web App
Shows how to use the web app programmatically via API calls
"""

import requests
import json
import time

def demo_gymnasion_web_app():
    """Demonstrate the Gymnasion web app functionality"""
    
    base_url = "http://127.0.0.1:5001"
    
    print("🏛️  Gymnasion Web App Demo")
    print("=" * 50)
    print()
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    # Test inputs
    test_inputs = [
        "I see a dark forest.",
        "The mountain towers above the valley.",
        "A bird sings in the ancient tree.",
        "The wolf hunts in the moonlight.",
        "I dream of the endless sea."
    ]
    
    print("Testing literary analysis responses:")
    print("-" * 40)
    
    for i, text_input in enumerate(test_inputs, 1):
        print(f"\n{i}. Input: \"{text_input}\"")
        
        try:
            response = session.post(
                f"{base_url}/analyze",
                json={"text": text_input},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   Gymnasion: {data['response']}")
                
                # Show session state
                if data.get('banished_words'):
                    print(f"   Banished: {', '.join(data['banished_words'])}")
                if data.get('to_imitate'):
                    print(f"   Imitating: {data['to_imitate']}")
                print(f"   Words written: {data.get('poem_length', 0)}")
            else:
                print(f"   Error: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"   Connection error: {e}")
            break
            
        time.sleep(1)  # Brief pause between requests
    
    print("\n" + "=" * 50)
    print("Demo completed!")
    print()
    print("To interact with the web app:")
    print("1. Open http://127.0.0.1:5001 in your browser")
    print("2. Enter text in the input area")
    print("3. Receive real-time literary guidance")
    print("4. Watch your session progress")

if __name__ == "__main__":
    demo_gymnasion_web_app()
