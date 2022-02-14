import praw
import pandas as pd

reddit = praw.Reddit(
    client_id="B9p-21QJHz9QYsiiY6bFpw",
    client_secret="DEOTHnpheAYiMjAEklkPmXYLT6141A",
    user_agent="prawtest")

def get_submissions(query, sub, **kwarg):
    if kwarg.get('limit'):
        limit = kwarg.get('limit')
    else:
        limit = None
    subreddit = reddit.subreddit(f'{sub}')
    df = pd.DataFrame([vars(post) for post in subreddit.search(f'{query}', limit = limit) ])
    query2 = query.replace('|','OR')
    query3 = query2.replace('+','AND')
    query4 = query3.replace(' ', '-')
    df.to_csv(f'../data/praw_q={query4}_subreddit={sub}.csv')

limit = 100

get_submissions('regulation|regulate', 'delta8', limit=limit)
