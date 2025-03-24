import csvRepository
import gitHubClient


# Fetch commits data from GitHub to commits.csv
# REPO_OWNER - owner of the repository to fetch commits from
# REPO_NAME - name of the repository to fetch commits from
# token - GitHub API token for authentication


def extract_commits_data(REPO_OWNER, REPO_NAME, token):
    commits_data = gitHubClient.fetch_github_commits(
        REPO_OWNER, REPO_NAME, token)
    for commit in commits_data:
        sha = commit['sha']
        # Add commit stats to commit data
        commit.update(
            gitHubClient.fetch_gitHub_commit_stats(token, REPO_OWNER, REPO_NAME, sha))

    # Save the fetched commit data to a CSV file
    csvRepository.save_commits_to_csv(commits_data, './dags/commits.csv')
