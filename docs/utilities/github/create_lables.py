import os
import github
from dotenv import load_dotenv
import subprocess

# Load environment variables from .env file
load_dotenv()

# Read GitHub token from environment variable
token = os.getenv("GITHUB_TOKEN")

# Create a GitHub API client
g = github.Github(token)

# Get repository name from environment variable or Git remote URL
repo_name = os.getenv("GITHUB_REPO")
if not repo_name:
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

# Get your repository
repo = g.get_repo(repo_name)

# Create labels
labels = [
    {"name": "Epic", "color": "ff9900"},
    {"name": "Feature", "color": "00ff00"},
    {"name": "Bug", "color": "ff0000"},
    {"name": "High", "color": "ff0000"},
    {"name": "Medium", "color": "ffff00"},
    {"name": "Low", "color": "00ff00"},
]

for label in labels:
    try:
        repo.create_label(label["name"], label["color"])
        print(f"Label '{label['name']}' created successfully.")
    except github.GithubException as e:
        if e.status == 422:
            print(f"Label '{label['name']}' already exists.")
        else:
            raise

# Create priorities (as labels)
priorities = [
    {"name": "High Priority", "color": "ff0000"},
    {"name": "Medium Priority", "color": "ffff00"},
    {"name": "Low Priority", "color": "00ff00"},
]

for priority in priorities:
    try:
        repo.create_label(priority["name"], priority["color"])
        print(f"Label '{priority['name']}' created successfully.")
    except github.GithubException as e:
        if e.status == 422:
            print(f"Label '{priority['name']}' already exists.")
        else:
            raise