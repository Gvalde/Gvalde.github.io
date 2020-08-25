import pymongo
from googletrans import Translator
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains 
import time, io, os, re
import requests
from PIL import Image
from bson import ObjectId


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["sales_db"]
users = mydb["companies"]

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

def Sales_Update_Profile_Picture(_id):
    data = users.find_one({"_id" : ObjectId(_id)})

    users.update({"_id" : ObjectId(_id)}, { "$set" : { "linkedin.username" : data["contact_persons"][0]["username"], "linkedin.password" : data["contact_persons"][0]["password"] } })
    
    data = users.find_one({"_id" : ObjectId(_id)})

    data = data["linkedin"]

    driver = webdriver.Chrome("/home/miriani/Desktop/rightnao/drivers/chromedriver")

    driver.implicitly_wait(15)

    ############## Sign In ######################################
    driver.get("https://rightnao.com/registration/login?type=user")

    driver.find_element_by_xpath('/html/body/app-root/div/app-registration/div/div[3]/app-user-login-page/div/div/div/app-user-login/form/div[1]/div/input').send_keys(data['username'])

    driver.find_element_by_xpath('/html/body/app-root/div/app-registration/div/div[3]/app-user-login-page/div/div/div/app-user-login/form/div[2]/input').send_keys(data['password'])

    time.sleep(1)

    driver.find_element_by_xpath('/html/body/app-root/div/app-registration/div/div[3]/app-user-login-page/div/div/div/app-user-login/form/div[4]/button').click()

    time.sleep(1)

    try:
        driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/app-user-verify-modal/div/button').click()
    except:
        print("Already Verified")

    #################### Upload Profile Picture #####################
    driver.find_element_by_xpath('/html/body/app-root/div/app-header/header/nav/div[2]/div/img').click()

    driver.find_element_by_xpath('//*[@id="ngb-popover-1"]/div[2]/div/div[1]/div/a').click()
    
    time.sleep(3)

    driver.find_element_by_xpath('/html/body/app-root/div/app-user/app-user-profile/main/div[2]/div/div[1]/app-main-user-details/div/div/div/div[1]/div').click()
    
    img_data = requests.get(data["photo"]).content

    with open('profile.jpg', 'wb') as handler:
        handler.write(img_data)

    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="upload-image"]').send_keys('/home/miriani/Desktop/link_tool/profile.jpg')

    # Change the size of a picture (Crop Size)
    element = driver.find_element_by_xpath('//*[@id="image-context"]/div[2]/input')
    move = ActionChains(driver)
    move.click_and_hold(element).move_by_offset(-400, 0).release().perform()

    # Click Save Button
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/app-edit-profile-picture/div/div[2]/button').click()
    print("Picture Updated")
    time.sleep(1)

    driver.close()
    
    
    ############### Not preferable way - Update profile picture using api ################
    # # https://rightnao.com/api/v1/uploading/avatar/
    
    # img_data = requests.get(data["photo"]).content

    # with open('profile.jpg', 'wb') as handler:
    #     handler.write(img_data)

    # im = Image.open("profile.jpg") # Getting the Image
    # fp = io.BytesIO()
    # im.save(fp,"JPEG")
    # output = fp.getvalue()

    # time.sleep(10)

