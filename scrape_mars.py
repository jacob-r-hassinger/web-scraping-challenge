from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import pymongo

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
    news_title = soup.find('a', target="_self").text
    
    browser.visit(url_img)
    browser.click_link_by_partial_text("FULL IMAGE")
    browser.click_link_by_partial_text("more info")
    html = browser.html
    soup = bs(html, "html.parser")
    mars_img = soup.find('figure', class_="lede").a["href"]
    mars_img = f"https://www.jpl.nasa.gov{mars_img}"

    browser.visit(url_twtr)
    html = browser.html
    soup = bs(html, "html.parser")
    mars_weather = soup.find('span', class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")
    
    mars_table_from_html = pd.read_html(url_table)
    dataframe = mars_table_from_html[0]
    mars_table = dataframe.rename(columns = {0 : "Category", 1 : "Fact"})
    mars_table = mars_table.set_index("Category")
    mars_table = mars_table.to_dict()

    browser.visit(url_hemispheres)
    html = browser.html
    soup = bs(html, "html.parser")
    hemi_list = soup.find('div', class_ = 'collapsible results')
    mars_hemis = hemi_list.find_all('div', class_='item')
    hemi_imgs = []
    for hemi in mars_hemis:
        i = hemi.find('img')['src']
        i = f"https://astrogeology.usgs.gov{i}"
        hemi_imgs.append(i)
    hemi_img_1 = hemi_imgs[0]
    hemi_img_2 = hemi_imgs[1]
    hemi_img_3 = hemi_imgs[2]
    hemi_img_4 = hemi_imgs[3]

    mars_scrape = {"News_Title": news_title,
           "Mars_Image": mars_img,
           "Mars_Weather": mars_weather,
           "Mars_Table": mars_table,
           "Hemisphere_1": hemi_img_1,
           "Hemisphere_2": hemi_img_2,
           "Hemisphere_3": hemi_img_3,
           "Hemisphere_4": hemi_img_4}
    
    browser.quit()

    client = pymongo.MongoClient("mongodb://localhost:27017/")
    mars_db = client["mars_db"]
    collection = mars_db["mars_data"]
    insert = mars_db.collection.insert_one(mars_scrape)

    return mars_scrape

if __name__ == "__main__":
    scrape()