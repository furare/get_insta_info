from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import requests
import json
import os
from logging import Logger

username = os.getenv('LOGIN_USERNAME')
password = os.getenv('LOGIN_PASSWORD')
targetuser = os.getenv('TARGET_USERNAME')
api_url = os.getenv('SS_API_URL')

try:
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.instagram.com")

    sleep(5)
    loginForm = driver.find_element(By.ID, "loginForm")
    loginForm.find_element(By.NAME,"username").send_keys(username) 
    loginForm.find_element(By.NAME,"password").send_keys(password)

    btns = driver.find_elements(By.TAG_NAME,"button")
    for b in btns:
        Logger.info(b.text)
        if b.text == 'Log in':
            b.click()
            break
    sleep(10)
    driver.get(f"https://www.instagram.com/{targetuser}/")
    sleep(10)

    followers = driver.find_element(By.XPATH, f'//a[@href="/{targetuser}/followers/"]')
    Logger.info(followers.text)
    follwers_count = followers.find_element(By.TAG_NAME,"span").get_attribute('title')
    Logger.info(follwers_count)

    following = driver.find_element(By.XPATH, f'//a[@href="/{targetuser}/following/"]')
    Logger.info(following.text)
    following_count = following.find_element(By.TAG_NAME,'span').get_attribute('innerHTML')
    Logger.info(following_count.replace("<span>","").replace("</span>",""))
    sleep(10)

    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'follower': follwers_count,
        'following': following_count.replace("<span>","").replace("</span>","")
    }

    request_response = requests.post(api_url,data=json.dumps(data), headers=headers)
    Logger.info(request_response.json())
except:
    Logger.exception("...What is doing when exception happens...")
finally:
    driver.quit()