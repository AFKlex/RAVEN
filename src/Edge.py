from src.Node import * 
from neo4j import GraphDatabase

class Edge:
    def __init__(self, unique_id_a:str, unique_id_b:Node, connection_type:str) -> None:
        
        
        self.unique_id_a= unique_id_a
        self.unique_id_b= unique_id_b
        self.connection_type = connection_type

    def create_in_database(self):
         # ---- Neo4j config ----
        NEO4J_URI = "bolt://localhost:7687"
        NEO4J_USER = "neo4j"
        NEO4J_PASS = "letmein1234"

        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))

        query = f"""
        Match (a) where a.refID = "{self.unique_id_a}"
        Match (b) where b.refID = "{self.unique_id_b}"
        Merge (a) - [:{self.connection_type}] -> (b)
        """
        #print(query)

        driver.execute_query(query) 

        driver.close()
        


