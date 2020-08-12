"""
A python script to automate typing on typeracer.com

Author: David Chen
"""
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

USER_DATA_DIR = '--user-data-dir=/home/dchen327/.config/google-chrome/Profile 2'
LINK = 'https://play.typeracer.com'


class Typer:
    def __init__(self, link, delay, practice=True):
        self.link = link
        self.delay = delay
        self.practice = practice
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
        sleep(1)
        self.focus_text_box()

    def launch_typing_area(self):
        """ 
        Loads the typing area by using the keyboard shortcuts 'CTRL+ALT+O' for practice
        mode and 'CTRL+ALT+I' for a real game.
        """
        key = 'o' if self.practice else 'i'
        ActionChains(self.driver).key_down(Keys.CONTROL).key_down(Keys.ALT).send_keys(
            key).key_up(Keys.CONTROL).key_up(Keys.ALT).perform()

    def get_text(self):
        """ 
        Grab the text to be typed.
        Typeracer splits the text into three parts:
            1) First letter of first word
            2) Rest of first word
            3) Rest of text
        If the first word is a single letter (e.g. I, A), this third part won't exist
        """
        first_letter_xpath = """//*[@id="gwt-uid-15"]/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div/span[1]"""
        end_of_first_word_xpath = """//*[@id="gwt-uid-15"]/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div/span[2]"""
        text_xpath = """//*[@id="gwt-uid-15"]/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div/span[3]"""
        text_available = False
        while not text_available:  # keep trying to grab text until it appears
            try:
                first_letter = self.driver.find_element_by_xpath(
                    first_letter_xpath).text
                text_available = True
            except:
                pass

        end_of_first_word = ''
        end_of_first_word = self.driver.find_element_by_xpath(
            end_of_first_word_xpath).text
        main_text = ''
        try:  # if the first word is a single letter, then this will fail
            main_text = self.driver.find_element_by_xpath(text_xpath).text
        except:
            pass

        text = first_letter
        # if first word is only a single letter, main text is empty, add a space after first letter
        if not main_text:
            text += ' ' + end_of_first_word
        else:
            text += end_of_first_word
            # add a space if the main text starts with a letter and not punctuation
            if (main_text[0].isalpha()) or not main_text:
                text += ' ' + main_text
            else:
                text += main_text
        print('Text:', text)
        self.text = text

    def focus_text_box(self):
        """ Click into text input area """
        input_xpath = """//*[@id="gwt-uid-15"]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/input"""
        self.text_box = self.driver.find_element_by_xpath(input_xpath)
        self.text_box.click()

    def send_text(self):
        """ Repeatedly attempts to type text in the input box until allowed """
        words = self.text.split()
        text_box_open = False
        while not text_box_open:  # keep trying to type until the textbox allows entry
            try:
                for i, word in enumerate(words):
                    # sending trailing space on the last word will lead to sub 100% accuracy
                    if i == len(words) - 1:  # last word, no trailing space
                        self.text_box.send_keys(word)
                    else:
                        self.text_box.send_keys(word + ' ')
                    text_box_open = True
                    sleep(self.delay)
            except:
                pass


if __name__ == "__main__":
    typer = Typer(LINK, delay=0.12, practice=False)
    typer.get_text()
    typer.send_text()
