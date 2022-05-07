from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from ...models import User, Publication
import time

base_url = "https://www.instagram.com/"
def main(username, action_type):
    login_url = "accounts/login/"
    option = webdriver.ChromeOptions()
    #option.add_argument("--incognito")
    driver = webdriver.Chrome("../chromedriver/chromedriver.exe", chrome_options=option)
    login(driver,base_url+ login_url,username, action_type)

def login(driver,url, username, action_type):
    try :        
        driver.get(url)
        wait=WebDriverWait(driver,120).until(EC.url_changes(url))
        url=driver.current_url
        
        if (url == "https://www.instagram.com/"):
            if (action_type == 'navigate_users'):
                navigate_followers(driver,username)
            elif (action_type == 'navigate_publications'):
                navigate_publications(driver)
            elif (action_type == 'navigate_comments'):
                navigate_comments(driver)
        else:
            login(driver,url,username, action_type)
        

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
        save_users(users)
        driver.close()
    except TimeoutException as ex:
        driver.close()
    except NoSuchElementException:
        print("NoSuchElementException")
        driver.close()

def save_users(users):
    for u in users:        
        user = User(username=u.get_attribute("title"),profile_url=base_url+u.get_attribute("title"))
        user.save_user()

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

def scroll_publications(driver):
    SCROLL_PAUSE_TIME = 1
    while True:

        # Get scroll height
        ### This is the difference. Moving this *inside* the loop
        ### means that it checks if scrollTo is still scrolling 
        last_height = driver.execute_script("return document.body.scrollHeight")
        #print(last_height)
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:

            # try again (can be removed)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")

            # check if the page height has remained the same
            if new_height == last_height:
                # if so, you are done
                break
            # if not, move on to the next loop
            else:
                last_height = new_height
                continue

def navigate_publications(driver):
    try :
        users = User.objects.all();
        for u in (users):
            print(u)
            print(u.profile_url)
            url = u.profile_url
            driver.get(url)
            scroll_publications(driver)
            wait = WebDriverWait(driver,120).until(EC.url_changes(url))
            print(wait)
            
    except TimeoutException as ex:
        driver.close()
    finally:
        driver.close()

def navigate_comments(driver):
    
    try :
        publications = Publication.objects.all();
        for p in (publications):
            url = p.publication_url
            print(url)
            driver.get(url)
            #wait = WebDriverWait(driver,120).until(EC.url_changes(url))
            time.sleep(1)
            
    except TimeoutException as ex:
        driver.close()
    finally:
        driver.close()