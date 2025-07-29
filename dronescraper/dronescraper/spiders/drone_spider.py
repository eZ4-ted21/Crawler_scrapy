import scrapy
from dronescraper.data_model.model import DataModel

class DroneSpider(scrapy.Spider):
    def __init__(self):
        pass

    name = "drone"
    start_urls = [
        "https://urbangadgets.ph/category/aerial-photography/drone/?srsltid=AfmBOoq2ykFbvAeqBvZOAVZN9OA0nx_RoFbIeE_uoKCTS55CkxhBEHbf",
    ]

    def parse(self, response):
        for item in response.css("div.product-small.box"):
            data = self.validateData(item)
            yield {
                'title' : data.title,
                'url' : data.url,
                'price' : data.price
            }
        next_page = self.getNextPage(response)
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def getNextPage(self, response) -> str:
        return response.css('la.next.page-number::attr("href")').get()

    def validateData(self, item) -> DataModel:
        data = DataModel(
            title = self.getTitle(item),
            url = self.getUrl(item),
            price = self.getPrice(item)
        )
        return data

    def getTitle(self, item) -> str:
        title : str = 'Not Found'
        try:
            title = item.css('p.name.product-title.woocommerce-loop-product__title a::text').get(default=title)
        except Exception as e:
            print(f'[x] Exception Ecountered on fetching Title : {e}')
        return title
    
    def getUrl(self, item) -> str:
        url : str = 'Not Found'
        try:
            url = item.css('a.woocommerce-LoopProduct-link.woocommerce-loop-product__link').attrib['href']
        except Exception as e:
            print(f'[x] Exception Ecountered on fetching URL : {e}')
        return url
    
    def getPrice(self, item) -> str:
        price : str = 'Not Found'
        try:
            price = item.css('span.price bdi::text').get(default=price)
        except Exception as e:
            print(f'[x] Exception Ecountered on fetching Price : {e}')
        return price