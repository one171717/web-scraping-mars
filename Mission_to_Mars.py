
# coding: utf-8

# In[6]:


# import all dependencies
import time
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser


# In[3]:


#pointing to the directory where chromedriver exists
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# In[4]:


#visiting the page
url = "https://mars.nasa.gov/news/"
browser.visit(url)


# In[7]:


#using bs to write it into html
html = browser.html
soup = bs(html,"html.parser")


# In[8]:


news_title = soup.find("div", "content_title").text
news_paragraph = soup.find("div", "article_teaser_body").text
print(f"Title: {news_title}")
print(f"Para: {news_paragraph}")


# In[9]:


url_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=featured#submit"
browser.visit(url_image)


# In[10]:


#Getting the base url
from urllib.parse import urlsplit
base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url_image))
print(base_url)


# In[11]:


#Design an xpath selector to grab the image
xpath = "//*[@id=\"page\"]/section[3]/div/ul/li[1]/a/div/div[2]/img"


# In[12]:


#Use splinter to click on the mars featured image
#to bring the full resolution image
results = browser.find_by_xpath(xpath)
img = results[0]
img.click()


# In[13]:


#get image url using BeautifulSoup
html_image = browser.html
soup = bs(html_image, "html.parser")
img_url = soup.find("img", "fancybox-image")["src"]
full_img_url = base_url + img_url
print(full_img_url)


# In[14]:


#get mars weather's latest tweet from the website
url_weather = "https://twitter.com/marswxreport?lang=en"
browser.visit(url_weather)


# In[16]:


html_weather = browser.html
soup = bs(html_weather, "html.parser")
#temp = soup.find('div', attrs={"class": "tweet", "data-name": "Mars Weather"})
mars_weather = soup.find("p", "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
print(mars_weather)


# In[17]:


url_facts = "https://space-facts.com/mars/"


# In[18]:


table = pd.read_html(url_facts)
table[0]


# In[19]:


df_mars_facts = table[0]
df_mars_facts.columns = ["Parameter", "Values"]
df_mars_facts.set_index(["Parameter"])


# In[20]:


mars_html_table = df_mars_facts.to_html()
mars_html_table = mars_html_table.replace("\n", "")
mars_html_table


# In[21]:


url_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(url_hemisphere)


# In[22]:


#Getting the base url
hemisphere_base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url_hemisphere))
print(hemisphere_base_url)


# In[25]:


# scrape images of Mars' hemispheres from the USGS site
mars_hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
hemi_dicts = []

for i in range(1,9,2):
    hemi_dict = {}
    
    browser.visit(mars_hemisphere_url)
    time.sleep(1)
    hemispheres_html = browser.html
    hemispheres_soup = bs(hemispheres_html, 'html.parser')
    hemi_name_links = hemispheres_soup.find_all('a', 'product-item')
    hemi_name = hemi_name_links[i].text.strip('Enhanced')
    
    detail_links = browser.find_by_css('a.product-item')
    detail_links[i].click()
    time.sleep(1)
    browser.find_link_by_text('Sample').first.click()
    time.sleep(1)
    browser.windows.current = browser.windows[-1]
    hemi_img_html = browser.html
    browser.windows.current = browser.windows[0]
    browser.windows[-1].close()
    
    hemi_img_soup = bs(hemi_img_html, 'html.parser')
    hemi_img_path = hemi_img_soup.find('img')['src']

    print(hemi_name)
    hemi_dict['title'] = hemi_name.strip()
    
    print(hemi_img_path)
    hemi_dict['img_url'] = hemi_img_path

    hemi_dicts.append(hemi_dict)

