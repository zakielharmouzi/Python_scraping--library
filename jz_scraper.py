from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from parsel import Selector 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import re
# remove the following line if you already have the chromedriver installed

LINKS = []
try:
    driver = webdriver.Chrome(ChromeDriverManager().install())
    url = 'https://libserv.aui.ma/search/X'
    driver.get(url)
    page_content = driver.page_source
    response = Selector(text=driver.page_source)
    time.sleep(5)
    key = 'Mathematics'
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
    # adjust the range here to include all the pages(replace 3 with num)
    for j in range(1, 3):
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
B_paper_type = []
Temp = []
publication_info = []
for z in range(len(LINKS)):
    try:
        driver.get(LINKS[z])
        page_content = driver.page_source
        response = Selector(text=driver.page_source)
        time.sleep(0.5)
        for i in range(1,4):
            try:
                element = driver.find_element(By.XPATH, '//*[@id="infoTable"]/table[1]/tbody/tr/td/table/tbody/tr['+str(i)+']').get_attribute("innerText")
                if(element.find('Title') != -1):
                    B_titles.append(element)
                    print(element)
                if(element.find('Publication') != -1):
                    publication_info.append(element)
                    print(element)
            except:
                break
        element = driver.find_element(By.ID, 'bibFullRecord').click()
        time.sleep(0.5)
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

for i in range(len(B_titles)):
    B_titles[i] = B_titles[i].replace('Title', '')
    # remove the space at the beginning of the string
    B_titles[i] = B_titles[i][1:]
    # remove the space at the end of the string
    B_titles[i] = B_titles[i][:-1]
    # remove the / and everything after it
    B_titles[i] = B_titles[i].split('/')[0]
    print(B_titles[i])
num_isbn = []
temp1 = []
for i in range(len(B_Isbn)):
    try:
        publication_info[i] = publication_info[i].replace('Publication Info.', '')
        B_Isbn[i] = B_Isbn[i].replace('ISBN', '')
        B_Isbn[i] = B_Isbn[i][1:]
        B_Isbn[i] = B_Isbn[i][:-1]
        temp1 = B_Isbn[i].split(' ')
        num_isbn.append(temp1[0])
    except:
        print('Failed to remove ISBN')

excel_file = 'BookData.xlsx'
for i in range(len(B_titles)):
    try:
        Temp.append([B_titles[i], B_Authors[i],num_isbn[i],'Mathematics',publication_info[i],'Available'])
        df = pd.DataFrame(Temp, columns = ['Title', 'Author', 'ISBN', 'Category','Publication_info','status'])
        df.to_excel(excel_file)
    except:
        print('Failed to add to excel file')