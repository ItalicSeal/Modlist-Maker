import shutil

import requests
import tempfile
import os

import patoolib


def replace_rename_move_directory(source, destination, temp_destination):
    source_name = os.path.basename(source)
    temp_dir = tempfile.mkdtemp(dir=temp_destination)
    shutil.copytree(source, os.path.join(temp_dir, source_name))
    shutil.rmtree(destination)
    shutil.copytree(os.path.join(temp_dir, source_name), destination)
    shutil.rmtree(temp_dir)


def extract_archive(archive_path, extract_path):
    try:
        patoolib.extract_archive(archive_path, outdir=extract_path)
    except patoolib.util.PatoolError as e:
        print(f"Error extracting archive: {e}")


class Utils:
    def __init__(self, modlist_maker_directory):
        self.modlist_maker_directory = modlist_maker_directory

    def download_mo2(self, download_url, install_directory):
        temp_dir = tempfile.mkdtemp(dir=self.modlist_maker_directory)

        response = requests.get(download_url)
        if response.status_code == 200:
            with open(os.path.join(temp_dir, 'mo2.7z'), 'wb') as file:
                file.write(response.content)
        else:
            return

        # unpack_7zarchive(os.path.join(temp_dir, 'mo2.7z'), os.path.join(temp_dir, ''))
        patoolib.extract_archive(os.path.join(temp_dir, 'mo2.7z'), outdir=os.path.join(temp_dir, ''))
        extracted_dir = os.path.join(temp_dir, '')
        for root, dirs, files in os.walk(extracted_dir):
            for file in files:
                src_file = os.path.join(root, file)
                dest_file = os.path.join(install_directory, os.path.relpath(src_file, extracted_dir))
                os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                os.rename(src_file, dest_file)

        shutil.rmtree(temp_dir)

    def add_ini(self, ini_info, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

        ini_file_path = os.path.join(directory, "ModOrganizer.ini")
        with open(ini_file_path, "w") as ini_file:
            ini_file.write(ini_info)

    def add_profile(self, profile_dir, profile_dest_dir, modlist):
        shutil.copytree(profile_dir, profile_dest_dir)
        with open(os.path.join(profile_dest_dir, "modlist.txt"), "w") as file:
            file.write(modlist.gen_modlist_file())

    def install_mod(self, mod_directory, install_directory, mod_name, install_steps=None):
        if not os.path.exists(mod_directory):
            print(f"Mod: '{mod_directory}' does not exist.")
            return
        if not os.path.exists(install_directory):
            os.makedirs(install_directory)

        base_path = os.path.join(install_directory, mod_name)
        extract_archive(mod_directory, base_path)

        if not install_steps:
            return

        for step_number, step in enumerate(install_steps, start=1):
            try:
                if step["command"] == "create_directory":
                    os.makedirs(os.path.join(base_path, step["arguments"]["directory"]))
                elif step["command"] == "move":
                    shutil.move(
                        os.path.join(base_path, step["arguments"]["source"]),
                        os.path.join(base_path, step["arguments"]["directory"])
                    )
                elif step["command"] == "copy":
                    source = os.path.join(base_path, step["arguments"]["source"])
                    destination = os.path.join(base_path, step["arguments"]["directory"])

                    if os.path.isdir(source):
                        shutil.copytree(source, destination)
                    else:
                        shutil.copy(source, destination)
                elif step["command"] == "delete":
                    source = os.path.join(base_path, step["arguments"]["directory"])

                    if os.path.isdir(source):
                        shutil.rmtree(source)
                    else:
                        os.remove(source)
            except Exception as e:
                print(
                    f"Error during step {step_number} ('{step['command']}' step). Arguments: {step['arguments']} - Error: {e}")
            continue
