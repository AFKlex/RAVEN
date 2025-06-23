import re 
from src.Edge import *
from src.Node import * 


def import_crackmapexec(file_path):


    with open(file_path, "r") as file: 
        lines = file.read().splitlines()

    
    for line in lines: 
        parts = line.split()
        

        cred = match_cred(line)
        #print(cred)

        if cred is not None: 
            userID =  cred['Credential']
            create_domain(cred['Domain'],{"Name": cred['Domain']})
            create_user(refID=userID,props=cred)
            create_edge_domain_user(cred['Domain'],userID)

            
            break
            


    shares = match_share(lines)

    host_prop = {}
    port_prop = {}
    for share in shares: 
        
        permission = shares[share].pop('permission', None) 
        hostname = shares[share].pop('target_host_name',None)
        host = shares[share].pop('hostname',None)
        port = shares[share].pop('port',None)
        protocol = shares[share].pop('protocol', None)

        port_prop["port"] =port 
        port_prop["protocol"] =protocol        
        port_id = f"{hostname}/tcp/{port}"

        host_prop['hostname'] = host


        create_host(hostname,host_prop) 

        create_port(port_id, port_prop) 

        create_edge_host_port(hostname, port_id)

        create_share(share, shares[share])
        print(share)

        create_edge_port_share(port_id, share)

        if permission is not None: 
            create_edge_user_share(userID, share, permission) 

def match_share(all_lines):
    shares = {}
    share_enumeration_found = False
    counter = 2
    for line in all_lines: 
        if "[+] Enumerated shares" in line:
            share_enumeration_found = True 
            continue
        
        if share_enumeration_found and counter != 0: 
            # skip two not share lines that are in the display 
            counter = counter -1
            continue

        if share_enumeration_found: 

           pattern = r'^(\S+)\s+(\d{1,3}(?:\.\d{1,3}){3})\s+(\d+)\s+(\S+)\s+(\S+)(?:\s+(READ|WRITE|FULL|NONE))?\s+(.*)$'

                       
           match = re.match(pattern, line)
           if match:
                protocol, ip, port, hostname, share, permission, description = match.groups()
                if not permission:
                    permission = None


                shares[f"{ip}/{port}/{share}"] = {
                    "share": share,
                    "protocol": protocol,
                    "hostname": hostname,
                    "port": int(port),
                    "target_host_name": ip,
                    "permission": permission,
                    "description": description.strip()
                }
                continue


        if re.search(r'\[.\]',line ) and share_enumeration_found: 
            # Share enumeration add end: 
            return shares  

    return shares 

    
    
def match_cred(line):
    """
    Check if a Line is a credential if so return it as a dict. 
    """
    cred_data= {} 

    # Match credentials
    cred_match = re.search(r'\[\+\] ([^\\]+)\\([^:]+):(.+)', line)

    if cred_match is None: 
        return None 

    if cred_match:
        domain, user, password = cred_match.groups()
        cred_data["Domain"] = domain
        cred_data["User"] = user
        cred_data["Credential"] = f"{domain}\{user}"
        cred_data['password'] = password

    return cred_data


if __name__ == '__main__':
    load_crackmapexec("./data/crackmapexec")
