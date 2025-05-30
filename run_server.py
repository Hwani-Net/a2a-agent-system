"""
A2A Agent Server Runner
"""
import os
import sys
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from a2a_server import A2AServer

def main():
    """Run the A2A server with configuration validation"""
    
    print("=== A2A Agent Server ===")
    print(f"Agent Name: {Config.AGENT_NAME}")
    print(f"Host: {Config.AGENT_HOST}")
    print(f"Port: {Config.AGENT_PORT}")
    print()
    
    # Validate configuration
    if not Config.validate_keys():
        print("⚠ Some API keys are missing. The agent will run with limited functionality.")
        response = input("Continue anyway? (y/N): ").strip().lower()
        if response != 'y':
            print("Server startup cancelled.")
            return
    else:
        print("✓ Configuration validated successfully!")
    
    print("\nStarting A2A Agent Server...")
    print("Press Ctrl+C to stop the server")
    print()
    
    try:
        # Create and run server
        server = A2AServer()
        server.run()
    except KeyboardInterrupt:
        print("\n\nServer stopped by user.")
    except Exception as e:
        print(f"\nError starting server: {str(e)}")
        print("Please check your configuration and try again.")

if __name__ == "__main__":
    main() 