import pandas as pd
import os
import praw
import requests
import json
import csv
import time
import datetime as dt
import praw
import psaw
import ntpath
from psaw import PushshiftAPI
import pmaw


def log_action(action):
    print(action)

### Global Variables ###
reddit = praw.Reddit(
    client_id="1chNuS_yxuVkA_qFKqFjsg",  # Personal Use Script - 14 characters
    client_secret="t728cM7ammQNSgQcQRvPxGM3ovTy-w",  # Secret key - 27 characters
    user_agent = "Antikythera22",  # App name
    username = 'Antikythera22',  # User name
    password = '#####'  # PW
)

api = PushshiftAPI()


subreddits = ['delta8', 'Drugs', 'trees', 'altcannabinoids', 'cleancarts', 'delta8testing']
basecorpus = r'C:\Users\19033\PycharmProjects\Analysis\Reddit_Analysis'
start_year = 2017
end_year = 2022

### BLOCK 1 ###

query = '"delta 8"|D8+"regulation"'

for year in range(start_year, end_year + 1):
    action = "[Year] " + str(year)
    log_action(action)

    dirpath = basecorpus + str(year)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    # timestamps that define window of posts
    ts_after = int(dt.datetime(year, 1, 1).timestamp())
    ts_before = int(dt.datetime(year + 1, 1, 1).timestamp())

    ### BLOCK 2 ###

    for subreddit in subreddits:
        start_time = time.time()

        action = "\t[Subreddit] " + subreddit
        log_action(action)

        subredditdirpath = dirpath + '/' + subreddit
        if os.path.exists(subredditdirpath):
            continue
        else:
            os.makedirs(subredditdirpath)

        submissions_csv_path = str(year) + '-' + subreddit + '-submissions.csv'

        ### BLOCK 3 ###

        submissions_dict = {
            "id": [],
            "url": [],
            "title": [],
            "score": [],
            "num_comments": [],
            "created_utc": [],
            "author": [],
            "permalink": [],
            "subreddit_id": [],
            "selftext": []
        }

        # submissions_dict["id"].append(submission_praw.id)
        # submissions_dict["url"].append(submission_praw.url)
        # submissions_dict["title"].append(submission_praw.title)
        # submissions_dict["score"].append(submission_praw.score)
        # submissions_dict["num_comments"].append(submission_praw.num_comments)
        # submissions_dict["created_utc"].append(submission_praw.created_utc)
        # submissions_dict["author"].append(submission_praw.author)
        # submissions_dict["permalink"].append(permalink.subreddit)
        # submissions_dict["subreddit_id"].append(submission_praw.subreddit_id)
        # submissions_dict["selftext"].append(submission_praw.selftext)

        ### BLOCK 4 ###

        # use PSAW only to get id of submissions in time interval
        gen = api.search_submissions(
            q=query,
            after=ts_after,
            before=ts_before,
            subreddit=subreddit,
            limit=100
        )

        ### BLOCK 5 ###

        # use PRAW to get actual info and traverse comment tree
        for submission_psaw in gen:
            # use psaw here
            submission_id = submission_psaw.d_['id']
            # use praw from now on
            submission_praw = reddit.submission(id=submission_id)

            submissions_dict["id"].append(submission_praw.id)
            submissions_dict["url"].append(submission_praw.url)
            submissions_dict["title"].append(submission_praw.title)
            submissions_dict["score"].append(submission_praw.score)
            submissions_dict["num_comments"].append(submission_praw.num_comments)
            submissions_dict["created_utc"].append(submission_praw.created_utc)
            submissions_dict["author"].append(submission_praw.author)
            submissions_dict["permalink"].append(submission_praw.permalink)
            submissions_dict["subreddit_id"].append(submission_praw.subreddit_id)
            submissions_dict["selftext"].append(submission_praw.selftext)




            ### BLOCK 6 ###

            submission_comments_csv_path = str(
                year) + '-' + subreddit + '-submission_' + submission_id + '-comments.csv'
            submission_comments_dict = {
                "author": [],
                "comment_id": [],
                "comment_parent_id": [],
                "comment_body": [],
                "comment_link_id": [],
                "created_utc": [],
                "is_submitter": [],
                "stickied": []
            }

            ### BLOCK 7 ###

            # extend the comment tree all the way
            submission_praw.comments.replace_more(limit=None)
            # for each comment in flattened comment tree
            for comment in submission_praw.comments.list():
                submission_comments_dict["author"].append(comment.author)
                submission_comments_dict["comment_id"].append(comment.id)
                submission_comments_dict["comment_parent_id"].append(comment.parent_id)
                submission_comments_dict["comment_body"].append(comment.body)
                submission_comments_dict["comment_link_id"].append(comment.link_id)
                # submission_comments_dict["retrieved_utc"].append(comment.retrieved_utc)
                submission_comments_dict["created_utc"].append(comment.created_utc)
                # submission_comments_dict["author_flair_type"].append(comment.author_flair_type)
                submission_comments_dict["is_submitter"].append(comment.is_submitter)
                submission_comments_dict["stickied"].append(comment.is_submitter)



            # for each submission save separate csv comment file
            pd.DataFrame(submission_comments_dict).to_csv(subredditdirpath + '/' + submission_comments_csv_path,
                                                          index=False)

        ### BLOCK 8 ###

        # single csv file with all submissions
        pd.DataFrame(submissions_dict).to_csv(subredditdirpath + '/' + submissions_csv_path,
                                              index=False)

        action = f"\t\t[Info] Found submissions: {pd.DataFrame(submissions_dict).shape[0]}"
        log_action(action)

        action = f"\t\t[Info] Elapsed time: {time.time() - start_time: .2f}s"
        log_action(action)
