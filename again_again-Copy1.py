# In order to get make requests to get the data
import requests
import json

# To work with the data we are going to store it in a dataframe
import pandas as pd
import numpy as np
from datetime import datetime
import time

# Visualization
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter


# Lets build the url which we will send requests to in order to get posts within a certain timeframe.

# For the sake of this project, we are interested in the top posts, but you can also change the 'sort_type' to
# get posts based on the time they were created ('created_utc'), the number of comments the submission has ('num_comments'),
# or mumber of upvotes
def get_pushshift_data(term, start, end, subreddit, num_posts, score_threshold):
    # Limit the data fields we get back. We don't need everything!
    # It'd be useful to collect the flair as a potential y for machine learning predictions we do later
    f = ('created_utc,' +
         'full_link,' +
         'num_comments,' +
         'score,' +
         'subreddit,' +
         'title,' +
         'link_flair_text' +
         'selftext'
         )

    # Build the url which will send the data we are looking for
    url = ('https://api.pushshift.io/reddit/search/submission?' +
           'title=' + str(term) +
           '&after=' + str(start) +
           '&before=' + str(end) +
           '&size=' + str(num_posts) +
           '&fields=' + f +
           '&score=<' + str(score_threshold) +
           '&sort_type=score' +
           '&subreddit=' + str(subreddit))
    # We are ensuring we are getting the highest posts with sort

    # Get the data, sleep so the successive calls do not trigger a 429 response
    time.sleep(1)
    r = requests.get(url)

    # Convert the request into a list of dict objects
    d = json.loads(r.text)

    # Return a list of dictionaries for the submissions
    return d['data']


# Lets test it by getting three posts from the world news subreddit in the year 2020 that contains Trump
ex = get_pushshift_data('Trump', '2020-01-01', '2020-12-31', 'worldnews', 3, 1000000)

print(ex)