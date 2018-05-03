
# coding: utf-8
import pandas as pd
import selenium
from selenium import webdriver
import time
from bs4 import BeautifulSoup

# 匯入資料
item = pd.read_csv('/Users/max/Desktop/Project_商品庫存/萬代商品庫存.csv')
pList = []



# 獲得爬取URL
for data in item['url']:
    data_url = data.split('?utm')[0]
    print(data_url)

    
# selenium開啟chrome等待網頁載入完成    
    driver = webdriver.Chrome('/Applications/chromedriver') 
    driver.get(data_url)
    time.sleep(5)
    
# 抓取網頁資料    
    soup = BeautifulSoup(driver.page_source,"html.parser")
    items = soup.select('#buy')
    print (soup.select('#buy'))
    for i in items:
        print (i.get('src').split('/').pop())

# 寫入pList    
    pList.append([data_url, 
                  i.get('src').split('/').pop(),
                  soup.select('#buy')
                ])

    driver.close()
    
print ('done!')    



# 儲存成csv
df = pd.DataFrame(pList)
df.columns = ['網址', '狀態1', '狀態2']
df.to_csv('/Users/max/Desktop/庫存測試.csv', index=False)
pList



# 發送信件
import os
import sys
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

COMMASPACE = ', '

def main():
    sender = '信箱帳號'
    gmail_password = '信箱密碼'
    recipients = ['寄送人1','寄送人2']
    
    # 建立郵件主題
    outer = MIMEMultipart()
    outer['Subject'] = 'Test'
    outer['To'] = COMMASPACE.join(recipients)
    outer['From'] = sender
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    # 檔案位置
    attachments = ['/Users/max/Desktop/庫存測試.csv']

    # 加入檔案到MAIL底下
    for file in attachments:
        try:
            with open(file, 'rb') as fp:
                print ('can read faile')
                msg = MIMEBase('application', "octet-stream")
                msg.set_payload(fp.read())
            encoders.encode_base64(msg)
            msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            outer.attach(msg)
        except:
            print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
            raise

    composed = outer.as_string()

    # 寄送EMAIL
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(sender, gmail_password)
            s.sendmail(sender, recipients, composed)
            s.close()
        print("Email sent!")
    except:
        print("Unable to send the email. Error: ", sys.exc_info()[0])
        raise


main()
 
