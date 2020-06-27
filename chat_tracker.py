#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup as bs
import urllib
from selenium import webdriver
from selenium.webdriver.support.ui import Select


# In[2]:


import pandas as pd
import numpy as np
import datetime
import time


# In[3]:


print("url :")
url = input()
print("tiem(s) : ")
sec = int(input())


# In[4]:


driver = webdriver.Chrome('/home/edward/twitch/chromedriver')
driver.get(url)
time.sleep(10)


# In[5]:


def getChats(sec):

    msgs = []
    times = []
    viewers=[]
    for i in range(int(sec/10)):
        soup=bs(driver.page_source,'lxml')
        viewer=soup.find("span",{"class":"tw-animated-number tw-animated-number--monospaced"}).text
        
        temp = soup.find("div",{"class":"chat-shell chat-shell__expanded tw-full-height"})

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


# In[ ]:


start = time.time()
result = getChats(sec)
print("while ",time.time()-start,"s")


# In[ ]:


msgs = result[0]
times = result[1]
viewers = result[2]


# In[ ]:


df = pd.DataFrame()
for i in range(len(msgs)):

    dfTemp = pd.DataFrame([x.split(":") for x in [x.text for x in msgs[i]]])

    dfTemp = dfTemp.iloc[:,:2]
    dfTemp['temp1'] = viewers[i]
    dfTemp['temp2'] = times[i]
    
    dfTemp.columns = ['id','contents','viewers','time']
    
    df = df.append(dfTemp)


# In[ ]:


df = df.drop_duplicates(['id','contents'])


# In[ ]:


filename = url.split('/')[-1]+"_"+datetime.datetime.now().strftime("%m%d")+".csv"


# In[ ]:


df.to_csv(filename,index=False)

