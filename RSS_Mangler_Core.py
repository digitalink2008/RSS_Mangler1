__name__ = "RSSMangler"
__version__ = (1, 0, 0)
__author__ = 'Donovan'

_generator_name = __name__ + "-" + ".".join(map(str, __version__))


import feedparser
import PyRSS2Gen
import shutil

class FeedItem2RSSItem:
    def GetRSSItem(self, feeditem):
        clist = []
        i = 0
        for ix1 in feeditem.tags:
            clist.append(feeditem.tags[i].term)
            i += 1

        # decide what to use as the description element
        if feeditem.content[0].type == "text/html":
            d = feeditem.content[0].value
        else:
            d = feeditem.description

        # test for author
        if hasattr(feeditem, 'author'):
            a = feeditem.author
        else:
            a = "NoAuthor"

        # test for comments
        if hasattr(feeditem, 'comments'):
            c = feeditem.comments
        else:
            c = ""

        r = PyRSS2Gen.RSSItem(
            title=feeditem.title,
            guid=feeditem.id,
            description=d,
            author=a,
            categories=clist,
            comments=c,
            link=feeditem.link,
            pubDate=feeditem.published,
        )
        return r

class MyRSSFeed:
    RSSInput = None
    RSSOutput = None
    OutPutFile = "myfile.xml"
    TempFile = "rsstemp.xml"
    FeedTitle = "TITLE"
    FeedLink = "LINK"
    FeedDescription = "Description"
    FeedURL = ""
    FeedProtocol = ""
    ItemCount = 0
    ItemFilter = []
    PublishLocation = ""


    def importrssfeed(self, feedurl):
        # parse out protocol for use later
        if feedurl.find("https") > 0:
            self.FeedProtocol = "https"
        elif feedurl.find("HTTPS") > 0:
            self.FeedProtocol = "https"
        else:
            self.FeedProtocol = "http"
        self.RSSInput = feedparser.parse(feedurl)
        self.ItemCount = self.GetFeedCount()
        self.aftermainimport() # call event

    # meant to be an event that is overridden
    def aftermainimport(self):
        i = 1

    def GetFeedCount(self):
        i = 0
        for ix1 in self.RSSInput.entries:
            i += 1
        return i

    def WriteRSSFile(self):
        self.RSSOutput = PyRSS2Gen.RSS2(
            title=self.FeedTitle,
            link=self.FeedLink,
            description=self.FeedDescription
        )
        self.AddItemsToOutput()
        self.beforewritetofile() # fire event
        self.RSSOutput.write_xml(open(self.TempFile, 'w', encoding="utf-8", errors="replace"), "UTF-8")
        shutil.copy(self.TempFile, self.OutPutFile)

    # meant to be an event that gets overridden
    def beforewritetofile(self):
        i = 1

    def AddItemsToOutput(self):
        f1 = FeedItem2RSSItem()
        for ix1 in self.RSSInput.entries:
            r1 = f1.GetRSSItem(ix1)
            self.RSSOutput.items.append(r1)

    def absorbfeed(self, feedurl):
        f1 = feedparser.parse(feedurl)
        for ix1 in f1.entries:
            self.RSSInput.entries.append(ix1)
        # self.ItemCount = self.GetFeedCount()

    def docustomstuff(self):
        i = 1
        # placeholder

