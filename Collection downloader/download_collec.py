import os
import re
import sys
import time
import threading
import subprocess
import requests
from bs4 import BeautifulSoup
import concurrent.futures

# Config
STEAM_APP_ID = "108600"
STEAMCMD_PATH = "steamcmd"  # Change to full path if needed
MAX_THREADS = 5
WORKSHOP_PATH = os.path.join("steamapps", "workshop", "content", STEAM_APP_ID)
FAILED_LOG_FILE = "failed_mods_final.txt"

# Thread-safe tracking
success_list = []
failed_list = []
list_lock = threading.Lock()

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

def download_mod_initial(mod_id):
    if is_mod_downloaded(mod_id):
        print(f"✅ [Mod {mod_id}] Already present.")
        return

    cmd = [STEAMCMD_PATH, "+login", "anonymous",
           "+workshop_download_item", STEAM_APP_ID, mod_id,
           "+quit"]
    try:
        subprocess.run(cmd, check=True)
        if is_mod_downloaded(mod_id):
            with list_lock:
                success_list.append(mod_id)
            print(f"✅ [Mod {mod_id}] Downloaded.")
        else:
            raise Exception("Folder not found after download.")
    except Exception as e:
        with list_lock:
            failed_list.append(mod_id)
        print(f"❌ [Mod {mod_id}] Initial download failed: {e}")

def persistent_retry_single_mod(mod_id):
    print(f"\n🔁 [Mod {mod_id}] Entering persistent SteamCMD session...")

    if is_mod_downloaded(mod_id):
        print(f"✅ [Mod {mod_id}] Already downloaded.")
        return

    attempt = 0
    while True:
        attempt += 1
        if is_mod_downloaded(mod_id):
            print(f"✅ [Mod {mod_id}] Downloaded after {attempt - 1} retry(s).")
            return

        script_lines = ["login anonymous"]
        script_lines += [f"workshop_download_item {STEAM_APP_ID} {mod_id}"] * 10  # Send 10 retries in one session
        script_lines.append("quit")

        temp_script = f"temp_retry_{mod_id}.txt"
        with open(temp_script, "w") as f:
            f.write("\n".join(script_lines))

        try:
            subprocess.run([STEAMCMD_PATH, "+runscript", temp_script], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ SteamCMD session failed: {e}")
        finally:
            if os.path.exists(temp_script):
                os.remove(temp_script)

        if is_mod_downloaded(mod_id):
            print(f"✅ [Mod {mod_id}] Successfully downloaded.")
            return
        else:
            print(f"⏳ [Mod {mod_id}] Still missing after {attempt * 10} tries. Retrying in 5s...")
            time.sleep(5)

def run_initial_parallel_downloads(mod_ids):
    print(f"\n🚀 Starting parallel downloads with {MAX_THREADS} threads...\n")
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        executor.map(download_mod_initial, mod_ids)

def run_persistent_retries():
    if not failed_list:
        print("✅ No mods to retry.")
        return

    print(f"\n🔄 Retrying {len(failed_list)} mods...")
    for mod_id in failed_list:
        persistent_retry_single_mod(mod_id)

def save_final_failures(all_ids):
    still_failed = [mid for mid in all_ids if not is_mod_downloaded(mid)]
    if still_failed:
        with open(FAILED_LOG_FILE, "w") as f:
            f.write('\n'.join(still_failed))
        print(f"❌ Still failed: {len(still_failed)} saved to {FAILED_LOG_FILE}")
    else:
        print("🎉 All mods downloaded.")

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

    run_initial_parallel_downloads(mod_ids)
    run_persistent_retries()
    save_final_failures(mod_ids)

    input("\n🔚 Done! Press Enter to exit...")

if __name__ == "__main__":
    main()
