import requests
import beautifulsoup4

print("Hello !")
r = requests.get("https://www.fanfiction.net/s/6910226/1/Harry-Potter-et-les-M%C3%A9thodes-de-la-Rationalit%C3%A9")
print(r.text)