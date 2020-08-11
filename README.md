# modupdater-mc

A tool for updating manually-downloaded Minecraft mods from curseforge to their latest versions, using [Selenium](https://selenium.dev) and [CurseProxy](https://github.com/NikkyAI/CurseProxy). It is currently in a very unstable state, and I cannot recommend that anybody use this program without first creating a backup of their mods folder.

## Prerequisites
- Minecraft installed with mods (Obviously)
- If using from source, you will need:
  - [Python 3.8](https://python.org) installed  
  - to install selenium via pip/pip3 with the command ```pip3 install selenium``` on Linux and ```pip install selenium``` on Windows
  - to install wget via pip/pip3 with the command ```pip3 install wget``` on Linux and ```pip install wget``` on Windows
  - You will also need to install the Gecko webdriver by Mozilla. That process is explained in [this StackOverflow question/answer](https://stackoverflow.com/questions/41190989/how-do-i-install-geckodriver). After this is done, you will need to specify the path to the webdriver in the options.txt file if you are on Windows. If you are on Linux, all you will need to do is run ```sudo apt install firefox-geckodriver```. You can also download the geckodriver binaries for all OSes from [here](https://github.com/mozilla/geckodriver/releases).
  
This does not currently and will not ever work with mods from sites that aren't [Curseforge](https://www.curseforge.com/minecraft/mc-mods/).    
Known mods that do not work either because of them not being on Curseforge or some other API error: Aether Legacy (API Error), Aroma1997Core (API Error), Aroma1997 Dimensional Worlds (API Error), ConnectedTexturesMod (API Error), Galacticraft and MicdooldleCore (Not on Curseforge).  
These mods will simply be ignored in the event that they are present in your mods folder.

#### Help! I keep trying to update my mods, but I keep getting the HTTPConnectionPool/MaxRetryError message!  
I am currently working on fixing this, so hang tight.
