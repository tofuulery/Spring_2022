from reddithelper import reddithelper
import os
import pandas as pd
from tqdm import tqdm
rh = reddithelper()


datapath = '../data'
os.chdir(datapath)
files = [f for f in os.listdir('.') if os.path.isfile(f)]
for file in files:
    if 'praw' in file:
        df = pd.read_csv(file)
        if os.path.isdir('comments_'+str(file.strip('.csv'))):
            pass
        else:
            os.mkdir('comments_'+str(file.strip('.csv')))
            # os.chdir('comments_'+str(file.strip('.csv')))
            for id in tqdm(df.id, desc=f'{id}'):
                try:
                    df_post = rh.grab_comments_praw(id)
                    df_post.to_csv('comments_'+file.strip('.csv') + '/' + id + '.csv')
                except AttributeError:
                    pass
