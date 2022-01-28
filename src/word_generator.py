import csv
import re
import random

# TODO: scrape wordle dictionary from https://www.powerlanguage.co.uk/wordle/main.e65ce0a5.js

# if a character is not in the puzzle = 0
# if a character is in the puzzle but in the wrong spot = 1
# if a character is in the puzzle and in the right spot = 2
rows = {0: [("T",1),("R",0),("A",0),("I",0),("N",1)],
        1: [("N",1),("O",2),("T",1),("E",0),("D",0)],
        2: [("",0),("",0),("",0),("",0),("",0)],
        3: [("",0),("",0),("",0),("",0),("",0)],
        4: [("",0),("",0),("",0),("",0),("",0)],
        5: [("",0),("",0),("",0),("",0),("",0)]
       }

# a starting list of possible letters for each box
boxes = {0: ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"],
         1: ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"],
         2: ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"],
         3: ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"],
         4: ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"] 
        }

# create emtpy sets for included and excluded letters
includes = set([])
precludes = set([])

# iterate through each row
for row in rows.items():
   for n, i in enumerate(row[1]):
      if i[1] == 0:
         # if a letter is grey, add it to the precludes list and remove it from that box. You need to do both
         # because we may end up ultimately removing the letter from the exclude list (see below) if the letter is in the puzzle twice
         # it's a little hacky and not 100% correct, but it will keep a duplicated letter from appearing
         # in *this* box if we know *this* box doesn't contain that letter (but the letter *does* appear elsewhere in the puzzle)
         precludes.add(i[0])
         boxes[n].remove(i[0]) if i[0] in boxes[n] else None
      if i[1] == 1:
         # if a letter is in the puzzle but in the wrong spot, add it to the includes list
         # and remove it from the list of possible letters for that box
         includes.add(i[0])
         boxes[n].remove(i[0]) if i[0] in boxes[n] else None
      if i[1] == 2:
         # if a letter is in the puzzle and in the right spot, add it to the includes list
         # and set the available letters for that box to that letter
         includes.add(i[0])
         boxes[n] = [i[0]]

# remove any letters that are in the includes list from the precludes set
# this is thanks to a qwirk in the game where a letter may be green *and* grey if listed twice
# if the letter is left in both lists, it will exclude *all* words
# (it will try to find a word that includes AND doesn't include that letter - physically impossible)
for i in includes:
   precludes.discard(i)

# geneerate a list of words from csv file
with open('./words/words_la_ta.csv', newline='') as f:
   words = [row[0] for row in csv.reader(f)]

# create an empty list to store possible solutions
solutions = []

# iterate over list of words from csv file
for word in words:
   # turn each word into list of letters
   letters = list(word)

   # check if word contains *all* of the letters in the includes list
   # and does not contain *any* of the letters in the precludes list
   if all(x in letters for x in includes) and \
   not any(x in letters for x in precludes):

      # If yes above, check if each letter in the word matches
      # the available letters in for that box
      if letters[0] in boxes[0] and \
      letters[1] in boxes[1] and \
      letters[2] in boxes[2] and \
      letters[3] in boxes[3] and \
      letters[4] in boxes[4]:

         # if the word matches all the requirements, add it to the solutions list
         solutions.append(word)

# print a random word from the list of possible solutions
print(f"Picking random word from {len(solutions)} possible solutions: {random.choice(solutions)}")