import requests
import pandas as pd



headers = {
    "User-Agent": "Chrome/97.0.4692.99 Safari/537.36 LikeWise/100.6.1135.36"}

subreddit = 'delta8'


def get_comments(subreddit, limit=100):
    res = requests.get("https://www.reddit.com/r/%s/comments.json?limit=%d" %
                    (subreddit, limit), headers=headers)

    comments = res.json()["data"]["children"]

    df = pd.DataFrame(comments)
    data = df['data']
    print(data)
    outfiledir = r'C:\Users\19033\PycharmProjects\Analysis\df_testing\\'
    outfilename = 'reddit_requestspydftest1.csv'
    outfilepath = outfiledir + outfilename
    # data.to_csv(outfilepath, encoding='utf-8', errors='ignore')

    print(data.keys())

    for i in data:
        id = i.get('id')
        body = i.get('body')
        created = i.get('created_utc')
        author = i.get('author')
        shared_link = i.get('url')
        parent = i.get('parent')
        print(created)
        print(id)
        print(body)
        print(author)
        print(shared_link)
        print(parent)
        print('='*30)
        print()

    # print(comments)
    for c in comments:
        comment = c["data"]
        # print(comment.keys())
        print("Subreddit: " + comment['display_name'])
        try:
            print("Link: " + comment['submit_link_label'])
        except TypeError:
            print("Link: None")
        print("Permalink: " + comment['url'])
        print("Body: " + comment['submit_text'])
        try:
            print("Is OP?: " + comment['user_is_contributor'])
        except TypeError:
            print("Is OP?: False")
        print("Subreddit ID: " + comment['name'])
        print("=" * 30)


if __name__ == "__main__":
    get_comments("delta-8")