# Githubclient to fetch commits from a repository.
import requests


def fetch_github_commits(repo_owner, repo_name, token):
    """
    Fetches a list of commits from a GitHub repository.

    Parameters:
        repo_owner (str): The owner of the GitHub repository.
        repo_name (str): The name of the GitHub repository.
        token (str): Your GitHub personal access token.

    Returns:
        list: A list of dictionaries containing commit data.
    """
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/commits'
    headers = {'Authorization': f'token {token}'}
    commits_data = []

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for request errors

        commits = response.json()

        for commit in commits:
            commit_info = {
                'sha': commit['sha'],
                'author': commit['commit']['author']['name'],
                'date': commit['commit']['author']['date'],
                'message': commit['commit']['message']
            }
            commits_data.append(commit_info)

        return commits_data

    except requests.RequestException as e:
        print(f"Error fetching commits: {e}")
        return []


def fetch_gitHub_commit_stats(token, repo_owner, repo_name, sha):
    """
    Fetches a full commit from a GitHub repository.

    Parameters:
        sha (str): The commit SHA.
        repo_owner (str): The owner of the GitHub repository.
        repo_name (str): The name of the GitHub repository.
        token (str): Your GitHub personal access token.

    Returns:
        dict: A dictionary of an extra commit data.
    """
    commit_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/commits/{sha}'
    headers = {'Authorization': f'token {token}'}
    commit_info = {}

    try:
        commit_response = requests.get(commit_url, headers=headers)
        commit_response.raise_for_status()  # Check for request errors

        commit_stats = commit_response.json()

        # Read additions and deletions
        stats = commit_stats.get('stats', {})

        commit_info = {
            'sha': sha,
            'additions': stats.get('additions', 0),
            'deletions': stats.get('deletions', 0),
            'total': stats.get('total', 0)
        }

        return commit_info

    except requests.RequestException as e:
        print(f"Error fetching commits: {e}")
        return commit_info
