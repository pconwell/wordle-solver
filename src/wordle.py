from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep

import word_generator


# we need to create a template to store our word selections so we
# can keep track if the letters are green/yellow/grey. 
# It start empty (obviously).
# if a character is not in the puzzle = 0
# if a character is in the puzzle but in the wrong spot = 1
# if a character is in the puzzle and in the right spot = 2
word_object = {0: [("",0),("",0),("",0),("",0),("",0)]}


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


def word_guesser(word_object, n):

   if n == 0:
      # seed (aka - cheat) the first word to help quickly narrow down the word list
      rand_word = ["NULL","audio"]
   else:
      # generate a random word from the list of possible solutions, based on the word_object "score"
      rand_word = word_generator.generate_word(word_object)
   print(f"Picking random word from {rand_word[0]} possible solutions: {rand_word[1]}")

   # for each letter in the word, click on the on-screen keyboard
   for letter in rand_word[1]:
      unpack_shadow_dom(f'game-app game-keyboard button[data-key="{letter}"]')[0].click()
   
   # click on the "SUBMIT" button and wait for the letter turning animation
   unpack_shadow_dom(f'game-app game-keyboard button[data-key="↵"]')[0].click()
   sleep(3) 

   # check the letters to see if they are green, yellow, or grey
   # and add them to the word object as appropriate
   tiles = unpack_shadow_dom(f'game-app game-row[letters="{rand_word[1]}"] game-tile')
   for n, tile in enumerate(tiles):
      print(tile.text, tile.get_attribute("evaluation"))
      if tile.get_attribute("evaluation") == "absent":
         # if the letter is gray, == 0
         word_object[0][n] = (tile.text, 0)
      elif tile.get_attribute("evaluation") == "present":
         # if the letter is yellow, == 1
         word_object[0][n] = (tile.text, 1)
      elif tile.get_attribute("evaluation") == "correct":
         # if the letter is green, == 2
         word_object[0][n] = (tile.text, 2)

   return word_object


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

# go through each of the 6 rows/guesses
for n, i in enumerate(range(7)):
   print(n)
   # if all of the letters are correct/green, we can stop the game
   if all(i[1] == 2 for i in word_object[0]):
      print(f"All letters are correct, the answer is: {[i[0] for i in word_object[0]]}")
      break
   if n == 6:
      print("The word was not found in the first 6 guesses.")
      break
   else:
      word_object = word_guesser(word_object, n)

driver.save_screenshot('WebsiteScreenShot.png')
driver.close()