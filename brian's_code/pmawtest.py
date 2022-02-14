
from psaw import PushshiftAPI
import pandas as pd

api = PushshiftAPI()

def get_submissions(query, sub, after, before, limit):
    gen = api.search_submissions(query=query,subreddit=sub,after=after, before=before, limit=limit)
    df = pd.DataFrame([obj.d_ for obj in gen])
    # df = pd.DataFrame(gen)
    query2 = query.replace('|','_')
    df.to_csv('data/' + query + sub + '.csv')
    return df

before = "1609480801"  # January 1 2021
after = "1577858401"
limit = 1000
df = get_submissions('health','delta8', after, before, limit)
df




#%%
df.loc[df.title.str.contains('boof', case=False, na=False)]
