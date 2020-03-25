from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

url = "https://mars.nasa.gov/news"
url_img = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
url_twtr = "https://twitter.com/MarsWxReport?lang=en"
url_table = "https://space-facts.com/mars/"
url_hemispheres = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

def scrape():
    browser = init_browser()
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")
    #news_text = soup.find('div', class_='list_text')
    # #new_parsing = news_text.find("div", class_="content_title")
    news_title = soup.find('a', target="_self")
    
    browser.visit(url_img)
    html = browser.html
    soup = bs(html, "html.parser")
    mars_img = browser.click_link_by_partial_text("FULL IMAGE")

    browser.visit(url_twtr)
    html = browser.html
    soup = bs(html, "html.parser")
    mars_weather = soup.find('span', class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")

    mars_table = pd.read_html(url_table)

    browser.visit(url_hemispheres)
    html = browser.html
    soup = bs(html, "html.parser")
    hemi_list = soup.find('div', class_ = 'collapsible results')
    mars_hemis = hemi_list.find_all('div', class_='item')
    hemi_imgs = []
    for hemi in mars_hemis:
        i = hemi.find('img')
        hemi_imgs.append(i)

    mars_scrape = {"News Title": news_title,
           "Mars_Image": mars_img,
           "Mars_Weather": mars_weather,
           "Mars_Table": mars_table,
           "Hemisphere_1": hemi_imgs[0],
           "Hemisphere_2": hemi_imgs[1],
           "Hemisphere_3": hemi_imgs[2],
           "Hemisphere_4": hemi_imgs[3]}
    
    browser.quit()
    return mars_scrape

if __name__ == "__main__":
    scrape()