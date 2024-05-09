from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import unicodedata

input_file = "uni_names.txt"
output_file = "uni_info.txt"
all_uni_names = set()
unis = []
cao_dang = []
with open(input_file, "r", encoding="utf-8") as file:
    for line in file:
        if "Cao đẳng" in line:
            cao_dang.append(line)
        else:
            unis.append(line)

def convert_to_url(input_string):
    input_string = input_string.lower()
    
    # Remove non-word characters
    input_string = re.sub(r'[^\w\s-]', '', input_string)
    
    # Remove diacritics
    input_string = ''.join(c for c in unicodedata.normalize('NFD', input_string) if unicodedata.category(c) != 'Mn')
    
    string_list = input_string.split(" ")
    if "-" in string_list:
        string_list.remove("-")

    input_string = "-".join(string_list)
    
    result = input_string.replace("đ", "d")
    
    return result

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
    time.sleep(2)  

    try: 
        uni_a_tag = driver.find_element(By.CSS_SELECTOR, ".lookup__result-name a")
        uni_url = uni_a_tag.get_attribute('href')
    except NoSuchElementException:
        return ""
    # if uni_url in all_unis_urls_set:
    #     return uni.strip() + ", " + "None" + ", " + "None, None" + ", " + "None" + ", " + "None"
    # else:
        # if convert_to_url(uni_name) not in uni_url:
        #     return uni_name.strip() + ", " + "None" + ", " + "None, None" + ", " + "None" + ", " + "None"
        #all_unis_urls_set.add(uni_url)
        #print(uni_url)

    driver.get(uni_url)
    try: 
        uni_name = driver.find_element(By.CLASS_NAME, "university__header-title").text
    except NoSuchElementException:
        return ""
    
    if uni_name in all_uni_names:
        return ""
    all_uni_names.add(uni_name)

    try: 
        code_span = driver.find_element(By.CLASS_NAME, "university__header-code").text
        info_list = code_span.split(": ")[1]
        info_string = info_list.replace(" ", ", ", 1)
        print("Header:", info_string)
    except NoSuchElementException:
        info_string = "None, None"

    try:
        uni_total = driver.find_element(By.CLASS_NAME, "university__method-total").text
    except NoSuchElementException:
        uni_total = "None"

    try:
        uni_method_lists = driver.find_element(By.CLASS_NAME, "university__method-list").text
        uni_methods = "{ " + " | ".join(uni_method_lists.split("\n")) + " }"
    except NoSuchElementException:
        uni_methods = "None"  
    print("Total: ", uni_total)
    print("Methods: ", uni_methods)
    return uni_name + ", " + uni_url + ", " + info_string + ", " + uni_total + ", " + uni_methods  + "\n"

driver = webdriver.Chrome()  
url = 'https://diemthi.vnexpress.net/tra-cuu-dai-hoc'

with open(output_file, "a", encoding="utf-8") as output_f:
    for uni in unis:
        output_f.write(get_uni_info(driver, "uni", url, uni))
        time.sleep(1)  

    for cd in cao_dang:
        output_f.write(get_uni_info(driver, "cd", url, cd))  
        time.sleep(1)

driver.quit()