def Sales_Update_Story_Info(_id):
    try:
        data = users.find_one({"_id" : ObjectId(_id)})
        
        data = data["linkedin"]

        driver = webdriver.Chrome("/home/miriani/Desktop/rightnao/drivers/chromedriver")

        driver.implicitly_wait(15)

        ############## Sign In ######################################
        driver.get("https://rightnao.com/registration/login?type=user")

        driver.find_element_by_xpath('/html/body/app-root/div/app-registration/div/div[3]/app-user-login-page/div/div/div/app-user-login/form/div[1]/div/input').send_keys(data['username'])

        driver.find_element_by_xpath('/html/body/app-root/div/app-registration/div/div[3]/app-user-login-page/div/div/div/app-user-login/form/div[2]/input').send_keys(data['password'])

        time.sleep(2)

        driver.find_element_by_xpath('/html/body/app-root/div/app-registration/div/div[3]/app-user-login-page/div/div/div/app-user-login/form/div[4]/button').click()

        time.sleep(1)

        try:
            driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/app-user-verify-modal/div/button').click()
        except:
            print("Already Verified")
        ############## Update Story Info (ABOUT) ######################
        driver.find_element_by_xpath('/html/body/app-root/div/app-header/header/nav/div[2]/div/img').click()

        driver.find_element_by_xpath('//*[@id="ngb-popover-1"]/div[2]/div/div[1]/div/a').click()

        driver.find_element_by_xpath('/html/body/app-root/div/app-user/app-user-profile/main/div[2]/div/div[2]/div[2]/div[1]/app-story/div/button').click()
        
        driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/app-story-modal/div/div/form/div/textarea').send_keys(data["about"])

        driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/app-story-modal/div/div/form/button').click()
        
        time.sleep(1)

        driver.close()

        print("Profile Story Updated")
    except Exception as e:
        print(e)

def Sales_Update_Headline_Info(_id):
    data = users.find_one({"_id" : ObjectId(_id)})
    
    data = data["linkedin"]

    driver = webdriver.Chrome("/home/miriani/Desktop/rightnao/drivers/chromedriver")

    driver.implicitly_wait(15)

    ############## Sign In ######################################
    driver.get("https://rightnao.com/registration/login?type=user")

    driver.find_element_by_xpath('/html/body/app-root/div/app-registration/div/div[3]/app-user-login-page/div/div/div/app-user-login/form/div[1]/div/input').send_keys(data['username'])

    driver.find_element_by_xpath('/html/body/app-root/div/app-registration/div/div[3]/app-user-login-page/div/div/div/app-user-login/form/div[2]/input').send_keys(data['password'])

    time.sleep(1)

    driver.find_element_by_xpath('/html/body/app-root/div/app-registration/div/div[3]/app-user-login-page/div/div/div/app-user-login/form/div[4]/button').click()

    time.sleep(1)

    try:
        driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/app-user-verify-modal/div/button').click()
    except:
        print("Already Verified")
    ############## Update Accomplishments Info ###########################
    driver.find_element_by_xpath('/html/body/app-root/div/app-header/header/nav/div[2]/div/img').click()

    driver.find_element_by_xpath('//*[@id="ngb-popover-1"]/div[2]/div/div[1]/div/a').click()

    driver.find_element_by_xpath('/html/body/app-root/div/app-user/app-user-profile/main/div[2]/div/div[1]/app-main-user-details/div/div/div/button').click()

    # Headline
    driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/app-headline/div/div/form/input').send_keys(data["headline"])

    # Save
    driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/app-headline/div/div/form/button').click()

    time.sleep(1)

    print("Headline Completed")

    driver.close()

