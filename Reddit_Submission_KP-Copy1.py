import pandas as pd
import requests
import json
import csv
import time
import datetime
import os
import ntpath
import sys
import datetime as dt


# logs the printout to a log file rather than printout in the terminal - an open text file :)
# log = open("reddit_submission_logFeb7.log", "a+")
# sys.stdout = log


def getPushshiftData(query, after, before, sub):
    # Search with specific subreddit parameters.
    url = 'https://api.pushshift.io/reddit/search/submission/?title=' + str(query) + '&size=100&after=' + str(after) + '&before=' + str(before) + '&subreddit=' + str(sub)
    # search without specific subreddit parameter
    # url = 'https://api.pushshift.io/reddit/search/submission/?title=' + str(query) + '&size=1000&after=' + str(after) + \
    #       '&before=' + str(before)
    print(url)
    response = requests.get(url)
    try:
        data = json.loads(response.text)
        return data['data']
    except ValueError:
        print(ValueError)



# This website is good for creating timestamps that are compatible for this task:
# https://www.unixtimestamp.com/index.php


def collectSubData(subm):
    subData = []  # list to store data points
    title = subm['title']
    subreddit = subm['subreddit']
    subreddit_id = subm['subreddit_id']
    # post_hint = subm['post_hint']
    url = subm['url']
    try:
        flairtxt = subm['link_flair_text']
    except KeyError:
        flairtxt = "NaN"
    author = subm['author']  # username of redditor
    sub_id = subm['id']  # submission (post) ID
    score = subm['score']  # upvote count?

    try:
        text = subm['selftext']
    except KeyError:
        text = "NaN"
    created = datetime.datetime.fromtimestamp(subm['created_utc'])  # 1520561700.0
    numComms = subm['num_comments']
    postlink = subm['full_link']
    retrieved_on = subm['retrieved_on']

    subData.append((sub_id, subreddit, subreddit_id, title, url, author, score, text, created, retrieved_on, numComms, postlink, flairtxt))
    subStats[sub_id] = subData



def updateSubs_file(stats, filename):
    upload_count = 0
    subStats = stats
    file_name = filename
    location = r'C:/Users/19033/PycharmProjects/Analysis/Delta8_Reddit_Data/' ##DIRECTORY TO STORE CSV OUTPUT FILES AND DESCRIPTION FILES##
    # print("Input filename of submission file, please add .csv")
    # filename = input()
    csvfilepath = location + file_name
    a = open(csvfilepath, 'a+', newline='')
    headers = ["Post ID", "Subreddit", "Subreddit ID", "Title", "Content Link", "Author", "Score", "Text", "Publish Date", "Retrieved On",
               "Total No. of Comments", "URL", "Flair"]
    with a:
        writer = csv.writer(a)
        writer.writerow(headers)
        for sub in subStats:
            try:
                writer.writerow(subStats[sub][0])
                upload_count += 1
            except ValueError:
                continue
        print(str(upload_count) + " submissions have been uploaded")
    a.close()
    # return textfilepath


def csv2txtfile_namer(f_lename):
    txtfilename = str(ntpath.basename(f_lename)).replace('.csv', '.txt')
    return txtfilename


def txtfile_dir_maker(textfilename, csvfiledir):
    foldername = textfilename.replace('.txt', '_about_files/')
    textfiledir = csvfiledir + foldername
    if os.path.exists(textfiledir):
        return textfiledir
    if not os.path.exists(textfiledir):
        os.makedirs(textfiledir)
    return textfiledir


def description_to_file(t_xtfilepath, txt_data, description):
    file_path = t_xtfilepath
    txt_metadata = txt_data
    descstring = description
    descr_text = f'Description/Note: {descstring}' + '\n'
    descriptiontxt = txt_metadata + '\n' + '\n' + descr_text
    # print(description)
    with open(file_path, 'a+', encoding='utf-8') as f:
        f.write(descriptiontxt)
    f.close()

def updateDescfile(txtfilepath, txtmetadata):
    txt_file = txtfilepath
    metadata = txtmetadata
    with open(txt_file, 'a') as w:
        w.write(metadata)
    w.close()


