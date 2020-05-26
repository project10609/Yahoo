# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from ..items import YahooItem
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager


class Yahooeyeliner1Spider(scrapy.Spider):
    name = 'yahooeyeliner1'
    start_urls = [
        'https://tw.bid.yahoo.com/tw/%E7%9C%BC%E7%B7%9A%E6%B6%B2-%E7%9C%BC%E9%83%A8%E5%BD%A9%E5%A6%9D-2092078673-category.html?.r=1586239909/']

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
            item['product_category'] = 'EyeLiner'
            item['product_source'] = 'Yahoo'
            item['product_subcategory'] = 'eyeliner'

            yield item

        # self.action.pause(3)
        # self.action.perform()
        next_page = 'https://tw.bid.yahoo.com/tw/%E7%9C%BC%E7%B7%9A%E6%B6%B2-%E7%9C%BC%E9%83%A8%E5%BD%A9%E5%A6%9D-2092078673-category.html?.r=1586239909&hpp=hp_category_2092073302&pg=' + str(
            Yahooeyeliner1Spider.page)
        if Yahooeyeliner1Spider.page <= 100:
            Yahooeyeliner1Spider.page += 1
            url = next_page
            yield response.follow(url, callback=self.parse)
