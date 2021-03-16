from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
options=Options()
options.add_argument('--headless')

options.add_argument("--window-size=1920,2840")
options.add_argument("--force-device-scale-factor=0.25")

options.add_experimental_option("detach", True)
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
driver = webdriver.Chrome(chrome_options=options,executable_path=r'C:\Users\asusi\Documents\bootcamp\chromedriver_win32\chromedriver.exe')
class jobs():
    def __init__(self):
        self.name="" 
        self.link=""
        self.loc=""
        self.etype=""
        self.eno=""

def login():
    driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')

    email=driver.find_element_by_xpath('//*[@id="username"]')
    email.send_keys('emailid.com')

    time.sleep(1)
    password=driver.find_element_by_xpath('//*[@id="password"]')
    password.send_keys('passwordpassword')

    time.sleep(1)
    login=driver.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button')
    login.click()

    time.sleep(1)#this keeps the page open or else it will close as loading of page is done
    return driver

joblist=[]
def get_name_link(driver):
    
    n=0
    driver.get(r'https://www.linkedin.com/jobs/search/?geoId=103644278&keywords=data%20analyst&start='+str(n))
    while n<100:
        soup=BeautifulSoup(driver.page_source,'html.parser')
        for a in soup.find_all('div',class_='full-width artdeco-entity-lockup__title ember-view')[0:7]:
            job=jobs()
            
            b=a.find('a',class_="disabled ember-view job-card-container__link job-card-list__title")

            job.link=('https://www.linkedin.com'+b['href']).strip('\n')

            c=a.findNextSibling().find('a',class_="job-card-container__link job-card-container__company-name ember-view")
            try:
                job.name=c.text.strip('\n').lstrip(' ').rstrip('\n')
            except:
                job.name='errr...'

            joblist.append(job)
        print ('====================================================================')
        n=n+7
        driver.get(r'https://www.linkedin.com/jobs/search/?geoId=103644278&keywords=data%20analyst&start='+str(n))

    return joblist

    

def get_details(joblist):
    for job in joblist:
        driver.get(job.link)
        soup=BeautifulSoup(driver.page_source,'html.parser')
        time.sleep(5)
        try:
            job.loc=(soup.find('span',class_="jobs-unified-top-card__bullet")).text.strip('\n').lstrip(' ').rstrip('\n')
            job.etype=soup.find_all('p',class_="t-14 mb3")[1].text.strip('\n').lstrip(' ').rstrip('\n')
            job.eno=soup.find('span',class_="jobs-company__inline-information").text.strip('\n').lstrip(' ').rstrip('\n')

            
        except:
            print ('tierd..')
        

    


get_details(get_name_link(login()))

for a in joblist:
    print(a.name)
    print(a.link)
    print(a.loc)
    print(a.etype)
    print(a.eno)

df=pd.DataFrame([t.__dict__ for t in joblist])
pd.options.display.max_rows=None
pd.options.display.max_columns=None
print(df)
df.to_csv('data.csv')