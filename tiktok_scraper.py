# region imported madules
import time
import pandas as pd
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

import scrape_tools as st
from my_utils import crint


# endregion

def count_to_int(input_text):
    if input_text[-1] == 'K':
        return int(float(input_text[:-1]) * 1000)
    elif input_text[-1] == 'M':
        return int(float(input_text[:-1]) * 1000000)


# region main_code
username = 'healthywomen'
url = f'https://www.tiktok.com/@{username}/'
driver = st.driver_initiation()
crint('bot started!')
# driver.get(url)
st.get_endless_web_selenium(url, driver, False)
time.sleep(25)
crint('sleep time finished')
link_elements = driver.find_elements(By.XPATH, '//a[contains(@class,"AMetaCaptionLine")]')
links = [link_element.get_attribute('href') for link_element in link_elements]

video_counts = driver.find_elements(By.XPATH, "//div[contains(@class, 'DivCardFooter')]")
view_counts = [count_to_int(view_count_element.text) for view_count_element in video_counts]

video_titles = driver.find_elements(By.XPATH, "//div[contains(@class, 'DivDesContainer')]")
titles = [title_element.text for title_element in video_titles]

df = pd.DataFrame([], columns=['caption', 'view_count', 'link', 'likes', 'comments', 'saves', 'shares', 'date'])
for i in range(len(links)):
    crint(links[i])
    driver.get(links[i])
    time.sleep(3)
    try:
        temp_list = [titles[i], view_counts[i], links[i]]
        number_buttons = driver.find_elements(By.XPATH,
                                              '//button[contains(@class,"ButtonActionItem")]')
        temp_text = number_buttons[0].text
        temp_list.append(count_to_int(temp_text))

        temp_text = number_buttons[1].text
        temp_list.append(count_to_int(temp_text))

        temp_text = number_buttons[2].text
        temp_list.append(count_to_int(temp_text))

        temp_text = number_buttons[3].text
        temp_list.append(count_to_int(temp_text))

        date_span = driver.find_elements(By.XPATH,
                                         '//span[contains(@class,"SpanOtherInfos")]')
        temp_text = date_span[0].text.split()
        temp_text = temp_text[-1]
        if 2 < len(temp_text) < 6 and not temp_text.endswith('ago'):
            temp_text = '2024-' + temp_text
        temp_list.append(temp_text)
        df.loc[len(df.index)] = temp_list
    except NoSuchElementException as e:
        print(driver.page_source)
        crint(e)
        driver.quit()
        df.to_excel(username + '.xlsx')
else:
    driver.quit()
    df.to_excel(username + '.xlsx')
# endregion
