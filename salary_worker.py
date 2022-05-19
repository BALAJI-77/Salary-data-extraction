import redis
from os import remove
from flask import Flask,request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
import time as time_delay
import asyncio
import threading
import json
from pymongo import MongoClient


skill_extraction=[]
india=[]
US=[]
Australia=[]
position2=[]
avg_india=[]
avg_US=[]
avg_Australia=[]
avg_values={}


# print(avg_values)
website_values={'Australia':Australia,'India':india,'US':US}
all_values={"position":position2,"website_salary":website_values,"average_salary":avg_values,"Required_Skills":skill_extraction}


def mongodb(name):
    values={"Name - "+name :all_values}
    client = MongoClient('localhost', 27017)
    # mydatabase = client['testdb']
    mydatabase = client['Salary_Data']
    # mydatabase.testcol.insert_one(values)
    mydatabase.salaryDB.insert_one(values)


def average_values():
    sum_india=[]
    for string in avg_india:
        new_string = (str(string).replace(",","")).replace('₹','')
        sum_india.append(int(new_string))
    sum_US=[]
    for string in avg_US:
        new_string = (str(string).replace(",","")).replace('$','')
        sum_US.append(int(new_string))
    sum_Australia=[]
    for string in avg_Australia:
        new_string = (str(string).replace(",","")).replace('$','')
        sum_Australia.append(int(new_string))
    Sum1 = sum(sum_india)
    if len(avg_india) != 0:
        div1=('₹'+str("{:,}".format(int(Sum1)/len(avg_india))))
        avg_values['India']=div1.split('.')[0]
    else:
        avg_values['India']=0
    Sum2 = sum(sum_US)
    if len(avg_US) != 0:
        div2=('$'+str("{:,}".format(int(Sum2)/len(avg_US))))
        avg_values['US']=div2.split('.')[0]
    else:
        avg_values['US']=0
    Sum3 = sum(sum_Australia)
    if len(avg_Australia) != 0:
        div3=('$'+str("{:,}".format(int(Sum3)/len(avg_Australia))))
        avg_values['Australia']=div3.split('.')[0]
    else:
        avg_values['Australia']=0
    print(all_values)
    
    
def empty():
    india.clear()
    US.clear()
    Australia.clear()
    position2.clear()
    avg_india.clear()
    avg_US.clear()
    avg_Australia.clear()
    skill_extraction.clear()
    avg_values.clear()

# --------------- chrome browser ----------------
def webbrowser():
    # options = webdriver.ChromeOptions()
    options = Options()
    options.headless = True
    time_delay.sleep(2)
    # options.add_extension('adblocker.crx')  
    # driver = webdriver.Chrome(options=options)
    path='/mnt/d/Project/salary scrapping/chromedriver.exe'
    driver = webdriver.Chrome(executable_path=path,options=options)
    
    return driver

# ------ main function assign the asynchronous function into task ---------
def main(name1,position1):
    global position
    position =position1
    global name
    name = name1
    print(name)
    print(position)
    position2.append(position)
    t1 = threading.Thread(target=monster_website_US_1)
    t2 = threading.Thread(target=glassdoor_india_2)
    t3 = threading.Thread(target=indeed_us_3)
    t4 = threading.Thread(target=linkedin_aus_4)
    t5 = threading.Thread(target=linkedin_india_5)
    t6 = threading.Thread(target=linkedin_us_6)
    # t7 = threading.Thread(target=payscale_AUS_Scrap_7)
    # t8 = threading.Thread(target=payscale_india_8)
    # t9 = threading.Thread(target=payscale_US_9)
    t10 = threading.Thread(target=seek_scrapy_aus_10)
    t11 = threading.Thread(target=talent_aus_scrapy_11)
    # t12 = threading.Thread(target=talent_india_12)
    t13 = threading.Thread(target=glassdoor_AUS_13)
    t14 = threading.Thread(target=sales_expect_US_14)
    t15 = threading.Thread(target=skills_extraction)
    
    # --------------start the function ---------------------------
    t1.start(),t2.start(),t3.start(),t4.start(),t5.start(),t6.start(),
    t10.start(),t11.start(),t13.start(),t14.start(),t15.start()
    
    # -------------- wait till the function executed ----------------
    t1.join(),t2.join(),t3.join(),t4.join(),t5.join(),t6.join(),t10.join(),t11.join(),t13.join(),t14.join(),t15.join()
    
    average_values()
    mongodb(name)
    return json.dumps(all_values)

