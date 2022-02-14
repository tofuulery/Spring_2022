import praw
import pandas as pd

reddit = praw.Reddit(
    client_id="B9p-21QJHz9QYsiiY6bFpw",
    client_secret="DEOTHnpheAYiMjAEklkPmXYLT6141A",
    user_agent="prawtest")

def get_submissions(query, sub):
    subreddit = reddit.subreddit(f'{sub}')
    df = pd.DataFrame([vars(post) for post in subreddit.search(f'{query}', limit = None) ])
    df.to_csv(f'../data/praw_q={query}_sub={sub}.csv')

get_submissions('safety', 'delta8')
