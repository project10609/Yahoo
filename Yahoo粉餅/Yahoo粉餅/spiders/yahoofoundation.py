# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from ..items import YahooItem
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager


class YahoofoundationSpider(scrapy.Spider):
    name = 'yahoofoundation'
    start_urls = [
        'https://tw.bid.yahoo.com/tw/%E7%B2%89%E9%A4%85-%E8%87%89%E9%83%A8%E5%BD%A9%E5%A6%9D-2092073304-category.html?.r=1585639662/']

    page = 2

    # def __init__(self):
    #     self.driver = webdriver.Chrome(ChromeDriverManager().install())
    #     self.action = webdriver.ActionChains(self.driver)

    def parse(self, response):
        # self.driver.get(response.url)
        # res = self.driver.execute_script("return document.documentElement.outerHTML")
        item = YahooItem()
        soup = BeautifulSoup(response.text, 'html.parser')

        for items in soup.find('div',
                               {'class': 'ResultList_priorityList_2_Lsz', 'data-testid': 'hitList'}).find_all_next('li',
                                                                                                                   class_='BaseGridItem__grid___2wuJ7'):
            item['product_name'] = items.find('span', {'class': 'BaseGridItem__itemInfo___3E5Bx'}).find('span', {
                'class': 'BaseGridItem__title___2HWui'}).text
            item['product_price'] = items.find('span', {'class': 'BaseGridItem__price___31jkj'}).text.split()[
                0].replace('/', '').replace('$', '').replace(',', '')
            item['product_url'] = items.find('a').attrs['href']
            item['product_images'] = items.find(
                'div', {'class': 'SquareFence_wrap_3jTo2'}).find('img').attrs['src']
            item['product_category'] = 'Foundation'
            item['product_source'] = 'Yahoo'
            item['product_subcategory'] = 'pressedpowder'

            yield item

        # self.action.pause(3)
        # self.action.perform()
        next_page = 'https://tw.bid.yahoo.com/tw/%E7%B2%89%E9%A4%85-%E8%87%89%E9%83%A8%E5%BD%A9%E5%A6%9D-2092073304-category.html?.r=1585639662&hpp=hp_category_2092073302&pg=' + str(
            YahoofoundationSpider.page)
        if YahoofoundationSpider.page <= 4:
            YahoofoundationSpider.page += 1
            url = next_page
            yield response.follow(url, callback=self.parse)
