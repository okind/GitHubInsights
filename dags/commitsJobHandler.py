import csvRepository
import gitHubClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Example usage:
# repo_owner = 'okind'
# repo_name = 'algorithmic_programming'
repo_owner = 'dddat1017'
repo_name = 'Scraping-Youtube-Comments'
token = os.getenv('GITHUB_TOKEN')

# Fetch commit data from GitHub
# Provide repo data: repo_owner, repo_name, token
commits_data = gitHubClient.fetch_github_commits(repo_owner, repo_name, token)

# Save the fetched commit data to a CSV file
csvRepository.save_commits_to_csv(commits_data, './dags/commits.csv')