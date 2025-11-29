import json
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

email = "diyar19961@mposhop.com"
password = "Admin@123"

def login_quora(email, password):
    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # Uncomment this line to run in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Open Quora login page
    driver.get('https://www.quora.com')
    
    time.sleep(2)
    # Find and fill the email and password fields
    email_field = driver.find_element(By.NAME, "email")
    email_field.send_keys(email)
    time.sleep(2)
    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys(password)
    time.sleep(2)
    password_field.send_keys(Keys.RETURN)
    time.sleep(3)  
    driver.refresh()
    cookies = driver.get_cookies()
    driver.quit()
    with open("cookies.json", "w") as file:
        json.dump(cookies, file, indent=4)

