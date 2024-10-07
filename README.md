# Modlist-Maker
A tool made to create and automatically install modlists with Python files, 
currently not finished and not ready for use.

### Installation
1. **Clone Repository:**
   ```bash
   git clone https://github.com/ItalicSeal/Modlist-Maker
2. **Install requirements:** Create a new env and install the required packages
   ```bash
   python -m venv c:\path\to\myenv
   pip install -r requirements.txt
3. **Create a firefox profile:** Create a firefox profile and log onto your nexus mods account. In this firefox profile about:config change the **xpinstall.signatures.required** value to **False**, download the additional firefox addon and install to the profile it.
4. **Run main script:**
   ```bash
   python modlist_maker.py

### Running

**Enter necessary details:** When prompted to config env file, select yes and enter details for running the scipt

   * MODLIST_MAKER_DIRECTORY: The folder where Modlist-Maker is located.
   * MODLIST_INSTALL_FILE_NAME: The name of the modlist installation file.
   * PARSE_FILE_DIRECTORY: The directory for parsing files.
   * COPY_GAME: Set to either True or False depending on whether you want to copy the game.
   * GAME_DIRECTORY: The directory where the game is located.
   * EXECUTABLE_DIRECTORY: The directory of the game's executable file, relative to the game directory.
   * FIREFOX_PROFILE_DIRECTORY: The directory of the previously created Firefox profile.
   * FIREFOX_DEV_EDITION_DIRECTORY: The directory of your firefox developer edition binary.

Alternatively edit the .env file by hand 