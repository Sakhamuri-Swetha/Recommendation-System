
'''
#Webscraping the Actors, Directors, Genre and Title from Wiki Links. 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd


driver_path = "./chromedriver.exe" 
service = Service(driver_path)
driver = webdriver.Chrome(service=service)
dramas_data = []

try:
    url = "https://en.wikipedia.org/wiki/List_of_Korean_dramas"
    driver.get(url)
    time.sleep(2)
    drama_elements = driver.find_elements(By.CSS_SELECTOR, "div.div-col ul li a")

   
    for i, element in enumerate(drama_elements):
        drama_name = element.text
        drama_link = element.get_attribute("href")
        driver.get(drama_link)
        time.sleep(2)  
        try:
            title = driver.find_element(By.ID, "firstHeading").text
            info_box = driver.find_element(By.CLASS_NAME, "infobox")  
            rows = info_box.find_elements(By.TAG_NAME, "tr")
            actors = []
            directors = []
            genre = []

            for row in rows:
                header = row.find_element(By.TAG_NAME, "th").text if row.find_elements(By.TAG_NAME, "th") else ""
                data = row.find_element(By.TAG_NAME, "td").text if row.find_elements(By.TAG_NAME, "td") else ""
                
                if "Directed by" in header:
                    directors = [d.strip() for d in data.split("\n")]
                elif "Starring" in header:
                    actors = [a.strip() for a in data.split("\n")]
                elif "Genre" in header:
                    genre = [g.strip() for g in data.split("\n")]
            dramas_data.append({
                "Title": title,
                "Actors": actors if actors else ["N/A"],
                "Directors": directors if directors else ["N/A"],
                "Genre": genre if genre else ["N/A"],
                "Link": drama_link
            })
        except Exception as e:
            print(f"Failed to extract details for {drama_name}. Error: {e}")
        driver.back()
        time.sleep(2)

finally:
    driver.quit()
dataset = pd.DataFrame(dramas_data)
print("\nK-Drama Dataset:")
print(dataset)
dataset.to_csv("kdrama_dataset.csv", index=False)

#Web Scraping for IMDb links
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from random import randint
kdrama_dataset = pd.read_csv('kdrama_dataset.csv')
driver_path = './chromedriver.exe'  
service = Service(driver_path)
driver = webdriver.Chrome(service=service)
imdb_links = {}
for title in kdrama_dataset['Title']:
    search_query = f"{title} IMDb"
    search_url = f"https://search.yahoo.com/search?p={'+'.join(search_query.split())}"
    
    print(f"Searching for: {title}")
    driver.get(search_url)
    time.sleep(randint(2, 5))  # Random delay to avoid detection  
    try:
        search_results = driver.find_elements(By.CSS_SELECTOR, "ol.searchCenterMiddle li a")
        for result in search_results:
            link = result.get_attribute("href")
            if "imdb.com" in link:
                imdb_links[title] = link
                print(f"Found IMDb link for {title}: {link}")
                break
        else:
            imdb_links[title] = "No IMDb link found"
            print(f"No IMDb link found for {title}")
    except Exception as e:
        imdb_links[title] = "Error"
        print(f"Error while searching for {title}: {e}")
driver.quit()
kdrama_dataset['IMDb_Link'] = kdrama_dataset['Title'].map(imdb_links)
output_file = 'kdrama_dataset_with_imdb_yahoo.csv'
kdrama_dataset.to_csv(output_file, index=False)
print(f"\nIMDb links have been added to the dataset and saved to '{output_file}'.")
print("\nPreview of the Updated Dataset:")
print(kdrama_dataset.head())


# Getting the Rating, Plot and Poster after getting the IMDb Link. 

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

kdrama_dataset = pd.read_csv('kdrama_dataset_with_imdb_yahoo.csv')  
service = Service('./chromedriver.exe')  
driver = webdriver.Chrome(service=service)
ratings = []
plots = []
images = []


for index, row in kdrama_dataset.iterrows():
    imdb_link = row['IMDb_Link']
    wiki_link = row['Link']
    if imdb_link != "No IMDb link found" and imdb_link != "Error":
        try:
            driver.get(imdb_link)
            time.sleep(2)  
            # Get IMDb rating
            try:
                rating_element = driver.find_element(By.CSS_SELECTOR, 
                    "[data-testid='hero-rating-bar__aggregate-rating__score'] span")
                ratings.append(rating_element.text)
            except:
                ratings.append("No rating")
            # Get IMDb plot
            try:
                plot_elements = driver.find_elements(By.CSS_SELECTOR, "[data-testid^='plot']")
                plot_text = " ".join([plot.text for plot in plot_elements])  # Combine all plot text
                plots.append(plot_text if plot_text else "No plot")
            except:
                plots.append("No plot")
        except Exception as e:
            ratings.append("Error")
            plots.append(f"Error: {str(e)}")
    else:
        ratings.append("No IMDb link")
        plots.append("No IMDb link")
    # Fetch Wiki Poster image if Wiki link is available
    if wiki_link != "No Wiki link found" and wiki_link != "Error":
        try:
            driver.get(wiki_link)
            time.sleep(2)  

            # Get image URL
            try:
                image_element = driver.find_element(By.CSS_SELECTOR, ".infobox-image img")
                image_url = image_element.get_attribute('src')
                images.append(image_url)
            except:
                images.append("No image")

        except Exception as e:
            images.append(f"Error: {str(e)}")
    else:
        images.append("No Wiki link")

driver.quit()

kdrama_dataset['IMDb_Rating'] = ratings
kdrama_dataset['Plot'] = plots
kdrama_dataset['Poster_Image'] = images
output_file = 'kdrama_dataset_with_ratings_plots_and_images.csv'
kdrama_dataset.to_csv(output_file, index=False)
print(f"\nIMDb ratings, plots, and poster images have been added to the dataset and saved to '{output_file}'.")
print("\nPreview of the Updated Dataset:")
print(kdrama_dataset.head())
'''