def get_date(t_mestamp):
    timestamp = (time.mktime(t_mestamp.timetuple())*1000)
    return timestamp

directory = r'C:/Users/19033/PycharmProjects/Analysis/Delta8_Reddit_Data/'

## QUERY 1
# query = r'delta-8"|d8|"Delta 8"+safety|quality|"lab reports"|legit|safe|clean|trust'
query = r'safety'
desc_text = str("Some combination of term/slang for delta-8 AND any of the words in the second bracket from main delta-8 mentioning subreddits (sub_list)")
filename = 'Query1_Posts.csv'
sub_list = ['delta8', 'Drugs', 'trees', 'altcannabinoids', 'cleancarts', 'delta8testing']

# ## QUERY 2
# # query = r'(D8|delta8|"delta-8"|delta8|"delta 8"|"Delta-8"|d8|"Delta 8")+("boof carts"|boof|dirty|sketch)'
# desc_text = str("enter a description here")
# filename = 'y8y8y8y89.csv'
# sub_list = ['delta8', 'Drugs', 'trees', 'altcannabinoids', 'cleancarts', 'delta8testing']
#
# ## QUERY 3 ###
# # query = r'(D8|delta8|"delta-8"|delta8|"delta 8"|"Delta-8"|d8|"Delta 8")+(vendor|supplier|manufacturer|shop|store|"gas station"|"head shops")+(report|lab|regulate|unregulated|safe|health)'
# desc_text = str("enter a description here")
# filename = 'y8y8y8y89.csv'
# sub_list = ['delta8', 'Drugs', 'trees', 'altcannabinoids', 'cleancarts', 'delta8testing']


# sub_list = 'delta8'
# desc_text = input(f'Enter a description or note about the query and {sub_list} here: ')


textfilename = csv2txtfile_namer(filename)

textfiledir = txtfile_dir_maker(textfilename, directory)

txtfilepath = textfiledir + textfilename

# before = datetime.date(2021, 02, 06)  # Feb 6 2021 UNIX timestamp for before/after posts

before = dt.datetime.now()  # makes 'now' timestamp
after = dt.date(2017, 1, 1)

# import datetime as dt
# before = int(dt.datetime(2021,2,1,0,0).timestamp())
# after = int(dt.datetime(2020,12,1,0,0).timestamp())

g_before = get_date(before)  # A hooman time stamp.
g_after = get_date(after)

text_metadata = f'CSV File: {filename}' + '\n' + f'Subreddits: {str(sub_list)}' + '\n' + f'Before: {g_before}' + '\n' + f'After: {g_after}' + '\n' + f'Query: + {query}'

description_to_file(txtfilepath, text_metadata, desc_text)  # writes description and text metadata for each
                                                            # search/subreddits list to an associated textfile


for element in sub_list:
    sub = element
    before = before
    after = after
    query = query
    subCount = 0
    subStats = {}
    data = getPushshiftData(query, after, before, sub)  # collect the data
    text_metadata2 = f'CSV File: {filename}' + '\n' + f'Subreddits: {str(sub_list)}' + '\n' + f'Before: {g_before}' + '\n' + f'After: {g_after}' + '\n' + f'Query: + {query}'
    data_counter = 0
    while len(data) > data_counter:
        for submission in data:
            collectSubData(submission)
            subCount += 1
            data_counter += 1
            # Calls getPushshiftData() with the created date of the last submission
            print(f'Gathering {len(data)} submissions.')
            # print(str(datetime.datetime.fromtimestamp(data[-1]['created_utc'])))
            # after = data[-1]['created_utc']
            data = getPushshiftData(query, after, before, sub)
            # after = data[-1]['created_utc']
            print(str(len(subStats)) + " submissions have added to list")
            updateSubs_file(subStats, filename)





    # first_entry = str(list(subStats.values())[0][0][1])
    # last_entry =  str(list(subStats.values())[-1][0][1])
    # sample_string = f'1st entry is: {first_entry}' + '\n' + 'Created: ' + {last_entry} + '\n'
    # updateDesc_file(txtfilepath, text_metadata2)

