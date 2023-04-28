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

try:
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
    num = int(num)
    for j in range(1, num):
        try:
            driver.find_element(By.XPATH, '//*[@id="id_icon_paging_prev"]').click()
        except:
            break
        for i in range(4, 53):
            try:
                element = driver.find_element(By.XPATH, '/html/body/table/tbody/tr[3]/td[1]/table/tbody/tr['+str(i)+']')
            except:
                break
            if element == None:
                break
            # fix this elif statement
            elif element == driver.find_element(By.XPATH,'/html/body/table/tbody/tr[3]/td[1]/table/tbody/tr[22]/td'):
                break
            else:
                try:
                    driver.execute_script("arguments[0].scrollIntoView();", element)
                    LINKS.append(driver.find_element(By.XPATH, '/html/body/table/tbody/tr[3]/td[1]/table/tbody/tr['+str(i)+']/td/table/tbody/tr[1]/td[3]/span[1]/a').get_attribute("href"))
                    count += 1
                    print(count, LINKS[count-1])
                except:
                    print('Failed to retrieve link')
        
    for z in range(count):
        try:
            print(z)
            print(LINKS[z])
        except:
            print('Failed to print link')
            
except Exception as e:
    print('Error:', e)

finally:
    driver.quit()
    print('Done')
    
