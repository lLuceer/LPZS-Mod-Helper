# Luceer-s-Project-Zomboid-Server-s-Mod-Helper
Hiya, wanted an easy way to add mods to a modded self hosted Project Zomboid server, it may or may not already exist but here's my iteration on it.

# Description
It's a pretty dumbed down scrapper it'll just take everything you have installed in the steam workshop for project zomboid and output it in a copy of your .ini file already at the inteded emplacement while your old .ini file will be renamed "backup_<old_name>.ini"

# Requierements
Python 3.x [Link Here](https://www.python.org/downloads/)

# **How to use**
Simply download the "PZ_mod_helper.py" and place it anywhere easily accessible

Then go to your server .ini file by default it should be located in "%userprofile%/zomboid/server" or "C:/Users/_your username_/zomboid/server"
And just drag n drop it on the .py script

You'll then be prompted with a CMD window who ask wich submods to include as some mods have different version separated by submods you can select just one by entering the numerical value that will be shown or multiple by separating the different numerical value by a comma EX : 1,3,4

# /!\ For those that have steam outside the default path you will need to manually change the steam location /!\
Just open the script with your notepad or any other file editor and change the path on "workshop_path =" by r"_Your Steam Path_\Steam\steamapps\workshop\content\108600"

# Collection downloader
For those that may have other mod than what they want to add I added 2 scripts to download only that collection, it uses SteamCMD download it [here](https://developer.valvesoftware.com/wiki/SteamCMD)

1. Place steamCMD in a new folder then launch it. It will download all requiered files and when it finish you can just close it

2. For getting the collec you will need python3.x, requests and beautifulsoup4 to install them make sure to check "pip" and on the next page "add python to environment variables" when installing python. If you forgot about it you can rerun the installer and select **modify** then run a cmd prompt and enter : **pip install requests beautifulsoup4**

3. Then run "generate collec.py" it'll ask for the collection just enter the ID EX: _1234567890_, it will generate a .txt file with all workshop IDs of mods in that collection

4. Next place "download collec.py" in your steamCMD folder and drag n drop the txt file containing your workshop items on it

5. Before dragging n dropping your .ini file on the "PZ_mod_helper.py" right click on it and open with notepad and replace the path by : workshop_path = r"Your steamCMD path\steamapps\workshop\content\108600" then exit and save and you will be able to then drag n drop your ini file on it

*It is thinked for project zomboid but you can easilly change it for any game that allow [anonymous download](https://steamdb.info/sub/17906/apps/) for that simply open "download collec.py" with your notepad and replace the **Steam_APP_ID = "_108600_"** by the ID of your game

* Download collec.py can be used outside steamCMD but you will need to specify a path in the script just open it and enter the steamCMD folder in **STEAM_CMD_PATH = "_your path_"**

# License
This project is licensed under the MIT License - see the [LICENSE](https://opensource.org/license/MIT) file for details.
