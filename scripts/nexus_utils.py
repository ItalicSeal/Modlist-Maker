import os
import time


import selenium.webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import requests

from tqdm.auto import tqdm

from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from pathlib import Path

def download_with_progress(url, save_path):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

    with open(save_path, 'wb') as file:
        for data in response.iter_content(chunk_size=1024):
            file.write(data)
            progress_bar.update(len(data))
    progress_bar.close()

class NexusInteractor:
    def __init__(self, firefox_profile_directory, firefox_dev_binary):
        firefox_options = Options()
        firefox_options.binary_location = r"C:\Program Files\Firefox Developer Edition\firefox.exe"
        firefox_options.add_argument("-headless")
        firefox_options.add_argument("-profile")
        firefox_options.add_argument(firefox_profile_directory)

        self.driver = selenium.webdriver.Firefox(options=firefox_options)
        self.driver.get("https://users.nexusmods.com/auth/sign_in")
    def download_via_link(self, url, download_dir, file_name):
        self.driver.get(url)
        try:
            self.driver.find_element(By.ID, "slowDownloadButton").click()
        except NoSuchElementException:
            return -1
        time.sleep(6)
        try:
            download_with_progress(self.driver.find_element(By.XPATH, "/html/body/div[1]/section/div/div[2]/div[2]/div/div[2]/div/div/div[6]/p/p[2]/a").get_attribute("href"), os.path.join(download_dir, file_name))
        except NoSuchElementException:
            print("ERROR")
    def exit(self):
        self.driver.quit()
