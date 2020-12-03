
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "/Users/nicolemuscanell/ChromeDriver/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    # Initialize the browser
    browser = init_browser()

    #### Visit NASA's mars page and scrape the first news title and pagraph ###
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the first news title
    title_results = soup.find_all('div', class_='content_title')
    news_title = title_results[0].text

    # Get paragraph text for that title
    paragraph_results = soup.find_all('div', class_='article_teaser_body')
    news_p = paragraph_results[0].text
    
    ### Visit NASA's mars page to scrape featured image ###

    # Initialize the browser
    browser = init_browser()

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    time.sleep(1)

    # Click through pages to find the url for the full image
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    browser.click_link_by_partial_text('more info')

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Find featured image url
    image = soup.find('figure', class_='lede').a['href']
    featured_image_url = 'https://www.jpl.nasa.gov' + image

    ### Visit the Space Facts webpage and use Pandas to scrape the Mars facts table ###
    
    # Initialize the browser
    browser = init_browser()

    # Scrape table data from page
    tables = pd.read_html('https://space-facts.com/mars/')

    # Turn into a DataFrame
    mars_facts = tables[0]

    # Rename columns
    mars_facts.columns=['Feature', 'Record']

    # Reset index
    mars_facts.set_index('Feature', inplace=True)

    # Convert table to html
    mars_table = mars_facts.to_html(header=True, index=True)

    ### Visit the astrogeology page and scrape info on the Mars' hemispheres ###
    
    # Initialize the browser
    browser = init_browser()

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Create an empty list to store hemisphere names
    hemisphere_names = []

    # Search for image titles (hemisphere names)
    hemispheres = soup.find_all('div', class_='collapsible results')
    names = hemispheres[0].find_all("h3")

    # Add hemisphere names to the list
    for name in names:
        hemisphere_names.append(name.text.strip('Enhanced'))
    
    # Create empty list to store image urls
    links = []

    # Locate image links
    urls = soup.find_all("div", class_="item")

    # Add base link to image links and append to the list
    for url in urls:
        hemis_links = url.find('a')['href']
        path = 'https://astrogeology.usgs.gov' + hemis_links
        links.append(path)
    
    # Finding urls to full sized images for each hemisphere
    image_url = []

    # Click each image link 
    for link in links:
        browser.visit(link)
        html = browser.html
        soup = bs(html, 'html.parser')
    
        # Find full jpgs
        url = soup.find_all('img', class_='wide-image')
     
        full_urls = url[0]['src']
        
        # Add base link to image links and append to the list
        final_path = 'https://astrogeology.usgs.gov' + full_urls
       
        image_url.append(final_path)

    # Zip lists
    hemis_zip = zip(hemisphere_names, image_url)

    # Ceate a new list to store dictionaries
    hemisphere_image_urls = []

    # Add name and url image lists to dictionaries
    for name,img in hemis_zip:
        hemispheres_dict = {}
    
        # Add hemisphere name to dictionary
        hemispheres_dict['hemisphere_names'] = name
    
        # Add image url to dictionary
        hemispheres_dict['image_url'] = img
     
        # Append the list with dictionaries
        hemisphere_image_urls.append(hemispheres_dict)
 
    # Store all mars data in the dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_table": mars_table,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data