def Sales_Update_Experience_Info(_id):
    data = users.find_one({"_id" : ObjectId(_id)})

    data = data["linkedin"]

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    
    driver = webdriver.Chrome("/home/miriani/Desktop/rightnao/drivers/chromedriver", chrome_options=options)

    driver.implicitly_wait(15)


    ############## Sign In ######################################
    driver.get("https://rightnao.com/registration/login?type=user")

    driver.find_element_by_xpath('/html/body/app-root/div/app-registration/div/div[3]/app-user-login-page/div/div/div/app-user-login/form/div[1]/div/input').send_keys(data['username'])

    driver.find_element_by_xpath('/html/body/app-root/div/app-registration/div/div[3]/app-user-login-page/div/div/div/app-user-login/form/div[2]/input').send_keys(data['password'])

    time.sleep(1)

    driver.find_element_by_xpath('/html/body/app-root/div/app-registration/div/div[3]/app-user-login-page/div/div/div/app-user-login/form/div[4]/button').click()

    time.sleep(1)

    try:
        driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/app-user-verify-modal/div/button').click()
    except:
        print("Already Verified")
    ############## Update Experience Info #########################
    driver.find_element_by_xpath('/html/body/app-root/div/app-header/header/nav/div[2]/div/img').click()

    driver.find_element_by_xpath('//*[@id="ngb-popover-1"]/div[2]/div/div[1]/div/a').click()

    time.sleep(2)

    for each in data["experience"]:
        driver.find_element_by_xpath('/html/body/app-root/div/app-user/app-user-profile/main/div[2]/div/div[2]/div[2]/div[2]/div/app-experience/div/button').click()
        
        time.sleep(1)

        driver.find_element_by_xpath('//*[@id="add-title"]').send_keys(each["position"])

        driver.find_element_by_xpath('//*[@id="add-company"]').send_keys(each["company"])

        driver.find_element_by_xpath('//*[@id="location-street-address-4-right"]').send_keys("Georgia")

        driver.find_element_by_xpath('//*[@id="location-street-address-3-left"]').send_keys("Jandabamde Gza gqonia")

        
        driver.find_element_by_xpath('//*[@id="experience-from"]').send_keys("January")  # Needs Modification

        year = each["time"].split("–")[0]
        year = re.sub("[^0-9]", "", year)
        driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/app-experience-modal/div/form/div[1]/div[4]/div[1]/div/div[2]/select').send_keys(year)

        if "Present" in each["time"]:
            driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/app-experience-modal/div/form/div[1]/div[4]/div[2]/div/div[3]/label').click()
        else:
            driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/app-experience-modal/div/form/div[1]/div[4]/div[2]/div/div[1]/select').send_keys("December")
            try:
                year = each["time"].split("–")[1]
                # print(year)
                year = re.sub("[^0-9]", "", year)
                driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/app-experience-modal/div/form/div[1]/div[4]/div[2]/div/div[2]/select').send_keys(year)
            except:
                driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/app-experience-modal/div/form/div[1]/div[4]/div[2]/div/div[2]/select').send_keys("2020")

        # Updating Company logo in company
        if "http" not in each["company_logo"]:
            a = 1
        else:
            img_data = requests.get(each["company_logo"]).content

            with open('experience.jpg', 'wb') as handler:
                handler.write(img_data)

            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="upload-photo"]').send_keys('/home/miriani/Desktop/link_tool/experience.jpg')

        # Adding Company link in Experience Description
        driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/app-experience-modal/div/form/div[1]/div[6]/app-media-and-link/form/div/div[2]/label').click()
        driver.find_element_by_xpath('//*[@id="add-link"]').send_keys(each["company_website"])
        driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/app-experience-modal/div/form/div[1]/div[6]/app-media-and-link/form/div/div[3]/button').click()

        driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/app-experience-modal/div/form/div[2]/button[2]').click()
        # driver.find_element_by_xpath('//*[@id="add-description"]').send_keys()

        # driver.find_element_by_xpath('//*[@id="add-title"]').send_keys()

        time.sleep(5)
    print("Experience Updated")
    driver.close()

