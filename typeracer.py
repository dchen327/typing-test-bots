"""
A python script to automate typing on typeracer.com

Author: David Chen
"""
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep

USER_DATA_DIR = '--user-data-dir=/home/dchen327/.config/google-chrome/Profile 2'
LINK = 'https://play.typeracer.com'


class Typer:
    def __init__(self, link):
        self.link = link
        self.words = []
        self.launch_browser()

    def launch_browser(self):
        """ Launch chrome and go to game link """
        options = Options()
        if USER_DATA_DIR:
            options.add_argument(USER_DATA_DIR)
        # remove the little popup in corner
        options.add_experimental_option(
            'excludeSwitches', ['enable-automation'])
        # allow instance to keep running after function ends
        options.add_experimental_option('detach', True)
        options.add_argument('--start-maximized')
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(self.link)
        sleep(2)  # wait for page load
        self.launch_typing_area()
        self.focus_text_box()

    def launch_typing_area(self, practice=True):
        """ 
        Loads the typing area by using the keyboard shortcuts 'CTRL+ALT+O' for practice
        mode and 'CTRL+ALT+I' for a real game.
        """
        key = 'o' if practice else 'i'
        ActionChains(self.driver).key_down(Keys.CONTROL).key_down(Keys.ALT).send_keys(
            key).key_up(Keys.CONTROL).key_up(Keys.ALT).perform()
        sleep(3)  # wait for countdown

    def get_text(self):
        """ 
        Grab the text to be typed.
        Typeracer splits the text into three parts:
            1) First letter of first word
            2) Rest of first word
            3) Rest of text
        """
        first_letter_xpath = """//*[@id="gwt-uid-15"]/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div/span[1]"""
        end_of_first_word_xpath = """//*[@id="gwt-uid-15"]/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div/span[2]"""
        text_xpath = """//*[@id="gwt-uid-15"]/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div/span[3]"""
        first_letter_element = self.driver.find_element_by_xpath(
            first_letter_xpath)
        end_of_first_word_element = self.driver.find_element_by_xpath(
            end_of_first_word_xpath)
        text_element = self.driver.find_element_by_xpath(text_xpath)
        text = first_letter_element.text + \
            end_of_first_word_element.text + ' ' + text_element.text
        print(text)
        for char in text:
            self.text_box.send_keys(char)

    def focus_text_box(self):
        """ Click into text input area """
        input_xpath = """//*[@id="gwt-uid-15"]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/input"""
        self.text_box = self.driver.find_element_by_xpath(input_xpath)
        self.text_box.click()


if __name__ == "__main__":
    typer = Typer(LINK)
    sleep(5)
    typer.get_text()
