import praw
import pandas as pd
import requests
import json

class reddithelper:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id="B9p-21QJHz9QYsiiY6bFpw",
            client_secret="DEOTHnpheAYiMjAEklkPmXYLT6141A",
            user_agent="prawtest"
        )
    def getPosts(self, query, before, after, sub):
        url = f"https://api.pushshift.io/reddit/search/submission/?q={query}&before={before}&after={after}&subreddit={sub}"
        request = requests.get(url)
        json_response = request.json()
        now = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        data = [query, before, after, sub, now]
        return json_response

    def posts_to_df(self, query, after, before, sub):
        submissions = self.getPosts(query, after, before, sub)['data']
        df_rows = df_rows = [[submission['id'], submission['title'], submission['score'], submission['created_utc'], submission['selftext']] for submission in submissions]
        df = pd.DataFrame(df_rows, columns=['ID', 'Title', 'Score', 'Created', 'Selftext'])
        df.to_csv(query+ after + before + sub +'.csv')
        return df

    def grab_comments(self, postid):
        post = self.reddit.submission(postid)
        post.comments.replace_more(limit=None)
        comments = post.comments
        df_rows = [[comment.parent(), comment.id, comment.score, comment.created, comment.body] for comment in comments.list()]
        df = pd.DataFrame(df_rows, columns=['Parent ID', 'Comment ID', 'Score', 'Created', 'Body'])
        df.to_csv(f'comments_{postid}.csv')
        return df

    def grab_comments_praw(self, postid):
        post = self.reddit.submission(postid)
        post.comments.replace_more(limit=None)
        comments = post.comments
        df = pd.DataFrame([vars(comment) for comment in comments])
        return df

    def get_hot_post_ids(self, subreddit, limit):
        subreddit = self.reddit.subreddit(subreddit)
        postids = []
        for post in subreddit.hot(limit = limit):
            postids.append(post.id)
        return postids

    def get_top_post_ids(self, subreddit, limit):
        subreddit = self.reddit.subreddit(subreddit)
        postids = []
        for post in subreddit.top(limit = limit):
            postids.append(post.id)
        return postids




# # #%%
# import datetime
# rh = reddithelper()
# before = "1609480801"  # January 1 2021
# after = "1577858401"
# posts = rh.posts_to_df('delta8&saftey', before, after, 'delta8')
#
# posts#
# # #%%
# rh.getPosts('delta8|saftey', start_epoch, None, 'drugs')
