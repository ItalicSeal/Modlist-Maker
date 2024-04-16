import os
import shutil

class Utils:
    def __init__(self, modlist_maker_directory):
        self.modlist_maker_directory = modlist_maker_directory

    def copy_game_files(self, game_files_directory, new_directory):
        try:
            shutil.copytree(game_files_directory, new_directory)
        except shutil.Error as e:
            print(f"Error: {e}")
        except OSError as e:
            print(f"Error: {e}")
