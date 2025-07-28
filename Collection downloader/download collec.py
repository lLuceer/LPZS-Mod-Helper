import os
import sys
import subprocess
import re

# 🔧 Replace with the correct App ID for your game
STEAM_APP_ID = "108600"

# 🔧 Replace with your actual SteamCMD path if needed
STEAMCMD_PATH = "steamcmd"

def extract_ids_from_file(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    ids = []
    for line in lines:
        match = re.search(r'id=(\d+)', line)
        if match:
            ids.append(match.group(1))
    return ids

def download_mods(workshop_ids):
    for wid in workshop_ids:
        print(f"[+] Downloading Workshop ID: {wid}")
        cmd = [
            STEAMCMD_PATH,
            "+login", "anonymous",
            "+workshop_download_item", STEAM_APP_ID, wid,
            "+quit"
        ]
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"[!] Failed to download {wid}: {e}")

def main():
    if len(sys.argv) < 2:
        print("Drag and drop your workshop_links.txt file onto this script or run:")
        print("python download_mods_with_steamcmd.py workshop_links.txt")
        return

    filepath = sys.argv[1]

    if not os.path.isfile(filepath):
        print(f"[!] File not found: {filepath}")
        return

    print(f"[+] Reading workshop links from {filepath}...")
    workshop_ids = extract_ids_from_file(filepath)

    if not workshop_ids:
        print("[!] No valid workshop IDs found in the file.")
        return

    print(f"[+] Found {len(workshop_ids)} items to download.")
    download_mods(workshop_ids)

if __name__ == "__main__":
    main()
