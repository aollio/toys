#!/usr/bin/env python3
import codecs
import time

import os
import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.phantomjs.webdriver import RemoteWebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


class QunarSpider:
    def get_hotel(self, driver: RemoteWebDriver, to_city, fromdate, todate):

        ele_tocity = driver.find_element_by_name('toCity')
        ele_fromdate = driver.find_element_by_id('fromDate')
        ele_todate = driver.find_element_by_id('toDate')
        ele_search = driver.find_element_by_class_name('search-btn')

        ele_tocity.clear()
        ele_tocity.send_keys(to_city)

        ele_fromdate.clear()
        ele_fromdate.send_keys(fromdate)

        ele_todate.clear()
        ele_todate.send_keys(todate)

        ele_search.click()

        page_num = 0

        while True:
            try:
                WebDriverWait(driver, 10).until(
                    EC.title_contains(to_city)
                )
            except Exception as e:
                print(e)
                break

            time.sleep(5)

            html_const = driver.page_source
            soup = BeautifulSoup(html_const, 'html.parser', from_encoding='utf-8')
            infos = soup.find_all(class_='item_hotel_info')
            file = codecs.open(os.path.join('dist', to_city + fromdate + '.html'), 'a', 'utf-8')
            for info in infos:
                file.write(str(page_num) + '--' * 50)
                content = info.get_text().replace(' ','').replace('\t','').strip()
                for line in [ln for ln in content.splitlines() if ln.strip()]:
                    file.write(line)
                    file.write('\r\n')
                file.close()
                try:
                    next_page =WebDriverWait(driver, 10).until(
                        EC.visibility_of(driver.find_element_by_css_selector('.item.next'))
                    )
                    next_page.click()
                    page_num += 1
                    time.sleep(10)
                except Exception as e:
                    print(e)
                    break


    def crawl(self, root_url, to_city):
        today = datetime.date.today().strftime('%Y-%m-%d')
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        tomorrow = tomorrow.strftime('%Y-%m-%d')

        driver = webdriver.Chrome()
        driver.set_page_load_timeout(50)
        driver.get(root_url)
        driver.maximize_window()
        driver.implicitly_wait(10)
        self.get_hotel(driver, to_city, today, tomorrow)


def main():
    spider = QunarSpider()
    spider.crawl('http://hotel.qunar.com/', '上海')

if __name__ == '__main__':
    main()