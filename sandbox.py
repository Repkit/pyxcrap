# import requests
import booklist
import constants
import scrapy
# print('*********************--START--*******************')
# print(newurl)
# print('**********************--END--********************')

# print(len(booklist.booklistpages))

class StorenlSpider(scrapy.Spider):
    name = 'storenlspirder'
    # start_urls = [booklist.booklistpages[0],booklist.booklistpages[1]];
    # start_urls = ['https://studystore.nl/boekenlijst/A-S-V-Devera/2020/BL103132/Verloskunde-Jaar-1']
    start_urls = booklist.booklistpages
    # custom_settings = {
    #     'ITEM_PIPELINES' : {'scrapy.pipelines.images.ImagesPipeline': 1},
    #     'IMAGES_STORE' : './images'
    # }

    # print(start_urls)

    # scrapy runspider sandbox.py -o quotes.json
    def parse(self, response):

        if len(response.css('.itemlist__row').getall()) < 1:
            filename = '/scripts/link-without-list.txt'
            f = open(filename, "a")
            f.write(response.url)
            f.write('\n')
            f.close
            if response.url.split("/")[-1] == 'keuzevakken':
                newurl = response.url.replace("/keuzevakken", "?electives=")
                for elective in response.css('input[name="electives"]'):
                    newurl = newurl + '&electives=' + elective.css('::attr(value)').get()
                    # print(elective.css('::attr(value)').get())
                # print('*********************--START--*******************')
                # print(newurl)
                # print('**********************--END--********************')
                yield scrapy.Request(url=newurl, callback=self.parse)
            return
        else:
            filename = '/scripts/link-with-list.txt'
            f = open(filename, "a")
            f.write(response.url)
            f.write('\n')
            f.close
            # return
        # for book in response.css('.booklist__product-info_container'):
        for book in response.css('.itemlist__row--clickable'):
            listhash = book.css('.list-items-products::attr(value)').get()
            if (listhash):
                # isbn = book.css('.subinfo-sm').css('div>div::text').get().replace('ISBN:','').strip()
                # print(isbn)
                author = book.css('.booklist__product-authors ::text').get()
                isbn = book.css('.subinfo-sm').css('div>div::text').get()
                if author:
                    author = author.strip()
                else:
                    author = ''
                if isbn:
                    isbn = isbn.replace('ISBN:','')
                    isbn = isbn.strip()
                else:
                    isbn = ''
                yield {
                'title': book.css('.booklist__product-info').css('p ::text').get(),
                'image': book.css('.booklist__product-image').css('img::attr(src)').get(), 
                'author': author, 
                'isbn': isbn, 
                'marketPrice': book.css('.product-list__price_from-to').css('.product-list__price_from::text').get(), 
                'price': book.css('.product-list__price_from-to').css('.product-list__price_to::text').get(), 
                'marketPriceUsed': book.css('.booklist__purchasetypes--secondhand').css('.product-list__price_from::text').get(), 
                'priceUsed': book.css('.booklist__purchasetypes--secondhand').css('.product-list__price_to::text').get(), 
                }

        # for next_page in response.css('a.next-posts-link'):
        #     yield response.follow(next_page, self.parse)
