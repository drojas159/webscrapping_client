from warnings import catch_warnings
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from ...models import User, Publication, Comment, Image, Catalog
import time
from datetime import datetime
from bs4 import BeautifulSoup
import sys


base_url = "https://www.instagram.com/"
def main(username, action_type):
    sys.setrecursionlimit(10000)
    try:
        login_url = "accounts/login/"
        option = webdriver.ChromeOptions()
        option.add_argument("--incognito")
        driver = webdriver.Chrome("../chromedriver/chromedriver", chrome_options=option)
        url=base_url+ login_url
        driver.get(url)
        time.sleep(2)
        username_input = driver.find_element(By.NAME,"username")
        username_input.send_keys("webscraping_smart")
        password_input = driver.find_element(By.NAME,"password")
        password_input.send_keys("Chelsea123!"+ Keys.ENTER)
        #wait=WebDriverWait(driver,120).until(EC.url_changes(url))
        login(driver,username, action_type)
    except TimeoutException as ex:
        driver.close()
def login(driver, username, action_type):
    try :        
        url=driver.current_url
        if ("https://www.instagram.com/accounts/onetap" in url):
            element=driver.find_element(By.XPATH,"//button[contains(@class, 'sqdOP yWX7d    y3zKF     ')]")
            element.click()
            time.sleep(1)
            login(driver,username, action_type)
        elif (url == "https://www.instagram.com/"):
            if (action_type == 'navigate_users'):
                navigate_followers(driver,username)
            elif (action_type == 'navigate_publications'):
                navigate_publications(driver)
            elif (action_type == 'navigate_comments'):
                navigate_comments(driver)
        else:
            login(driver,username, action_type)     

    except TimeoutException as ex:
        driver.close()

def navigate_followers(driver,original_user):
    try:
        url = driver.current_url
        driver.get(url+original_user+"/" )
        time.sleep(2)
        element=driver.find_element(By.XPATH,"//a[@href='/"+original_user+"/following/']")
        element.click()
        time.sleep(2)
        scroll_modal_users(driver)
        users = driver.find_elements(By.XPATH,"//a[contains(@class, 'notranslate _0imsa')]")
        save_users(users,original_user)
        driver.close()
    except TimeoutException as ex:
        driver.close()
    except NoSuchElementException:
        print("NoSuchElementException")
        driver.close()

def save_users(users,original_user):
    following_user=User.objects.get(username=original_user)
    for u in users:
        user = User(username=u.get_attribute("title"),profile_url=base_url+u.get_attribute("title"))
        user.save_user()
        user_from_db = User.objects.get(username=user.username)
        following_user.user_following.add(user_from_db)
        

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

def scroll_publications(driver,u):
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
        posts = driver.find_elements(By.XPATH,"//div[contains(@class, '_aabd _aa8k _aanf')]")
        save_posts(posts,u)
        u.is_reviewed=True
        u.save()
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
        users = User.objects.filter(is_reviewed = False)
        for u in (users):
            url = u.profile_url
            driver.get(url)
            time.sleep(2)
            get_user_details(driver,u)
            scroll_publications(driver,u)            
            wait = WebDriverWait(driver,120).until(EC.url_changes(url))
            print(wait)
            
    except TimeoutException as ex:
        driver.close()
    finally:
        driver.close()
def save_posts(posts,instagram_user):
    for i in posts:
        tag=i.find_element(By.TAG_NAME,"a").get_attribute("href")
        p = Publication(publication_url=tag, user=instagram_user)
        p.save_publication()




def navigate_comments(driver):
    
    try :
        publications = Publication.objects.filter(is_reviewed = False)
        for p in (publications):
            url = p.publication_url
            driver.get(url)
            time.sleep(2)
            get_publication_details(driver,p)
            scroll_comments(driver,p)           
                 
    except TimeoutException as ex:
        driver.close()
    finally:
        driver.close()

def process_comments(general_comments,publication):
    i=0
    for gc in (general_comments):
        source = gc.get_attribute('innerHTML') 
        soup = BeautifulSoup(source, "html.parser")
        
        owner=soup.find("a")
        user = User(username=owner.text,profile_url=base_url+owner.text)
        user.save_user() 
        user_from_db = User.objects.get(username=user.username)
               
        text = soup.find("span",{"class":"_aacl _aaco _aacu _aacx _aad7 _aade"})
        
        comment_dt = soup.find("time")
        format_data = "%Y-%m-%dT%H:%M:%S.%fZ"
        comment_dt  = datetime.strptime(comment_dt['datetime'], format_data)

        comment = Comment(text=text.text,user=user_from_db,comment_url=user_from_db.username+"/"+str(publication.id)+str(i),publication=publication, comment_date=comment_dt)
        comment.save_comment()
        i+=1
        
def scroll_comments(driver,p):
    scroll = 400
    height=0
    last_height=0
    new_height=10
    count=0
    while True :
        try:
            general_comments = driver.find_elements(By.XPATH,"//div[contains(@class, '_a9zr')]")       
            p.is_reviewed=True
            p.save()
            time.sleep(1)
            if (len(general_comments)==0): 
                print('No se encontraron comentarios')
                break
            process_comments(general_comments,p)

            last_height=height
            
            driver.execute_script("document.querySelector('#react-root > div > div > section > main > div > div.ltEKP > article > div > div.qF0y9.Igw0E.IwRSH.eGOV_.acqo5._4EzTm > div > div.eo2As > div.EtaWk > ul').scrollTop = "+str(scroll))    
            height = int(driver.execute_script("return document.querySelector('#react-root > div > div > section > main > div > div.ltEKP > article > div > div.qF0y9.Igw0E.IwRSH.eGOV_.acqo5._4EzTm > div > div.eo2As > div.EtaWk > ul').scrollTop"))
            new_height = height
            
            if (last_height == new_height):
                count=count+1 
            else:
                count=0
            time.sleep(1)        
            if( height>=scroll):
                scroll = scroll*height
            
            if(count>2):
                try:
                    more_comments_button=driver.find_element(By.XPATH,"//div[contains(@class, '             qF0y9          Igw0E     IwRSH        YBx95     acqo5   _4EzTm                                                                                                            NUiEW  ')]/button")
                    more_comments_button.click()
                    time.sleep(1)
                except NoSuchElementException:
                    break
        except Exception as e:
            break    
                #print("end scrolling")
                #break; 
