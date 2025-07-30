import os
import sys
import shutil

workshop_path = r"steamapps\workshop\content\108600"

def parse_mod_info(mod_info_path):
    mod_ids = []
    try:
        with open(mod_info_path, 'r', encoding='cp1252') as f:
            for line in f:
                line = line.strip()
                if line.startswith("id="):
                    ids = line[3:].strip().split(";")
                    mod_ids.extend([i.strip() for i in ids if i.strip()])
    except Exception as e:
        print(f"⚠️ Could not read {mod_info_path}: {e}")
    return mod_ids

def gather_mods(base_path):
    workshop_ids = []
    mod_ids = []

    print(f"📂 Scanning: {base_path}")
    if not os.path.exists(base_path):
        raise FileNotFoundError(f"Workshop path does not exist: {base_path}")

    for workshop_id in os.listdir(base_path):
        full_path = os.path.join(base_path, workshop_id)
        if not os.path.isdir(full_path):
            continue

        mods_path = os.path.join(full_path, "mods")
        if not os.path.exists(mods_path):
            continue

        found_ids = []
        mod_folder_paths = []

        for mod_folder in os.listdir(mods_path):
            mod_info_path = os.path.join(mods_path, mod_folder, "mod.info")
            if not os.path.isfile(mod_info_path):
                continue

            ids = parse_mod_info(mod_info_path)
            if ids:
                found_ids.extend(ids)
                mod_folder_paths.append((mod_folder, ids))

        if len(found_ids) == 0:
            continue
        elif len(found_ids) == 1:
            mod_ids.extend(found_ids)
            workshop_ids.append(workshop_id)
        else:
            print(f"\n🛠️ Workshop ID {workshop_id} has multiple Mod folders with IDs:")
            for idx, (mod_folder, ids) in enumerate(mod_folder_paths):
                print(f"  [{idx + 1}] Folder: {mod_folder} → ID: {', '.join(ids)}")

            while True:
                choice = input("👉 Enter the number(s) of the Mod(s) to include (e.g., 1 or 1,2): ").strip()
                try:
                    selections = [int(i) - 1 for i in choice.split(",")]
                    for sel in selections:
                        if 0 <= sel < len(mod_folder_paths):
                            mod_ids.extend(mod_folder_paths[sel][1])
                    workshop_ids.append(workshop_id)
                    break
                except:
                    print("❌ Invalid input. Please enter numbers separated by commas.")

    return workshop_ids, mod_ids

def update_ini_file(input_path, workshop_ids, mod_ids):
    try:
        with open(input_path, 'r', encoding='cp1252') as f:
            lines = f.readlines()

        updated_lines = []
        found_mods = found_workshops = False

        for line in lines:
            if line.strip().startswith("Mods="):
                found_mods = True
                updated_lines.append(f"Mods={';'.join(mod_ids)}\n")
            elif line.strip().startswith("WorkshopItems="):
                found_workshops = True
                updated_lines.append(f"WorkshopItems={';'.join(workshop_ids)}\n")
            else:
                updated_lines.append(line)

        if not found_mods:
            updated_lines.append(f"Mods={';'.join(mod_ids)}\n")
        if not found_workshops:
            updated_lines.append(f"WorkshopItems={';'.join(workshop_ids)}\n")

        # Backup old file
        backup_path = os.path.join(
            os.path.dirname(input_path),
            f"backup_{os.path.basename(input_path)}"
        )
        shutil.move(input_path, backup_path)
        print(f"📦 Original file backed up as: {backup_path}")

        # Save new file with original name
        with open(input_path, 'w', encoding='cp1252') as f:
            f.writelines(updated_lines)

        print(f"✅ Updated file saved to: {input_path}")
    except Exception as e:
        print(f"❌ Error updating INI file: {e}")

def main():
    if len(sys.argv) < 2:
        print("❌ Drag and drop your server .ini file onto this script or executable.")
        input("Press Enter to exit...")
        return

    ini_path = sys.argv[1]
    print(f"📄 Processing: {ini_path}")

    if not os.path.isfile(ini_path):
        print("❌ That file does not exist or is not a file.")
        input("Press Enter to exit...")
        return

    try:
        workshop_ids, mod_ids = gather_mods(workshop_path)
        print(f"\n🎯 Found {len(workshop_ids)} Workshop IDs and {len(mod_ids)} Mod IDs.")
        update_ini_file(ini_path, workshop_ids, mod_ids)
    except Exception as e:
        print(f"🚨 An error occurred:\n{e}")

    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
