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
from selenium.common.exceptions import NoSuchElementException

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

print("Current working directory: {}".format(current_dir))
print("Using minecraft version {}".format(version))

# Get mod project ID number for the Curseproxy API
def get_project_id(mod_name):
    query_url = "https://google.com/search?q=site:curseforge.com+" + mod_name
    browser.get(query_url)
    try:
        mod_link = browser.find_element_by_partial_link_text("Mods - Minecraft - CurseForge") 
        mod_link.click()
    except NoSuchElementException:    
            print("Element was not found. This could mean that there was an internal error, but \nit usually means that the mod is not on Curseforge.")
            browser.quit()
            exit()
    files = browser.find_element_by_partial_link_text("Files")
    files.click
    project_id = browser.find_element_by_css_selector("div.mb-3:nth-child(2) > div:nth-child(1) > span:nth-child(2)").text

    browser.quit()
    return project_id

mod_id = get_project_id("ProjectE-1.12.2-PE1.4.1.jar")
print(mod_id)