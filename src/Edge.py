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
        

def create_edge_domain_user(domain, user):
    new_edge = Edge(domain, user, "HAS_USER")
    new_edge.create_in_database()

def create_edge_user_share(user, share, permission): 
    new_edge = Edge(user, share, f"{(permission).upper()}_ACCESS")
    new_edge.create_in_database()

def create_edge_host_port(host, port):
    new_edge = Edge(host, port, "HAS_PORT")
    new_edge.create_in_database()

def create_edge_port_share(port,share):
    new_edge = Edge(port, share, "EXPOSES_SHARE")
    new_edge.create_in_database()

        
