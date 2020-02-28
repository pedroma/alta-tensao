from bs4 import BeautifulSoup
from podgen import Podcast, Episode, Media
import requests
import arrow
import re
import os
import boto3


base_href = "https://www.rtp.pt/"
base_url = "https://www.rtp.pt/play/p254/alta-tensao"

REGION = os.environ.get("DO_BUCKET_REGION", "fra1")
ACCESS_KEY = os.environ.get("DO_SPACE_KEY", "")
ACCESS_SECRET = os.environ.get("DO_SPACE_SECRET", "")
BUCKET_NAME = os.environ.get("DO_BUCKET_NAME", "")


content = requests.get(base_url).content

soup = BeautifulSoup(content, features="lxml")


urls_to_follow = []
for anchor in soup.select("#listProgramsContent a")[:10]:
    urls_to_follow.append(base_href + anchor.get("href"))


p = Podcast(
   name="Alta Tensão",
   description="Alta Tensão com António Freitas",
   image="https://cdn-images.rtp.pt/EPG/radio/imagens/1068_10159_53970.jpg",
   website=base_url,
   explicit=True,
)

episodes = []

for url in urls_to_follow:
    content = requests.get(url).content
    soup = BeautifulSoup(content, features="lxml")
    res = re.search(b'file : "(.+?)",\\n', content)
    title = soup.select("b.vod-title")[0].text
    date = soup.select(".vod-data p span.episode-date")[0].text
    media_url = res.groups()[0].decode()
    head = requests.head(url)
    episodes.append(
       Episode(
          title=soup.title.text,
          media=Media(media_url, head.headers["Content-Length"]),
          summary=title,
          publication_date=arrow.get(date, "DD MMM. YYYY", locale="pt").datetime
       )
   )


# Add some episodes
p.episodes = episodes
# Generate the RSS feed
rss = p.rss_str()

filename = "alta-tensao.xml"

with open(filename, "wb") as f:
   f.write(rss.encode())

session = boto3.session.Session()
client = session.client(
   's3',
   region_name=REGION,
   endpoint_url=f'https://{REGION}.digitaloceanspaces.com',
   aws_access_key_id=ACCESS_KEY,
   aws_secret_access_key=ACCESS_SECRET
)

client.upload_file(
   filename, BUCKET_NAME, filename, ExtraArgs={'ACL': 'public-read'}
)
