from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import unicodedata
import pandas as pd

def get_uni_info(driver, uni_type, url, uni):
    driver.get(url)
    if uni_type == "cd":
        # Wait for the dropdown to be clickable
        dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "form-selector-custom"))
        )
        dropdown.click()

        # Locate and click on the desired option "Hệ cao đẳng"
        he_cao_dang_option = driver.find_element(By.XPATH, "//li[@class='form-selector-custom__item home_btn_hecaodang']")
        he_cao_dang_option.click()

    input_field = driver.find_element(By.ID, "input_college") 
    # Get info of universities one by one
    input_field.send_keys(uni)
    time.sleep(1)  

    try: 
        uni_a_tag = driver.find_element(By.CSS_SELECTOR, ".lookup__result-name a")
        uni_url = uni_a_tag.get_attribute('href')
    except NoSuchElementException:
        return ""

    driver.get(uni_url)
    try: 
        uni_name = driver.find_element(By.CLASS_NAME, "university__header-title").text
    except NoSuchElementException:
        return ""

    try: 
        code_span = driver.find_element(By.CLASS_NAME, "university__header-code").text
        info_list = code_span.split(": ")[1]
        info_string = info_list.replace(" ", ",", 1)
    except NoSuchElementException:
        info_string = "None,None"

    print(uni_name + "," + info_string)
    return uni_name + "," + info_string + "\n"

driver = webdriver.Chrome()  
url = 'https://diemthi.vnexpress.net/tra-cuu-dai-hoc'
input_file = "random_crawl_src/data-1715525250280.csv"
output_file = "random_crawl_src/additionals.txt"
df = pd.read_csv(input_file)
names = df['name'].tolist()

with open(output_file, 'a', encoding="utf-8") as file:
    for name in names:
        file.write(get_uni_info(driver, "uni", url, name))

driver.quit()
