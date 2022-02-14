from typing import TextIO
import pandas as pd
import csv
from pmaw import PushshiftAPI
import praw
import datetime as dt

reddit = praw.Reddit(
    client_id="1chNuS_yxuVkA_qFKqFjsg",  # Personal Use Script - 14 characters
    client_secret="t728cM7ammQNSgQcQRvPxGM3ovTy-w",  # Secret key - 27 characters
    user_agent="my user agent",  # App name
    username='redditor',
    password='redditorpw',
)

# directory = r'C:\Users\19033\PycharmProjects\Analysis\Delta8_Reddit_Data\'
# filename = 'q1_a.csv'
# outfiledir = directory + filename


query = 'regulation|report|analysis|laboratory|clean)+regulate|regulation'
query_num = 'd8_safety'
api = PushshiftAPI()

api = PushshiftAPI()
start_epoch = int(dt.datetime(2020, 1, 1).timestamp())

gen = api.search_submissions(q=query, after=start_epoch, subreddit='delta8', limit=3)

# print(gen)
df = pd.DataFrame(gen)

print(df)
df.to_csv('df_test_02.11.csv', encoding_errors=ignore)
# outcsv = f'{query_num}.csv'
#
# df.to_csv(outcsv, encoding='utf-8', index=False)
#
# with open('q1_a.txt', 'a+') as a:
#     a.write(query + ' altcannabinoids ' + (dt.fromtimestamp(start_epoch).strftime('%YYYY-%mm-%dd')))


# submissions = api.search_submissions(subreddit="wallstreetbets", limit=30, filter=['selftext'])
#
# print(submissions)
#
# df = pd.DataFrame(submissions)
#
# print(df)
#
# df.to_csv('dataframe_test.csv', sep=",")

# with open('submissions_list.csv', 'w') as outfile:
#     writer = csv.DictWriter(outfile, fieldnames=headers)
#     blank = ''
#     for item in submissions_list:
#         for element in item.values():
#             try:
#                 writer.writerow(item)
#             except ValueError:
#                 writer.writewrow(blank)
# outfile.close()
