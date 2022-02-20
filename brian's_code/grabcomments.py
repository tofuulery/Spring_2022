from reddithelper import reddithelper
import os
import pandas as pd
from tqdm import tqdm
rh = reddithelper()


def reorder_columns(dataframe, col_name, position):
    """Reorder a dataframe's column.
    Args:
        dataframe (pd.DataFrame): dataframe to use
        col_name (string): column name to move
        position (0-indexed position): where to relocate column to
    Returns:
        pd.DataFrame: re-assigned dataframe
    """
    temp_col = dataframe[col_name]
    dataframe = dataframe.drop(columns=[col_name])
    dataframe.insert(loc=position, column=col_name, value=temp_col)
    return dataframe

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
                    columns_list = ['id', 'author', 'title', 'body', 'created','author_flair_text', 'link_flair_text']
                    for i,j in enumerate(columns_list):
                        df = reorder_columns(dataframe=df, col_name= j, position=i)
                        print('csv created')
                    df_post.to_csv('comments_'+file.strip('.csv') + '/' + id + '.csv')
                except AttributeError:
                    pass
