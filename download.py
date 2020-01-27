import requests
from bs4 import BeautifulSoup

# Parameters
base_url = "https://www.fanfiction.net/s/"
id_fanfic = "6910226"

# Doing the request !
r = requests.get(base_url+id_fanfic)
soup = BeautifulSoup(r.text, features="html.parser")
print(soup.prettify())