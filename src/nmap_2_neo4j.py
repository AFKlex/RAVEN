import xml.etree.ElementTree as ET 
from src.Edge import Edge
from src.Node import * 


# ---- Functions ----

def create_host(ip,attributes): 
    refID = ip 

    new_node = Node(unique_id=ip, node_type="Host", properties=attributes)
    new_node.create_in_database()


def create_port(port_id, port_attributes) :
    """
    port, host_ip, protocol are used to uniquly identify the port node in the graph 
    """
 
    new_node = Node(unique_id=port_id, node_type="Port",properties=port_attributes)
    new_node.create_in_database()

def create_connection_between_port_host(host_id, port_id):

    new_Edge = Edge(host_id,port_id,"HAS_PORT")
    new_Edge.create_in_database()


def create_service(service_id,attributes):
    new_Service = Node(unique_id=service_id,node_type="Service", properties=attributes)
    new_Service.create_in_database()

def create_connection_betwen_port_service(port_id, service_id):
    new_Edge = Edge(port_id,service_id, "RUNS_SERVICE")
    new_Edge.create_in_database()

# ---- Main Import ----

def build_service_id(service_dict):
    parts = [service_dict.get("name", "")]
    if "product" in service_dict:
        parts.append(service_dict["product"])
    if "version" in service_dict:
        parts.append(service_dict["version"])
    if "extrainfo" in service_dict:
        parts.append(service_dict["extrainfo"])
    if "tunnel" in service_dict:
        parts.append(service_dict["tunnel"])
    return "|".join(parts)

def import_nmap_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    #print(root.tag)
    #print(root.attrib)
    
    print("--------------------")

    for host in root.findall("host"):
        status = host.find("status").attrib
        address = host.find("address").attrib
        port_list = host.find("ports").findall("port")
        
        host_ip =address["addr"]
        
        create_host(host_ip,status)

        for port in port_list: 
            port_state = port.find("state").attrib
            service_info = port.find("service").attrib
            port_info = port.attrib

            ## merga dicts: 
            port_info  = {**port_state, **port_info}

            service_id = build_service_id(service_info)
            create_service(service_id, service_info)
    

            protocol = port_info["protocol"]
            port = port_info["portid"]
            port_id = f"{host_ip}/{protocol}/{port}"

            
            create_port(port_id, port_info) 
            create_connection_between_port_host(host_ip, port_id)

            create_service(service_id, service_info) 
            create_connection_betwen_port_service(port_id,service_id)

        


    
# ---- Entry ----

if __name__ == "__main__":
    import_nmap_xml("./data/nmap.xml")

