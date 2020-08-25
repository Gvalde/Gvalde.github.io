import pymongo
from googletrans import Translator
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["database"]
mycol = mydb["test"]

username = "budwuehfxjdzgquega@miucce.online"
password = "password123"


driver = webdriver.Chrome("/home/miriani/Desktop/rightnao/drivers/chromedriver")

driver.implicitly_wait(5)

driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")

driver.find_element_by_xpath('//*[@id="username"]').send_keys(username)

driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)

driver.find_element_by_xpath('//*[@id="app__container"]/main/div[2]/form/div[3]/button').click()

def sel_get(link):
    driver.get(f"{link}")

    driver.find_element_by_xpath('/html/body').send_keys(Keys.CONTROL, Keys.END)
    time.sleep(5)

    with open('templates/page.html', 'w') as f:
        f.write(driver.page_source)


# sel_get('https://www.linkedin.com/in/lasha-khutsishvili-11313a99/')

    
    # driver.find_element_by_id("source").send_keys(text)

    # translated = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/div[1]/div[2]/div/span[1]").text
    # return translated
# sel_get("https://www.linkedin.com/in/michaelkurkudjian/")

# driver.find_element_by_css_selector("#top-menu > ul.nav.navbar-nav.navbar-right.left.aut > li.contact-details > a").click()


# https://translate.google.com/

# /html/body/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/div[1]/div[2]/div/span[1]/span