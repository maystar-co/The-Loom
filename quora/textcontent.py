# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from webdriver_manager.chrome import ChromeDriverManager
# import time
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC



# def login_quora():

#     options = webdriver.ChromeOptions()
#     options.add_argument('--headless')
    
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-dev-shm-usage')
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


#     try:
        
#         with open("quora_answer_links.txt", "r") as file:
#             questions= file.readlines()

#         for question in questions:
            
#             driver.get(question)

#             WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "q-box")))

#             # Get the page source after JavaScript has executed
#             page_source = driver.page_source

#             # Parse the page content using BeautifulSoup
#             soup = BeautifulSoup(page_source, 'html.parser')

#             # Extract all text content
#             content_divs = soup.find_all('p', class_='q-text qu-display--block qu-wordBreak--break-word qu-textAlign--start')
#             texts = [div.get_text(separator=' ', strip=True) for div in content_divs]
            
#             j=0
#             for i, text in enumerate(texts):
#                 j+=1
#                 print(f"Content {i+1}:\n{text}\n")

#             print("*********************##################################*********************##################################")
#             content_divs = soup.find_all('li', class_='q-relative')
#             texts = [div.get_text(separator=' ', strip=True) for div in content_divs]

#             for i, text in enumerate(texts):
#                 j+=1
#                 print(f"Content {i+1}:\n{text}\n")

#             print("*********************##################################*********************##################################")
#             content_divs = soup.find_all('ol', class_='q-box')
#             texts = [div.get_text(separator=' ', strip=True) for div in content_divs]

#             for i, text in enumerate(texts):
#                 j+=1
#                 print(f"Content {i+1}:\n{text}\n")
#     #q-box qu-userSelect--text
#             print("*********************##################################*********************##################################")
#             content_divs = soup.find_all('div', class_='q-text qu-wordBreak--break-word')
#             texts = [div.get_text(separator=' ', strip=True) for div in content_divs]

#             for i, text in enumerate(texts):
#                 # print("answers from the following quesiton : ", question)
#                 print(f"Content {i+1}:\n{text}\n")
#             print("total answers: ",j)
#     finally:
#         driver.quit()
 
    
# login_quora()



from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrapetext():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # Initialize the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        with open("quora_answer_links.txt", "r") as file:
            questions = file.readlines()

        for question_url in questions:
            driver.get(question_url.strip())  
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "q-box")))

            page_source = driver.page_source

            soup = BeautifulSoup(page_source, 'html.parser')

            answer_texts = []

            # Extract all text content from different types of answer containers
            for tag, class_name in [('p', 'q-text qu-display--block qu-wordBreak--break-word qu-textAlign--start'),
                                    ('li', 'q-relative'),
                                    ('ol', 'q-box'),
                                    ('div', 'q-text qu-wordBreak--break-word'),
                                    ('div', 'q-box spacing_log_answer_content puppeteer_test_answer_content')]:
                content_divs = soup.find_all(tag, class_=class_name)
                for i, div in enumerate(content_divs):
                    text = div.get_text(separator=' ', strip=True)
                    answer_texts.append(f"Content {len(answer_texts)+1}:\n{text}\n")
            
            # Write all answers to the raw_data.txt file
            with open("raw_data.txt", "a", encoding="utf-8") as raw_file:
                raw_file.write(f"Answers from: {question_url}\n\n")
                raw_file.write("\n".join(answer_texts))
                raw_file.write("\n\n")

            print(f"Saved answers from: {question_url}")

    finally:
        driver.quit()

# Execute the function
scrapetext()
