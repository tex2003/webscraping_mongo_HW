from bs4 import BeautifulSoup
import requests
from splinter import Browser
from selenium import webdriver
import re
import pandas as pd
import time

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path)

def scrape ():
    browser = init_browser()
    mars = {}
    # # Scraping NASA Mars News - news_title, news_p
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    time.sleep(5)
    mars["news_title"] = soup.find("div", class_="content_title").text.strip()
    mars["news_p"] = soup.find("div", class_="rollover_description_inner").text.strip()
    # # Scraping JPL Mars Images - featured_image_url
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    html = browser.html
    soup_2 = BeautifulSoup(html, 'html.parser')
    images = soup_2.find('section', class_='centered_text clearfix main_feature primary_media_feature single')
    div_style = images.find('article')['style']
    href = re.search("(?P<url>/[^\s]+)", div_style).group("url")
    full_url='https://www.jpl.nasa.gov' + href
    mars["featured_image_url"] = full_url[:-3]
    # # Scraping Mars Weather - mars_weather
    url_3 = 'https://twitter.com/marswxreport?lang=en'
    response_3 = requests.get(url_3)
    soup_3 = BeautifulSoup(response_3.text, 'html.parser')
    mars["mars_weather"] = soup_3.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    # Scraping Mars Facts - mars_table
    url_4 = 'https://space-facts.com/mars/'
    response_4 = requests.get(url_4)
    mars["mars_table"] = []
    soup_4 = BeautifulSoup(response_4.text, 'html.parser')
    tables = soup_4.find('table', class_='tablepress tablepress-id-mars')
    trs =tables.find_all('tr')
    for tr in trs:
        value = tr.find('td', class_="column-1").text
        entry= tr.find('td', class_="column-2").text
        mars['mars_table'].append({'value': value, 'entry': entry})   
    # Scraping Mars Hemispheres - hemisphere_image_urls
    url_5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response_5 = requests.get(url_5)
    mars["hemisphere_image_urls"] = []
    soup_5 = BeautifulSoup(response_5.text, 'html.parser')
    links = soup_5.find_all('a', class_='itemLink product-item')
    n=1
    for link in links:
        href = link.get('href')
        title = link.find('h3').text
        link = 'https://astrogeology.usgs.gov'+ href  
        response_loop = requests.get(link)
        soup_loop = BeautifulSoup(response_loop.text, 'html.parser')
        hem_img_div = soup_loop.find('div', class_='downloads')
        hem_img_a = hem_img_div.find('a')
        hem_img_url = hem_img_a.get('href')
        mars["hemisphere_image_urls"].append({'title_'+ str(n): title, 'img_url_'+ str(n): hem_img_url})
        n = n+1
    return mars
    browser.quit()