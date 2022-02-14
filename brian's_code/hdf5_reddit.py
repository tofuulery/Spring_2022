import requests
import h5py
import datetime
from reddithelper import *
from tqdm import tqdm

def getPosts(query, before, after, sub, filename):
    url = f"https://api.pushshift.io/reddit/search/submission/?q={query}&before={before}&after={after}&subreddit={sub}"
    request = requests.get(url)
    json_response = request.json()
    now = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    data = [query, before, after, sub, now]
    with h5py.File(filename, 'w') as f:
        f.create_dataset('creation_data', data=data)
    return json_response

def postsToHDF5(json_object, filename):
    with h5py.File(filename, 'a') as f:
        dt = h5py.special_dtype(vlen=str)
        #####
        analysisgroup = f.create_group('analysis')

        #####
        for post in json_object['data']:
            if '/' in post['title']:
                post['title'] = post['title'].replace('/','*slash*')
            grp = f.create_group(post['title'])
            # selftext = grp.create_dataset('selftext', , data=post['selftext'], dtype=dt)
            for key in post.keys():
                if post[key] is list:
                    pass
                elif post[key] is dict:
                    pass
                else:
                    try:
                        grp.attrs[key] = post[key]
                    except Exception:
                        pass

def addComments(filename, limit):
    with h5py.File(filename, 'a') as f:
        for post in f:
            if post == 'analysis':
                pass
            if post == 'creation_data':
                pass
            try:
                link_id = f[post].attrs['id']
                url = f"https://api.pushshift.io/reddit/comment/search/?link_id={link_id}&limit={limit}"
                request = requests.get(url)
                json_response = request.json()
                for comment in tqdm(json_response['data'],leave=True):
                    dset = f[post].create_dataset(comment['id'], data='') ## change
                    for key in comment.keys():
                        if comment[key] is list:
                            pass
                        elif comment[key] is dict:
                            pass
                        else:
                            try:
                                dset.attrs[key] = comment[key]
                            except Exception:
                                pass
            except KeyError:
                print(post +'has no ID')




#%%
before = "1609480801"  # January 1 2021
after = "1577858401"  # January 1 2020
json_response= getPosts('delta8|d8|d8thc&saftey|safe|health', before, after, 'drugs', 'test2.hdf5')
postsToHDF5(json_response, 'test2.hdf5')
addComments('test2.hdf5',10)


#%%
