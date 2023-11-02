import scrapy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

nltk.download("stopwords")
nltk.download("punkt")


class WikiSpider(scrapy.Spider):
    name = "wiki-spider"
    start_urls = [
        "http://cai.rz.fh-ingolstadt.de/mediawiki/index.php/Computer_Science_and_Artificial_Intelligence",
    ]
    custom_settings = {"DEPTH_LIMIT": 10}
    blacklisted_parts = ["/Special:", "/File:", "Category:Student"]

    def __init__(self, *args, **kwargs):
        super(WikiSpider, self).__init__(*args, **kwargs)
        self.scrapedLinks = []

    def parse(self, response):
        texts = response.css("p::text").getall()
        entries = self.makeEntries(texts)
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
            if len(text.split(" ")) > 5:
                keywords = self.extractKeywords(text)
                entries.append({"tags": keywords, "answer": text})
        return entries

    def extractKeywords(self, text):
        words = word_tokenize(text)
        words = [word.lower() for word in words if word.isalpha()]

        stop_words = set(stopwords.words("english"))
        words = [word for word in words if word not in stop_words]

        freq_dist = Counter(words)
        keywords = [word for word, freq in freq_dist.most_common(10)]

        return keywords