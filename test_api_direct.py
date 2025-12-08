"""
Test GitHub API directly to see how many commits it actually returns
"""
import requests
import time

url = "https://api.github.com/repos/facebook/react/commits"
total_fetched = 0
page = 1
commits_list = []

print("="*70)
print("TESTING GITHUB API DIRECTLY")
print("="*70)

while total_fetched < 200 and page <= 3:  # Check first 3 pages
    params = {'per_page': 100, 'page': page}
    
    print(f"\nFetching page {page}...")
    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"  Commits on this page: {len(data)}")
            commits_list.extend(data)
            total_fetched += len(data)
            
            if len(data) < 100:
                print(f"  ⚠ This page has fewer than 100 commits - API may have no more")
                break
        elif response.status_code == 403:
            print(f"  ⚠ Rate limit hit!")
            print(f"  Response: {response.text[:200]}")
            break
        else:
            print(f"  ⚠ Error: {response.status_code}")
            break
            
        page += 1
        time.sleep(0.5)  # Be respectful
        
    except Exception as e:
        print(f"  ⚠ Error: {e}")
        break

print(f"\n" + "="*70)
print(f"TOTAL COMMITS FETCHED: {total_fetched}")
print(f"Expected: 200")
print("="*70)

if total_fetched < 200:
    print(f"\n⚠ ISSUE: API only returned {total_fetched} commits")
    print(f"  This explains why visualization shows fewer commits")
    print(f"  Possible reasons:")
    print(f"    1. Rate limiting (check response headers)")
    print(f"    2. Repository doesn't have 200 recent commits")
    print(f"    3. API pagination limits")
else:
    print(f"\n✓ API returned {total_fetched} commits - should be enough for 200")

# Save result
with open('API_TEST_RESULT.txt', 'w') as f:
    f.write(f"GitHub API Test Result\n")
    f.write("="*70 + "\n\n")
    f.write(f"Total commits fetched: {total_fetched}\n")
    f.write(f"Pages checked: {page-1}\n")
    f.write(f"Expected: 200\n")

print("\n✓ Result saved to API_TEST_RESULT.txt")