def Sales_Update_Education_Info(_id):
    data = users.find_one({"_id" : ObjectId(_id)})
    
    data = data["linkedin"]

    driver = webdriver.Chrome("/home/miriani/Desktop/rightnao/drivers/chromedriver")

    driver.implicitly_wait(15)
    

    ############## Sign In ######################################
    driver.get("https://rightnao.com/registration/login?type=user")

    driver.find_element_by_xpath('/html/body/app-root/div/app-registration/div/div[3]/app-user-login-page/div/div/div/app-user-login/form/div[1]/div/input').send_keys(data['username'])

    driver.find_element_by_xpath('/html/body/app-root/div/app-registration/div/div[3]/app-user-login-page/div/div/div/app-user-login/form/div[2]/input').send_keys(data['password'])

    time.sleep(1)

    driver.find_element_by_xpath('/html/body/app-root/div/app-registration/div/div[3]/app-user-login-page/div/div/div/app-user-login/form/div[4]/button').click()

    time.sleep(1)

    try:
        driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/app-user-verify-modal/div/button').click()
    except:
        print("Already Verified")
    ############## Update Education Info ###########################
    driver.find_element_by_xpath('/html/body/app-root/div/app-header/header/nav/div[2]/div/img').click()

    driver.find_element_by_xpath('//*[@id="ngb-popover-1"]/div[2]/div/div[1]/div/a').click()

    time.sleep(4)

    for each in data["education"]:
        try:
            driver.find_element_by_xpath('/html/body/app-root/div/app-user/app-user-profile/main/div[2]/div/div[2]/div[2]/div[3]/app-education/div/button').click()
            
            time.sleep(1)

            # Institution
            driver.find_element_by_xpath('//*[@id="add-school"]').send_keys(each["institution"])

            # Major
            driver.find_element_by_xpath('//*[@id="add-field"]').send_keys(each["major"])

            # Start month
            driver.find_element_by_xpath('//*[@id="education-from"]').send_keys("January")  # Needs Modification

            # Start Year
            year = each["years"].split("–")[0]
            year = re.sub("[^0-9]", "", year)
            if year is None or year =="":
                driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/app-education-modal/div/form/div[1]/div[5]/div[1]/div/div[2]/select').send_keys("2020")
            else:
                driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/app-education-modal/div/form/div[1]/div[5]/div[1]/div/div[2]/select').send_keys(year)

            # End Month and Year
            if "Present" in each["years"]:
                driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/app-education-modal/div/form/div[1]/div[6]/label').click()
            else:
                driver.find_element_by_xpath('//*[@id="education-to"]').send_keys("December")
                try:
                    year = each["years"].split("–")[1]
                    # print(year)
                    year = re.sub("[^0-9]", "", year)
                    driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/app-education-modal/div/form/div[1]/div[5]/div[2]/div/div[2]/select').send_keys(year)
                except:
                    driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/app-education-modal/div/form/div[1]/div[5]/div[2]/div/div[2]/select').send_keys("2020")

            # Adding education Description
            driver.find_element_by_xpath('//*[@id="add-education-description"]').send_keys(each['activities'])


            # Updating Company logo in company
            if "http" not in each["institution_logo"]:
                a = 1
            else:
                img_data = requests.get(each["institution_logo"]).content

                with open('education.jpg', 'wb') as handler:
                    handler.write(img_data)

                time.sleep(1)
                driver.find_element_by_xpath('//*[@id="upload-photo"]').send_keys('/home/miriani/Desktop/link_tool/education.jpg')

            # Clicking Save Button
            driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/app-education-modal/div/form/div[2]/button[2]').click()

            time.sleep(2)
        except Exception as e:
            print("Education", e)
            continue
    print("Education Filled")
    driver.close()

def Sales_Update_Language_Info(_id):
    data = users.find_one({"_id" : ObjectId(_id)})
    
    data = data["linkedin"]

    driver = webdriver.Chrome("/home/miriani/Desktop/rightnao/drivers/chromedriver")

    driver.implicitly_wait(15)

    ############## Sign In ######################################
    driver.get("https://rightnao.com/registration/login?type=user")

    driver.find_element_by_xpath('/html/body/app-root/div/app-registration/div/div[3]/app-user-login-page/div/div/div/app-user-login/form/div[1]/div/input').send_keys(data['username'])

    driver.find_element_by_xpath('/html/body/app-root/div/app-registration/div/div[3]/app-user-login-page/div/div/div/app-user-login/form/div[2]/input').send_keys(data['password'])

    time.sleep(1)

    driver.find_element_by_xpath('/html/body/app-root/div/app-registration/div/div[3]/app-user-login-page/div/div/div/app-user-login/form/div[4]/button').click()

    time.sleep(1)

    try:
        driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/app-user-verify-modal/div/button').click()
    except:
        print("Already Verified")
    ############## Update Language Info ###########################
    driver.find_element_by_xpath('/html/body/app-root/div/app-header/header/nav/div[2]/div/img').click()

    driver.find_element_by_xpath('//*[@id="ngb-popover-1"]/div[2]/div/div[1]/div/a').click()

    # Scroll Down a little bit 
    time.sleep(2)
    driver.find_element_by_xpath('/html/body').send_keys(Keys.SPACE)
    time.sleep(2)

    for each in data["language"]:
        try:
            driver.find_element_by_xpath('/html/body/app-root/div/app-user/app-user-profile/main/div[2]/div/div[2]/div[2]/div[6]/app-language/div/div/button').click()
        except:
            driver.find_element_by_xpath('/html/body/app-root/div/app-user/app-user-profile/main/div[2]/div/div[2]/div[2]/div[6]/app-language/div[1]/button').click()
        driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/app-language-modal/div/div/form/div[1]/select').click()
        time.sleep(2)

        driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/app-language-modal/div/div/form/div[1]/select').send_keys(each['language'])
        time.sleep(2)
        driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/app-language-modal/div/div/form/div[1]/select').send_keys(Keys.ENTER)

        driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/app-language-modal/div/div/form/div[2]/div/ngb-rating/span[10]').click()

        driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/app-language-modal/div/div/form/div[3]/button[2]').click()
        
        time.sleep(1)

    print("Languages Completed")
    driver.close()

