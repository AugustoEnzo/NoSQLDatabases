import logging

from neo4j import Driver
from neo4j.exceptions import DriverError, Neo4jError
from Neo4jConnection import Neo4JConnection


class Neo4jOperations:
    def __init__(self):
        self.driver: Driver = Neo4JConnection().create_driver()

    def close(self):
        self.driver.close()

    def format_hashtag_string(self, hashtag_string: str) -> str:
        hashtag_string = hashtag_string.lower()
        hashtag_string = hashtag_string.replace("-", str())
        hashtag_string = hashtag_string.replace("_", str())
        hashtag_string = hashtag_string.replace("\n", str())
        hashtag_string = hashtag_string.replace("@", str())
        hashtag_string = hashtag_string.strip()

        return hashtag_string

    def create_hashtag(self, hashtag: str):
        ru: int = 3987863
        query = (
            "MERGE ( hs1:Hashtag { value: $hashtag_value } ) "
            "RETURN $hashtag_value"
        )

        try:
            record = self.driver.execute_query(
                query,
                hashtag_value=self.format_hashtag_string(hashtag),
                result_transformer_=lambda r: r.single(strict=True)
            )

            return record
        except (DriverError, Neo4jError) as exception:
            logging.error('%s raised an error: \n%s', query, exception)
            raise

    def create_tweet(self, raw_tweet):
        ru: int = 3987863
        query = (
            "MERGE (tw: Tweet {id: $id, text: $text, source: $source, author_id: $author_id, created_at: "
            "$created_at})"
            "RETURN tw"
        )

        try:
            record = self.driver.execute_query(
                query,
                id=raw_tweet['id'],
                text=raw_tweet['text'],
                source=raw_tweet['source'],
                author_id=raw_tweet['author_id'],
                created_at=raw_tweet['created_at'],
                result_transformer_=lambda r: r.single(strict=True)
            )

            return record
        except (DriverError, Neo4jError) as exception:
            logging.error('%s raised an error: \n%s', query, exception)
            raise

    def create_user(self, user):
        ru: int = 3987863
        query = (
            "MERGE ( us1: User { value: $user_value } )"
            "RETURN us1"
        )

        try:
            record = self.driver.execute_query(
                query,
                user_value=self.format_hashtag_string(user),
                result_transformer_=lambda r: r.single(strict=True)
            )

            return record
        except (DriverError, Neo4jError) as exception:
            logging.error('%s raised an error: \n%s', query, exception)
            raise

    def create_hashtag_relation(self, tweet_id, hashtag):
        ru: int = 3987863
        query = (
            "MATCH (tw:Tweet), (hs:Hashtag)"
            "WHERE tw.id = $tweet_id_value"
            "  AND hs.value = $hashtag_value\n"
            "CREATE (tw)-[r:USED]->(hs)"
            "RETURN r"
        )

        try:
            record = self.driver.execute_query(
                query,
                tweet_id_value=tweet_id,
                hashtag_value=self.format_hashtag_string(hashtag)
            )

            return record
        except (DriverError, Neo4jError) as exception:
            logging.error('%s raised an error: \n%s', query, exception)
            raise

    def create_user_relations(self, tweet_id, user):
        ru: int = 3987863
        query = (
            "MATCH (tw:Tweet), (us:User)"
            "WHERE tw.id = $tweet_id_value"
            "  AND us.value = $user_value\n"
            "CREATE (tw)-[r:NAMED]->(us)"
            "RETURN r"
        )

        try:
            record = self.driver.execute_query(
                query,
                tweet_id_value=tweet_id,
                user_value=self.format_hashtag_string(user)
            )

            return record
        except (DriverError, Neo4jError) as exception:
            logging.error('%s raised an error: \n%s', query, exception)
            raise
