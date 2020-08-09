# Import necessary modules
import os
from time import sleep
import wget
import requests as rq
import json


# Import Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located



# Get current dir so script can be run from anywhere
current_dir = os.path.dirname(os.path.realpath(__file__))

# Create and populate the options_txt variable with the options.txt file
options_txt = []
with open(current_dir + "/options.txt") as source:
    for line in source:
        options_txt.append(line)

# Create geckopath variable and remove newline chars from options.txt
geckopath = r""
for character in options_txt[3]:
    if character != "\n":
        geckopath = geckopath + character

# Create version variable and remove newline chars from options.txt
version = ""
for character in options_txt[1]:
    if character != "\n":
        version = version + character

browser = webdriver.Firefox(executable_path=geckopath)
options = Options()

base_api_url = "https://curse.nikky.moe/api/addon/"

print(current_dir)
print("Using minecraft version {}".format(version))

sleep(0.5)

query_url = "https://google.com/search?q=site:curseforge.com+Aether2"

# Get mod project ID number for the Curseproxy API
browser.get(query_url)
mod_link = browser.find_element_by_partial_link_text("Mods - Minecraft - CurseForge") 
mod_link.click()
files = browser.find_element_by_partial_link_text("Files")
files.click
current_browser_url = browser.current_url
project_id = browser.find_element_by_css_selector("div.mb-3:nth-child(2) > div:nth-child(1) > span:nth-child(2)").text

browser.quit()
print(project_id)

api_data = json.loads(rq.get(base_api_url + project_id).content)

print("Currently processing mod {}".format(api_data["name"]))