def Sales_Update_Accomplishments_Info(_id):
    data = users.find_one({"_id" : ObjectId(_id)})
    
    data = data["linkedin"]

    driver = webdriver.Chrome("/home/miriani/Desktop/rightnao/drivers/chromedriver")

    driver.implicitly_wait(15)

    ############## Sign In ######################################
    driver.get("https://rightnao.com/registration/login?type=user")

    driver.find_element_by_xpath('/html/body/app-root/div/app-registration/div/div[3]/app-user-login-page/div/div/div/app-user-login/form/div[1]/div/input').send_keys(data['username'])

    driver.find_element_by_xpath('/html/body/app-root/div/app-registration/div/div[3]/app-user-login-page/div/div/div/app-user-login/form/div[2]/input').send_keys(data['password'])

    time.sleep(1)

    driver.find_element_by_xpath('/html/body/app-root/div/app-registration/div/div[3]/app-user-login-page/div/div/div/app-user-login/form/div[4]/button').click()

    time.sleep(1)

    try:
        driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/app-user-verify-modal/div/button').click()
    except:
        print("Already Verified")
    ############## Update Accomplishments Info ###########################
    driver.find_element_by_xpath('/html/body/app-root/div/app-header/header/nav/div[2]/div/img').click()

    driver.find_element_by_xpath('//*[@id="ngb-popover-1"]/div[2]/div/div[1]/div/a').click()
    
    # Scroll Down a little bit 
    time.sleep(2)
    driver.find_element_by_xpath('/html/body').send_keys(Keys.SPACE)
    time.sleep(2)

    for each in data["accomplishments"]:
        try:
            driver.find_element_by_xpath('/html/body/app-root/div/app-user/app-user-profile/main/div[2]/div/div[2]/div[2]/div[7]/app-accomplishment/div/button').click()

            driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/div/div/form/div[1]/div[1]/div[1]/label').click()

            driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/div/div/form/div[2]/button').click()

            # Name
            driver.find_element_by_xpath('//*[@id="certificate-name"]').send_keys(each['name'])

            # Authority
            driver.find_element_by_xpath('//*[@id="certificate-authority"]').send_keys(each['authority'])

            # Month From
            driver.find_element_by_xpath('//*[@id="project-from"]').send_keys("January")

            # year From
            driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/app-accomplishment-modal/div/div/form/div[1]/div[4]/div[1]/div/div[2]/select').send_keys("2020")

            # This Certification does not expire
            driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/app-accomplishment-modal/div/div/form/div[1]/div[4]/div[2]/div/div[3]/label').click()


            # Media
            if "http" not in each["media"]:
                a = 1
            else:
                img_data = requests.get(each["media"]).content

                with open('accomplishment.jpg', 'wb') as handler:
                    handler.write(img_data)

                time.sleep(1)
                driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/app-accomplishment-modal/div/div/form/div[1]/app-media-and-link/form/div/div[1]/label').send_keys('/home/miriani/Desktop/link_tool/accomplishment.jpg')

            # Submit/Save
            driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/app-accomplishment-modal/div/div/form/div[2]/div/button[2]').click()

            time.sleep(1)


        except Exception as e:
            print("Accomplishments", e)
            continue
    print("Accomplishments Done")
    driver.close()

