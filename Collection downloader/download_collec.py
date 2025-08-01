import os
import re
import sys
import time
import subprocess
import requests
from bs4 import BeautifulSoup

# Config
STEAM_APP_ID = "108600"
STEAMCMD_PATH = "steamcmd"
WORKSHOP_PATH = os.path.join("steamapps", "workshop", "content", STEAM_APP_ID)
FAILED_LOG_FILE = "failed_mods_final.txt"

def check_steamcmd():
    try:
        subprocess.run([STEAMCMD_PATH, "+login", "anonymous", "+quit"], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        print("❌ SteamCMD not found or not working. Check STEAMCMD_PATH.")
        sys.exit(1)

def extract_collection_id(input_str):
    match = re.search(r'id=(\d+)', input_str)
    return match.group(1) if match else (input_str if input_str.isdigit() else None)

def fetch_workshop_ids_from_collection(collection_id):
    url = f"https://steamcommunity.com/sharedfiles/filedetails/?id={collection_id}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    print(f"[+] Fetching collection: {url}")

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch collection: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    ids = []
    for div in soup.find_all('div', class_='collectionItem'):
        link_tag = div.find('a', href=True)
        if link_tag:
            match = re.search(r'id=(\d+)', link_tag['href'])
            if match:
                ids.append(match.group(1))

    if not ids:
        print("⚠️ No items found — Steam layout may have changed.")
    return ids

def is_mod_downloaded(mod_id):
    return os.path.exists(os.path.join(WORKSHOP_PATH, mod_id))

def download_mod_with_retry(mod_id, max_attempts=5, retry_delay=5):
    if is_mod_downloaded(mod_id):
        print(f"✅ [Mod {mod_id}] Already downloaded.")
        return True

    print(f"\n⬇️  [Mod {mod_id}] Starting download...")

    attempt = 0
    while attempt < max_attempts:
        attempt += 1

        script_lines = [
            "login anonymous",
            f"workshop_download_item {STEAM_APP_ID} {mod_id}",
            "quit"
        ]

        temp_script = f"temp_retry_{mod_id}.txt"
        with open(temp_script, "w") as f:
            f.write("\n".join(script_lines))

        try:
            subprocess.run([STEAMCMD_PATH, "+runscript", temp_script], check=True)
        except subprocess.CalledProcessError as e:
            print(f"⚠️ SteamCMD error (attempt {attempt}): {e}")
        finally:
            if os.path.exists(temp_script):
                os.remove(temp_script)

        if is_mod_downloaded(mod_id):
            print(f"✅ [Mod {mod_id}] Downloaded successfully after {attempt} attempt(s).")
            return True
        else:
            print(f"🔁 [Mod {mod_id}] Not downloaded. Retrying in {retry_delay}s...")
            time.sleep(retry_delay)

    print(f"❌ [Mod {mod_id}] Failed after {max_attempts} attempts.")
    return False

def save_failed_mods(failed_ids):
    if failed_ids:
        with open(FAILED_LOG_FILE, "w") as f:
            f.write('\n'.join(failed_ids))
        print(f"❌ Failed mods saved to: {FAILED_LOG_FILE}")
    else:
        print("🎉 All mods downloaded successfully.")

def main():
    check_steamcmd()

    user_input = input("🔗 Enter Steam collection URL, ID, or mod list file path: ").strip()
    mod_ids = []

    if "steamcommunity.com" in user_input or user_input.isdigit():
        collection_id = extract_collection_id(user_input)
        if not collection_id:
            print("❌ Invalid collection ID.")
            return
        mod_ids = fetch_workshop_ids_from_collection(collection_id)
    elif os.path.isfile(user_input):
        with open(user_input, 'r') as f:
            for line in f:
                line = line.strip()
                if line.isdigit():
                    mod_ids.append(line)
                else:
                    match = re.search(r'id=(\d+)', line)
                    if match:
                        mod_ids.append(match.group(1))
    else:
        print("❌ Input not recognized as URL, ID, or file.")
        return

    if not mod_ids:
        print("⚠️ No mods found to download.")
        return

    print(f"[+] Total mods to process: {len(mod_ids)}")

    failed = []

    for mod_id in mod_ids:
        success = download_mod_with_retry(mod_id)
        if not success:
            failed.append(mod_id)

    successful_count = len(mod_ids) - len(failed)
    failed_count = len(failed)

    print(f"\n📦 Summary: {successful_count} mods downloaded, {failed_count} failed.")

    save_failed_mods(failed)
    input("🔚 Press Enter to exit...")

if __name__ == "__main__":
    main()
