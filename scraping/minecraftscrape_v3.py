#dependencies
import pandas as pd
import mcserver_list_scraper as list_scraper

frames = []
#Build DataFrame from extracted dicts from each site.
for count in range(0,2):
    frames.append(pd.DataFrame.from_dict(list_scraper.extract_info(count), orient = 'index', columns = ['Name', 'Description', 'IP']))

servers_frame = pd.concat(frames, ignore_index = True)

#Convert to CSV and output.
print(servers_frame.to_csv())