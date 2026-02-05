"""Test NASA Earthdata credentials"""
import os
import sys

# Load credentials
sys.path.insert(0, os.path.dirname(__file__))
from load_env import load_credentials

print("=" * 50)
print("  NASA CREDENTIALS TEST")
print("=" * 50)

load_credentials()

# Test 1: NASA POWER API (no auth needed, just API)
print("\n[1] Testing NASA POWER API...")
import requests
try:
    url = 'https://power.larc.nasa.gov/api/temporal/daily/point'
    params = {
        'parameters': 'T2M',
        'community': 'RE',
        'longitude': 55.27,
        'latitude': 25.20,
        'start': '20250101',
        'end': '20250103',
        'format': 'JSON'
    }
    response = requests.get(url, params=params, timeout=30)
    if response.status_code == 200:
        data = response.json()
        temps = data['properties']['parameter']['T2M']
        print("    Dubai temperatures (Jan 2025):")
        for date, temp in temps.items():
            print(f"      {date}: {temp:.1f}C")
        print("    NASA POWER API: SUCCESS")
    else:
        print(f"    POWER API returned: {response.status_code}")
except Exception as e:
    print(f"    POWER API error: {e}")

# Test 2: Earthdata Search (public, no auth)
print("\n[2] Testing NASA CMR Search...")
try:
    import earthaccess
    results = earthaccess.search_data(
        short_name='MCD43A4',
        bounding_box=(54, 24, 56, 26),
        temporal=('2025-01-01', '2025-01-07'),
        count=2
    )
    print(f"    Found {len(results)} MODIS granules")
    print("    NASA CMR Search: SUCCESS")
except Exception as e:
    print(f"    CMR Search error: {e}")

# Test 3: Earthdata Login with token
print("\n[3] Testing NASA Earthdata Login...")
try:
    import earthaccess
    token = os.getenv('NASA_TOKEN')
    if token:
        # Store credentials in netrc format for earthaccess
        auth = earthaccess.login(strategy='environment')
        if auth:
            print("    Earthdata Login: SUCCESS")
        else:
            print("    Login returned None - trying token auth...")
            # Direct token test
            headers = {'Authorization': f'Bearer {token}'}
            test_url = 'https://cmr.earthdata.nasa.gov/search/collections.json?short_name=MCD43A4&page_size=1'
            r = requests.get(test_url, headers=headers, timeout=10)
            if r.status_code == 200:
                print("    Token authentication: SUCCESS")
            else:
                print(f"    Token test returned: {r.status_code}")
    else:
        print("    NASA_TOKEN not set")
except Exception as e:
    print(f"    Login error: {e}")

print("\n" + "=" * 50)
print("  TEST COMPLETE")
print("=" * 50)
