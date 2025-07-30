# **Luceer-s-Project-Zomboid-Server-s-Mod-Helper**
Hiya, wanted an easy way to add mods to a modded self hosted Project Zomboid server, it may or may not already exist but here's my iteration on it.

# **Description**
It's a pretty dumbed down scrapper it'll just take everything you have installed in the steam workshop for project zomboid and output it in a copy of your .ini file already at the inteded emplacement while your old .ini file will be renamed "backup_<old_name>.ini"

After quite a lot of update I can no longer call it dumb 😔 It now ask for steam path (it'll use it to set workshop path so if you use the **Collection Downloader** you can set the "SteamCMD" path

There are two versions the "PZ_mod_helper.py" that just scan the downloaded workshop files and input it in your .ini file

And the newer version "PZ_mod_helper_CopyWorkshop.py" that will like the first version scan your downloaded workshop items and input it in the .ini file but it will also copy all the mods in the folder into your local or dedicated server so you don't have to download them 2 times it also allow to never get the infamous stuck on 0/172304 error

# **Requierements**
Python 3.x [Link Here](https://www.python.org/downloads/)

# **How to use**
1. Simply download "PZ_mod_helper.py" or "PZ_mod_helper_CopyWorkshop.py" and place it anywhere easily accessible

2. Double click it to setup your steam and game paths then press enter to close when prompted to

3. Then go to your server .ini file by default it should be located in "%userprofile%/zomboid/server" or "C:/Users/_your username_/zomboid/server"

4. And just drag n drop it on the .py script

5. You'll then be prompted with a CMD window who ask wich submods to include as some mods have different version separated by submods you can select just one by entering the numerical value that will be shown or multiple by separating the different numerical value by a comma EX : 1,3,4

* To change the saved steam path or game path either delete "path_config.txt" and double click the script or you can edit it and set both path manually the first one being your steam/steamCMD path and the second one being your Project Zomboid/PZ Dedicated Server path

* **/!\ It doesn't import workshop maps**

# **Collection downloader**
For those that may have other mod than what they want to add I added 2 scripts to download only that collection, it uses SteamCMD download it [here](https://developer.valvesoftware.com/wiki/SteamCMD)

1. Place steamCMD in a new folder then launch it. It will download all requiered files and when it finish you can just close it

2. For getting the collec you will need python3.x, requests and beautifulsoup4 to install them make sure to check "pip" and on the next page "add python to environment variables" when installing python. If you forgot about it you can rerun the installer and select **modify** then run a cmd prompt and enter : **pip install requests beautifulsoup4**

3. Then run "generate collec.py" it'll ask for the collection just enter the ID EX: _1234567890_, it will generate a .txt file with all workshop IDs of mods in that collection

4. Next place "download collec.py" in your steamCMD folder and drag n drop the txt file containing your workshop items on it

* It is thinked for project zomboid but you can easilly change it for any game that allow [anonymous download](https://steamdb.info/sub/17906/apps/) for that simply open "download collec.py" with your notepad and replace the **Steam_APP_ID = "_108600_"** by the ID of your game
