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
        NEO4J_PASS = "letmein1234"

        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))
                
        # {{ will result in { in the query
        # we need the query to be created before scince neo4j (GraphDatabase) does not allow the lable (node_type) to be set as a propertie in the query itself... 
        query = f"Merge (n:{self.node_type} {{ refID:'{self.unique_id}' }}) Set n += $properties"

        driver.execute_query(query, properties=self.properties)
        
        driver.close()




def create_host(refID, props= {}):
    new_node = Node(unique_id=refID, node_type="Host", properties=props)
    new_node.create_in_database()

def create_domain(refID, props= {}):
    new_node = Node(unique_id=refID, node_type="Domain", properties=props)
    new_node.create_in_database()

def create_port(refID, props= {}):
    new_node = Node(unique_id=refID, node_type="Port", properties=props)
    new_node.create_in_database()

def create_service(refID, props= {}):
    new_node = Node(unique_id=refID, node_type="Service", properties=props)
    new_node.create_in_database()

def create_share(refID, props= {}):
    new_node = Node(unique_id=refID, node_type="Share", properties=props)
    new_node.create_in_database()

def create_file(refID, props= {}):
    new_node = Node(unique_id=refID, node_type="File", properties=props)
    new_node.create_in_database()

def create_folder(refID, props= {}):
    new_node = Node(unique_id=refID, node_type="Folder", properties=props)
    new_node.create_in_database()

def create_vulnerability(refID, props= {}):
    new_node = Node(unique_id=refID, node_type="Vulnerability", properties=props)
    new_node.create_in_database()

def create_exploit(refID, props= {}):
    new_node = Node(unique_id=refID, node_type="Exploit", properties=props)
    new_node.create_in_database()

def create_user(refID, props= {}):
    new_node = Node(unique_id=refID, node_type="User", properties=props)
    new_node.create_in_database()

def create_group(refID, props= {}):
    new_node = Node(unique_id=refID, node_type="Group", properties=props)
    new_node.create_in_database()

def create_component(refID, props= {}):
    new_node = Node(unique_id=refID, node_type="Component", properties=props)
    new_node.create_in_database()
