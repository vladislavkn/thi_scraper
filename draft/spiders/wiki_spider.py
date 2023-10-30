import scrapy
import spacy
from scrapy.linkextractors import LinkExtractor

nlp = spacy.load("en_core_web_sm")

start_url = "http://cai.rz.fh-ingolstadt.de/mediawiki/index.php/Computer_Science_and_Artificial_Intelligence"


class WikiSpider(scrapy.Spider):
    name = "wiki"
    start_urls = [
        "http://cai.rz.fh-ingolstadt.de/mediawiki/index.php/Computer_Science_and_Artificial_Intelligence"
    ]
    custom_settings = {"DEPTH_LIMIT": 10}

    def __init__(self, *args, **kwargs):
        super(WikiSpider, self).__init__(*args, **kwargs)
        self.visited_urls = set()

    def parse(self, response):
        self.visited_urls.add(response.url)

        page_text = response.css("p::text").getall()
        page_text = " ".join(page_text)

        keywords = self.extract_keywords(page_text)

        key_value_pair = {"tags": keywords, "body": page_text}
        yield {response.url: key_value_pair}

        for link in LinkExtractor(allow=("/mediawiki/")).extract_links(response):
            if link.url not in self.visited_urls:
                next_page = response.urljoin(link.url)
                yield response.follow(next_page, self.parse)

    def extract_keywords(self, text):
        doc = nlp(text)
        keywords = [token.text for token in doc if token.is_alpha and not token.is_stop]
        return keywords
