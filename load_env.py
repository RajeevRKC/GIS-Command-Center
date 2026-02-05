"""
Load GIS Command Center environment variables from .env file
Usage: from load_env import load_credentials
"""

import os
from pathlib import Path

def load_credentials():
    """Load credentials from .env file into environment variables"""
    env_path = Path(__file__).parent / ".env"

    if not env_path.exists():
        print("Warning: .env file not found. Create one with your API keys.")
        return False

    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

    print("Credentials loaded:")
    print(f"  MAPBOX_USERNAME: {os.getenv('MAPBOX_USERNAME', 'NOT SET')}")
    print(f"  NASA_USERNAME: {os.getenv('NASA_USERNAME', 'NOT SET')}")
    print(f"  MAPBOX_API_KEY: {'SET' if os.getenv('MAPBOX_API_KEY') else 'NOT SET'}")
    print(f"  NASA_TOKEN: {'SET' if os.getenv('NASA_TOKEN') else 'NOT SET'}")
    return True

def get_mapbox_token():
    """Get Mapbox API token"""
    load_credentials()
    return os.getenv('MAPBOX_API_KEY')

def get_nasa_token():
    """Get NASA Earthdata token"""
    load_credentials()
    return os.getenv('NASA_TOKEN')

if __name__ == "__main__":
    load_credentials()
