__author__ = 'Donovan'
import feedparser
import PyRSS2Gen
from RSSFeed2Generator import FeedItem2RSSItem

orss = feedparser.parse("https://mojang.com/feed/")

for ix1 in orss.entries:
    print(ix1.description)
    print("")
    print("")

myfile = PyRSS2Gen.RSS2(
    title="my test",
    link="",
    description=orss.entries[0].description,
)

f1 = FeedItem2RSSItem()
for ix1 in orss.entries:
    r1 = f1.GetRSSItem(ix1)
    myfile.items.append(r1)

myfile.write_xml(open("myfile.xml", 'w'))
