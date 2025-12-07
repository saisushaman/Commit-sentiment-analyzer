"""
Commit Message Sentiment Analyzer
Fetches and analyzes GitHub commit messages using sentiment analysis.
"""

import requests
from datetime import datetime
from typing import List, Dict, Optional
import time


class CommitFetcher:
    """Fetches commit messages from GitHub repositories."""
    
    def __init__(self, owner: str, repo: str):
        """
        Initialize the commit fetcher.
        
        Args:
            owner: GitHub repository owner (username or organization)
            repo: Repository name
        """
        self.owner = owner
        self.repo = repo
        self.base_url = f"https://api.github.com/repos/{owner}/{repo}/commits"
        
    def fetch_commits(self, limit: int = 200, per_page: int = 100) -> List[Dict]:
        """
        Fetch commit messages from GitHub.
        
        Args:
            limit: Maximum number of commits to fetch
            per_page: Number of commits per API request (max 100)
            
        Returns:
            List of dictionaries containing commit data (message, date, sha)
        """
        commits = []
        page = 1
        
        print(f"Fetching commits from {self.owner}/{self.repo}...")
        
        try:
            while len(commits) < limit:
                params = {
                    'per_page': min(per_page, limit - len(commits)),
                    'page': page
                }
                
                response = requests.get(self.base_url, params=params)
                
                # Handle rate limiting
                if response.status_code == 403:
                    if 'rate limit' in response.text.lower():
                        print("Rate limit exceeded. Waiting 60 seconds...")
                        time.sleep(60)
                        continue
                    
                response.raise_for_status()
                data = response.json()
                
                if not data:
                    break
                
                for commit in data:
                    commit_info = {
                        'sha': commit['sha'][:7],
                        'message': commit['commit']['message'],
                        'date': commit['commit']['author']['date'],
                        'author': commit['commit']['author']['name']
                    }
                    commits.append(commit_info)
                    
                    if len(commits) >= limit:
                        break
                
                if len(data) < per_page:
                    break
                    
                page += 1
                
                # Be respectful to GitHub API
                time.sleep(0.1)
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching commits: {e}")
            if "404" in str(e):
                print(f"Repository {self.owner}/{self.repo} not found or is private.")
            return []
        
        print(f"Found {len(commits)} commits")
        return commits
    
    def format_commit_message(self, message: str) -> str:
        """
        Clean and format commit message (remove extra whitespace, etc.)
        
        Args:
            message: Raw commit message
            
        Returns:
            Cleaned commit message
        """
        # Split by newlines and take the first line (subject)
        lines = message.strip().split('\n')
        return lines[0].strip()

