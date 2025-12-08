"""Quick test to see if we can fetch commits"""
import requests
import time

def test_fetch():
    url = "https://api.github.com/repos/facebook/react/commits"
    params = {'per_page': 100, 'page': 1}
    
    print("Testing GitHub API connection...")
    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Successfully fetched {len(data)} commits from first page")
            print(f"Sample commit SHA: {data[0]['sha'][:7] if data else 'N/A'}")
            return True
        else:
            print(f"Error: {response.status_code}")
            print(response.text[:200])
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == '__main__':
    test_fetch()

