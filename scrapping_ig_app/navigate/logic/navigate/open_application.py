from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

base_url = "https://www.instagram.com/"
def main(username):
    login_url = "accounts/login/"
    option = webdriver.ChromeOptions()
    driver = webdriver.Chrome("../chromedriver/chromedriver.exe", chrome_options=option)
    login(driver,base_url+ login_url,username)

def login(driver,url, username):
    try :
        driver.get(url)
        wait=WebDriverWait(driver,120).until(EC.url_changes(url))
        url=driver.current_url
        
        if (url == "https://www.instagram.com/"):
            navigate_followers(driver,username)
        else:
            print("AQUÍ ")
            login(driver,url,username)
    except TimeoutException as ex:
        driver.close()

def navigate_followers(driver,original_user):
    try:
        url = driver.current_url
        driver.get(url+original_user+"/" )
        
        element=driver.find_element_by_xpath("//a[@href='/"+original_user+"/following/']")
        element.click()
        time.sleep(3)
        scroll_modal_users(driver)
        users = driver.find_elements_by_xpath("//a[contains(@class, 'notranslate _0imsa')]")
        
        driver.close()
    except TimeoutException as ex:
        driver.close()
    except NoSuchElementException:
        print("NoSuchElementException")
        driver.close()

def scroll_modal_users(driver):
    scroll = 500
    height=0
    last_height=0
    new_height=10
    count=0
    while True :
        last_height=height
        driver.execute_script("document.querySelector('body > div.RnEpo.Yx5HN > div > div > div > div.isgrP').scrollTop = "+str(scroll))    
        height = int(driver.execute_script("return document.querySelector('body > div.RnEpo.Yx5HN > div > div > div > div.isgrP').scrollTop"))
        new_height = height
        
        if (last_height == new_height):
            count=count+1
        else:
            count=0
        time.sleep(0.5)        
        if( height>=scroll):
            scroll = scroll*height
        
        if(count>2):
            print("end scrolling")
            break; 