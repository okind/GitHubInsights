import pandas as pd

def save_commits_to_csv(commits_data, output_csv='commits.csv'):
    """
    Saves a list of commit data to a CSV file.

    Parameters:
        commits_data (list): A list of dictionaries containing commit data.
        output_csv (str): The name of the CSV file to save the commits data.
    """
    if commits_data:
        df = pd.DataFrame(commits_data)
        df.to_csv(output_csv, index=False)
        print(f'Successfully saved {len(commits_data)} commits to {output_csv}')
    else:
        print("No commit data to save.")