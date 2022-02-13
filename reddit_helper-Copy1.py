import praw
import pandas as pd
import os
import datetime as dt
import numpy as np


## C:\Users\19033\PycharmProjects\Analysis\Delta8_Reddit_Data

### RedditHelper ####

class reddithelper:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id="1chNuS_yxuVkA_qFKqFjsg",  # Personal Use Script - 14 characters
            client_secret="t728cM7ammQNSgQcQRvPxGM3ovTy-w",  # Secret key - 27 characters
            user_agent="Antikythera22",  # App name
            username='Antikythera22',  # User name
            password='Nautilus265389'  # PW
        )

    def grab_comments(self, postid, outfile):
        post = self.reddit.submission(postid)
        post.comments.replace_more(limit=None)
        comments = post.comments
        df_rows = [[comment.subreddit, comment.parent(), comment.id, comment.author, comment.is_submitter, comment.score, comment.created, comment.body] for
                   comment in comments.list()]
        df = pd.DataFrame(df_rows, columns=['Subreddit', 'Parent ID', 'Comment ID', 'Author', 'Submitter', 'Score', 'Created', 'Body'])

        df.to_csv(outfile)
        return df

    def appnd_datetime(self, d_taframe):
        df = d_taframe
        df['Timestamp'] = df.apply(lambda row: get_date(row.Created), axis=1)

    def get_hot_post_ids(self, subreddit, limit):
        subreddit = self.reddit.subreddit(subreddit)
        postids = []
        for post in subreddit.hot(limit=limit):
            postids.append(post.id)
        return postids

    def get_top_post_ids(self, subreddit, limit):
        subreddit = self.reddit.subreddit(subreddit)
        postids = []
        for post in subreddit.top(limit=limit):
            postids.append(post.id)
        return postids


### Convert UTC to 'human readable' time ###
def get_date(created):
    return dt.datetime.fromtimestamp(created)


### Subreddit Name ###
subreddit_name = 'delta8'
rh = reddithelper()

## top with a year/date/day ##


# ## HOT POSTS ###
hotposts = rh.get_hot_post_ids(subreddit_name, 5)  # args = subreddit, limit
[rh.grab_comments(i, f'{subreddit_name}hot_post_comments-{i}.csv') for i in hotposts]  # gets comments - etc.


### Top Posts ###
# topposts = rh.get_top_post_ids(subreddit, limit)
# topcomments = rh.grab_comments(i, f'{subreddit_name}top_post_comments-{i}.csv) for i in topposts] # get comments - etc.

# ### FROM CSV ###
# df = pd.read_csv(r'C:\Users\19033\PycharmProjects\Analysis\Delta8_Reddit_Data\query1.csv', encoding_errors='ignore')
# directory_path = r'C:\Users\19033\PycharmProjects\Analysis\Delta8_Reddit_Data\comment_files\ '
# for itter, post in enumerate(df['Post ID']):
#     try:
#         outfilepath = directory_path + str(post)
#         rh.grab_comments(post, outfilepath)
#         print(itter)
#     except Exception:
#         pass

# - - - - working - - - - #
# ## TOP POSTS ALL TIME ###
# top_posts_all = rh.get_hot_post_ids(subreddit_name, 50)  # args = subreddit, limit
# [rh.grab_comments(f'{i}{subreddit_name}_tpa', f'{subreddit_name}top_posts_all-{i}.csv') for i in top_posts_all]  # gets comments - etc.

"""
.hot, .new, .controversial, .top, and .gilded. You can also use .search("SEARCH_KEYWORDS") to get only results matching
an engine search.
"""
## DOCS ##
"""
https://praw.readthedocs.io/en/PRAW-1.0.9/praw.html#praw.objects.Subreddit.get_top_from_all
"""
