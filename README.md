# Luceer-s-Project-Zomboid-Server-s-Mod-Helper
Hiya, wanted an easy way to add mods to a modded self hosted Project Zomboid server, it may or may not already exist but here's my iteration on it.

# Description
It's a pretty dumbed down scrapper it'll just take everything you have installed in the steam workshop for project zomboid and output it in a copy of your .ini file already at the inteded emplacement while your old .ini file will be renamed "backup_<old_name>.ini"

# **How to use**
Simply download the "PZ_mods.py" and place it anywhere easily accessible

Then go to your server .ini file by default it should be located in "%userprofile%/zomboid/server" or "C:/Users/_your username_/zomboid/server"
And just drag n drop it on the .py script

# /!\ For those that have steam outside the default path you will need to manually change the steam location /!\
Just open the script with your notepad or any other file editor and change the path on "workshop_path =" by r"_Your Steam Path_\Steam\steamapps\workshop\content\108600"

Other thing to mention is that you still have to check if the mods include subversion as some mod have for exemple multiple parameters stashed in the same mod and you pick the one you want by putting the mod ID in the ini file, there is no check so it'll add all of them and that may cause some issue but still better than taking 2 hours to manually add everything.

# License
This project is licensed under the MIT License - see the [LICENSE](https://opensource.org/license/MIT) file for details.
