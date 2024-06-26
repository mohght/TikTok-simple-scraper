from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests


def driver_initiation():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Ensure GUI is off
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-web-security")  # Disable CORS policy
    chrome_options.add_argument("--disable-site-isolation-trials")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

    # Set path to chromedriver as per your configuration
    webdriver_service = Service('c:/chromedriver.exe')  # Use your specified path

    # Initialize the WebDriver
    return webdriver.Chrome(service=webdriver_service, options=chrome_options)


def get_tiktok_photo_details_by_selenium(url="https://www.tiktok.com/@healthywomen/photo/7381131641588075808"):
    driver = driver_initiation()
    try:
        driver.get(url)
        time.sleep(10)
        # Wait for the likes element to be present
        likes_tag = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="main-content-video_detail"]/div/div[2]/div[1]/div[1]/div[1]/div[3]/button[1]'))
        )
        # Extract likes
        number_of_likes = likes_tag.text if likes_tag else 'N/A'

        # Extract comments
        comments_tag = driver.find_element(By.XPATH,
                                           '//*[@id="main-content-video_detail"]/div/div[2]/div[1]/div[1]/div[1]/div[3]/button[2]')
        number_of_comments = comments_tag.text if comments_tag else 'N/A'

        # Extract shares
        shares_tag = driver.find_element(By.XPATH,
                                         '//*[@id="main-content-video_detail"]/div/div[2]/div[1]/div[1]/div[1]/div[3]/button[3]')
        number_of_shares = shares_tag.text if shares_tag else 'N/A'

        # Extract shares
        saves_tag = driver.find_element(By.XPATH,
                                        '//*[@id="main-content-video_detail"]/div/div[2]/div[1]/div[1]/div[1]/div[3]/button[4]')
        number_of_saves = saves_tag.text if shares_tag else 'N/A'

        # Extract creation date
        date_tag = driver.find_element(By.XPATH,
                                       '//*[@id="main-content-video_detail"]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div/a[2]/span[2]')
        date_of_creation = date_tag.text if date_tag else 'N/A'

        return {
            "number_of_likes": number_of_likes,
            "number_of_comments": number_of_comments,
            "number_of_saves": number_of_saves,
            "number_of_shares": number_of_shares,
            "date_of_creation": date_of_creation
        }
    except Exception as e:
        return {"error": f"Failed to extract photo details: {str(e)}"}
    finally:
        driver.quit()


def get_tiktok_photo_details_by_bs4(url="https://www.tiktok.com/@healthywomen/photo/7381131641588075808"):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    # print(page.content)
    with open('temp.html', 'wb') as hf:
        hf.write(page.content)


def save_web_selenium(url, file_name, driver, endless=False):
    driver.get(url)
    time.sleep(10)
    print(driver.page_source)
    if endless:
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    content = driver.page_source
    with open(file_name, 'w', encoding="utf-8") as hf:
        hf.write(content)


def get_endless_web_selenium(url, driver, login_needed=False):
    driver.get(url)
    if login_needed:  # need time for manual login
        time.sleep(200)
    else:
        time.sleep(10)
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    return driver.page_source


def soup_from_file(file_url):
    with open(file_url, 'rb') as fp:
        return BeautifulSoup(fp, 'html.parser')


def soup_from_url(url):
    page = requests.get(url)
    return BeautifulSoup(page.content, 'html.parser')


def find_in_soup_contain(soup, tag, attr, partial_text):
    return soup.select(tag + '[' + attr + '*="' + partial_text + '"]')


def driver_page_source_to_html(page_source_, output_file_):
    with open(output_file_, 'w') as of:
        of.write(page_source_)
