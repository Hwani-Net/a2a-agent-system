"""
Quick Start Script for A2A Agent System
"""
import os
import sys
import subprocess
import time
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✓ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n=== Installing Dependencies ===")
    
    try:
        print("Installing required packages...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✓ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def setup_environment():
    """Setup environment if .env doesn't exist"""
    env_file = Path(".env")
    
    if env_file.exists():
        print("✓ .env file already exists")
        return True
    
    print("\n=== Environment Setup ===")
    print("Setting up basic environment...")
    
    # Create basic .env file
    basic_env = """# A2A Agent System Configuration
# Edit this file to add your API keys

# AI Service API Keys (add your keys here)
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GOOGLE_API_KEY=
COHERE_API_KEY=

# A2A Agent Settings
A2A_AGENT_NAME=MyCustomAgent
A2A_AGENT_PORT=8000
A2A_AGENT_HOST=localhost

# Optional Service API Keys
WEATHER_API_KEY=
NEWS_API_KEY=
"""
    
    try:
        with open(env_file, "w") as f:
            f.write(basic_env)
        print("✓ Basic .env file created")
        print("📝 Edit .env file to add your API keys")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def test_server():
    """Test if server starts correctly"""
    print("\n=== Testing Server ===")
    print("Starting server for quick test...")
    
    try:
        # Import and test server
        from config import Config
        from a2a_server import A2AServer
        
        print(f"✓ Server modules imported successfully")
        print(f"✓ Agent name: {Config.AGENT_NAME}")
        print(f"✓ Server will run on {Config.AGENT_HOST}:{Config.AGENT_PORT}")
        
        # Quick validation
        server = A2AServer()
        print("✓ Server instance created successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please check if all dependencies are installed correctly")
        return False
    except Exception as e:
        print(f"❌ Server test failed: {e}")
        return False

def show_next_steps():
    """Show next steps to user"""
    print("\n" + "="*50)
    print("🎉 A2A Agent System Setup Complete!")
    print("="*50)
    
    print("\n📋 Next Steps:")
    print("1. Edit .env file to add your API keys:")
    print("   - OpenAI API key for text generation")
    print("   - Other AI service keys (optional)")
    
    print("\n2. Start the A2A server:")
    print("   python run_server.py")
    
    print("\n3. Test the client (in another terminal):")
    print("   python a2a_client.py")
    
    print("\n4. View your agent:")
    print("   - Agent Card: http://localhost:8000/agent-card")
    print("   - Health Check: http://localhost:8000/health")
    print("   - Skills List: http://localhost:8000/skills")
    
    print("\n📚 Documentation:")
    print("   - README.md for detailed usage")
    print("   - A2A Protocol: https://google-a2a.github.io/A2A/")
    
    print("\n🔧 Configuration:")
    if not os.getenv("OPENAI_API_KEY"):
        print("   ⚠ Add your OpenAI API key to .env for full functionality")
    else:
        print("   ✓ API keys configured")

def main():
    """Main quick start function"""
    print("🚀 A2A Agent System Quick Start")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Setup environment
    if not setup_environment():
        return False
    
    # Test server
    if not test_server():
        return False
    
    # Show next steps
    show_next_steps()
    
    # Ask if user wants to start server now
    print("\n" + "="*50)
    response = input("🚀 Start the A2A server now? (y/N): ").strip().lower()
    
    if response == 'y':
        print("\nStarting A2A server...")
        print("Press Ctrl+C to stop the server")
        
        try:
            from run_server import main as run_server
            run_server()
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped. Thanks for trying A2A Agent System!")
        except Exception as e:
            print(f"\n❌ Error starting server: {e}")
            print("Please check the configuration and try 'python run_server.py'")
    else:
        print("\n👋 Setup complete! Run 'python run_server.py' when ready.")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1) 