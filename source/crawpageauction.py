from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import schedule
from requests_html import HTMLSession
from concurrent.futures import ThreadPoolExecutor
from models.landauctions import LandAuctions
from models.districts import Districts
from models.users import Users
from models.LandAuctionCategories import LandAuctionCategories

from db import session  # Assuming you have a session object from db.py





recordnumber = 327850
def getrecordnumber():
    while True:
        try:
            service = FirefoxService("/snap/bin/firefox.geckodriver")
            options = webdriver.FirefoxOptions() 
            options = FirefoxOptions()
            url ="https://dgts.moj.gov.vn/thong-bao-cong-khai-viec-dau-gia.html" 
            options.add_argument("--headless")
            driver = webdriver.Firefox(options=options, service=service)
            driver.get(url)
            page = driver.page_source
            AuctionDetail = BeautifulSoup(page, 'html.parser')
            WebDriverWait(driver, 40).until(
                            EC.visibility_of_element_located((By.XPATH, '//*[@id="wrapper"]/main/div[2]/div[1]/div[3]/div[2]/div[1]/label/b'))
                        )
            element = driver.find_element(By.XPATH, '//*[@id="wrapper"]/main/div[2]/div[1]/div[3]/div[2]/div[1]/label/b')
            recordnumber = element.text
            print(recordnumber)
            driver.quit()
            print("Current RecordsNumber:",recordnumber )
            return int(recordnumber) 
        except:
            driver.quit()
            pass
