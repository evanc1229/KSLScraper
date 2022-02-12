#!/usr/bin/env python
# coding: utf-8

# In[69]:


# Most straight-forward way to import a library in Python
import requests

# BeautifulSoup is a module inside the "bs4" library, we only import the BeautifulSoup module
from bs4 import BeautifulSoup

# Pandas and numpy are always helpful
import numpy as np
import pandas as pd
import tweepy


# In[70]:


headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
ksl_raw = requests.get('https://classifieds.ksl.com/search/keyword/arcteryx/priceFrom/0/priceTo/1000/Private/Sale',headers=headers).text
ksl_soup = BeautifulSoup(ksl_raw,'html.parser')
URL = 'https://classifieds.ksl.com/search/keyword/arcteryx/priceFrom/0/priceTo/1000/Private/Sale'


# In[71]:


raw_listings = ksl_soup.find_all('section',{'class':'listing-item featured'})


# In[72]:


def ExtractListingInfoDF(raw_listings):
    Titles = []
    Prices = []
    Locations = []
    for i in raw_listings:
        Titles.append(i.find('img')['alt'])
        Prices.append(i.find('div',{'class':'item-info-price info-line'}).text)
        Locations.append(i.find('a',{'class':'item-address'}).text)
    return pd.DataFrame({'Titles':Titles, 'Prices':Prices, 'Locations':Locations})
        


# In[73]:


New_Listings = ExtractListingInfoDF(raw_listings)


# In[74]:


New_Listings.head(23)


# In[75]:


History = pd.read_csv('History.csv').iloc[:,1:]


# In[76]:


History.head(23)


# In[77]:


merged = pd.merge(New_Listings, History, on=['Titles','Prices','Locations'], how='outer', indicator=True)


# In[78]:


merged


# In[79]:


tweet = merged[merged['_merge'] == 'left_only'].iloc[:,:-1]


# In[80]:


tweet


# In[81]:


merged.iloc[:,:-1].to_csv('History.csv')


# In[82]:


consumer_key = '2LlCS74i3TcPCB1f1rMj2LrXi'
consumer_secret = 'fLQw16Rx2VSmnWmlGX6wQEO20ODnFVdQ4J8qPWTVG9npVzjRDv' 
access_token = '1490836142714810370-byS7DykGYT6MVWWJQv3SnPqHisTiD6' 
access_token_secret = 'X5llf5ERCIaTSD8MY8kWapbecwoMwJq2YGQp5IbnyCrtx' 


# In[83]:


auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


# In[84]:


def GenerateTweetText(df_tweets):
    tweets = []
    for index,lab,price,loc in df_tweets.itertuples():
        tweets.append(f'GEAR ALERT: {lab} for {price} in {loc}')
    return tweets


# In[85]:


to_tweet = list(set(GenerateTweetText(tweet)))


# In[87]:


for i in to_tweet:
    try:
        api.update_status(i)
    except:
        print('Hi')
        pass

