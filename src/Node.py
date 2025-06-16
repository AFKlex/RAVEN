from neo4j import GraphDatabase

class Node:
    def __init__(self,  unique_id:str, node_type:str, properties:dict ={} ) -> None:
        """
        unique_id: a string that is unique through the graph datbasa string that is unique through the graph datbasee
        properties: dict requires a flat structure {a:b,b:c} not {a:{b:c}}

        """
        self.unique_id = unique_id
        self.node_type = node_type
        self.properties = properties

    def create_in_database(self):
        # ---- Neo4j config ----
        NEO4J_URI = "bolt://localhost:7687"
        NEO4J_USER = "neo4j"
        NEO4J_PASS = "letmein"

        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))
                
        # {{ will result in { in the query
        # we need the query to be created before scince neo4j (GraphDatabase) does not allow the lable (node_type) to be set as a propertie in the query itself... 
        query = f"Merge (n:{self.node_type} {{ refID:'{self.unique_id}' }}) Set n += $properties"

        driver.execute_query(query, properties=self.properties)
        
        driver.close()