def Sales_Update_Interests_Info(_id):
    data = users.find_one({"_id" : ObjectId(_id)})
    
    data = data["linkedin"]

    driver = webdriver.Chrome("/home/miriani/Desktop/rightnao/drivers/chromedriver")

    driver.implicitly_wait(15)

    ############## Sign In ######################################
    driver.get("https://rightnao.com/registration/login?type=user")

    driver.find_element_by_xpath('/html/body/app-root/div/app-registration/div/div[3]/app-user-login-page/div/div/div/app-user-login/form/div[1]/div/input').send_keys(data['username'])

    driver.find_element_by_xpath('/html/body/app-root/div/app-registration/div/div[3]/app-user-login-page/div/div/div/app-user-login/form/div[2]/input').send_keys(data['password'])

    time.sleep(1)

    driver.find_element_by_xpath('/html/body/app-root/div/app-registration/div/div[3]/app-user-login-page/div/div/div/app-user-login/form/div[4]/button').click()

    time.sleep(1)

    try:
        driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/app-user-verify-modal/div/button').click()
    except:
        print("Already Verified")
    ############## Update Accomplishments Info ###########################
    driver.find_element_by_xpath('/html/body/app-root/div/app-header/header/nav/div[2]/div/img').click()

    driver.find_element_by_xpath('//*[@id="ngb-popover-1"]/div[2]/div/div[1]/div/a').click()
    
    # Scroll Down a little bit 
    time.sleep(2)
    driver.find_element_by_xpath('/html/body').send_keys(Keys.SPACE)
    time.sleep(2)

    for each in data["interests"]:
        try:
            try:
                driver.find_element_by_xpath('/html/body/app-root/div/app-user/app-user-profile/main/div[2]/div/div[2]/div[2]/div[9]/app-interest/div[1]/button').click()
            except:
                driver.find_element_by_xpath('/html/body/app-root/div/app-user/app-user-profile/main/div[2]/div/div[2]/div[2]/div[9]/app-interest/div/button').click()

            # Interest
            driver.find_element_by_xpath('//*[@id="add-interest"]').send_keys(each["interest"])

            # Description
            driver.find_element_by_xpath('//*[@id="add-interest-description"]').send_keys(each["description"])

            # Media
            if "http" not in each["media"]:
                a = 1
            else:
                img_data = requests.get(each["media"]).content

                with open('interest.jpg', 'wb') as handler:
                    handler.write(img_data)

                time.sleep(1)
                driver.find_element_by_xpath('//*[@id="upload-image"]').send_keys('/home/miriani/Desktop/link_tool/interest.jpg')

            # Save
            driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/app-interest-modal/div/div/form/div[2]/div/button[2]').click()

            time.sleep(3)

        except Exception as e:
            driver.find_element_by_xpath('/html/body/ngb-modal-window/div/div/div/h1/a').click()
            print("Interests", e)
            continue
        
    print("Interests Completed")
    driver.close()



# test_id = "5f102ba7780fd607abdaa59f"

# Sales_Update_Profile_Picture(test_id)
# Sales_Update_Story_Info(test_id)
# Sales_Update_Headline_Info(test_id)
# Sales_Update_Interests_Info(test_id)
# Sales_Update_Accomplishments_Info(test_id)
# Sales_Update_Language_Info(test_id)
# Sales_Update_Education_Info(test_id)
# Sales_Update_Experience_Info(test_id)


'''
    Need to work on, It is very difficult because of our back-end:

    1) - Tools & Technology Module
    2) - Skills Module
'''