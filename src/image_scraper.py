# import library
from bs4 import BeautifulSoup
import requests
import shutil
import re
import os
import pandas as pd
from urllib.parse import quote

print("Hello! Welcome to Google Images Scraper 🌟\nCredit to https://github.com/bashirhanafi\n------------------------------------------")
file_path = input("File path: ")
column = input("Please input the column: ")

df = pd.read_csv(f"../{file_path}")
df_array = df[f'{column}'].tolist()

# url
urls = []
src_image = []

for query in df_array:
    query = quote(query)
    url = f"https://www.google.com/search?q={query}&source=lnms&tbm=isch&#imgrc=q-EoOgh5uX8z3M"
    urls.append(url)

# requests url and parse html to img tag
for i, url in enumerate(urls):
    response = requests.get(url)
    resUrl = BeautifulSoup(response.text, "html.parser")
    filter_url = resUrl.find("img", {"src":re.compile("https:")})
    src_image.append(filter_url.get('src'))
    print(f"Image {i} has been scraped")

# dir
save_dir = '../output/'
# if dir doesn't exists
if not os.path.exists(save_dir):
    os.mkdir(save_dir)

# download and save images
for i, image_url in enumerate(src_image):
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        with open(os.path.join(save_dir, f'image_{i}.jpg'), 'wb') as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)
    else:
        print("Failed to request. Please check again your query.")

print(f"{len(src_image)} images has been downloaded and save to {save_dir}.")







