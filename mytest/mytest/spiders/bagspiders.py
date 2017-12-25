# import the necessary packages
from mytest.items import OneB
import datetime
import scrapy
import ast

class BagSpiders(scrapy.Spider):
    name = "pyimagesearch-bag-spider"
    #store_loc = ["us","vg"]
    store_loc = ["us", "vg", "gg", "dm", "ar","je", "vi","al", "ua"]
    def start_requests(self):
        # let the starting urls be all the bag search pages for all stores in store_loc

        urls = ['https://www.net-a-porter.com/' + loc + '/en/d/shop/bags'  for loc in self.store_loc]
        print("starting urls are: ")
        print(urls)
        #urls = [
        #    'https://www.net-a-porter.com/al/en/d/shop/bags',
            #'https://www.net-a-porter.com/us/en/d/Shop/Bags/All?pn=2&npp=60&image_view=product&dScroll=0',
        #]
        for url in urls:
            print("#################################")
            print("now processing starting url " + url)
            print("#################################")
            yield scrapy.Request(url=url, callback=self.parse)



    #start_urls = ["https://www.net-a-porter.com/gg/en/d/Shop/Bags/All?pn=1&npp=60&image_view=product&dScroll=0"]
    loc_pid_scraped = dict()
    def parse(self, response):
        # just start parse page from the start url which is page 1

        num_pages = int(response.xpath("//div[@class='data_totalPages']/text()").extract_first())

        page_urls = response.xpath("//a[contains(@class,'pagination-page')]/@href").extract_first()

        for i in range(num_pages):
            page_url = "=".join(page_urls.split("=")[:-1] + [str(i + 1)])
            page_url_full = response.urljoin(page_url)
            yield scrapy.Request(page_url_full, self.parse_page)

    def parse_page(self, response):
        product_urls = response.xpath("//div[@class='product-image']/a/@href").extract()

        # get absolute urls
        product_urls = [response.urljoin(url) for url in product_urls]
        for product_url in product_urls:
            yield scrapy.Request(product_url, callback=self.parse_product)

        # after finishing

        #next_page = response.xpath("//a[@class='next-page']/@href").extract_first()
        #if next_page is not None:
        #    next_page = response.urljoin(next_page)
        #    yield scrapy.Request(next_page, callback=self.parse_page)




    def parse_product(self, response):
        # data and image for 1 product page

        # get the location and shortcut for loc first
        temp = response.xpath("//a[@class='country-name-flag']/span[contains(@class, 'flag flag')]/@class").extract_first()
        country_sc = temp.split('-')[-1]
        country = response.xpath("//span[@class='country-name']/text()").extract_first()

        # product code
        product_code = response.xpath("//div[@class='top-product-code']/div[@class='product-code']/span/text()").extract_first()

        # print(self.loc_pid_scraped)
        # only continue when we first see this product code in this country
        if (country, product_code) not in self.loc_pid_scraped:
            product_title_info = response.xpath("//head/meta[@property='og:title']/@content").extract_first()



            # pids with different style/color
            pids_list = response.xpath("//nap-product-swatch-collector/@pids").extract_first()
            if pids_list is not None:
                swatch_pids_list = ast.literal_eval(pids_list)  # this returns a list
            else:
                swatch_pids_list = None

            # prices
            price_dict = ast.literal_eval(response.xpath("//div[@class='container-title']/nap-price/@price").extract_first())
            price_info = dict({'price':price_dict["amount"]/price_dict["divisor"],
                          'currency':price_dict["currency"]})




            # designer information
            designer_name = response.xpath("//div[@class='container-details']/form[@id='product-form']/meta/@data-designer-name").extract_first()
            designer_id = response.xpath(
                "//div[@class='container-details']/form[@id='product-form']/meta/@data-designer-id").extract_first()

            # images
            main_img_url = response.xpath("//div[contains(@class, 'container-imagery')]/meta/@content").extract_first()
            img_urls = [main_img_url] + response.xpath("//img[@class='thumbnail-image']/@src").extract()
            img_urls = ["https:" + url  for url in img_urls]


            out = OneB(product_code=product_code, product_title_info=product_title_info,
                       alter_style_pid = swatch_pids_list,
                       designer_name=designer_name, designer_id=designer_id, price_info=price_info,
                       image_urls=img_urls, country = country)
            self.loc_pid_scraped[(country, product_code)] = 1  # record that we've seen this before
            yield out
            # yield the result

            # the base url for this country
            base_url = "https://www.net-a-porter.com/" +  country_sc + "/en/product/"


            if swatch_pids_list is not None:
                # go through all the alternative styles
                #swatch_pids_list = ast.literal_eval(pids_list)  # this returns a list
                for pid in swatch_pids_list:
                    swatch_url = base_url + str(pid)
                    yield scrapy.Request(swatch_url, callback=self.parse_product)
