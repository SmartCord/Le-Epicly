from os import environ
from pymongo import MongoClient
import praw

reddit = praw.Reddit(
    client_id=environ.get('reddit_id'),
    client_secret=environ.get('reddit_secret'),
    user_agent=f'Overtimed 1.0 by /u/{environ.get("reddit_user")}'
)