# ---------------  monster website for united state  ---------------
def monster_website_US_1():
    driver=webbrowser()
    try:
        time_delay.sleep(4)
        url="https://www.monster.com/salary/"
        driver.get(url)
        time_delay.sleep(4)
        driver.switch_to.window(driver.window_handles[0])
        time_delay.sleep(4)
        element = driver.find_element_by_xpath("/html/body/div[1]/main/section[1]/div/div/div/div/div[1]/div[2]/span/input")
        element.send_keys(position)
        element1=driver.find_element_by_xpath("/html/body/div[1]/main/section[1]/div/div/div/div/div[2]/div[2]/span/input")
        element1.send_keys("United States Military Acade, NY")
        time_delay.sleep(15)
        element.send_keys(Keys.ENTER)
        element2=driver.find_element_by_id("doQuickSearch2")
        element2.click()
        time_delay.sleep(2)
        salary_content=driver.find_element_by_class_name("avg-salary").text.strip()
        print('1-------->',salary_content)
        avg_US.append(salary_content)
        US.append(url+" == "+salary_content)
    except:
        # print('------- Error -1----- ')
        pass

#  ---------------------   glassdoor India   -----------------------
def glassdoor_india_2():
    try:
        driver=webbrowser()
        replaced_position=position.replace(' ', '-')
        url = 'https://www.glassdoor.co.in/Salaries/chennai-'+replaced_position+'-salary-SRCH_IL.0,7_IM1067_KO8,25.htm?'
        driver.get(url)
        driver.switch_to.window(driver.window_handles[0])
        salary = driver.find_element_by_xpath("//span[@class='m-0 css-146zilq ebrouyy2']")
        salary_content = salary.get_attribute('innerHTML').strip()
        time_delay.sleep(2.0)
        print('2-------->',salary_content)
        avg_india.append(salary_content)
        india.append(url+" == "+salary_content)
    except:
        # print('------- Error -2----- ')
        pass

def indeed_us_3():
    try:
        driver=webbrowser()
        replaced_position=position.replace(' ', '-')
        url = 'https://www.indeed.com/career/'+replaced_position+'/salaries'
        driver.get(url)
        driver.switch_to.window(driver.window_handles[0])
        select = Select(driver.find_element_by_xpath("//select[@name='payPeriodSelect']"))
        time_delay.sleep(0.8)
        select.select_by_visible_text('Per year')
        select.select_by_value('YEARLY')
        time_delay.sleep(8)
        salary = driver.find_element_by_xpath("//div[@class='css-cd2ps3 eu4oa1w0']")
        salary_content = salary.get_attribute('innerHTML').strip()
        print('3------------------->',salary_content)
        avg_US.append(salary_content)
        US.append(url+" == "+salary_content)
    except:
        # print('------- Error - 3 -------- ')
        pass

def linkedin_aus_4():
    try:
        driver=webbrowser()
        replaced_position=position.replace(' ', '%20')
        url = 'https://www.linkedin.com/salary/search?countryCode=au&geoId=101452733&keywords='+replaced_position
        driver.get(url)
        driver.switch_to.window(driver.window_handles[0])
        time_delay.sleep(2)
        salary = driver.find_element_by_xpath("//span[@class='searchTopCard__baseCompensation']")
        salary_content = salary.get_attribute('innerHTML').strip()
        print('4------------------->',salary_content)
        avg_Australia.append(salary_content)
        Australia.append(url+" == "+salary_content)
    except:
        # print('------- Error - 4 -------- ')
        pass

