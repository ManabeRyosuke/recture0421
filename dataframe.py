
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
import pandas as pd

# selenium 4.0 以上のバージョンでのインポート
from selenium.webdriver.common.by import By
from time import sleep

# データフレームを定義　追加
df_obj = pd.DataFrame(columns=["店名", "お問い合わせ", "住所", "営業時間", "URL"])

# Chrome WebDriverのオプションを設定する
chrome_options = Options()
# ヘッドレスモードを有効にする場合は以下のコメントアウトを外す
# chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options) 

# ウェブページを開く
driver.get("https://tabelog.com/osaka/A2701/A270101/rstLst/?SrtT=rt&Srt=D&sort_mode=1")

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
        if i == 1: # ページ数の制限
            break
    except:
        break

# 各レストランのページを開く
for EACH_LIST in HREF_LIST:
    driver.get(EACH_LIST)
    sleep(1)
    # タイトルを取得する
    title = driver.find_element(By.XPATH, '//h2/span').text
    
    # テーブルを取得する
    tables = driver.find_elements(By.CSS_SELECTOR, ".c-table.c-table--form")
    
    for table in tables:
        table = table.text
        
        #改行で分割してリストにする
        lines = table.split('\n')
    
        #####コードの追加#####
        # 営業時間と定休日を取得する
        if '営業時間' in lines:
            # 営業時間と定休日のインデックスを取得する
            business_hours_index = lines.index('営業時間')

            # 営業時間と定休日を取得する
            business_hours_list = lines[business_hours_index + 1 : ]
            business_hours = ", ".join(business_hours_list)


        # お問い合わせの行を抜き出して変数に格納
        for i, line in enumerate(lines):
            if "お問い合わせ" in line:
                contact_info = lines[i+1].strip()  # 次の行を取得し、前後の空白を削除して格納
                break
        # 住所の行を抜き出して変数に格納
        for i,line in enumerate(lines):
            if "住所" in line:
                address = lines[i+1].strip()
                break

        # データフレームに追加する
    df_obj = pd.concat([df_obj, pd.DataFrame({"店名": [title],"お問い合わせ":[contact_info],"住所":[address],"営業時間":business_hours,"URL":EACH_LIST})], ignore_index=True)

# WebDriverを閉じる
driver.quit()


###追加###
# CSVファイルに出力します
df_obj.to_csv('output.csv', index=False)
# Excelファイルに出力します
df_obj.to_excel('output.xlsx', index=False)