from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

# input_file = "uni_names.txt"
# output_file = "uni_info.txt"
# uni = []
# cao_dang = []
# with open(input_file, "r", encoding="utf-8") as file:
#     for line in file:
#         if "Cao đẳng" in line:
#             cao_dang.append(line)
#         else:
#             uni.append(line)

driver = webdriver.Chrome()  

url = 'https://diemthi.vnexpress.net/tra-cuu-dai-hoc'
driver.get(url)

input_field = driver.find_element(By.ID, "input_college") 

# Get info of universities one by one
input_field.send_keys('BMU')
time.sleep(2)  

uni_a_tag = driver.find_element(By.CSS_SELECTOR, ".lookup__result-name a")
uni_url = uni_a_tag.get_attribute('href')
print(uni_url)

driver.get(uni_url)

code_span = driver.find_element(By.CLASS_NAME, "university__header-code").text
info_list = code_span.split(": ")[1]
info_string = info_list.replace(" ", ", ", 1)
print("Text:", info_string)

driver.quit()