def get_user_details(driver,usr):
    try:
        profile_picture_link = number_posts = number_followers = number_following = user_public_name = user_description = user_other_url=None
        if (len(driver.find_elements(By.XPATH,"//div/span[@class='_2dbep ']/img")) > 0 ):
            profile_picture_link = driver.find_element(By.XPATH,"//div/span[@class='_2dbep ']/img").get_attribute('src')

        if (len(driver.find_elements(By.XPATH,"//ul[@class='k9GMp ']/li/div/span")) > 0 ):
            number_posts = driver.find_element(By.XPATH,"//ul[@class='k9GMp ']/li/div/span").text
            number_posts=int(number_posts.replace('.',''))

        if (len(driver.find_elements(By.XPATH,"//ul[@class='k9GMp ']/li/a[contains(@href,'followers')]/div/span")) > 0 ):
            number_followers = driver.find_element(By.XPATH,"//ul[@class='k9GMp ']/li/a[contains(@href,'followers')]/div/span").get_attribute('title')
            number_followers = int(number_followers.replace('.',''))
        elif (len(driver.find_elements(By.XPATH,"//ul[@class='k9GMp ']/li/div[text()[contains(., 'followers')]]/span")) > 0) :
            number_followers = driver.find_element(By.XPATH,"//ul[@class='k9GMp ']/li/div[text()[contains(., 'followers')]]/span").get_attribute('title')
            number_followers = int(number_followers.replace('.',''))
        else:
            number_followers = None

        if (len(driver.find_elements(By.XPATH,"//ul[@class='k9GMp ']/li/a[contains(@href,'following')]/div/span")) > 0 ):
            number_following = driver.find_element(By.XPATH,"//ul[@class='k9GMp ']/li/a[contains(@href,'following')]/div/span").text
            number_following = int(number_following.replace('.',''))
        elif (len(driver.find_elements(By.XPATH,"//ul[@class='k9GMp ']/li/div[text()[contains(., 'following')]]/span")) > 0):
            number_following = driver.find_element(By.XPATH,"//ul[@class='k9GMp ']/li/div[text()[contains(., 'following')]]/span").text
            number_following = int(number_following.replace('.',''))
        else:
            number_following = None

        if (len(driver.find_elements(By.XPATH,"//div[@class='QGPIr']/span")) > 0 ):
            user_public_name = driver.find_element(By.XPATH,"//div[@class='QGPIr']/span").text

        if (len(driver.find_elements(By.XPATH,"//div[@class='QGPIr']/div")) > 0 ):
            user_description = driver.find_element(By.XPATH,"//div[@class='QGPIr']/div").text

        if (len(driver.find_elements(By.XPATH,"//div[@class='QGPIr']/a")) > 0 ):
            user_other_url = driver.find_element(By.XPATH,"//div[@class='QGPIr']/a").get_attribute('href')        

        img = Image(image_link=profile_picture_link, user = usr, image_type=Catalog.objects.get(variable = "PROFILE_PICTURE"))
        img.save_image()
    
        usr.number_posts = number_posts
        usr.number_followers = number_followers
        usr.number_following = number_following
        usr.user_public_name = user_public_name
        usr.user_description = user_description
        usr.user_other_url = user_other_url
        
        usr.save_user()

    except NoSuchElementException as err :
        print(err)

def scrape_page(driver):
    
    body = driver.execute_script("return document.body")
    source = body.get_attribute('innerHTML') 
    soup = BeautifulSoup(source, "html.parser")
    return soup

def get_publication_details(driver, post):
    try:
        picture_link = number_likes = publication_date = None

        if (len(driver.find_elements(By.XPATH,"//div[@class='eLAPa kPFhm']//img")) > 0 ):
            picture_link = driver.find_element(By.XPATH,"//div[@class='eLAPa kPFhm']//img").get_attribute('src')

        if (len(driver.find_elements(By.XPATH,"//div[@class ='_7UhW9   xLCgt        qyrsm KV-D4               fDxYl    T0kll ']/span")) > 0 ):
            number_likes = driver.find_element(By.XPATH,"//div[@class ='_7UhW9   xLCgt        qyrsm KV-D4               fDxYl    T0kll ']/span").text
            number_likes = int(number_likes.replace('.',''))
        else:
            number_likes = 0

        if (len(driver.find_elements(By.XPATH,"//time[@class='_1o9PC']")) > 0 ):
            format_data = "%Y-%m-%dT%H:%M:%S.%fZ"
            publication_date = driver.find_element(By.XPATH,"//time[@class='_1o9PC']").get_attribute("datetime")
            publication_date  = datetime.strptime(publication_date, format_data)  

        img = Image(image_link=picture_link, user = post.user, publication=post,image_type=Catalog.objects.get(variable = "POST_PICTURE"))
        img.save_image()


        post.number_likes= number_likes
        post.publication_date = publication_date

        post.save_publication()
            
    except Exception as err:
        print(err)
