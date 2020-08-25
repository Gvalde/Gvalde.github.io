import pymongo
from googletrans import Translator
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bson import ObjectId
from random import randint
from bson import ObjectId


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["linkedin"]
users = mydb["users"]

months = {
    "01": "January",
    "02": "February",
    "03": "March",
    "04": "April",
    "05": "May",
    "06": "June",
    "07": "July",
    "08": "August",
    "09": "September",
    "10": "October",
    "11": "November",
    "12": "December"
}

def Register_User(_id):
    data = users.find_one({"_id" : ObjectId(_id)})
    
    driver = webdriver.Chrome("/home/miriani/Desktop/rightnao/drivers/chromedriver")

    driver.implicitly_wait(5)

    driver.get("https://rightnao.com/registration/user")
    
    # Input Username
    driver.find_elements_by_xpath('/html/body/app-root/div/app-registration/div/div[3]/app-user-register/div/div/form/div[3]/input')[0].send_keys(data['username'])

    # Input First Name
    driver.find_element_by_xpath('/html/body/app-root/div/app-registration/div/div[3]/app-user-register/div/div/form/div[1]/input').send_keys(data['first_name'])

    # Input Last Name
    driver.find_element_by_xpath('/html/body/app-root/div/app-registration/div/div[3]/app-user-register/div/div/form/div[2]/input').send_keys(data['last_name'])

    # # Input Username (I found that website generates it automatically)
    # driver.find_element_by_xpath('/html/body/app-root/div/app-registration/div/div[3]/app-user-register/div/div/form/div[3]/input').send_keys(data['username'])

    # Input Password
    driver.find_element_by_xpath('/html/body/app-root/div/app-registration/div/div[3]/app-user-register/div/div/form/div[4]/input').send_keys(data['password'])

    # Input Email
    driver.find_element_by_xpath('/html/body/app-root/div/app-registration/div/div[3]/app-user-register/div/div/form/div[5]/input').send_keys(data['email'])

    # Choos country Code
    driver.find_element_by_xpath('/html/body/app-root/div/app-registration/div/div[3]/app-user-register/div/div/form/div[6]/div[1]/select').send_keys('GE')

    # Input Phone Number
    driver.find_element_by_xpath('/html/body/app-root/div/app-registration/div/div[3]/app-user-register/div/div/form/div[6]/div[2]/input').send_keys(data['phone'])

    # Choose country
    driver.find_element_by_xpath('/html/body/app-root/div/app-registration/div/div[3]/app-user-register/div/div/form/select').send_keys(data['country'])

    # Choose B-day
    driver.find_element_by_xpath('/html/body/app-root/div/app-registration/div/div[3]/app-user-register/div/div/form/div[7]/div[2]/select').send_keys(data['b_day'])

    # Choose B-month
    driver.find_element_by_xpath('/html/body/app-root/div/app-registration/div/div[3]/app-user-register/div/div/form/div[7]/div[3]/select').send_keys(months[data['b_month']])

    # Choose B-year
    driver.find_element_by_xpath('/html/body/app-root/div/app-registration/div/div[3]/app-user-register/div/div/form/div[7]/div[4]/select').send_keys(data['b_year'])


    time.sleep(1)
    # Choose Gender
    if "female" in data["gender"]:
        driver.find_element_by_xpath('/html/body/app-root/div/app-registration/div/div[3]/app-user-register/div/div/form/div[8]/label[1]').click()
    else:
        driver.find_element_by_xpath('/html/body/app-root/div/app-registration/div/div[3]/app-user-register/div/div/form/div[8]/label[2]').click()

    time.sleep(1)
    
    # # Sign Up
    driver.find_element_by_xpath('/html/body/app-root/div/app-registration/div/div[3]/app-user-register/div/div/form/div[9]/button').click()

    driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/app-user-agree-modal/div/div[2]/div/label').click()

    time.sleep(1)

    driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/app-user-agree-modal/div/div[2]/button').click()


    users.update_one({"_id" : ObjectId(_id)}, {"$set" : {"registered" : True}} )

    time.sleep(1)

# Register_User('5f3fb0fe9aefc896db50c5e0')