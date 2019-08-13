from bs4 import BeautifulSoup
import requests
import shutil
import time,re
import os
from selenium import webdriver

print('================ Dcard 圖片下載器 ================')
URL = input("輸入欲下載的Dcard頁面 : ")
mypath = os.getcwd()

driver =  webdriver.Chrome(mypath+'\\chromedriver')
driver.implicitly_wait(3)
driver.get(URL)
Height = driver.execute_script('return document.body.scrollHeight')
count = 0
page = 0

for i in range (1,999):
    page+=1

    #javascript指令，使網頁下拉至最底層
    driver.execute_script("window.scrollTo(0,"+str(Height)+(');')) # 使頁面下拉至底部
    Height+=Height
    print("下拉次數 : " , page)
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    #抓取直接回應視窗(至最下層)
    if soup.select(".CommentList_content_1KaR30"):
        print("頁面至最底部\n\n"+"圖片開始下載 : ")
        break

for img in soup.select('.GalleryImage_image_3lGzO5'):

    if img['src'][0:23] == 'https://imgur.dcard.tw/':
            count += 1
            filename = img['src'].split('/')[-1]
            res2 = requests.get(img['src'],stream=True)

            # 新建資料夾
            download_path = mypath + "\\" + "Download"
            if not os.path.exists(download_path):
                os.makedirs(download_path)
                print("新建Download資料夾成功")

            print("成功,已下載第", count, "張", img['src'])

            # 把圖片載入Download
            f = open(download_path+'\\'+filename,'wb')

            shutil.copyfileobj(res2.raw,f)
            f.close()
            del res2
    else:
         print("失敗,無法下載", img['src'])

print("\n下載結束")




