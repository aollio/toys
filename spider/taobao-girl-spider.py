#!/usr/bin/env python3
import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import requests

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'

USER_AGENT = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36'
              '(KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36')


class Logging:
    def error(self, *args):
        print(*args)

    def info(self, *args):
        print(*args)


logging = Logging()


def revise_img_src(src):
    """修正图片的URL值."""
    if src.startswith('http'):
        return src
    elif src.startswith('//'):
        return 'http:' + src
    else:
        return 'http://' + src


def save_img(name, url):
    if not os.path.exists('dist'):
        os.mkdir('dist')
    try:
        with open(os.sep.join(['dist', name]), 'wb') as file:
            headers = {'User-Agent': USER_AGENT}
            res = requests.get(revise_img_src(url), headers=headers,
                               stream=True)
            if res.status_code == 200:
                file.write(res.content)
    except Exception as e:
        logging.error('保存一张图片出错, 文件名: %s, 图片地址: %s' % (name, url), e)


class TaoBaoGirlSpider:
    def __init__(self):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap['phantomjs.page.settings.userAgent'] = USER_AGENT
        self.driver = webdriver.PhantomJS(executable_path='/Users/Aollio/Development/phantomjs/bin/phantomjs',
                                          desired_capabilities=dcap)

        self.driver.get('https://www.taobao.com/markets/mm/mmku')
        time.sleep(2)
        self.pages = int(self.driver.find_element_by_xpath('//*[@id="fn_page"]/div/span[@class="skip-wrap"]/em').text)
        logging.info('总页数:', self.pages)

        self.current_page = 1

    def start(self):
        logging.info('start.')
        try:
            self.crawl()
        except Exception:
            logging.error('出现异常')
        finally:
            self.close()
        logging.info('done.')

    def crawl(self):
        driver = self.driver

        for page_index in range(self.current_page, self.pages + 1):
            soup = BeautifulSoup(driver.page_source, 'lxml')
            logging.info('     当前第%s页' % page_index)
            # 每张图片的item在dom中class=cons_li
            cons_li_list = soup.select('.cons_li')
            len_cons_list = len(cons_li_list)
            logging.info('     当前页的个数:', len_cons_list)

            for cons_li in cons_li_list:
                name = cons_li.select('.item_name p')[0].get_text()
                logging.info('         name:', name)
                img = cons_li.select('.item_img img')[0]
                img_src = img.get('src')
                if img_src is None:
                    img_src = img.get('data-ks-lazyload')
                logging.info('         img_src:', img_src)

                filename = name + os.path.splitext(img_src)[1]
                save_img(name=filename, url=img_src)

            if page_index == self.pages:
                break
            logging.info('     开始跳转到第%s页' % (page_index + 1))
            self.jump(page_index + 1)

    def jump(self, page_index):
        driver = self.driver
        # click to next page
        page_input = driver.find_element_by_xpath('//*[@id="fn_page"]/div/span[@class="skip-wrap"]/input')
        page_input.clear()
        page_input.send_keys(str(page_index))

        # '确定'按钮
        ok_button = driver.find_element_by_xpath('//*[@id="fn_page"]/div/span[@class="skip-wrap"]/button')
        ok_button.click()

        # sleep
        time.sleep(3)

    def close(self):
        self.driver.quit()


if __name__ == '__main__':
    TaoBaoGirlSpider().start()
