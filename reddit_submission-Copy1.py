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
from replace_query_symbols import replace_q_symbols


# logs the printout to a log file rather than printout in the terminal - an open text file :)
# log = open("reddit_submission_logFeb7.log", "a+")
# sys.stdout = log


def getPushshiftData(query, after, before, sub):
    # Search with specific subreddit parameters.
    url = 'https://api.pushshift.io/reddit/search/submission/?title=' + str(query) + f'&{size}=5&after=' + str(after) + '&before=' + str(before) + '&subreddit=' + str(sub)
    # search without specific subreddit parameter
    # url = 'https://api.pushshift.io/reddit/search/submission/?title=' + str(query) + '&size=1000&after=' + str(after) + \
    #       '&before=' + str(before)
    print(url)
    r = requests.get(url)
    data = json.loads(r.text)
    return data['data']


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
    created = dt.datetime.fromtimestamp(subm['created_utc'])  # 1520561700.0
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

def compile_description(txt_data, d_scription):
    text_data = txt_data
    desc_txt = d_scription
    current_date_time = dt.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
    complete_desc = f'Retrieved on: {current_date_time} + "\n" + {text_data} + "\n" + {desc_txt} '


def description_to_file(t_xtfilepath, txt_data, **kwargs):
    if kwarg.get('description_text'):
        desc_text = kwarg.get('description_text')
    else:
        desc_text = ''
    file_path = t_xtfilepath
    txt_metadata = txt_data
    descstring = description
    descr_text = f'Description/Note: {descstring}' + '\n'
    descriptiontxt = txt_metadata + '\n' + descr_text
    divider = str('-'*30) + '\n'
    # print(description)
    with open(file_path, 'a+', encoding='utf-8') as f:
        f.write(descriptiontxt)
    f.close()

def updateDescfile(txtfilepath, txtmetadata):
    txt_file = txtfilepath
    submissiondata = txtmetadata + '\n'
    divider = str('='*30) + '\n'
    with open(txt_file, 'a') as w:
        w.write(submissiondata)
        w.write(divider)
    w.close()


def get_date(t_mestamp):
    timestamp = int(t_mestamp)
    return dt.datetime.fromtimestamp(timestamp)



directory = r'C:/Users/19033/PycharmProjects/Analysis/Delta8_Reddit_Data/'
sub_list = ['delta8', 'Drugs', 'trees', 'altcannabinoids', 'cleancarts', 'delta8testing']
# sub_list = 'delta8'
# desc_text = input(f'Enter a description or note about the query and {sub_list} here: ')
desc_text = str("enter a description here" + '\n')
filename = 'y8y8y8y89.csv'
textfilename = csv2txtfile_namer(filename)

textfiledir = txtfile_dir_maker(textfilename, directory)
txtfilepath = textfiledir + textfilename
before = "1609480801"  # January 1 2021 UNIX timestamp for before/after posts
after = "1577858401"  # January 1 2020

g_before = get_date(before)
g_after = get_date(after)
# query = r'(D8|delta8|"delta-8"|delta8|"delta 8"|"Delta-8"|d8|"Delta 8")+(safety|quality|"lab reports"|legit|safe|clean|trust)'
query = r'delta8'
query_text = replace_q_symbols(query)
q_metadata = f'CSV File: {filename}' + '\n' + f'Subreddits: {str(sub_list)}' + '\n' + f'Before: {g_before}' + '\n' + f'After: {g_after}' + '\n' + f'Query: + {query_text}'

description_to_file(txtfilepath, q_metadata, description_text=desc_text)  # writes text metadata for whole query (e.g., multiple subreddits) to .txt file, longer description text in **kwarg - otherwise description_text=None


for element in sub_list:
    sub = element
    before = before
    after = after
    query = query
    submissionCount = 0
    subStats = {}
    size = 50
    data = getPushshiftData(query, after, before, sub)  # collect the data
    text_metadata2 = f'CSV File: {filename}' + '\n' + f'Subreddit: {str(sub)}' + '\n' + f'Before: {g_before}' + '\n' + f'After: {g_after}' + '\n' + f'Query: {query_text}'
    data_counter = 0
    while len(data) > data_counter:
        for submission in data:
            collectSubData(submission)
            submissionCount += 1
            # Calls getPushshiftData() with the created date of the last submission
            print(f'Gathering {len(data)} submissions.')
            # print(str(datetime.datetime.fromtimestamp(data[-1]['created_utc'])))
            # after = data[-1]['created_utc']
            data = getPushshiftData(query, after, before, sub)
            submission_description = compile_description(text_metadata2, )
            # after = data[-1]['created_utc']
            print(str(len(subStats)) + " submissions have added to list")
            # updateSubs_file(subStats, filename)
            updateDesc_file(txtfilepath, text_metadata)
            data_counter += 1


    # first_entry = str(list(subStats.values())[0][0][1])
    # last_entry =  str(list(subStats.values())[-1][0][1])
    # sample_string = f'1st entry is: {first_entry}' + '\n' +  + {last_entry} + '\n'
    # updateDesc_file(txtfilepath, text_metadata2)
