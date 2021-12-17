import requests
from bs4 import BeautifulSoup as bs
import urllib
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import pandas as pd
import numpy as np
import datetime
import time

print("url :")
url = input()
print("time(s) : ")
sec = int(input())

driver = webdriver.Chrome('C:/Users/edward/projects/twitch_livechat_collector/chromedriver.exe')
driver.get(url)
time.sleep(10)  # Wait for connecting site


def getChats(sec):

    msgs = []
    times = []
    viewers=[]
    for i in range(int(sec/10)):
        soup=bs(driver.page_source,'lxml')
        viewer=soup.find("p",{"data-a-target":"animated-channel-viewers-count"}).text
        temp = soup.find('div', {'class': 'chat-shell'})
        msg = temp.findAll("div",{"class":"chat-line__message"})
        msgs.append(msg)
        times.append(datetime.datetime.now().strftime("%H:%M"))
        viewers.append(viewer)
        if((i%5)==4):
            timetime=i/int(sec/10)*100
            print("%0.1f" % timetime, "%")

        time.sleep(10)


    driver.quit()
    return(msgs,times,viewers)


start = time.time()
result = getChats(sec)
print("while ",time.time()-start,"s")

msgs = result[0]
times = result[1]
viewers = result[2]


df = pd.DataFrame()
# preprocessing
for i in range(len(msgs)):

    dfTemp = pd.DataFrame([x.split(":") for x in [x.text for x in msgs[i]]])

    dfTemp = dfTemp.iloc[:,:2]
    dfTemp['temp1'] = viewers[i]
    dfTemp['temp2'] = times[i]
    
    dfTemp.columns = ['id','contents','viewers','time']
    
    df = df.append(dfTemp)

df = df.drop_duplicates(['id','contents'])
filename = url.split('/')[-1]+"_"+datetime.datetime.now().strftime("%m%d")+".csv"
df.to_csv(filename,index=False)
