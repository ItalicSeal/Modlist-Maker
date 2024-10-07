import shutil
import time
from scripts import game_utils, mo2_utils, parser, nexus_utils, edit_env
from dotenv import load_dotenv

import os
print("Please install firefox to continue, create a custom profile and log into your nexus account from there")
collect_info_input = input("Collect Info? (Type y if this is your first time): ").lower()
if collect_info_input == 'y' or collect_info_input == 'yes':
    env_editor = edit_env.EnvEditor('.env')
    env_editor.get_info()

load_dotenv()

mo2_download_url = os.getenv("MO2_URL")
modlist_maker_download_path = os.getenv("MODLIST_MAKER_DIRECTORY")
mo2_directory = os.getenv("MO2_DIRECTORY")
downloads_directory = os.getenv("DOWNLOADS_DIRECTORY")
firefox_profile_directory = os.getenv("FIREFOX_PROFILE_DIRECTORY")
firefox_dev_directory = os.getenv("FIREFOX_DEV_EDITION_DIRECTORY")

proceed_input = input(
    f"Proceed, will clear the following directory if not empty {modlist_maker_download_path}: ").lower()
if not proceed_input == 'y' or proceed_input == 'yes':
    exit()

if os.path.exists(modlist_maker_download_path):
    shutil.rmtree(modlist_maker_download_path)
    print("clearing modlist maker directory...")
else:
    os.mkdir(modlist_maker_download_path)
    print("creating modlist maker directory...")

Mo2_utils = mo2_utils.Utils(modlist_maker_download_path)
Game_utils = game_utils.Utils(modlist_maker_download_path)
modlist = parser.ParseModlist("modlist.json")
if bool(os.getenv("COPY_GAME")):
    print("copying game files...")
    game_directory = os.getenv("NEW_GAME_DIRECTORY")
    Game_utils.copy_game_files(os.getenv("GAME_DIRECTORY"), os.getenv("NEW_GAME_DIRECTORY"))
    binary_directory = os.path.join(game_directory, os.getenv("EXECUTABLE_DIRECTORY"))
else:
    game_directory = os.getenv("GAME_DIRECTORY")
    binary_directory = os.path.join(game_directory, os.getenv("EXECUTABLE_DIRECTORY"))

print("downloading mod organizer 2...")
Mo2_utils.download_mo2(mo2_download_url, mo2_directory)

with open("cloneable/game_ini/DaggerfallUntiy.ini", 'r') as file:
    file_content = file.read()

lines = file_content.split("\n")

for i, line in enumerate(lines):
    if line.startswith("gamePath"):
        path = os.path.normpath(game_directory).replace("\\", "\\\\")
        lines[i] = f"{line.split('=')[0].strip()}=@ByteArray({path})"
    elif line.startswith(r"1\binary"):
        lines[i] = f"{line.split('=')[0].strip()}={os.path.normpath(binary_directory).replace(os.sep, '/')}"
    elif line.startswith(r"1\workingDirectory"):
        lines[i] = f"{line.split('=')[0].strip()}={os.path.normpath(game_directory).replace(os.sep, '/')}"
    elif line.startswith(r"2\binary"):
        explorer_path = os.path.normpath(os.path.join(mo2_directory, 'explorer++/Explorer++.exe'))
        lines[i] = f"{line.split('=')[0].strip()}={os.path.normpath(explorer_path).replace(os.sep, '/')}"
modified_content = "\n".join(lines)

print("configuring mod organizer 2...")
Mo2_utils.add_ini(modified_content, mo2_directory)
Mo2_utils.add_profile('cloneable\game_profiles\DaggerfallUnity\Default', f"{mo2_directory}/profiles/Default", modlist)

if not os.path.exists(downloads_directory):
    print("creating downloads directory...")
    os.mkdir(downloads_directory)

print("downloading mods...")
webdriver = nexus_utils.NexusInteractor(firefox_profile_directory, firefox_dev_directory)
time.sleep(10)
for mod in modlist.get_list()['mods']:
    print(f"Downloading {mod['name']}...")
    webdriver.download_via_link(mod["download_link"], downloads_directory, f"{mod['name']}{mod['file_extension']}")
    time.sleep(10)
webdriver.exit()

if not os.path.exists(os.path.join(mo2_directory, 'mods')):
    print("creating mods directory...")
    os.mkdir(os.path.join(mo2_directory, 'mods'))

for mod in modlist.get_list()['mods']:
    print(f"installing {mod['name']}...")
    download_dir = os.path.join(downloads_directory, f"{mod['name']}{mod['file_extension']}")
    if 'game_folder' in mod and mod['game_folder'] is not None:
        Mo2_utils.install_mod(download_dir, os.path.join(mo2_directory, 'mods'), mod['name'], mod['game_folder'])
    else:
        Mo2_utils.install_mod(download_dir, os.path.join(mo2_directory, 'mods'), mod['name'])
print("Done! enjoy")
