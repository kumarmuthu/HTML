__version__ = "2024.08.03.01"
__author__ = "Muthukumar Subramanian"

"""
HTML page testing use Selenium and Network Connectivity Check from HTML page
"""

import os
import time
import multiprocessing
from collections import OrderedDict
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from prettytable import PrettyTable
import re
import platform
import subprocess


class SeleniumTestExecution:
    def __init__(self):
        options = Options()
        options.add_argument("--disable-notifications")
        options.add_argument("no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("window-size=1400,600")
        # options.add_argument("headless=new")
        # options.add_experimental_option("detach", True)  # Restrict auto close of chrome

        # Initialize Chrome WebDriver
        self.browser = webdriver.Chrome(options=options)
        self.browser.maximize_window()
        # Locate the HTML file path
        html_file_path = os.path.abspath('HtmlFile.html')
        self.browser.get(f'file://{html_file_path}')
        time.sleep(2)
        self.wait = WebDriverWait(self.browser, 10)
        self.final_dict = OrderedDict({})

    def print_text(self):
        print("{:*^60}".format("Print text from HTML page - Start "))
        try:
            # Access get text
            print_get_text = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//div[@class="first second"]/p[contains(text(), "get text")]')))
            print(f"Process done for Get Text, text Value: {print_get_text.text}")

            # Access not get text
            print_not_get_text = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//div/p[contains(text(), "not get text")]')))
            print(f"Process done for Get Text, text Value: {print_not_get_text.text}")
        except StaleElementReferenceException:
            print("Observed exception in Try block")
        except Exception as Err:
            print(f"Observed exception, Error: {Err}")
        print("{:*^60}".format("Print text from HTML page - End "))

    def test_network_connectivity(self):
        print("{:*^60}".format("Network connectivity check on HTML page - Start"))
        html_file_path = os.path.abspath('InternetCheckWithCORSWithAsync.html')
        self.browser.get(f'file://{html_file_path}')
        time.sleep(5)
        html_file_path = os.path.abspath('InternetCheckWithCORSWithoutAsync.html')
        self.browser.get(f'file://{html_file_path}')
        time.sleep(5)
        html_file_path = os.path.abspath('InternetCheckWithoutCORS.html')
        self.browser.get(f'file://{html_file_path}')
        time.sleep(5)
        print("{:*^60}".format("Network connectivity check on HTML page - End"))

    def execute_test_scenarios(self):
        try:
            self.print_text()
            self.test_network_connectivity()
        except StaleElementReferenceException:
            print("Observed exception in Try block")
        self.browser.quit()


def main_script():
    cls_obj = SeleniumTestExecution()
    cls_obj.execute_test_scenarios()


if __name__ == '__main__':
    print("{:#^30}".format("Script Start"))
    multiprocess_obj = multiprocessing.Process(target=main_script)
    multiprocess_obj.start()
    multiprocess_obj.join(timeout=120)
    if multiprocess_obj.is_alive():
        multiprocess_obj.terminate()

    print("{:#^30}".format("Script End"))
