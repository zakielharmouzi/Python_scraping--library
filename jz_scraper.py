from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import json
import re
import pandas as pd
from parsel import Selector 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


# def print_to_excel(LINKS):
#     df = pd.DataFrame(columns=['Link'])
#     for i in range(len(LINKS)):
#         df.loc[i, 'Link'] = LINKS[i]
#     df.to_excel("links.xlsx", index=False)

driver = webdriver.Chrome(ChromeDriverManager().install())
url = 'https://libserv.aui.ma/'
driver.get(url)
page_content = driver.page_source
response = Selector(text=driver.page_source)
time.sleep(5)
key = 'biology'
element = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[2]/div[1]/table/tbody/tr/td[1]/form/input[1]')
element.send_keys(key)
element.send_keys(Keys.ENTER)
time.sleep(5)
table = driver.find_element(By.XPATH, '/html/body/table/tbody/tr[3]/td[1]/table/tbody/tr[4]')
LINKS = []
count = 0  
num = driver.find_element(By.XPATH, '/html/body/table/tbody/tr[2]/td[1]/ul/li[11]').get_attribute("innerText")
# cast num to int
num = int(num)
for j in range(1, num):
    driver.find_element(By.XPATH, '//*[@id="id_icon_paging_prev"]').click()
    for i in range(4, 53):
        element = driver.find_element(By.XPATH, '/html/body/table/tbody/tr[3]/td[1]/table/tbody/tr['+str(i)+']')
        if element == None:
            break
        # fix this elif statement wa wa
        elif element == driver.find_element(By.XPATH,'/html/body/table/tbody/tr[3]/td[1]/table/tbody/tr[22]/td'):
            break
        else:
            driver.execute_script("arguments[0].scrollIntoView();", element)
            LINKS.append(driver.find_element(By.XPATH, '/html/body/table/tbody/tr[3]/td[1]/table/tbody/tr['+str(i)+']/td/table/tbody/tr[1]/td[3]/span[1]/a').get_attribute("href"))
            count += 1
            print(count, LINKS[count-1])
        
for z in range(count):
    print(z)
    print(LINKS[z])

# element = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[2]/div[1]/table/tbody/tr/td[1]/form/input[1]')
# element.send_keys(key)
# element.send_keys(Keys.ENTER)
# time.sleep(5)
# # table = driver.find_element(By.XPATH, '/html/body/table/tbody/tr[3]/td[1]/table/tbody/tr[4]')
# src = []
# names = []
# counter = 0
# f_ile = open("data.txt", "w")
# count = driver.find_element(By.XPATH, '/html/body/table/tbody/tr[2]/td[1]/ul/li[11]/a').get_attribute("innerText")
# # for j in range(1, int(count)+1):
# for j in range(1, 3):
#     driver.find_element(By.XPATH, '//*[@id="id_icon_paging_prev"]').click()
#     # time.sleep(5)
#     for i in range(4, 50):
#         element = driver.find_element(By.XPATH, '/html/body/table/tbody/tr[3]/td[1]/table/tbody/tr['+str(i)+']')
#         if element == None:
#             break
#         else:
#             driver.execute_script("arguments[0].scrollIntoView();", element)
#             imgResults = driver.find_element(By.XPATH, '/html/body/table/tbody/tr[3]/td[1]/table/tbody/tr['+str(i)+']/td/table/tbody/tr[1]/td[2]/a/img').get_attribute("src")
#             print(imgResults,i)
#             src.append(imgResults)
#             name = driver.find_element(By.XPATH, '/html/body/table/tbody/tr[3]/td[1]/table/tbody/tr['+str(i)+']/td/table/tbody/tr[1]/td[3]/span[1]').get_attribute("innerText")
#             print(name,i)
#             names.append(name)

# for i in range(0, len(src)):
#     f_ile.write(src[i]+","+names[i]+'\n')

# time.sleep(10)

# element = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[241]/div/a')

# time.sleep(5)
# driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[3]/div/a').click()
# time.sleep(25)


# time.sleep(5)
# for i in range(1, 230):
#     element = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div['+str(i+1)+']')
#     if element == None:
#         break
#     else:
#         driver.execute_script("arguments[0].scrollIntoView();", element)
#         # time.sleep(10)
# j = 1
# for i in range(3, 230,2):
#     element = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div['+str(j+3)+']')
#     # if element == None:
#     #     break
#     # else:
#     driver.execute_script("arguments[0].scrollIntoView();", element)
#     driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div['+str(i)+']/div/a').click()
#     # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div['+str(i)+']/div/a'))).click()
#     names = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div[1]/div[1]/div[1]/h1').get_attribute("innerText")
#     print(names)
#     time.sleep(2)


# # driver.execute_script("arguments[0].scrollIntoView();", element)
# time.sleep(5)

# results = []
# for el in response.xpath('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div'):
#     results.append({
#         # 'link': el.xpath('./a/@href').extract_first(''),

#         'title': el.xpath('./a/@aria-label').extract_first('')
#     })
# print(results)
# # Create a list to store the names of the gas stations
