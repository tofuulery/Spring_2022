import praw
import pandas as pd

reddit = praw.Reddit(client_id='lfhvscBzya8JROr7HybOGQ',
                     client_secret='HiY3yLrP45N6FVIUT0OrKuVFx7mqNA',
                     usernme='Antikythera22',
                     password='Nautilus265389',
                     user_agent='windows:scrapey:v1(by/u/Antikythera22)')

subreddit_list = ['delta8', 'altcannabinoids']

author_list = []
id_list = []
link_flair_text_list = []
num_comments_list = []
score_list = []
title_list = []
text_list = []
upvote_ratio_list = []
url_list = []
created_list = []
top_text_list = []

for subred in subreddit_list:

    subreddit = reddit.subreddit(subred)
    hot_post = subreddit.hot(limit=100)

    for sub in hot_post:
        author_list.append(sub.author)
        id_list.append(sub.id)
        link_flair_text_list.append(sub.link_flair_text)
        num_comments_list.append(sub.num_comments)
        score_list.append(sub.score)
        title_list.append(sub.title)
        try:
            text_list.append(sub.selftext)
        except ValueError:
            text_list.append(' ')
        upvote_ratio_list.append(sub.upvote_ratio)
        url_list.append(sub.permalink)
        created_list.append(sub.created_utc)


        for top_level_comment in sub.comments:
            top_text_list.append(top_level_comment.body)

print(top_text_list[0:1])

print(subred, 'completed; ', end='')

print('total', len(author_list), 'posts has been scraped')


df = pd.DataFrame({'ID': id_list,
                   'Author': author_list,
                   'Title': title_list,
                   'Text': text_list,
                   'Count_of_Comments': num_comments_list,
                   'Upvote_Count': score_list,
                   'Upvote_Ratio': upvote_ratio_list,
                   'Flair': link_flair_text_list,
                   'Permalink': url_list,
                   'Created': created_list
                   })

df2 = pd.DataFrame({'Top_Text': top_text_list})

df.to_csv('reddit_dataset_2.csv', index=False, encoding='utf-8')