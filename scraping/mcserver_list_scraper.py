#dependencies
import httpx
from bs4 import BeautifulSoup

#Dict with addresses for each supported site, as well as if a CSS class is required for proper searching. Private member.
__addresses = {}
__addresses[0] = {'address': 'https://minecraft-server-list.com/', 'needs_css': True}
__addresses[1] = {'address': 'https://minecraftservers.org/', 'needs_css': False}
__addresses[2] = {'address': 'https://minecraft-server.net/', 'needs_css': False}


#Pulls server name from relevant place in HTML depending on site ID. Private function.
def __extract_server_name(site_id, row):
    if(site_id == 0):
        row_n2 = row.find('td', class_ = 'n2')
        server_name = row_n2.find('h2').get_text(strip = True)
    elif(site_id == 1):
        server_name = row.find(class_ = 'server-name').get_text(strip = True)
    else:
        server_name = row.find('h3').get_text(strip = True)
    
    return server_name

#Pull server description from relevant place in HTML depending on site ID. Private function.
def __extract_server_desc(site_id, row):
    if(site_id == 0):
        row_n2 = row.find('td', class_ = 'n2')
        server_description = row_n2.find('div', class_ = 'serverListing').get_text(strip = True)
    elif(site_id == 1):
        server_description = row.find('td', class_ = 'col-players').get_text(strip = True)
    else:
        server_description = row.find('p').get_text(strip = True)
    
    return server_description

#Pulls server IP from relevant place in HTML depending on site ID. Private function.
def __extract_server_ip(site_id, row):
    if(site_id == 0):
        row_n3 = row.find('td', class_ = 'n3')
        server_ip = row_n3.find('div', class_ = 'adressen online').get_text(strip = True)
    elif(site_id == 1):
        server_ip = row.find('p').get_text(strip = True)
    else:
        server_ip = row.find(class_ = 'col-12 form-control copy-ip-trigger').get('value')
    return server_ip

#Gets content from given address and gives back a collection of table rows. Private function.
def __collect_table_rows(site_address, needs_css):
    response = httpx.get(site_address)

    response_soup = BeautifulSoup(response.content, 'html.parser')

    servers_table = response_soup.find('tbody')

    if(needs_css):
        table_rows = servers_table.find_all('tr', class_ = True, recursive = False)
    else:
        table_rows = servers_table.find_all('tr', recursive = False)
    
    return table_rows

#Recieves a site ID, returns a dict with the scraped table info.
def extract_info(site_id):
    servers_dict = {}
    counter = 0
    target_site = __addresses[site_id]

    table_rows = __collect_table_rows(target_site['address'], target_site['needs_css'])

    #Iterate through each table row, pulling server name, descripiton, and IP from the relevant place depending on site ID
    for row in table_rows:

        #Get server name
        server_name = __extract_server_name(site_id, row)

        #Get server description
        server_description = __extract_server_desc(site_id, row)

        #Get server IP
        server_ip = __extract_server_ip(site_id, row)

        #Build dict with name, description, IP
        servers_dict[counter] = [server_name, server_description, server_ip]

        counter = counter + 1

    return servers_dict

#Returns the site address associated with the given ID.
def get_site_address(site_id):
    if(site_id < len(__addresses)):
        return __addresses[site_id]['address']
    else:
        return 'Invalid site ID'