import json
import os
import twitter

from twitter import ParseTweet
from Neo4jOperations import Neo4jOperations

# Constants
json_folder_path: str = os.path.join("JSONs")
json_files: list[str] = [x for x in os.listdir(json_folder_path) if x.endswith(".json")]
hashtags: dict[str, int] = dict()
neo4j_ops: Neo4jOperations = Neo4jOperations()
ru: int = 3987863

print(f"RU: {ru}")
print("Number of json files: {}".format(len(json_files)))

for json_filename in json_files:
    json_file_path: str = os.path.join(json_folder_path, json_filename)
    with open(json_file_path, "r") as f:
        json_file = json.load(f)
        for raw_tweet in json_file['data']:
            tweet: ParseTweet = twitter.ParseTweet(tweet=str(raw_tweet), timeline_owner=raw_tweet['author_id'])
            neo4j_ops.create_tweet(raw_tweet)

            for hashtag in tweet.Hashtags:
                neo4j_ops.create_hashtag(hashtag)
                neo4j_ops.create_hashtag_relation(tweet_id=raw_tweet['id'], hashtag=hashtag)

            for user in tweet.UserHandles:
                neo4j_ops.create_user(user)
                neo4j_ops.create_user_relations(tweet_id=raw_tweet['id'], user=user)

            print(f"{raw_tweet['id']} tweet was correctly inserted at database")
