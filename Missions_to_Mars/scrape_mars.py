# import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def scrape():

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # ### NASA Mars News

    # visit Mars news website and take HTML code
    url = 'https://redplanetscience.com'
    browser.visit(url)
    html = browser.html

    # convert HTML to BeautifulSoup and pretty print to search through for needed content
    soup = bs(html, "html.parser")
    #print(soup.prettify())

    # locate most recent article title
    news_title = browser.find_by_xpath('//*[@id="news"]/div[1]/div/div[2]/div/div[2]').text
    #news_title

    # locate most recent article paragraph
    news_p = browser.find_by_xpath('//*[@id="news"]/div[1]/div/div[2]/div/div[3]').text
    #news_p

    # ### JPL Mars Space Images - Featured Image

    # visit Mars Space Images website and take HTML code
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    html=browser.html

    # parse for the featured image source
    browser.find_by_xpath('/html/body/div[1]/div/a/button').click()

    # append entire url with featured image source
    featured_image_url = browser.find_by_xpath('/html/body/div[8]/div/div/div/div/img')['src']
    
    # print for verification
    #featured_image_url

    # convert HTML to BeautifulSoup and pretty print to search through for needed content
    soup = bs(html, "html.parser")
    #print(soup.prettify())


    # ### Mars Facts

    # visit Mars Space Images website using pandas and take HTML code
    url = 'https://galaxyfacts-mars.com'
    browser.visit(url)

    # specify table to target, rename columns, and set index
    df_table = pd.read_html('https://galaxyfacts-mars.com')[0]
    df_table.columns=['Description', 'Mars', 'Earth']
    df_table.set_index('Description', inplace = True)
    #df_table

    # convert dataframe back to html and display
    mars_facts_html = df_table.to_html()


    # ### Mars Hemispheres

    # visit Mars Hemispheres website and take HTML code
    base_url = "https://marshemispheres.com/"
    browser.visit(base_url)
    html = browser.html

    # convert HTML to BeautifulSoup and pretty print to search through for needed content
    soup = bs(html, "html.parser")
    #print(soup.prettify())

    # use BeautifulSoup to find all div with specified class
    div_list = soup.body.find_all("div", class_="description")

    # create empty list
    sites = []

    # cycle through each div returned
    for div in div_list:
        
        # find the a element with specified class in the div element and pull the data for href to get the end location for the full image
        site = div.find("a", class_="product-item")["href"]
        
        # append site href to list
        sites.append(site)

    # display list
    #sites

    # create empty list to store dictionaries
    hemisphere_image_urls = []

    # cycle through each site href
    for site in sites:
        try:
            
            # visit specifichemisphere page and take HTML code
            url = base_url + site
            browser.visit(url)
            html = browser.html
            
            # convert HTML to BeautifulSoup
            soup = bs(html, "html.parser")
            
            # use BeautifulSoup to find image with specified class and access source of image
            img_url_ending = soup.body.find("img", class_="wide-image")["src"]
            
            # add base url to the image source to get full url
            img_url = base_url + img_url_ending
            
            # use title on page, removing unneeded trailing " Enhanced" to get title
            title = soup.body.find("h2", class_="title").text.strip()[:-9]
            
            # append dictionary of information to list
            hemisphere_image_urls.append({"title": title, "img_url": img_url})
        except Exception as e:
            print(e)

    # print dictionary
    #print(hemisphere_image_urls)

    browser.quit()

    ##### create one dictionary for return of all scraped info

    scraped_data = {
        "NewsTitle": news_title,
        "NewsParagraph": news_p,
        "FeaturedImage": featured_image_url,
        "MarsFactsTable": mars_facts_html, 
        "HemisphereImages": hemisphere_image_urls
    }

    return scraped_data 