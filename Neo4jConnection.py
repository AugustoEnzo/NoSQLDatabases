from neo4j import GraphDatabase, Driver


class Neo4JConnection:
    def __init__(self):
        self.URI = "neo4j://localhost:7687"
        self.AUTH = ("neo4j", "12345678")
        self.DATABASE = "neo4j"

    def create_driver(self) -> Driver:
        return GraphDatabase.driver(self.URI, auth=self.AUTH, database=self.DATABASE)
