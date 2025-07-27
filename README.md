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

# License
This project is licensed under the MIT License - see the [LICENSE](https://opensource.org/license/MIT) file for details.
