#this is the web scraping for Amazon.ca
#importing scrapy
import scrapy
#importing items that should be scraped 
from ..items import AmazonScrapingItem


#creating Spider function
class AmazonSpider(scrapy.Spider):
    #creating spider name
    name = 'amazon_spider'
    #allowing demains
    allowed_domains = ['amazon.ca']
    #valid url to crawl
    start_urls = ['https://www.amazon.ca/s?k=laptop']
    
    #creating a Parse function
    def parse(self, response):
        #identifying cards from the start_urls
        cards = response.css('.s-card-container')
        #creating a for loop to reach each product
        for card in cards:
            #reaching product link for each card
            product_link = 'https://www.amazon.ca'+card.css('.a-link-normal').attrib['href']
            #calling another function to get product information
            yield scrapy.Request(product_link, callback=self.parse_product_details)
            
            try:
            
                #in case of next page, let's create a code to reach page 2, page 3...
                next_page = 'https://www.amazon.ca'+response.css('.s-widget-container div span a.s-pagination-item').attrib['href']  #when you use a.<something> you say to find a a tag with class name as <something>
                
                                
                if next_page is None: #checking if there is a next page
                    next_page = response.urljoin(next_page) #joing the new url for request
                
                #removing the new request block out of the if statement
                yield scrapy.Request(next_page, callback=self.parse) #in case of next page, using Parse function as a callback and reach the cards for the next page and finds product information
            except:
                break
                
            
    def parse_product_details(self, response):
        #creating a try/exception block, avoding break the code
        
        try:
            #creating product object
            product = AmazonScrapingItem() 
            #product url
            product['product_link'] = response.url
            #product title
            product['title'] = response.css('#titleSection h1 span::text').get().strip()
            #expected delivery date
            product['delivery_date'] = response.css('#deliveryBlockMessage div div span span::text').get()
            #prodcut price
            product['price'] = response.css('.a-offscreen::text').get()
            if product['price'] is None or product['delivery_date'] is None:
                product['price'] = 'Out of Stock'
                product['delivery_date'] = 'Out of Stock'
            
        except:
            pass
                
        #defining which information should be as a result of the web scraping process
        yield product
        
        #running the spider
        #using terminal, out of the scrapy shell part, type scrapy crawl <spider_name>
        
        #defining some rules using the spider configuration
        # using fake agents providers
        # FAKEUSERAGENT_PROVIDERS = [
        #     'scrapy_fake_useragent.providers.FakeUserAgentProvider',  # This is the first provider we'll try
        #     'scrapy_fake_useragent.providers.FakerProvider',  # If FakeUserAgentProvider fails, we'll use faker to generate a user-agent string for us
        #     'scrapy_fake_useragent.providers.FixedUserAgentProvider',  # Fall back to USER_AGENT value
        # ]
        # # Obey robots.txt rules
        # ROBOTSTXT_OBEY = False

        # #defining user agent to avoid problems during the scraping
        # USER_AGENT = 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
        
        #creating a .csv file as a output
        # scrapy crawl <spider_name> -o <file_name>.csv 