def get_latest_result():
    try:
        with open("/home/hieu/Documents/craw data website dau gia/craw/recordnumber.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return None
    
def getindex(recordnumberPage):
    
    recordnumber = get_latest_result()
    RecordneedtobeCraw = recordnumberPage - recordnumber
    quotient, remainder = divmod(RecordneedtobeCraw, 10)
    nextpageClick = quotient
    print(RecordneedtobeCraw)
    return nextpageClick, remainder

def getlinkfromMainUrl(nextpageClick, remainder):
    t = time.time()
    numberclick = 10
    while True:
        try:
            service = FirefoxService("/snap/bin/firefox.geckodriver")
            options = webdriver.FirefoxOptions()
            options = FirefoxOptions()  
            options.add_argument("--headless")
            driver = webdriver.Firefox(options=options, service=service)
            url ="https://dgts.moj.gov.vn/thong-bao-cong-khai-viec-dau-gia.html"
            driver.get(url)
            time.sleep(5)
            linkurls =[]
            locators = [
                ("//*[@id='wrapper']/main/div[2]/div[1]/div[3]/div[2]/ul/li[1]/a"),
                ("//*[@id='wrapper']/main/div[2]/div[1]/div[3]/div[2]/ul/li[2]/a"),
                ("//*[@id='wrapper']/main/div[2]/div[1]/div[3]/div[2]/ul/li[3]/a"),
                ("//*[@id='wrapper']/main/div[2]/div[1]/div[3]/div[2]/ul/li[4]/a"),
                ("//*[@id='wrapper']/main/div[2]/div[1]/div[3]/div[2]/ul/li[5]/a"),
                ("//*[@id='wrapper']/main/div[2]/div[1]/div[3]/div[2]/ul/li[6]/a"),
                ("//*[@id='wrapper']/main/div[2]/div[1]/div[3]/div[2]/ul/li[7]/a"),
                ("//*[@id='wrapper']/main/div[2]/div[1]/div[3]/div[2]/ul/li[8]/a"),
                ("//*[@id='wrapper']/main/div[2]/div[1]/div[3]/div[2]/ul/li[9]/a")
            ]
            if nextpageClick < 4:
                count = nextpageClick+2
                for i in range(1, count):
                    print(i)
                    if i >= 3:
                        locator = locators[i]
                    elif i < 3:
                        locator = locators[i-1]
                    currentpage = driver.find_element(By.XPATH, locator)
                    currentpage.click()
                    
                    links = driver.find_elements(By.XPATH, "//a[@class='ng-binding']")
                    if i == count-1 and remainder != 0:
                        for i in range(0, remainder):
                            links[i].click()
                        numberclick = remainder
                    elif i == count-1 and remainder == 0:
                        numberclick = 0
                    else:
                        numberclick =10
                        for i in range(0, numberclick):
                            links[i].click()
                            
                    WebDriverWait(driver, 40).until(EC.number_of_windows_to_be(numberclick+1))
                    time.sleep(8)
                        
                    all_windows = driver.window_handles
                    for i in range(1, len(all_windows)):
                        driver.switch_to.window(all_windows[i])
                        url = driver.current_url
                        linkurls.append(url)
                        driver.close()
                    driver.switch_to.window(all_windows[0])
                    time.sleep(5)
                print(linkurls)
                print(len(linkurls))
                print("done in ", time.time() - t)
                return linkurls
            if nextpageClick >= 4:
                count = nextpageClick+2
                for i in range(1, count):
                    print(i)
                    if i >= 3 and i <= 4:
                        locator = locators[i]
                    elif i < 3:
                        locator = locators[i-1]
                    elif i > 4:
                        locator = locators[5]
                    currentpage = driver.find_element(By.XPATH, locator)
                    currentpage.click()
                    
                    links = driver.find_elements(By.XPATH, "//a[@class='ng-binding']")
                    if i == count-1 and remainder != 0:
                        for i in range(0, remainder):
                            links[i].click()
                        numberclick = remainder
                    elif i == count-1 and remainder == 0:
                        numberclick =0
                    else:
                        numberclick =10
                        for i in range(0, numberclick):
                            links[i].click()
                            
                    WebDriverWait(driver, 40).until(EC.number_of_windows_to_be(numberclick+1))
                    time.sleep(8)                       
                    all_windows = driver.window_handles
                    for i in range(1, len(all_windows)):
                        driver.switch_to.window(all_windows[i])
                        url = driver.current_url
                        linkurls.append(url)
                        driver.close()
                    driver.switch_to.window(all_windows[0])
                    time.sleep(5)
                    
                    
                driver.quit()        
                print(linkurls)
                print(len(linkurls))
                print("done in ", time.time() - t)
            return linkurls
        except Exception as e:
            print(e)
            driver.quit()  

def savedata(AuctionData):
    #while True:
        try:
            for item in AuctionData:
                open_price_str = item.get("OpenPrice")
                open_price_str_clean = ''.join(filter(str.isdigit, open_price_str))
                LandAuction = LandAuctions(
                    Description = item.get("Description"),
                    Title = item.get("Title"),
                    DistrictID = 1,
                    UserID = 249,
                    LandAuctionCategoryID = 1,
                    AuctionAddress = item.get("AuctionAddress"),
                    NamePropertyOwner = item.get("NamePropertyOwner"),
                    NameProperty = item.get("NameProperty"),
                    AddressProperty = item.get("AddressProperty"),
                    OpenPrice = float(open_price_str_clean),
                    DepositPrice = item.get("DepositPrice"),
                    AddressPropertyOwner = item.get("AddressPropertyOwner"),
                    NameAuctionHouse = item.get("NameAuctionHouse"),
                    AddressAuctionHouse = item.get("AddressAuctionHouse"),
                    PhoneNumberAuctionHouse = item.get("PhoneNumberAuctionHouse"),
                    EventSchedule = item.get("EventSchedule"),
                    RegistrationStartTime = item.get("RegistrationStartTime"),
                    RegistrationEndTime = item.get("RegistrationEndTime"),
                    DepositPaymentStartTime = item.get("DepositPaymentStartTime"),
                    DepositPaymentEndTime = item.get("DepositPaymentEndTime"),
                    AuctionUrl = item.get("AuctionUrl")    
                )
                session.add(LandAuction)
                session.commit()
                print("saved")
        except Exception as e:
            print(e)
            session.rollback()
def getdatafromurl(link):
    while True:
        try:
            print("Crawing data...")
            service = FirefoxService("/snap/bin/firefox.geckodriver")
            options = webdriver.FirefoxOptions() 
            options = FirefoxOptions()  
            options.add_argument("--headless")
            driver = webdriver.Firefox(options=options, service=service)
            driver.get(link)
            page = driver.page_source
            # Wait for the <table> element to be present
            #time.sleep(10)
            # Now wait for all <td> elements inside the <table> to be visible
            locators = [
                (By.XPATH, '//*[@id="generate-content"]/table/tbody/tr[2]/td[2]'),
                (By.XPATH, '//*[@id="generate-content"]/table/tbody/tr[2]/td[4]'),
                (By.XPATH, '//*[@id="generate-content"]/table/tbody/tr[2]/td[5]'),
                (By.XPATH, '//*[@id="generate-content"]/table/tbody/tr[2]/td[6]')  
            ]      
            for locator in locators:
                WebDriverWait(driver, 40).until(
                    EC.visibility_of_element_located(locator)
                )
            listtd = []
            locators2 = [
                ('//*[@id="generate-content"]/table/tbody/tr[2]/td[2]'),
                ('//*[@id="generate-content"]/table/tbody/tr[2]/td[4]'),
                ('//*[@id="generate-content"]/table/tbody/tr[2]/td[5]'),
                ('//*[@id="generate-content"]/table/tbody/tr[2]/td[6]')  
            ] 
            for item in locators2:
                element = driver.find_element(By.XPATH,item)
                element_text = element.text
                listtd.append(element_text)
            session = HTMLSession()
            html_content = session.get(link)
            AuctionDetail = BeautifulSoup(html_content.content, 'html.parser')
            AuctionData = []
            data = dict()
            listp = AuctionDetail.find_all('b')
    
            data["AuctionUrl"] = link
            data["Title"] = AuctionDetail.find('h1').get_text(strip=True)
            data["Description"] = listp[16].get_text(strip = True)
            data["AuctionAddress"] = listp[13].get_text(strip = True)
            data["NamePropertyOwner"] = listp[6].get_text(strip = True)
            data["NameProperty"] = listtd[0]
            data["AddressProperty"] = listtd[1]
            data["OpenPrice"] = listtd[2]
            data["DepositPrice"] = listtd[3]
            data["AddressPropertyOwner"] = listp[7].get_text(strip = True)
            data["NameAuctionHouse"] = listp[8].get_text(strip = True)
            data["AddressAuctionHouse"] = listp[9].get_text(strip = True)
            data["PhoneNumberAuctionHouse"] = listp[10].get_text(strip = True)
            data["EventSchedule"] = datetime.strptime(listp[12].get_text(strip = True), '%H:%M %d/%m/%Y').strftime('%Y-%m-%dT%H:%M:%S')
            data["RegistrationStartTime"] = datetime.strptime(listp[14].get_text(strip = True), '%H:%M %d/%m/%Y').strftime('%Y-%m-%dT%H:%M:%S')
            data["RegistrationEndTime"] = datetime.strptime(listp[15].get_text(strip = True), '%H:%M %d/%m/%Y').strftime('%Y-%m-%dT%H:%M:%S')
            data["DepositPaymentStartTime"] = datetime.strptime(listp[17].get_text(strip = True), '%H:%M %d/%m/%Y').strftime('%Y-%m-%dT%H:%M:%S')
            data["DepositPaymentEndTime"] = datetime.strptime(listp[18].get_text(strip = True), '%H:%M %d/%m/%Y').strftime('%Y-%m-%dT%H:%M:%S')
            driver.quit()
            AuctionData.append(data)
            savedata(AuctionData)
            return AuctionData
        except Exception as e:
            print(e)
            driver.quit()
            pass

def crawdata(linkurls):
    
    t = time.time()
    result =[]
    with ThreadPoolExecutor(max_workers=2) as exe:
         
        # Maps the method 'cube' with a list of values.
        result = exe.map(getdatafromurl,linkurls)
    for r in result:
      print(r)
                
    print("done in ", time.time() - t)


def main():
    a=0
    while a==0:
        a = getrecordnumber()
    result = getindex(a)
    if result[0] == 0  and result[1] == 0:
        print("There is not new record to be crawed")
        pass
    else:
        print(result)
        linkurls = getlinkfromMainUrl(result[0], result[1])
        crawdata(linkurls)
        with open("/home/hieu/Documents/craw data website dau gia/craw/recordnumber.txt", "w") as file:
            file.write(str(a)) 
        print("Craw data successfully")
main()     
"""# Schedule the job every day at 10:30 AM
schedule.every().day.at("16:17").do(main)

# Run the scheduler in an infinite loop
while True:
    schedule.run_pending()
    time.sleep(1)"""
