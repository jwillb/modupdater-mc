# modupdater-mc

A tool for updating Minecraft mods from curseforge to their latest versions, using [Selenium](https://selenium.dev) and [CurseProxy](https://github.com/NikkyAI/CurseProxy).

## Prerequisites
- Minecraft installed with mods (Obviously)
- If using from source, you will need:
  - [Python 3.8](https://python.org) installed  
  - to install selenium via pip/pip3 with the command ```pip3 install selenium``` on Linux and ```pip install selenium``` on Windows
  - to install wget via pip/pip3 with the command ```pip3 install wget``` on Linux and ```pip install wget``` on Windows
  - You will also need to install the Gecko webdriver by Mozilla. That process is explained in [this StackOverflow question/answer](https://stackoverflow.com/questions/41190989/how-do-i-install-geckodriver).
  
This does not currently and will not ever work with mods from sites that aren't [Curseforge](https://www.curseforge.com/minecraft/mc-mods/).  
