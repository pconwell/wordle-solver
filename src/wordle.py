import csv
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from time import sleep

import word_generator


# we need to create a template to store our word selections so we
# can keep track if the letters are green/yellow/grey. 
# It start empty (obviously).
# if a character is not in the puzzle = 0
# if a character is in the puzzle but in the wrong spot = 1
# if a character is in the puzzle and in the right spot = 2
word_object = {0: [("",0),("",0),("",0),("",0),("",0)],
               1: [("",0),("",0),("",0),("",0),("",0)],
               2: [("",0),("",0),("",0),("",0),("",0)],
               3: [("",0),("",0),("",0),("",0),("",0)],
               4: [("",0),("",0),("",0),("",0),("",0)],
               5: [("",0),("",0),("",0),("",0),("",0)]
              }


def unpack_shadow_dom(shadow_elements):
   """   
   Wordle website uses nested shadow DOMs to... hide stuff? IDK.
   This function just unpack the shadow DOMs and return the last element so we can interact with it

   Accepts a space delimited string of shadow elements,
   and assumes that the last element is not a shadow element.
   """

   elements = [i for i in shadow_elements.split(" ")]

   temp_list = []
   for n, _ in enumerate(elements[:-1]):
      if n == 0:
         temp_list.append(driver.execute_script('return arguments[0].shadowRoot', driver.find_element(By.CSS_SELECTOR, f"{elements[0]}")))
      else:
         temp_list.append(driver.execute_script('return arguments[0].shadowRoot', temp_list[n-1].find_element(By.CSS_SELECTOR, f"{elements[n]}")))

   return temp_list[-1].find_elements(By.CSS_SELECTOR, f"{elements[-1]}")


## WEBDRIVER
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=chrome_options)



# open wordle website and wait for it to load
driver.get("https://www.powerlanguage.co.uk/wordle/")
sleep(1)

# close the pop-up box by "clicking" the game icon (aka, the X)
unpack_shadow_dom("game-app game-modal game-icon")[0].click()
sleep(1)



## word 1
# get a random 5 letter word from the word_generator.py file
rand_word = word_generator.generate_word(word_object)
print(f"Picking random word from {rand_word[0]} possible solutions: {rand_word[1]}")

for letter in rand_word[1]:
   unpack_shadow_dom(f'game-app game-keyboard button[data-key="{letter}"]')[0].click()
unpack_shadow_dom(f'game-app game-keyboard button[data-key="↵"]')[0].click()
sleep(3) #turning over letters animation takes a while

# check the letters to see if they are green, yellow, or grey
# and add them to the word object as appropriate
tiles = unpack_shadow_dom(f'game-app game-row[letters="{rand_word[1]}"] game-tile')
for tile in tiles:
   print(tile.text, tile.get_attribute("evaluation"))
   if tile.get_attribute("evaluation") == "absent":
      # do something
      print("absent")




## word 2
# enter five letters, then press enter
word = "audio"
for letter in word:
   unpack_shadow_dom(f'game-app game-keyboard button[data-key="{letter}"]')[0].click()
unpack_shadow_dom(f'game-app game-keyboard button[data-key="↵"]')[0].click()
sleep(3) #turning over letters animation takes a while


tiles = unpack_shadow_dom(f'game-app game-row[letters="{word}"] game-tile')

for tile in tiles:
   print(tile.text, tile.get_attribute("evaluation"))





driver.save_screenshot('WebsiteScreenShot.png')
driver.close()














# for tile in tiles:
#    print(tile)
#    # i.send_keys("A")
#    # print(i.get_attribute("evaluation"))
#    # driver.execute_script("arguments[0].setAttribute('letter','A')", i)

# Now do the same thing to access the letter boxes
# shadow_root1 = driver.execute_script('return arguments[0].shadowRoot', driver.find_element(By.CSS_SELECTOR, "game-app"))
# shadow_root2 = driver.execute_script('return arguments[0].shadowRoot', shadow_root1.find_element(By.CSS_SELECTOR, "game-row"))
# shadow_root3 = shadow_root2.find_elements(By.CSS_SELECTOR, "game-tile")
# sleep(1)

# print(shadow_root3)

# for i in shadow_root3:
#    print(i)
   # i.send_keys("A")
   # print(i.get_attribute("evaluation"))
   # driver.execute_script("arguments[0].setAttribute('letter','A')", i)


# shadow_root3[0].send_keys(Keys.RETURN)





# driver.save_screenshot('WebsiteScreenShot.png')

# # element = driver.find_element_by_tag_name('head')
# # print(element)

# driver.close()








# with open('./words.csv', newline='') as f:
#    data = [row[0] for row in csv.reader(f)]



