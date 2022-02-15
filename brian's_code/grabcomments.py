from reddithelper import reddithelper
import os
import pandas as pd
from tqdm import tqdm
rh = reddithelper()


datapath = '../data'
os.chdir(datapath)

for file in os.listdir(datapath):
    if 'praw' in file:
        df = pd.read_csv(file)
        os.mkdir('comments_'+str(file.strip('.csv')))
        # os.chdir('comments_'+str(file.strip('.csv')))
        for id in tqdm(df.id):
            try:
                df_post = rh.grab_comments_praw(id)
                df_post.to_csv('comments_'+file.strip('.csv') + '/' + id + '.csv')
            except AttributeError:
                pass
