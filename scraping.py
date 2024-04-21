from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
import pandas as pd

# selenium 4.0 以上のバージョンでのインポート
from selenium.webdriver.common.by import By
from time import sleep

# Chrome WebDriverのオプションを設定する
chrome_options = Options()
# ヘッドレスモードを有効にする場合は以下のコメントアウトを外す
# chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options) 

# ウェブページを開く
driver.get("https://tabelog.com/osaka/A2701/A270101/rstLst/?SrtT=rt&select_sort_flg=1&Srt=D&sort_mode=1")

# 待機する時間
# driver.implicitly_wait(10)
sleep(3)

i = 0

# レストランのリンクを取得する
HREF_LIST = []
while True:
    HREFS = driver.find_elements(By.CSS_SELECTOR, "a.list-rst__rst-name-target.cpy-rst-name")
    for HREF in HREFS:
        HREF_TITLE = HREF.get_attribute("href")
        HREF_LIST.append(HREF_TITLE)
    try:
        # 「次へ」ボタンをクリックする
        driver.find_element(By.XPATH, '//li[@class="c-pagination__item" and position()=last()]/a').click()
        i += 1
        if i == 5: # ページ数の制限
            break
    except:
        break

# 各レストランのページを開く
for EACH_LIST in HREF_LIST:
    driver.get(EACH_LIST)
    sleep(1)
    # タイトルを取得する
    title = driver.find_element(By.XPATH, '//h2/span').text
    print("[INFO] title :", title)
    # テーブルを取得する
    tables = driver.find_elements(By.CSS_SELECTOR, ".c-table.c-table--form")
    
    for table in tables:
        table = table.text
        print("[INFO] table :", table)
        
# WebDriverを閉じる
driver.quit()
