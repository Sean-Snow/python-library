import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils import downloader

# 图片存储目录
base_path = "1688/"


def parse_detail(url: str):
    """
    抓取详情页面数据
    :param url: 商品详情地址
    :return:
    """
    goods_id = url.split("/")[-1]
    goods_id = goods_id.split(".")[0]

    options = webdriver.ChromeOptions()
    # 解决滑块验证码失败问题
    options.add_argument('--disable-blink-features=AutomationControlled')

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    # 循环判断root-container元素是否出现，未出现则一直等待
    while True:
        try:
            wait.until(EC.presence_of_element_located((By.ID, "root-container")))
            break
        except:
            print("等待页面加载完成...")
            time.sleep(3)  # 每隔1秒检查一次
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # 使用BeautifulSoup查找img-list-wrapper下的所有img标签
    img_tags = soup.select('.img-list-wrapper .detail-gallery-img')
    for img_tag in img_tags:
        downloader.download(img_tag.get('src'), base_path + goods_id + '/gallery')

    detail_images = soup.select('.content-detail img')
    for img_tag in detail_images:
        downloader.download(img_tag.get('data-lazyload-src'), base_path + goods_id + '/detail')

    print("加载完成...")


parse_detail("https://detail.1688.com/offer/852609123387.html?spm=a26g8.29862146.375571050796101.29.1cac48c0hfsAiq&resourceId=3555284&udsPoolId=23503978&traceId=2150404317337503541566319ece21&__track_uuid=375571050796101")
