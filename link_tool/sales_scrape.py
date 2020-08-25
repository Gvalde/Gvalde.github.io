from scrapy.selector import Selector
from w3lib.html import remove_tags
from pprint import pprint as pp
import re
from random import randint
from datetime import datetime
import pymongo
from bson import ObjectId

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["sales_db"]
companies = mydb["companies"]

def Sales_GetProfile(_id):
    with open("templates/page.html", "r") as f:
        page = f.read()

    # Name
    try:
        name = Selector(text=page).xpath('/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[1]/section/div[2]/div[2]/div[1]/ul[1]/li[1]/text()').get()
        person_name = name.strip()
        first_name = person_name.split(" ")[0]
        last_name = person_name.split(" ")[1]
    except:
        person_name = ""
        first_name = ""
        last_name = ""

    # Photo
    try:
        photo = Selector(text=page).xpath('/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[1]/section/div[2]/div[1]/div[1]/div/div/img/@src').get()
    except:
        photo = ""

    # Headline
    try:
        headline = Selector(text=page).xpath('/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[1]/section/div[2]/div[2]/div[1]/h2/text()').get()
        headline = headline.strip()
    except:
        headline = ""

    # Country
    try:
        country = Selector(text=page).xpath('/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[1]/section/div[2]/div[2]/div[1]/ul[2]/li[1]/text()').get()
        country = country.strip()
    except:
        country = ""

    # Number of connections
    try:
        number_of_connections = Selector(text=page).xpath('/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[1]/section/div[2]/div[2]/div[1]/ul[2]/li[2]/span/text()').get()
        number_of_connections = number_of_connections.strip()
    except:
        number_of_connections = ""

    # Current Company
    try:
        current_company = Selector(text=page).xpath('/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[1]/section/div[2]/div[2]/div[2]/ul/li[1]/a/span/text()').get()
        current_company = current_company.strip()
    except:
        current_company = ""

    # # Education
    # try:
    #     education = Selector(text=page).xpath('//*[@id="ember95"]/text()').get()
    #     education = education.strip()
    # except:
    #     education = ""

    # # Personal Website
    # try:
    #     website = Selector(text=page).xpath('/html/body/main/section[1]/section/section[1]/div/div[1]/div[2]/div/div[3]/a/@href').get()
    # except:
    #     website = ""

    # About
    try:
        about = Selector(text=page).xpath('/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[3]/section/p').get()
        about = remove_tags(about)
        about = about.replace("\n", "")
        about = re.sub(" +", " ", about)
        about = about.replace("see more", "")
        about = about.strip()
    except:
        about = ""


    experience = []
    for i in range(1, 10):
        try:
            # Position
            try:
                position = Selector(text=page).xpath(f'/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[5]/span/div/section/div[1]/section/ul/li[{i}]/section/div/div/a/div[2]/h3/text()').get()
                position = position.strip()
            except:
                position = ""


            # Company
            try:
                company = Selector(text=page).xpath(f'/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[5]/span/div/section/div[1]/section/ul/li[{i}]/section/div/div/a/div[2]/p[2]/text()').get()
                company = company.strip()
            except:
                company = ""

            # Company Website
            try:
                company_website = Selector(text=page).xpath(f'/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[5]/span/div/section/div[1]/section/ul/li[{i}]/section/div/div/a/@href').get()
                company_website = "https://www.linkedin.com" + company_website
            except:
                company_website = ""

            # Company Logo
            try:
                company_logo = Selector(text=page).xpath(f'/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[5]/span/div/section/div[1]/section/ul/li[{i}]/section/div/div/a/div[1]/img/@src').get()
            except:
                company_logo = ""

            # time
            try:
                time = Selector(text=page).xpath(f'/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[5]/span/div/section/div[1]/section/ul/li[{i}]/section/div/div/a/div[2]/div/h4[1]/span[2]/text()').get()
                time = time.strip()
            except:
                time = ""

            # Location
            try:
                location = Selector(text=page).xpath(f'/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[5]/span/div/section/div[1]/section/ul/li[{i}]/section/div/div/a/div[2]/h4/span[2]/text()').get()
            except:
                location = ""
            if company is None or company == "":
                continue
            insertion = {
                "position" : position,
                "company" : company,
                "company_website" : company_website,
                "company_logo" : company_logo,
                "time" : time,
                "location" : location
            }
            experience.append(insertion)
        except:
            print("no more")
            continue

        
    languages = []
    for i in range(1, 10):
        try:
            # Language
            try:
                language = Selector(text=page).xpath(f'/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[8]/section/div/section/div/div/ul/li[{i}]').get()
                language = remove_tags(language)
                language = language.strip()
            except:
                language = ""
            
            proficiency = "fluent"

            if language is None or language == "":
                continue
            insertion = {
                "language" : language,
                "proficiency" : proficiency
            }
            languages.append(insertion)

        except:
            print("no more")
            continue

    education = []
    for i in range(1, 10):
        try:
            # Institution
            try:
                institution = Selector(text=page).xpath(f'/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[5]/span/div/section/div[2]/section/ul/li[{i}]/div/div/a/div[2]/div/h3/text()').get()
            except:
                institution = ""
            
            if institution is None or institution == "":
                continue

            # major
            try:
                major = Selector(text=page).xpath(f'/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[5]/span/div/section/div[2]/section/ul/li[{i}]/div/div/a/div[2]/div/p[1]/span[2]/text()').get()
            except:
                major = ""

            # years
            try:
                years = Selector(text=page).xpath(f'/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[5]/span/div/section/div[2]/section/ul/li[{i}]/div/div/a/div[2]/p[1]/span[2]').get()
                years = remove_tags(years)
                years = years.strip()
            except:
                years = ""

            # Activities
            try:
                activities = Selector(text=page).xpath(f'/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[5]/span/div/section/div[2]/section/ul/li[{i}]/div/div/a/div[2]/p[2]/span[2]').get()
                activities = remove_tags(activities)
                activities = activities.strip()
            except:
                activities = ""

            # Institution logo
            try:
                institution_logo = Selector(text=page).xpath(f'/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[5]/span/div/section/div[2]/section/ul/li[{i}]/div/div/a/div[1]/img/@src').get()
            except:
                institution_logo = ""        

            insertion = {
                "institution" : institution,
                "major" : major,
                "years" : years,
                "activities" : activities,
                "institution_logo" : institution_logo
            }

            education.append(insertion)
        except:
            print("no more")
            continue


    accomplishments = []
    for i in range(1, 10):
        try:
            # Name
            try:
                name = Selector(text=page).xpath(f'/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[5]/span/div/section/div[3]/section/ul/li[{i}]/div/a/div[2]/h3/text()').get()
            except:
                name = ""
            if name is None or name == "":
                continue

            # Authority
            try:
                authority = Selector(text=page).xpath(f'/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[5]/span/div/section/div[3]/section/ul/li[{i}]/div/a/div[2]/p/span[2]/text()').get()
            except:
                authority = ""

            # Media
            try:
                media = Selector(text=page).xpath(f'/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[5]/span/div/section/div[3]/section/ul/li[{i}]/div/a/div[1]/img/@src').get()
            except:
                media = ""
            
            insertion = {
                "name" : name,
                "authority" : authority,
                "media" : media
            }
            
            accomplishments.append(insertion)
        except:
            print("No More")
            continue

    interests = []
    for i in range(1, 10):
        try:
            # Interest
            try:
                interest = Selector(text=page).xpath(f'/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[9]/div/section/ul/li[{i}]/a/div[2]/h3/span/text()').get()
            except:
                interest = ""
            if interest is None or interest == "":
                continue

            # Description
            try:
                description = Selector(text=page).xpath(f'/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[9]/div/section/ul/li[{i}]/a/div[2]/p[2]/text()').get()
            except:
                description = ""

            # Media
            try:
                media = Selector(text=page).xpath(f'/html/body/div[7]/div[3]/div/div/div/div/div[2]/main/div[2]/div[9]/div/section/ul/li[{i}]/a/div[1]/img/@src').get()
            except:
                media = ""

            insertion = {
                "interest" : interest,
                "description" : description,
                "media" : media
            }

            interests.append(insertion)


        except:
            print("No More")
            continue

    data = {
        "name" : person_name,
        "first_name" : first_name,
        "last_name" : last_name,
        "photo" : photo,
        "headline" : headline,
        "country" : country,
        "current_company" : current_company,
        "number_of_connections" : number_of_connections,
        "education" : education,
        # "website" : website,
        "about" : about,
        "experience" : experience,
        "language" : languages,
        "interests" : interests,
        "raw_html" : page,
        "accomplishments" : accomplishments,
        "created_at" : datetime.utcnow()
    }

    companies.update({"_id" : ObjectId(_id)}, { "$set" : { "linkedin" : data } })

    companies.update({"_id" : ObjectId(_id)}, {"$set" : { "updated" : True }})

    print(data)
    return data

# Sales_GetProfile("5f102ba7780fd607abdaa59f")