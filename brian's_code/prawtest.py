import praw
import pandas as pd
from tqdm import tqdm
import os

reddit = praw.Reddit(
    client_id="B9p-21QJHz9QYsiiY6bFpw",
    client_secret="DEOTHnpheAYiMjAEklkPmXYLT6141A",
    user_agent="prawtest")

def get_submissions(query, sub, **kwarg):
    query2 = query.replace('|','OR')
    query3 = query2.replace('+','AND')
    query4 = query3.replace(' ', '-')
    filename = f'../data/praw_q={query4}_subreddit={sub}.csv'
    if kwarg.get('limit'):
        limit = kwarg.get('limit')
    else:
        limit = None
    subreddit = reddit.subreddit(f'{sub}')
    if os.path.exists(filename):
        pass
    else:
        df = pd.DataFrame([vars(post) for post in subreddit.search(f'{query}', limit = limit) ])
        if 'id' in df.keys():
            df.to_csv(filename)
        else:
            pass


if __name__ == '__main__':
    limit = 1000
    sublist = ['delta8', 'delta8testing']
    qlist = ['law|legislation|legislator|government']

    for sub in tqdm(sublist, desc=f'Subreddit = {sub}'):
        for q in tqdm(qlist, desc = f'Query = {q}'):
            get_submissions(q, sub, limit=limit)
