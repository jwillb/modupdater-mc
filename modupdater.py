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
# Create necessary variables
script_dir = path.dirname(path.realpath(__file__))
total_mods_done = 0
base_api_url = "https://curse.nikky.moe/api/addon/"
recent_date = ""
bad_list = ["OptiFine", "Galacticraft", "MicdoodleCore", "Aroma1997", "CTM", "Thaumcraft", "aether_legacy"]
impossible_mods = []
mods_skipped = 0
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

# Display status message that shows when you start the appilication
print("Using minecraft version {}".format(game_version))

# Creates raw_mod_list and mod_list variables
raw_mod_list = glob(mod_path + "*.jar")
mod_list = []
for item in raw_mod_list:
    mod_list.append(sub(mod_path, "", item))

# Get mod project ID number for the Curseproxy API
def get_project_id(mod_name):
    query_url = "https://duckduckgo.com/?q=site:curseforge.com+" + mod_name
    browser.get(query_url)
    try:
        # Finding the project id by going to the mod's CurseForge page, after finding it on Google
        sleep(4.5)
        mod_link = browser.find_element_by_partial_link_text("curseforge.com") 
        mod_link.click()
        project_id = browser.find_element_by_css_selector("div.mb-3:nth-child(2) > div:nth-child(1) > span:nth-child(2)").text
    except NoSuchElementException:    
        # What to do if the mod was unable to find the link or find the project id
        print("Element was not found. This could mean that Selenium is broken, or \nthat the mod is not on Curseforge.")
        pass
    return project_id

chdir(mod_path)
for item in mod_list:
    no_version = False
    # Checking if mod matches any known problematic mod names
    skip = False
    for word in bad_list:
        if not item.find(word):
            skip = True
    if skip:
        impossible_mods.append(item)
        mods_skipped += 1
        print("\nSkipping current mod. ({})".format(item))
        continue
    
    # Shows user info about the file and its project id from CurseForge, if applicable
    print("\nWorking on file: {}\n".format(item))
    try:
        mod_id = get_project_id(item)
    except UnboundLocalError:
        continue
    print("CurseForge Project ID: {}".format(mod_id))
    
    # Getting the mod info from CurseProxy
    query = base_api_url + mod_id
    raw_api_response = get(query)
    
    # Showing the HTTP status code to the user, both in the event of a succesful and an unsuccesful fetch
    if raw_api_response.ok == True:
        print("The request went through successfully (Status Code: {})\n".format(raw_api_response.status_code))
    else:
        print("An error occured with the API request. Status code {}".format(raw_api_response.status_code))
    if raw_api_response.status_code == 404:
        continue
    
    # Repeatedly trying to decode the JSON data from the request until it works. For some unknown reason, the
    # .json() function really likes to fail for no reason and make programmers very angry
    while True:
        try:
            api_response = raw_api_response.json()
            files_response = get(query + "/files").json()
            break
        except:
            pass
    
    # Shows the user the mod name and other useful info
    print("Mod name: {}".format(api_response["name"]))
    # Finds the most recent file for the specified game version
    for entry in files_response:
        try:    
            if entry["gameVersion"][0] == game_version:
                if entry["fileDate"] > recent_date:
                    recent_date = entry["fileDate"]
        except IndexError:
            print("Mod {} has an API Error, skipping.".format(api_response["name"]))
            impossible_mods.append(item)
            mods_skipped += 1
    # Shows user the last uploaded file date
    print("Most recent file date: {}\n".format(recent_date))
    
    # Finds and downloads the file, after displaying the URL from which the file will download
    for list_item in files_response:
        if list_item["fileDate"] == recent_date and list_item["fileName"] != item:
            print(list_item["downloadUrl"])
            download(list_item["downloadUrl"])
            print("\n")
            remove(item)
        elif list_item["fileName"] == item:
            print("This mod is the latest version or there was \nno mod to be found in the specified version.")
            pass
    recent_date = ""
    
    # Shows the user the total amount of mods completed and skipped
    total_mods_done += 1
    print("Total mods completed: {}.".format(total_mods_done))

# Shows the user the mods that could not be checked or downloaded
if impossible_mods == []:
    impossible_mods = "None"

print("Mods that were not checked: {} {}".format(mods_skipped, impossible_mods))

browser.quit()