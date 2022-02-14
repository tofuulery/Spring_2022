
from psaw import PushshiftAPI
import pandas as pd

api = PushshiftAPI()

def get_submissions(query, sub, after, before, limit):
    gen = api.search_submissions(query=query,subreddit=sub,after=after, before=before, limit=limit)
    df = pd.DataFrame([obj.d_ for obj in gen])
    # df = pd.DataFrame(gen)
    df.to_csv(query + sub + '.csv')
    return df

before = "1609480801"  # January 1 2021
after = "1577858401"
limit = 10000
df = get_submissions('saftey','delta8', after, before, limit)

df.subreddit_id
#%%
df.loc[df.selftext.str.contains('boof', case=False, na=False)]
