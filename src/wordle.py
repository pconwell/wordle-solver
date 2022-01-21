import csv
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep


## WEBDRIVER
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=chrome_options)

# open wordle website and wait for it to load
driver.get("https://www.powerlanguage.co.uk/wordle/")
sleep(1)

# wordle uses nested shadow doms to... hide stuff? ... so jump through the dom layers and close the pop-up
shadow_root1 = driver.execute_script('return arguments[0].shadowRoot', driver.find_element(By.CSS_SELECTOR, "game-app"))
shadow_root2 = driver.execute_script('return arguments[0].shadowRoot', shadow_root1.find_element(By.CSS_SELECTOR, "game-modal"))
shadow_root3 = shadow_root2.find_element(By.CSS_SELECTOR, "game-icon").click()
sleep(1)

# Now do the same thing to access the letter boxes
shadow_root1 = driver.execute_script('return arguments[0].shadowRoot', driver.find_element(By.CSS_SELECTOR, "game-app"))
shadow_root2 = driver.execute_script('return arguments[0].shadowRoot', shadow_root1.find_element(By.CSS_SELECTOR, "game-row"))
shadow_root3 = shadow_root2.find_elements(By.CSS_SELECTOR, "game-tile")
sleep(1)

for i in shadow_root3:
   print(i)


driver.save_screenshot('WebsiteScreenShot.png')

# element = driver.find_element_by_tag_name('head')
# print(element)

driver.close()








# with open('./words.csv', newline='') as f:
#    data = [row[0] for row in csv.reader(f)]



