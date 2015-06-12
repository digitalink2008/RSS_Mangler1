__name__ = "RSSMangler"
__version__ = (1, 0, 0)
__author__ = 'Donovan'

_generator_name = __name__ + "-" + ".".join(map(str, __version__))


import feedparser
import PyRSS2Gen
import shutil
import urllib2_file
from bs4 import BeautifulSoup

# ===========================================================================================
# FeedItem2RSSItem
#
# This is the translator from the feedparser class to the PyRSS2Gen class structure
# ===========================================================================================
class FeedItem2RSSItem:
    def GetRSSItem(self, feeditem):
        # Re-Format item tags
        # shouldnt assume tags are present tho i gues
        if hasattr(feeditem, "tags"):
            clist = []
            i = 0
            for ix1 in feeditem.tags:
                clist.append(feeditem.tags[i].term)
                i += 1
        else:
            clist = []

        # at the time the conversion from feeditem to RSSoutput is done i everything you want in
        # the body of the RSS item needs to be in the description field. Its just much cleaner
        # and less confusing that way. To handle things like content in the media_content field
        # do that in an instance of MYRSSFeed's custom functions
        d = feeditem.description

        self.validate_fields(feeditem)

        r = PyRSS2Gen.RSSItem(
            title=feeditem.title,
            guid=feeditem.id,
            description=d,
            author= feeditem.author,
            categories=clist,
            comments= feeditem.comments,
            link=feeditem.link,
            pubDate=feeditem.published,
        )
        if hasattr(feeditem, 'media_rating'):
            r.rating = feeditem.media_rating["content"]
        else:
            r.rating = "no rating"
        if hasattr(feeditem, "tags"):
            r.label = feeditem.tags[0]["label"]
        else:
            r.label = ""
        return r

    def validate_fields(self, feeditem):
        # test for author
        if hasattr(feeditem, 'author'):
            a = feeditem.author
        else:
            a = "NoAuthor"
        feeditem.author = a

        # test for comments
        if hasattr(feeditem, 'comments'):
            c = feeditem.comments
        else:
            c = ""
        feeditem.comments = c


# ===========================================================================================
# MyRSSFeed
#
# This class represents a whole RSS feed. It contains a set of RSS items within both the
#   RSSInput and RSSOutput objects
# ===========================================================================================
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

# ===========================================================================================
# ImageItem Class
#
# just helps reduce my errors when coding html tags
# ===========================================================================================
class ImageItem:

    ImageURL = ""

    def __init__(self, url):
        self.ImageURL = url

    def get_html_img(self):
        return '<img src="' + self.ImageURL + '">'

    def get_img_with_div(self):
        return "<div>" + self.get_html_img() + "</div>"

    def get_img_with_P(self):
        return "<P>" + self.get_html_img() + "</P>"

# ===========================================================================================
# PinButton Class
#
# for adding a Pinterest button to stuff!
# ===========================================================================================
class PinButton:
    imgclass = "pin-it-button"
    pinbutton = "http://pinterest.com/pin/create/button/?"
    url = ""
    media = ""
    description = ""
    rel = "nofollow"
    target = "_blank"
    imgborder = "0"
    buttonimg = "http://assets.pinterest.com/images/PinExt.png"
    title = "Pin It"

    def __init__(self, url, media, description):
        self.url = url
        self.media = media
        self.description = description

    def get_pinbutton(self):
        html = ""
        # add button class
        html = html + '<a class="' + self.imgclass + '" '
        # add pinterest link
        html = html + 'href="' + self.pinbutton
        # add page link
        html = html + 'url=' + self.url + '&'
        # add image link
        html = html + 'media=' + self.media + '&'
        # add image description
        html = html + 'description=' + self.description + '" '
        # add rel
        html = html + 'rel="' + self.rel + '" '
        # add target
        html = html + 'target="' + self.target + '">'
        # start adding pin button image
        html = html + '<img border="' + self.imgborder + '" '
        # link to pin button image
        html = html + 'src="' + self.buttonimg + '" '
        # add button title
        html = html + 'title="' + self.title + '">   '
        # add text to button
        html = html + 'Pin-It</a>'
        # done
        return html

# ===========================================================================================
# htmlpage Class
#
# using beautiful soup 4 for screen scraping
# ===========================================================================================
class htmlpage:
    page = ""
    url = ""

    def __init__(self, url):
        self.url = url
        req = urllib2.Request(url)
        res = urllib2.urlopen(req)
        self.page = res.read()

