import os
import re

# --- Settings ---
folder_path = input("Enter the folder path containing your save files (e.g. C:/Users/%userprofile%/zomboid/saves/multiplayer/xxxxx): ").strip()

# --- File type selection ---
print("Select file type to delete:")
print("1 - map_X_Y.bin")
print("2 - chunkdata_X_Y.bin")
print("3 - zpop_X_Y.bin")
file_choice = input("Choice (1/2/3): ").strip()

file_patterns = {
    "1": r"^map_(-?\d+)_(-?\d+)\.bin$",
    "2": r"^chunkdata_(-?\d+)_(-?\d+)\.bin$",
    "3": r"^zpop_(-?\d+)_(-?\d+)\.bin$"
}

if file_choice not in file_patterns:
    print("Invalid file type choice.")
    exit()

pattern = re.compile(file_patterns[file_choice])

# --- Coordinates ---
coord1 = input("Enter first coordinate (X_Y): ").strip()
coord2 = input("Enter second coordinate (X_Y): ").strip()
x1, y1 = map(int, coord1.split("_"))
x2, y2 = map(int, coord2.split("_"))

min_x, max_x = sorted((x1, x2))
min_y, max_y = sorted((y1, y2))

# --- Mode selection ---
print("Select delete mode:")
print("1 - Include (delete inside area)")
print("2 - Exclude (delete outside area)")
mode_choice = input("Choice (1/2): ").strip()

if mode_choice not in ("1", "2"):
    print("Invalid mode choice.")
    exit()

# --- File search ---
to_delete = []
for filename in os.listdir(folder_path):
    match = pattern.match(filename)
    if match:
        file_x = int(match.group(1))
        file_y = int(match.group(2))

        if mode_choice == "1":  # Include
            if min_x <= file_x <= max_x and min_y <= file_y <= max_y:
                to_delete.append(filename)
        else:  # Exclude
            if file_x < min_x or file_x > max_x or file_y < min_y or file_y > max_y:
                to_delete.append(filename)

# --- Summary ---
if not to_delete:
    print("No matching files found for the selected options.")
else:
    count = len(to_delete)
    print(f"Found {count} files to delete.")
    if count <= 20:
        for f in sorted(to_delete):
            print(f)
    else:
        print("(Showing first 10 for preview)")
        for f in sorted(to_delete)[:10]:
            print(f)

    confirm = input("Are you sure you want to delete these files? (Y/N): ").strip().lower()
    if confirm == "y":
        for f in to_delete:
            os.remove(os.path.join(folder_path, f))
        print("Files deleted.")
    else:
        print("Operation cancelled.")
