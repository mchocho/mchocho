import io
import random
import pathlib
import requests
import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen

random.seed(str(datetime.datetime.now()))
root = pathlib.Path(__file__).parent.resolve()

def ranInt(maxSize, minSize = 0):
  return (random.randint(minSize, maxSize))

def req(url):
  session = requests.Session()
  agent   = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36"
  headers = {
        "User-Agent": agent, 
        "Accept":     "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
  }
  html    = session.get(url, headers=headers).text
  bsObj   = BeautifulSoup(html, "html.parser")
  session.close()
  return (bsObj)

def fetchQOTD():
  base   = "https://www.brainyquote.com"
  page   = ranInt(10, 1)
  url    = base + "/topics/technology-quotes_" + str(page)
  bsObj  = req(url)
  quotes = bsObj.findAll("a", {"title": "view quote"})
  i      = ranInt(len(quotes) - 1)
  j      = 0

  if len(quotes) == 0:
      return (None)

  while len(quotes[i].text) > 110 and j <= 50:
    i  = ranInt(len(quotes))
    j += 1

  quote   = quotes[i]
  url     = base + quote.attrs["href"]
  return ([url, quote.text])

def fetchLatestFollower():
  url       = "https://github.com/mchocho?tab=followers"
  bsObj     = req(url)
  followers = bsObj.findAll("a", {"data-hovercard-type": "user"})
  follower  = followers[1].attrs["href"][1:]
  return (follower)

def updateREADME(readme):
  bsObj   = BeautifulSoup(readme, "html.parser")
  link    = bsObj.find("a", {"class": "follower"})
  quote   = fetchQOTD()
  latest  = fetchLatestFollower()
  current = link.text

  if latest != current:
    link.string        = latest 
    link.attrs["href"] = "https://github.com/" + latest

  if quote is not None: 
    blockq          = bsObj.find("blockquote")
    newQuote        = bsObj.new_tag("a", href=quote[0])
    newQuote.string = quote[1]
    blockq.clear()
    blockq.insert(0, newQuote)
  return (str(bsObj))

if __name__ == "__main__":
  path     = root / "README.md"
  with io.open(path, 'r', encoding="utf8") as f:
    readme = f.read()
  update = updateREADME(readme)
  with io.open(path, 'w', encoding="utf8") as f:
    f.write(update)
