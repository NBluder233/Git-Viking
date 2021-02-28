#dependencies
import httpx
from bs4 import BeautifulSoup
import pandas as pd

#Pulls server name from relevant place depending on site ID
def extract_server_name(site_id, row):
    if(site_id == 0):
        row_n2 = row.find('td', class_ = 'n2')
        server_name = row_n2.find('h2').get_text(strip = True)
    elif(site_id == 1):
        server_name = row.find(class_ = 'server-name').get_text(strip = True)
    else:
        server_name = row.find('h3').get_text(strip = True)
    
    return server_name

#Pull server description from relevant place depending on site ID
def extract_server_desc(site_id, row):
    if(site_id == 0):
        row_n2 = row.find('td', class_ = 'n2')
        server_description = row_n2.find('div', class_ = 'serverListing').get_text(strip = True)
    elif(site_id == 1):
        server_description = row.find('td', class_ = 'col-players').get_text(strip = True)
    else:
        server_description = row.find('p').get_text(strip = True)
    
    return server_description

#Pulls server IP from relevant place depending on site ID
def extract_server_ip(site_id, row):
    if(site_id == 0):
        row_n3 = row.find('td', class_ = 'n3')
        server_ip = row_n3.find('div', class_ = 'adressen online').get_text(strip = True)
    elif(site_id == 1):
        server_ip = row.find('p').get_text(strip = True)
    else:
        server_ip = row.find(class_ = 'col-12 form-control copy-ip-trigger').get('value')
    return server_ip

#Recieves a table and site ID, builds dict with relevant info
def extract_info(site_id, table_rows):
    servers_dict = {}
    counter = 0

    #Iterate through each table row, pulling server name, descripiton, and IP from the relevant place depending on site ID
    for row in table_rows:

        #Get server name
        server_name = extract_server_name(site_id, row)

        #Get server description
        server_description = extract_server_desc(site_id, row)

        #Get server IP
        server_ip = extract_server_ip(site_id, row)

        #Build dict with name, description, IP
        servers_dict[counter] = [server_name, server_description, server_ip]

        counter = counter + 1

    return servers_dict

#Gets content from given address and gives back a collection of table rows
def collect_table_rows(site_address, needs_css):
    response = httpx.get(site_address)

    response_soup = BeautifulSoup(response.content, 'html.parser')

    servers_table = response_soup.find('tbody')

    if(needs_css):
        table_rows = servers_table.find_all('tr', class_ = True, recursive = False)
    else:
        table_rows = servers_table.find_all('tr', recursive = False)
    
    return table_rows

#Get servers table from each site
tables_dict = {}
##Site # 1
tables_dict[0] = collect_table_rows('https://minecraft-server-list.com/', True)

##Site #2
tables_dict[1] = collect_table_rows('https://minecraftservers.org/', False)

##Site #3
tables_dict[2] = collect_table_rows('https://minecraft-server.net/', False)

frames = []
#Build DataFrame from extracted dicts from each site
for count in range(0,2):
    frames.append(pd.DataFrame.from_dict(extract_info(count, tables_dict[count]), orient = 'index', columns = ['Name', 'Description', 'IP']))

servers_frame_final = pd.concat(frames, ignore_index = True)

#Convert to JSON and output
print(servers_frame_final.to_json())