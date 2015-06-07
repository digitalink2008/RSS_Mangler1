__author__ = 'Dman'
from RSS_Mangler_Core import MyRSSFeed

# ===========================================================================================
# INSPARATION GRID
# ===========================================================================================
class InsparationGrid_Feed(MyRSSFeed):
    def docustomstuff(self):
        self.ModifyDescriptions()
        self.FeedDescription = "Feed items = " + str(self.ItemCount)

    def ModifyDescriptions(self):
        for ix1 in self.RSSInput.entries:
            # print("Before________________________________")
            # print(ix1.description.encode('ascii', 'ignore'))
            ix1.description = ix1.description.replace('"//', '"' + self.FeedProtocol + '://')
            ix1.content[0].value = ix1.content[0].value.replace('"//', '"' + self.FeedProtocol + '://')
            # print("After________________________________")
            # print(ix1.description.encode('ascii', 'ignore'))

# ===========================================================================================
# FANDOM POST
# ===========================================================================================
class FandomPost_Feed(MyRSSFeed):
    def docustomstuff(self):
        self.FeedDescription = "Feed items = " + str(self.ItemCount)

# ===========================================================================================
# DEVIANT ART REFORMATTED
# ===========================================================================================
class DeviantArt_Feed(MyRSSFeed):
    def docustomstuff(self):
        #self.absorbfeed("http://backend.deviantart.com/rss.xml?q=boost:popular%20in:photography/nature/domestic%20max_age:744h&type=deviation")
        #self.absorbfeed("http://backend.deviantart.com/rss.xml?q=boost:popular%20max_age:744h%20devil&type=deviation")
        #self.absorbfeed("http://backend.deviantart.com/rss.xml?q=boost:popular%20max_age:744h%20shiba&type=deviation")
        #self.absorbfeed("http://backend.deviantart.com/rss.xml?q=boost:popular%20in:digitalart/paintings%20max_age:744h&type=deviation")
        #self.absorbfeed("http://backend.deviantart.com/rss.xml?q=boost:popular%20in:photography/horror%20max_age:744h&type=deviation")
        #self.absorbfeed("http://backend.deviantart.com/rss.xml?q=boost:popular%20max_age:744h%20warhammer&type=deviation")
        #self.absorbfeed("http://backend.deviantart.com/rss.xml?q=boost:popular%20in:digitalart/paintings/macabre%20max_age:744h&type=deviation")
        #self.absorbfeed("http://backend.deviantart.com/rss.xml?q=boost:popular%20in:digitalart/paintings/scifi%20max_age:744h&type=deviation")
        #self.absorbfeed("http://backend.deviantart.com/rss.xml?q=boost:popular%20in:digitalart/paintings/fantasy%20max_age:744h&type=deviation")
        #self.FeedDescription = "Feed items = " + str(self.ItemCount)
        for ix1 in self.RSSInput.entries:
            self.includefullimages()

    def beforewritetofile(self):
        for ix1 in self.RSSOutput.items:
            self.reformatcategories(ix1)

    # The deviant art feed has terrible tagging. Lets make it more usable
    def reformatcategories(self, fi):
        clist = []
        for ix2 in fi.categories:
            ix3 = ix2.split("/")
            for ix4 in ix3:
                clist.append(ix4)
        fi.categories = clist

    # lets put the real images into the rss feed for deviant art as well
    def includefullimages(self):
        # fi needs to by of type feedparser.entries[i]
        for fi in self.RSSInput.entries:
            if not (hasattr(fi, "media_content")):
                return
            img = fi.media_content[0]['url']
            fi.summary = '<img src="' + str(img) + '">' + fi.summary

o2 = FandomPost_Feed()
o2.FeedTitle = "FandomPost"
o2.OutPutFile="E:\downloads\dropbox\RSSfiles\\fandompost.xml"
o2.importrssfeed("http://www.fandompost.com/feed/")
o2.docustomstuff()
o2.WriteRSSFile()

o1 = InsparationGrid_Feed()
o1.FeedTitle="Testing"
o1.OutPutFile="E:\downloads\Dropbox\RSSFiles\\rsstest.xml"
o1.importrssfeed("http://theinspirationgrid.com/feed/")
o1.docustomstuff()
o1.WriteRSSFile()

o3 = DeviantArt_Feed()
o3.FeedTitle="DA Test"
o3.OutPutFile="E:\downloads\Dropbox\RSSFiles\\DeviantArt.xml"
o3.importrssfeed("http://backend.deviantart.com/rss.xml?q=boost:popular%20max_age:168h%20baphomet&type=deviation")
o3.docustomstuff()
o3.WriteRSSFile()
