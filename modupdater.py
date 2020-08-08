import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located

browser = webdriver.Firefox()
options = Options()

# Get current dir so script can be run from anywhere
current_dir = os.path.dirname(os.path.realpath(__file__))

# Create and populate the options_txt variable with the options.txt file
options_txt = []
with open(current_dir + "/options.txt") as source:
    for line in source:
        options_txt.append(line)

# Create version variable and remove newline chars
version = ""
for character in options_txt[1]:
    if character != "\n":
        version = version + character

print(current_dir)
print("Using minecraft version {}".format(version))

sleep(0.5)

print("Searching...")
query_url = "https://www.google.com/search?q=site:curseforge.com+fossilsarcheology"

browser.get(query_url)
links = browser.find_element_by_partial_link_text("Mods - Minecraft - CurseForge") 
links.click()
files = browser.find_element_by_partial_link_text("Files")
files.click
current_browser_url = browser.current_url
new_url = current_browser_url + "/files"
browser.get(new_url)

sleep(3)
browser.quit()
print(new_url)