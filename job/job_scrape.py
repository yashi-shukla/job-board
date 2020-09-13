#%%
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys # for search
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import  WebDriverWait
from selenium.webdriver.support import expected_conditions as EC # to wait until element exists 
import  pandas as pd
from bs4 import BeautifulSoup
import time

#%%
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

df = pd.DataFrame(columns =['Title', 'Location', 'Company', 'Description', 'link'])

#%%
for i range(0, 500, 10):

    driver.get("https://www.indeed.co.in/jobs?q=data+analyst&l=India&start="+str(i))
    # driver.get("https://www.indeed.co.in/jobs?q=data+analyst&l=India")

    driver.maximize_window()
    driver.implicitly_wait(4)

    jobs = driver.find_elements_by_class_name("result")
    for job in jobs:
        result_html = job.get_attribute('innerHTML')
        soup = BeautifulSoup(result_html, 'html.parser')

        try:
            profile = soup.find("a", class_ ="jobtitle").text.replace('\n','')
            
        except:
            profile = 'None'
        print(profile)
        try:
            location = soup.find(class_="location").text
        except:
            location = 'None'
        print(location)
        try:
            company = soup.find(class_ = "company").text
        except:
            company = 'None'
        print(company)
        
        sum_div = job.find_element_by_class_name("summary")
        try:
            sum_div.click()

            try:
                job_desc = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div#vjs-desc'))
                )
            except :
                job_desc = 'None'

        except :
            close_button = driver.find_elements_by_class_name('popover-x-button-close')
            close_button.click()
            sum_div.click()

        # job_desc = driver.find_element_by_css_selector('div#vjs-desc')
        print(job_desc.text)

        link = driver.current_url
        print(link)

        df = df.append({'Title': profile, 'Location' : location, 'Company': company, 'Description': job_desc, 'link'}, ignore_index = True)

    

#%%