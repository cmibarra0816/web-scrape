#Conversion

#Dependencies and Setup
import os
#import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
import datetime as dt

#!which cromedriver
#Set executable path w/ Chrome - MAC
executable_path={"executable_path": "/usr/local/bin/chromedriver"}
browser=Browser("chrome", **executable_path, headless=False)

#Set executable path w/ Chrome - WINDOWS
#executable_path={"executable_path": "./chromedriver.exe"}
#browser=Browser("chrome", **executable_path)

#browser.quit()

#NASA Mars News Site web scraper
def mars_news(browser):

#Visit the NASA Mars News site
url="https://mars.nasa.gov/news/"
browser.visit(url)

#Scrape the latest news & wait for it... if not immediately present
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=0.10)
    
html=browser.html
news_soup=BeautifulSoup(html, "html.parser")

#Parse results HTML with BeautifulSoup (bs)
#Find everything inside:
 
#Visit the NASA JPL (Jet Propulsion Laboratory) site web scraper
#executable_path={"executable_path": "/usr/local/bin/chromedriver"}
#browser=Browser("chrome", **executable_path)
def featured_image(browser):
    #NASA JPL (Jet Propulsion Laboratory) site
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    #Ask splinter - click button & class name
    #<button class="full_image">Full Image</button>
    full_image_button = browser.find_by_id("full_image")
    full_image_button.click()

    #Find "More Info" button & click it
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_element = browser.find_link_by_partial_text("more info")
    more_info_element.click()

    #Parse results HTML with BeautifulSoup (bs)
    html = browser.html
    image_soup = BeautifulSoup(html, "html.parser")

    img = image_soup.select_one("figure.lede a img")
    try:
        img_url = img.get("src")
    except AttributeError:
        return None 
   #Use Base URL to create an absolute
    img_url = f"https://www.jpl.nasa.gov{img_url}"
    return img_url

#Visit the Mars Weather Twitter account site web scraper
#executable_path={"executable_path": "/usr/local/bin/chromedriver"}
#browser Browser("chrome", **executable_path, headless=False)
def twitter_weather(browser):
    #Mars Weather Twitter Account site
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    
    #Parse results HTML with BeautifulSoup (bs)
    html=browser.html
    weather_soup=bs(html, "html.parser")
    
    #Find a Tweet with the data-name `Mars Weather`
    latest_tweets = soup.find_all('div', class_="js-tweet-text-container")

    #Search within for tweet txt
    weather_tweet = tweet.find('p').text
            if 'Sol' and 'pressure' in weather_tweet:
                print(weather_tweet)
                break
            else: 
                pass

#Visit Mars Facts site web scraper
def mars_facts():
    #Use pandas
        try:
            df = pd.read_html("https://space-facts.com/mars/")[0]
        except BaseException:
            return None
            df.columns=["Description", "Value"]
            df.set_index("Description", inplace=True)

        return df.to_html(classes="table table-striped")


#Visit the USGS Astrogeology Science Center site web scrape
#executable_path={"executable_path": "/usr/local/bin/chromedriver"}
#browser=Browser("chrome", **executable_path, headless=False)
def hemisphere(browser):
    #USGS Astrogeology Science Center site
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    hemisphere_image_urls = []

    # Get a list
    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}
        
        #Find element on each loop & click
        browser.find_by_css("a.product-item h3")[item].click()
        
        #Find sample & exctract (Sample)
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]
        
        #Get the title (h2.title)
        hemisphere["title"] = browser.find_by_css("h2.title").text
        
        #Append (hemisphere)
        hemisphere_image_urls.append(hemisphere)
        
        #Navigate by going backwards
        browser.back()
    return hemisphere_image_urls

#Helper
def scrape_hemisphere(html_text):
    hemisphere_soup = BeautifulSoup(html_text, "html.parser")
    try: 
        title_element = hemisphere_soup.find("h2", class_="title").get_text()
        sample_element = hemisphere_soup.find("a", text="Sample").get("href")
    except AttributeError:
        title_element = None
        sample_element = None 
    hemisphere = {
        "title": title_element,
        "img_url": sample_element
    }
    return hemisphere

#Main
def scrape_all():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)
    news_title, news_paragraph = mars_news(browser)
    img_url = featured_image(browser)
    mars_weather = twitter_weather(browser)
    facts = mars_facts()
    hemisphere_image_urls = hemisphere(browser)
    timestamp = dt.datetime.now()

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": img_url,
        "weather": mars_weather,
        "facts": facts,
        "hemispheres": hemisphere_image_urls,
        "last_modified": timestamp
    }
    browser.quit()
    return data 

if __name__ == "__main__":
    print(scrape_all())