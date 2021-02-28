#dependencies
import httpx
from bs4 import BeautifulSoup
import pandas as pd

#Get server listing page
response = httpx.get('https://minecraft-server-list.com/')

#Convert to soup
response_soup = BeautifulSoup(response.content, 'html.parser')

servers_dict = {}
counter = 0

#Get servers table
servers_table = response_soup.find('tbody')

#Get collection of table rows. Must have CSS class to ignore banner ad rows.
table_rows = servers_table.find_all('tr', class_ = True, recursive = False)

#td class='n2' for server name & description
    #server name under h2 tag
    #server description under div class='serverListing' tag
#td class='n3' for IP
    #IP under div class='adressen online' tag

#Iterate through each table row in servers table
for row in table_rows:
    #Get n2 section
    row_n2 = row.find('td', class_ = 'n2')

    #Get server name from n2 section
    server_name = row_n2.find('h2').get_text()

    #Get server description from n2 section
    server_description = row_n2.find('div', class_ = 'serverListing').get_text()

    #Get n3 seciton
    row_n3 = row.find('td', class_ = 'n3')

    #Get server IP from n3 section
    server_ip = row_n3.find('div', class_ = 'adressen online').get_text()

    #Build dict with name, description, IP
    servers_dict[counter] = [server_name, server_description, server_ip]

    counter = counter + 1

#Convert dict to DataFrame
servers_frame = pd.DataFrame.from_dict(servers_dict, orient = 'index', columns = ['Name', 'Description', 'IP'])

#Convert DataFrame to CSV
print(servers_frame.to_csv())