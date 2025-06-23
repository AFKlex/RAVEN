
from src.crackmapexec_2_neo4j import import_crackmapexec
from src.nmap_2_neo4j import * 
from src.Edge import *
from src.Node import * 
import click 
from click_shell import shell


@shell(prompt='RAVEN >', intro='Starting into RAVEN Shell')
def raven_shell():
    pass

@raven_shell.command()
@click.option('--file_path', default="./data/nmap.xml", help="Provide the File Path to the XML Scan results of NMAP.")
def load_nmap(file_path):
    """
    filePath: provide the filePath to the XML Scan result of nmap. 
    """

    import_nmap_xml(file_path)
    
@raven_shell.command()
@click.option('--file_path', default="./data/crackmapexec", help="Provide the File Path to the XML Scan results of NMAP.")
def load_crackmapexec(file_path):
    """
    filePath: provide the filePath to the Scan result of nmap. 
    """
    import_crackmapexec(file_path)


if __name__ == '__main__':
    raven_shell()

#import_nmap_xml("./data/nmap.xml")
#import_nmap_xml("./data/nmap2.xml")

