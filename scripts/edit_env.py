import os
class EnvEditor:
    def __init__(self, env_file):
        self.env_file = env_file

    def get_user_input(self, prompt):
        value = input(prompt + ": ")
        return value.strip()

    def get_info(self):
        modlist_maker_folder = self.get_user_input("MODLIST_MAKER_DIRECTORY")
        modlist_maker_file_name = self.get_user_input("MODLIST_INSTALL_FILE_NAME")

        modlist_maker_directory = os.path.join(modlist_maker_folder, modlist_maker_file_name)
        parse_file_directory = self.get_user_input("PARSE_FILE_DIRECTORY")
        copy_game = self.get_user_input("COPY_GAME (True/False)")
        game_directory = self.get_user_input("GAME_DIRECTORY")
        executable_directory = self.get_user_input("EXECUTABLE_DIRECTORY (Relative to game directory)")
        firefox_profile_directory = self.get_user_input("FIREFOX_PROFILE_DIRECTORY")

        with open(self.env_file, 'w') as f:
            f.write(f"MO2_URL=https://github.com/ModOrganizer2/modorganizer/releases/download/v2.5.0/Mod.Organizer-2.5.0.7z\n")
            f.write(f"MODLIST_MAKER_DIRECTORY={modlist_maker_directory}\n")
            f.write(f"MO2_DIRECTORY={modlist_maker_directory}/MO2\n")
            f.write(f"DOWNLOADS_DIRECTORY={modlist_maker_directory}/DOWNLOADS\n")
            f.write("\n")
            f.write(f"PARSE_FILE_DIRECTORY={parse_file_directory}\n")
            f.write(f"GAME_DIRECTORY={game_directory}\n")
            f.write(f"EXECUTABLE_DIRECTORY={executable_directory}\n")
            f.write("\n")
            f.write(f"COPY_GAME={copy_game}\n")
            f.write(f"NEW_GAME_DIRECTORY={modlist_maker_directory}/STOCK_GAME\n")
            f.write("\n")
            f.write(f"FIREFOX_PROFILE_DIRECTORY={firefox_profile_directory}\m")
            f.write(f"GECKO_DRIVER_DIRECTORY=geckodriver.exe")
