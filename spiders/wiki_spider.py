import scrapy
from utils.annotate_text import annotate_text
import re


class WikiSpider(scrapy.Spider):
    name = "wiki-spider"
    start_urls = [
        "http://cai.rz.fh-ingolstadt.de/mediawiki/index.php/Computer_Science_and_Artificial_Intelligence",
    ]
    custom_settings = {"DEPTH_LIMIT": 10}
    blacklisted_parts = ["/Special:", "/File:", "Category:"]

    def __init__(self, *args, **kwargs):
        super(WikiSpider, self).__init__(*args, **kwargs)
        self.scrapedLinks = []

    def parse(self, response):
        texts = response.css("p::text").getall()
        sentences = []
        for text in texts:
            sentences += list(re.split("[.?!]", text))

        entries = self.makeEntries(sentences)
        for entry in entries:
            yield entry

        for link in response.xpath(".//a/@href"):
            newUrl = str(link.get())
            if self.testLinkInteresting(newUrl):
                newUrl = self.makeLinkComplete(newUrl)

                if newUrl not in self.scrapedLinks:
                    self.scrapedLinks.append(newUrl)
                    yield response.follow(newUrl, self.parse)

    def testLinkInteresting(self, url):
        if "/mediawiki/index.php/" not in url:
            return False
        for blacklisted_part in WikiSpider.blacklisted_parts:
            if blacklisted_part in url:
                return False
        return True

    def makeLinkComplete(self, url):
        if "http://cai.rz.fh-ingolstadt.de/" in url:
            return url
        else:
            return "http://cai.rz.fh-ingolstadt.de/" + url

    def makeEntries(self, texts):
        entries = []
        for text in texts:
            tags = annotate_text(text)
            if tags:
                entries.append({"tags": tags, "answer": text})
        return entries
