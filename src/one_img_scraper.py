# import library
from bs4 import BeautifulSoup
import requests
import shutil
import re
import os
from urllib.parse import quote

print("Hello! Welcome to Google Images Scraper 🌟\nCredit to https://github.com/bashirhanafi")
query = quote(input("Search: "))
url = f"https://www.google.com/search?q={query}&source=lnms&tbm=isch&#imgrc=q-EoOgh5uX8z3M"
print(url)

# requests url and parse html to img tag
response = requests.get(url)
resUrl = BeautifulSoup(response.text,"html.parser")
filter_url = resUrl.find_all("img", {"src":re.compile("https:")})

# source of images
src_image = []
for i, src in enumerate(filter_url):
  src_image.append(src.get('src'))
  print(f"Image {i} has been scraped")

print(src_image)

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