def linkedin_india_5():
    try:
        driver=webbrowser()
        replaced_position=position.replace(' ',"%2B")
        url = 'https://www.linkedin.com/salary/search?countryCode=in&geoId=102713980&keywords='+replaced_position
        driver.get(url)
        driver.switch_to.window(driver.window_handles[0])
        time_delay.sleep(2.0)
        salary = driver.find_element_by_xpath("//span[@class='searchTopCard__baseCompensation']")
        salary_content = salary.get_attribute('innerHTML').strip()
        v=((salary_content.replace('₹','')).replace('/mo','')).replace(',','')
        salary_content_2 = int(v)*12
        avg_india.append(salary_content_2)
        print('5------------------->',salary_content_2)
        india.append(url+" == ₹"+str(salary_content_2))
    except:
        # print('------- Error - 5 -------- ')
        pass

def linkedin_us_6():
    try:
        driver=webbrowser()
        replaced_position=position.replace(' ',"+")
        url = 'https://www.linkedin.com/salary/search?keywords='+replaced_position
        driver.get(url)
        driver.switch_to.window(driver.window_handles[0])
        time_delay.sleep(2.0)
        salary = driver.find_element_by_xpath("//span[@class='searchTopCard__baseCompensation']")
        salary_content = salary.get_attribute('innerHTML').strip()
        print('6------------------->',salary_content)
        salary_content_2=salary_content.split('/y')[0]
        avg_US.append(salary_content_2)
        US.append(url+" == "+salary_content_2)
    except:
        # print('------- Error - 6 -------- ')
        pass

# def payscale_AUS_Scrap_7():
#     try:
#         driver=webbrowser()
#         replaced_position=position.replace(' ',"_")
#         url = 'https://www.payscale.com/research/AU/Job='+replaced_position+'/Salary'
#         driver.get(url)
#         driver.switch_to.window(driver.window_handles[0])
#         time.sleep(2.0)
#         salary = driver.find_element_by_xpath("//span[@class='paycharts__value']")
#         salary_content = salary.get_attribute('innerHTML')
#         print('7------------------>',salary_content)
#         Australia.append(salary_content)
#     except:
#         print('------- Error - 7 -------- ')
#         pass

# def payscale_india_8():
#     try:
#         driver=webbrowser()
#         replaced_position=position.replace(' ',"_")
#         url = 'https://www.payscale.com/research/IN/Job='+replaced_position+'/Salary'
#         driver.get(url)
#         driver.switch_to.window(driver.window_handles[0])
#         driver.implicitly_wait(0.5)
#         salary = driver.find_element_by_xpath("//span[@class='paycharts__value']")
#         salary_content = salary.get_attribute('innerHTML')
#         print('8------------------>',salary_content)
#         india.append(salary_content)
#     except:
#         print('------- Error - 8 --------')
#         pass

# def payscale_US_9():
#     try:
#         driver=webbrowser()
#         replaced_position=position.replace(' ',"_")
#         url = 'https://www.payscale.com/research/US/Job='+replaced_position+'/Salary'
#         driver.get(url)
#         driver.switch_to.window(driver.window_handles[0])
#         driver.implicitly_wait(0.5)
#         salary = driver.find_element_by_xpath("//span[@class='paycharts__value']")
#         salary_content = salary.get_attribute('innerHTML')
#         print('9------------------>',salary_content)
#         US.append(salary_content)
#     except:
#         print('------- Error - 9 --------')
#         pass

def seek_scrapy_aus_10():
    try:
        driver=webbrowser()
        replaced_position=position.replace(' ',"-").lower()
        url = 'https://www.seek.com.au/career-advice/role/'+replaced_position
        driver.get(url)
        driver.switch_to.window(driver.window_handles[0])
        salary = driver.find_element_by_xpath("//div[@data-testid='salary-value']")
        salary_content = salary.get_attribute('innerHTML').strip()
        v=(salary_content.replace('$','')).replace('k','')
        salary_content_2 = (int(v)*1000)
        print('10------------------>',salary_content_2)
        avg_Australia.append(salary_content_2)
        Australia.append(url+" == $"+str(salary_content_2))
    except:
        # print('------- Error - 10 --------')
        pass

