import scrapy
from books.items import BooksItem

class BookSpider(scrapy.Spider):
    name = "book"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]
    
    def parse(self, response, **kwargs):
        if response.status != 200:
            self.logger.error(f"The spider returned incorect status. STATUS: {response.status}")
            return
        
        if not "books.toscrape.com" in response.url:
            self.logger.error(f"The spider returned incorrect url. URL: {response.url}")
            return
        
        for book in response.css("article.product_pod"):
            item = BooksItem()
            item['url'] = book.css("h3 > a::attr(href)").get()
            item['title'] = book.css("h3 > a::attr(title)").get()
            item['price'] = book.css(".price_color::text").get()
            yield item
            
            # get next page details
            next_page = response.css("li.next > a::attr(href)").get()
            page_info = response.css("li.current::text").get().strip()
            page_number = int(page_info.split()[1]) # Get a single page number
            
            self.logger.info(f"Next Page URL: {next_page}")
            self.logger.info(f"Page Number: {page_number}")
            
            # handlde a recursive crawling from paginated pages
            if next_page and page_number <= 3:
                next_page_url = response.urljoin(next_page) # join relative url with base url
                yield scrapy.Request(url=next_page_url, callback=self.parse)
            
                 
            
        
        
        