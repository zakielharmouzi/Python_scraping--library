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
LINKS = []
try:
    driver = webdriver.Chrome(ChromeDriverManager().install())
    url = 'https://libserv.aui.ma/search/X'
    driver.get(url)
    page_content = driver.page_source
    response = Selector(text=driver.page_source)
    time.sleep(5)
    key = 'biology'
    element = driver.find_element(By.XPATH, '//*[@id="st1"]')
    element.send_keys(key)
    element = driver.find_element(By.XPATH, '//*[@id="m"]/option[3]').click()
    time.sleep(5)
    element = driver.find_element(By.XPATH, '//*[@id="search"]/table/tbody/tr/td[2]/font/a').click()
    time.sleep(5)
    table = driver.find_element(By.XPATH, '/html/body/table/tbody/tr[3]/td[1]/table/tbody/tr[4]')
    count = 0  
    num = driver.find_element(By.XPATH, '/html/body/table/tbody/tr[2]/td[1]/ul/li[10]').get_attribute("innerText")
    num = int(num)
    # FIX: go through all the pages until you encounter the Next word and then assign num to the number of pages
    print(num)
    for j in range(1, num):
        try:
            if(j != 1):
                driver.find_element(By.XPATH, '//*[@id="id_icon_paging_prev"]').click()
        except:
            break
        # add 53 here instead of 11
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
    print('Done')
    

driver = webdriver.Chrome(ChromeDriverManager().install())
B_titles = []
B_Authors = []
B_Isbn = []
Temp = []
for z in range(len(LINKS)):
    try:
        driver.get(LINKS[z])
        page_content = driver.page_source
        response = Selector(text=driver.page_source)
        time.sleep(2)
        for i in range(1,4):
            try:
                element = driver.find_element(By.XPATH, '//*[@id="infoTable"]/table[1]/tbody/tr/td/table/tbody/tr['+str(i)+']').get_attribute("innerText")
                if(element.find('Title') != -1):
                    B_titles.append(element)
                    print(element)
            except:
                break
        element = driver.find_element(By.ID, 'bibFullRecord').click()
        time.sleep(1)
        for i in range(1,3):
            for j in range(1,11):
                try:
                    element = driver.find_element(By.XPATH, '/html/body/div[4]/div/div[3]/div/span[4]/table['+str(i)+']/tbody/tr/td/table/tbody/tr['+str(j)+']/td[1]').get_attribute("innerText")
                    if(element.find('Author') != -1):
                        element = driver.find_element(By.XPATH, '/html/body/div[4]/div/div[3]/div/span[4]/table['+str(i)+']/tbody/tr/td/table/tbody/tr['+str(j)+']/td[2]').get_attribute("innerText")
                        B_Authors.append(element)
                        print(element)
                    elif(element.find('ISBN') != -1):
                        element = driver.find_element(By.XPATH, '/html/body/div[4]/div/div[3]/div/span[4]/table['+str(i)+']/tbody/tr/td/table/tbody/tr['+str(j)+']/td[2]').get_attribute("innerText")
                        B_Isbn.append(element)
                        print(element)
                    elif(element.find('Added Author')!= -1):
                        element = driver.find_element(By.XPATH, '/html/body/div[4]/div/div[3]/div/span[4]/table['+str(i)+']/tbody/tr/td/table/tbody/tr['+str(j)+']/td[2]').get_attribute("innerText")  
                        B_Authors = B_Authors + element.split(';')
                        print(element)
                except:
                    break
    except:
        print('Failed to retrieve info')

excel_file = 'BookData.xlsx'
for i in range(len(B_titles)):
    Temp.append([B_titles[i], B_Authors[i], B_Isbn[i]])
    df = pd.DataFrame(Temp, columns = ['Title', 'Author', 'ISBN'])
    df.to_excel(excel_file)