def talent_aus_scrapy_11():
    try:
        driver=webbrowser()
        replaced_position=position.replace(' ',"+")
        url = 'https://au.talent.com/salary?job='+replaced_position
        driver.get(url)
        driver.switch_to.window(driver.window_handles[0])
        driver.implicitly_wait(0.5)
        salary = driver.find_element_by_xpath("//div[@class='c-card__stats-mainNumber timeBased']")
        salary_content = salary.get_attribute('innerHTML').strip()
        print('11------------------>',salary_content)
        avg_Australia.append(salary_content)
        Australia.append(url+" == "+salary_content.strip())
    except:
        # print('------- Error - 11 --------')
        pass

# def talent_india_12():
#     try:
#         driver=webbrowser()
#         replaced_position=position.replace(' ',"+")
#         url = 'https://in.talent.com/salary?job=',replaced_position
#         driver.get(url)
#         driver.switch_to.window(driver.window_handles[0])
#         time.sleep(1)
#         salary = driver.find_element_by_xpath("//div[@class='c-card__stats-mainNumber timeBased']")
#         salary_content = salary.get_attribute('innerHTML')
#         print('12------------------>',salary_content.strip())
#     except:
#         print('------- Error - 12 --------')
#         pass

def glassdoor_AUS_13():
    try:
        driver=webbrowser()
        replaced_position=position.replace(' ',"-")
        url = 'https://www.glassdoor.co.in/Salaries/australia-'+replaced_position+'-salary-SRCH_IL.0,9_IN16_KO10,27.htm?clickSource=searchBtn'
        driver.get(url)
        driver.implicitly_wait(0.5)
        salary = driver.find_element_by_xpath("//span[@class='m-0 css-146zilq ebrouyy2']")
        salary_content = salary.get_attribute('innerHTML').strip()
        salary_content_2=salary_content.replace('A','')
        print('13-------------->',salary_content_2)
        avg_Australia.append(salary_content_2)
        Australia.append(url+" == "+salary_content_2.strip())
    except:
        # print('------- Error - 13 --------')
        pass
    
def sales_expect_US_14():
    try:
        driver=webbrowser()
        url="https://www.salaryexpert.com/salary/area"
        driver.get(url)
        time_delay.sleep(5)
        element=driver.find_element_by_xpath("/html/body/main/div/div[1]/div[1]/div/form/div[1]/div[1]/span/input")
        element.send_keys(position)
        element1=driver.find_element_by_xpath("/html/body/main/div/div[1]/div[1]/div/form/div[1]/div[2]/span/input")
        element1.send_keys("Australia")
        time_delay.sleep(5)
        element.send_keys(Keys.ENTER)
        time_delay.sleep(5)
        salary_content=driver.find_element_by_class_name("base").text.strip()
        salary_content_2=(salary_content.split('\n')[1]).split(' (')[0]
        print('14-------------->',salary_content_2)
        avg_US.append(salary_content_2)
        US.append(url+" == "+salary_content_2.strip())
    except:
        # print('------- Error - 14 --------')
        pass


def skills_extraction():
    try:
        driver=webbrowser()
        replaced_position=position.replace(' ',"-")
        url = 'https://www.indeed.com/career/'+replaced_position+'/salaries'
        driver.get(url)
        driver.implicitly_wait(0.5)
        driver.find_element_by_link_text("Skills").click()
        time_delay.sleep(5.0)
        salary = driver.find_element_by_xpath("//ul[@class='css-vurnku eu4oa1w0']")
        skill=salary.text
        skill_list = skill.split("\n")
        print(skill_list)
        for skill in skill_list:
            skill_extraction.append(skill)
    except:
        try:
            driver=webbrowser()
            replaced_position=position.replace(' ',"-")
            url = 'https://www.seek.com.au/career-advice/role/'+replaced_position
            driver.get(url)
            driver.implicitly_wait(0.5)
            salary = driver.find_element_by_xpath("//div[@class='css-1r274bm']")
            skill=salary.text
            skill_list = skill.split("\n")
            print(skill_list)
            for skill in skill_list:
                skill_extraction.append(skill)
        except:
            pass