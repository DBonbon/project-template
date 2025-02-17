from github import Github
from datetime import datetime
import os
from dotenv import load_dotenv
import subprocess

class DebugLogger:
    def __init__(self, repo_name: str = None):
        """Initialize with repository name."""
        # Load environment variables
        load_dotenv()
        
        # Get GitHub token
        token = os.getenv('GITHUB_TOKEN')
        if not token:
            raise ValueError("GITHUB_TOKEN not found in environment variables")
        
        # Get repository name
        if not repo_name:
            # Try from environment
            repo_name = os.getenv('GITHUB_REPO')
            if not repo_name:
                # Try to get from git remote
                try:
                    remote_url = subprocess.check_output(['git', 'remote', 'get-url', 'origin']).decode('utf-8').strip()
                    # Handle SSH URL format: git@github.com:owner/repo.git
                    if remote_url.startswith('git@'):
                        repo_name = remote_url.split(':')[1].replace('.git', '')
                    # Handle HTTPS URL format: https://github.com/owner/repo.git
                    elif remote_url.startswith('https://'):
                        repo_name = remote_url.split('github.com/')[1].replace('.git', '')
                except Exception as e:
                    print(f"Error getting remote URL: {str(e)}")
                    raise ValueError("Could not determine repository name")

        print(f"Attempting to connect to repository: {repo_name}")
        
        self.github = Github(token)
        try:
            # Test authentication
            user = self.github.get_user()
            print(f"Authenticated as: {user.login}")
            
            # Get repository
            self.repo = self.github.get_repo(repo_name)
            print(f"Successfully connected to repository: {self.repo.full_name}")
        except Exception as e:
            print(f"Error connecting to repository: {str(e)}")
            print("\nAvailable repositories:")
            for repo in self.github.get_user().get_repos():
                print(f"- {repo.full_name}")
            raise

    def create_simple_issue(self, title: str, description: str, labels=None, related_issues=None):
        """Create a simple debug issue."""
        # Format related issues if any
        related_links = ""
        if related_issues:
            related_links = "\n### Related Issues\n" + "\n".join(
                f"- #{issue}" for issue in related_issues
            )

        # Create structured body
        body = f"""
## Debug Session
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

### Description
{description}

### Status
- [ ] Investigation started
- [ ] Solution identified
- [ ] Implemented
- [ ] Verified

### Notes
- Initial setup
{related_links}
"""
        # Create issue
        issue = self.repo.create_issue(
            title=title,
            body=body,
            labels=labels or []
        )
        
        print(f"Created issue #{issue.number}: {issue.html_url}")
        return issue

if __name__ == "__main__":
    try:
        # Example usage
        logger = DebugLogger()  # Will use GITHUB_REPO from .env or git remote
        
        # Create a dummy issue first
        dummy = logger.create_simple_issue(
            title="Initial Project Setup",
            description="Setting up basic project structure and utilities.",
            labels=["documentation"]
        )
        
        # Create main debug logger issue
        logger.create_simple_issue(
            title="Implementing GitHub Debug Logger",
            description="Setting up a debug logging system using GitHub Issues API.",
            labels=["enhancement", "documentation"],
            related_issues=[str(dummy.number)]  # Link to the dummy issue
        )
    except Exception as e:
        print(f"\nError: {str(e)}")
        exit(1)