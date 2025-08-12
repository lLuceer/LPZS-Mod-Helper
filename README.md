# **Luceer-s-Project-Zomboid-Server-s-Mod-Helper**
Hiya, wanted an easy way to add mods to a modded self hosted Project Zomboid server for me and my friends but figured I could share it with the community, it may or may not already exists but here's my iteration on it.

# **Description**
It's a pretty dumbed down scrapper it'll just take everything you have installed in the steam workshop for project zomboid and output it in a copy of your .ini file already at the intended emplacement while your old .ini file will be renamed "backup_<old_name>.ini"

After quite a lot of update I can no longer call it dumb 😔 It now ask for steam path (it'll use it to set workshop path so if you use the **Collection Downloader** you can set the "SteamCMD" as path. As well as the game/server path so you won't have to take any more steps if you use a dedicated server or have your game outside the usual location

There are two versions the "PZ_mod_helper.py" that just scan the downloaded workshop files and input it in your .ini file

And the newer version "PZ_mod_helper_CopyWorkshop.py" that will like the first version scan your downloaded workshop items and input it in the .ini file but it will also copy all the mods in the folder into your local or dedicated server so you don't have to download them 2 times. It also allow to never get the infamous stuck on 0/172304 error

I included a shortcut to open the default location of .ini files but downloading it modify the extension to **Open Ini location.lnk.download** you will need to manually delete the .download extension if successful it'll look like a folder with a shortcut Icon and no visible extension

# **Tutorials**
[PZ_Mod_Helper](https://www.youtube.com/watch?v=kZ4J03z4sEA)

[Collection_Downloader](https://www.youtube.com/watch?v=L98L-_9AdOM)

# **Requierements**
Python 3.x [Link Here](https://www.python.org/downloads/)

# **How to use**
1. Simply download "PZ_mod_helper.py" or "PZ_mod_helper_CopyWorkshop.py" and place it anywhere easily accessible

2. Double click it to setup your steam and game paths then press enter to close when prompted to

3. Then go to your server .ini file by default it should be located in "%userprofile%/zomboid/server" or "C:/Users/_your username_/zomboid/server"

4. And just drag n drop it on the .py script

5. You'll then be prompted with a CMD window who ask wich submods to include as some mods have different version separated by submods you can select just one by entering the numerical value that will be shown or multiple by separating the different numerical value by a comma e.g. : 1 or 3 or 1,3,4

* To change the saved steam path or game path either delete "path_config.txt" and double click the script or you can edit it and set both path manually the first one being your steam/steamCMD path and the second one being your Project Zomboid/PZ Dedicated Server path

* **/!\ It doesn't import workshop maps**

# **Collection downloader**
For those that may have other mod than what they want to add I added 2 scripts to download only that collection, it uses SteamCMD download it [here](https://developer.valvesoftware.com/wiki/SteamCMD)

1. Place steamCMD in a new folder then launch it. It will download all requiered files and when it finish you can just close it

2. For getting the collec you will need python3.x, requests and beautifulsoup4 to install them make sure to check "pip" and on the next page "add python to environment variables" when installing python. If you forgot about it you can rerun the installer and select **modify** then run a cmd prompt and enter : **pip install requests beautifulsoup4**

3. Next place **download_collec.py** in your SteamCMD folder and double click it it'll take a few second to load then paste your collection ID or link when prompted to and it'll download everything

* SteamCMD being a bit clunky it may takes some time especially with bigger mods that may fail multiple times, added a bruteforce at the end for those bigger mods but I only tested it with brita's weapon pack, it should still work with multiple of those bigger mods but I haven't been able to verify it

* It is thinked for project zomboid but you can easilly change it for any game that allow [anonymous download](https://steamdb.info/sub/17906/apps/) for that simply open "download_collec.py" with your notepad and replace the **STEAM_APP_ID = "_108600_"** by the ID of your game

# **Map Reset Helper**
Added a script to delete map cells, chunk data or zpop chunk

**How to use ?**

1. Double click on the script "Map_reset_helper.py"

2. When prompted enter your save files path usually %userprofile%/zomboid/saves/multiplayer/xxxxxxx

3. You'll then be prompted which files you wanna delete, [1] map cells/[2] chunk data/[3] zpop chunk select the one you want to delete files for

4. Then use [this site](https://map.projectzomboid.com/) to find the coordinates, don't forget to check "Overlay Grid" to actually see the coordinates.  **green top righ are map cells and yellow top right are chunk cell**

5. Then enter top left cell/chunk coordinate in X_Y format > press enter

6. Do the same for bottom right coordinate

7. You'll then be prompted to [1]include or [2]exclude, include means that everything between X1_Y1 and X2_Y2 will be deleted, exclude means that everything but X1_Y1 and X2_Y2 will be deleted

8. You'll be prompted with a confirmation just write out "y" and it'll delete either all files between this square or all other files depending on include/exclude mode
