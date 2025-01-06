import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pyautogui

# create list of dictionary words to be used
file = "dict.csv"
wordList = []
for row in csv.reader(open(file)):
    word = row[0]
    if len(word) <= 3:
        continue
    else :
        wordList.append(word.upper())
wordList.sort(key=len, reverse=True)


driver = webdriver.Chrome()
driver.get("https://www.nytimes.com/puzzles/spelling-bee")
time.sleep(1)

# Terms will not be updated forever so this can be taken away at some point
updateTermsContinue = driver.find_element(By.CLASS_NAME, "purr-blocker-card__button")
updateTermsContinue.click()
time.sleep(1)

playButton = driver.find_element(By.CLASS_NAME, "pz-moment__button-wrapper:nth-child(1) > .primary")
playButton.click()
time.sleep(1)

# get center letter --> this is the letter that MUST be in the word
centerCell = driver.find_element(By.CSS_SELECTOR, ".hive-cell.center")
centerLetter = centerCell.find_element(By.CSS_SELECTOR, ".cell-letter").text

# list of outer cells
outerCells = driver.find_elements(By.CSS_SELECTOR, ".hive-cell.outer")

# list of the letters in ONLY the outer cells
letters = []
for cell in outerCells:
    outerLetter = cell.find_element(By.CSS_SELECTOR, ".cell-letter").text
    letters.append(outerLetter)

# find words that work for the hive cells
possibleWords = []
for word in wordList:
    possible = True
    for letter in word:
        if letter not in letters and letter is not centerLetter:
            possible = False
            break
    if centerLetter in word and possible:
        possibleWords.append(word)

print(possibleWords)

for word in possibleWords:
    pyautogui.typewrite(word)
    time.sleep(0.5)
    pyautogui.press('enter')

time.sleep(10)

driver.quit()