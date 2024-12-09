import praw
from praw import Reddit
import sys
from utils.constants import POST_FIELDS
import pandas as pd
import numpy as np

def connect_reddit(client_id, client_secret, user_agent):
    try:
        reddit = praw.Reddit(client_id = client_id, client_secret = client_secret, user_agent = user_agent)
        print('Connected!')
        return reddit
    except Exception as e:
        print(e)
        sys.exit(1)

def extract_posts(instance, subreddit, time_filter, limit = None):
    subreddit = instance.subreddit(subreddit)
    posts = subreddit.top(time_filter = time_filter, limit = limit)

    posts_list = []

    for post in posts:
        post_dict = vars(post)
        post = {key : post_dict[key] for key in POST_FIELDS}
        posts_list.append(post)

    return posts_list

def transform_data(post_df):
    post_df['created_utc'] = pd.to_datetime(post_df['created_utc'], unit='s')
    post_df['over_18'] = np.where((post_df['over_18'] == True), True, False)
    post_df['author'] = post_df['author'].astype(str)
    edited_mode = post_df['edited'].mode()
    post_df['edited'] = np.where(post_df['edited'].isin([True, False]),
                                 post_df['edited'], edited_mode).astype(bool)
    post_df['num_comments'] = post_df['num_comments'].astype(int)
    post_df['score'] = post_df['score'].astype(int)
    post_df['title'] = post_df['title'].astype(str)

    return post_df

def load_data_to_csv(data, path):
    data.to_csv(path, index=False)