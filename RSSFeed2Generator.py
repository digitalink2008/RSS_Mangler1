__author__ = 'Donovan'
import feedparser
import PyRSS2Gen


# Custom class to convert feedparser entries into single PyRSS2Gen.RSSitems
#
# Use:
# init the object
# input an object of type feedparser.entries[i]
# return value should be a type of PyRSS2Gen.RSSitem

class FeedItem2RSSItem:
    def GetRSSItem(self, feeditem):
        clist = []
        i = 0
        for ix1 in feeditem.tags:
            clist.append(feeditem.tags[i].term)
            i += 1
        r = PyRSS2Gen.RSSItem(
            title=feeditem.title,
            guid=feeditem.id,
            description=feeditem.description,
            author=feeditem.author,
            categories=clist,
            comments=feeditem.comments,
            link=feeditem.link,
            pubDate=feeditem.published,
        )
        return r
