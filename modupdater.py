# Import necessary modules
from os import path, chdir, remove
from time import sleep
from wget import download
from requests import get
from glob import glob
from re import sub

# Import Selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

script_dir = path.dirname(path.realpath(__file__))

# Create and populate the options_txt variable with the options.txt file
options_txt = []
with open(script_dir + "/options.txt") as source:
    for line in source:
        options_txt.append(line)

# Create geckopath variable and remove newline chars from options.txt
geckopath = r""
for character in options_txt[3]:
    if character != "\n":
        geckopath = geckopath + character

# Create version variable and remove newline chars from options.txt
game_version = ""
for character in options_txt[1]:
    if character != "\n":
        game_version = game_version + character

# Create mod_path variable and remove newline chars from options.txt
mod_path = ""
for character in options_txt[5]:
    if character != "\n":
        mod_path = mod_path + character


# Create and specify options for webdriver
options = Options()
options.headless = True

# Create the webdriver
if geckopath != "":
    browser = webdriver.Firefox(options=options, executable_path=geckopath)
else:
    browser =  webdriver.Firefox(options=options)

print("Using minecraft version {}".format(game_version))

raw_mod_list = glob(mod_path + "*.jar")
mod_list = []
for item in raw_mod_list:
    mod_list.append(sub(mod_path, "", item))

# Get mod project ID number for the Curseproxy API
def get_project_id(mod_name):
    query_url = "https://google.com/search?q=site:curseforge.com+" + mod_name
    browser.get(query_url)
    try:
        mod_link = browser.find_element_by_partial_link_text("Mods - Minecraft - CurseForge") 
        mod_link.click()
        project_id = browser.find_element_by_css_selector("div.mb-3:nth-child(2) > div:nth-child(1) > span:nth-child(2)").text
    except NoSuchElementException:    
        print("Element was not found. This could mean that there was an internal error, but \nit usually means that the mod is not on Curseforge.")
        browser.quit()
        pass
    return project_id

total_mods_done = 0

base_api_url = "https://curse.nikky.moe/api/addon/"

list_number = -1

recent_date = ""

chdir(mod_path)

for item in mod_list:
    list_number += 1
    if not (item.find("Galacticraft")):
        print(item)
        continue
    print("\nWorking on file: {}\n".format(item))
    try:
        mod_id = get_project_id(item)
    except UnboundLocalError:
        continue
    print("CurseForge Project ID: {}".format(mod_id))
    query = base_api_url + mod_id
    raw_api_response = get(query)
    if raw_api_response.ok == True:
        print("The request went through successfully (Status Code: {})\n".format(raw_api_response.status_code))
    else:
        print("An error occured with the API request. Status code {}".format(raw_api_response.status_code))
    while True:
        try:
            api_response = raw_api_response.json()
            files_response = get(query + "/files").json()
            break
        except:
            pass
    print("Mod name: {}".format(api_response["name"]))
    for entry in files_response:
        if entry["gameVersion"][0] == "1.12.2":
            if entry["fileDate"] > recent_date:
                recent_date = entry["fileDate"]
    print("Most recent file date: {}\n".format(recent_date))
    for list_item in files_response:
        if list_item["fileDate"] == recent_date and list_item["fileName"] != item:
            print(list_item["downloadUrl"])
            download(list_item["downloadUrl"])
            print("\n")
            remove(item)
        elif list_item["fileName"] == item:
            print("This mod is already the latest version.")
            pass
    recent_date = ""
    total_mods_done += 1
    print("Total mods completed: {}.".format(total_mods_done))
    sleep(2)

browser.quit()