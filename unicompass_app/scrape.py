from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import os
import base64
import csv

def scrape_apartment_data(base_url):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    
    # Set up the Chrome WebDriver
    service = Service('C:\\Users\\User\\Desktop\\chromedriver-win64\\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Create a directory to store the images
        if not os.path.exists('apartment_images'):
            os.makedirs('apartment_images')

        # Create and open a CSV file to store apartment details
        with open('apartment_details.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            page = 1
            total_images = 0
            
            while page < 3:
                url = f"{base_url}?page={page}"
                print(f"Navigating to {url}")
                driver.get(url)

                # Wait for the content to load
                wait = WebDriverWait(driver, 10)
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "new_list_item")))

                print(f"Page {page} loaded, parsing content")
                soup = BeautifulSoup(driver.page_source, 'html.parser')

                # Find all div elements with class 'new_list_item'
                apartment_divs = soup.find_all('div', class_='new_list_item')
                print(f"Found {len(apartment_divs)} apartment divs on page {page}")

                if not apartment_divs:
                    print("No more apartments found. Ending scrape.")
                    break

                # Iterate through each apartment div
                for div in apartment_divs:
                    # Find the img tag within the specific structure
                    img_tag = div.select_one('div.img_box div.img_link_line a.img_link img')
                    
                    # Find the title div
                    title_div = div.select_one('div.description_box div.title_line div.title_link')
                    
                    if img_tag and img_tag.has_attr('src') and title_div:
                        # Get the image URL
                        img_url = 'https://www.novostroy-m.ru' + img_tag['src']
                        print(f"Found image URL: {img_url}")
                        
                        # Extract apartment details
                        title_text = title_div.get_text(strip=True)
                        rooms = title_text.split()[0]
                        area = title_text.split()[1]
                        price = title_div.select_one('span.def_black').get_text(strip=True).split()[0]
                        
                        try:
                            # Use Selenium to load the image
                            driver.get(img_url)
                            
                            # Wait for the image to load
                            wait.until(EC.presence_of_element_located((By.TAG_NAME, "img")))
                            
                            # Get the image as base64
                            img_base64 = driver.execute_script("""
                                var img = document.querySelector('img');
                                var canvas = document.createElement('canvas');
                                canvas.width = img.width;
                                canvas.height = img.height;
                                var ctx = canvas.getContext('2d');
                                ctx.drawImage(img, 0, 0);
                                return canvas.toDataURL('image/jpeg').split(',')[1];
                            """)
                            
                            # Decode and save the image
                            img_data = base64.b64decode(img_base64)
                            total_images += 1
                            image_filename = f'apartment_{total_images}.jpg'
                            with open(f'apartment_images/{image_filename}', 'wb') as f:
                                f.write(img_data)
                            
                            print(f"Downloaded image {total_images}")
                            
                            # Write apartment details to CSV
                            csv_writer.writerow([rooms, area,])
                            
                            # Add a delay between requests
                            time.sleep(1)
                        except Exception as e:
                            print(f"Error processing apartment {total_images}: {e}")
                    else:
                        print(f"Missing image or title for apartment {total_images + 1}")

                # Move to the next page
                page += 1

        print(f"Scraping completed. Total apartments processed: {total_images}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

# Usage
base_url = 'https://www.novostroy-m.ru/kvartiry/novostroyka/jk_symphony_34_simfoniya/trehkomnatnye'
scrape_apartment_data(base_url)