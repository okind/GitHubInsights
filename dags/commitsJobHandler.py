# GitHubInsights fetches commits data from GitHub and saves it to a CSV file.

import os
from dotenv import load_dotenv
import csvRepository
import gitHubClient


# Load environment variables from .env file
load_dotenv()

# Example usage:
# REPO_OWNER = 'okind'
# REPO_NAME = 'algorithmic_programming'
REPO_OWNER = 'dddat1017'
REPO_NAME = 'Scraping-Youtube-Comments'
token = os.getenv('GITHUB_TOKEN')

# Fetch commit data from GitHub
# Provide repo data: repo_owner, repo_name, token
commits_data = gitHubClient.fetch_github_commits(REPO_OWNER, REPO_NAME, token)

# Save the fetched commit data to a CSV file
csvRepository.save_commits_to_csv(commits_data, './dags/commits.csv')
