import praw
import pandas as pd
from tqdm import tqdm
import os

reddit = praw.Reddit(
    client_id="B9p-21QJHz9QYsiiY6bFpw",
    client_secret="DEOTHnpheAYiMjAEklkPmXYLT6141A",
    user_agent="prawtest")

def reorder_columns(dataframe, col_name, position):
    """Reorder a dataframe's column.
    Args:
        dataframe (pd.DataFrame): dataframe to use
        col_name (string): column name to move
        position (0-indexed position): where to relocate column to
    Returns:
        pd.DataFrame: re-assigned dataframe
    """
    temp_col = dataframe[col_name]
    dataframe = dataframe.drop(columns=[col_name])
    dataframe.insert(loc=position, column=col_name, value=temp_col)
    return dataframe



def get_submissions(query, sub, limit=None):
    query2 = query.replace('|','OR')
    query3 = query2.replace('+','AND')
    query4 = query3.replace(' ', '-')
    filename = f'data/praw_q={query4}_subreddit={sub}.csv'
    subreddit = reddit.subreddit(f'{sub}')
    if os.path.exists(filename):
        print('file exists')
    else:
        df = pd.DataFrame([vars(post) for post in subreddit.search(f'{query}', limit = limit) ])
        if 'id' in df.keys():
            columns_list = ['id', 'author', 'title', 'selftext', 'created','author_flair_text', 'link_flair_text', 'url']
            for i,j in enumerate(columns_list):
                df = reorder_columns(dataframe=df, col_name= j, position=i)
                print('csv created')
            df.reset_index(drop=True, inplace=True)
            df.to_csv(filename)
        else:
            print('no submissions')


if __name__ == '__main__':
    limit = 1000
    sublist = ['drugs']
    qlist = ['delta-8']

    for sub in tqdm(sublist):
        for q in tqdm(qlist):
            get_submissions(q, sub, limit=limit)
