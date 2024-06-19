# region imported madules
import random
import json
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import csv
import logging

# endregion

# region initiation
service = Service(executable_path=r'C:/chromedriver.exe')
options = webdriver.ChromeOptions()
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=service, options=options)
# endregion

# region main_code
# story_buttons=driver.find_elements(By.CSS_SELECTOR,"button[class=_aam8]")
username='healthywomen'
driver.get(f'https://www.tiktok.com/@{username}')

time.sleep(40)

SCROLL_PAUSE_TIME = 2
last_height = driver.execute_script("return document.body.scrollHeight")

for i in range(4):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
# <div class="css-11u47i-DivCardFooter e148ts220"><svg class="like-icon css-h342g4-StyledPlay e148ts225" width="18" data-e2e="" height="18" viewBox="0 0 48 48" fill="#fff" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M16 10.554V37.4459L38.1463 24L16 10.554ZM12 8.77702C12 6.43812 14.5577 4.99881 16.5569 6.21266L41.6301 21.4356C43.5542 22.6038 43.5542 25.3962 41.6301 26.5644L16.5569 41.7873C14.5577 43.0012 12 41.5619 12 39.223V8.77702Z"></path></svg><strong data-e2e="video-views" class="video-count css-dirst9-StrongVideoCount e148ts222">696.1K</strong></div>

class_name="video-count"
video_counts = driver.find_elements(By.XPATH, "//div[contains(@class, 'DivCardFooter')]")
video_titles = driver.find_elements(By.XPATH, "//div[contains(@class, 'DivDesContainer')]")

data=[]
fields=['title','count']
for i in range(min(len(video_titles),len(video_counts))):
    temp_dict={"title":video_titles[i].text,"count":video_counts[i].text}
    data.append(temp_dict)

output_file = 'tiktok_video_views.csv'

def save_to_csv(data, output_file,fields):
    with open(output_file, 'w',encoding='UTF-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
    
        # writing headers (field names)
        writer.writeheader()
    
        # writing data rows
        writer.writerows(data)
        
save_to_csv(data, output_file, fields)
driver.quit()