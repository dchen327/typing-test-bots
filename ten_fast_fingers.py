"""
A python script to automate typing on 10fastfingers.com

Author: David Chen
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

USER_DATA_DIR = '--user-data-dir=/home/dchen327/.config/google-chrome/Profile 2'
LINK = 'https://10fastfingers.com/typing-test/english'


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

    def focus_text_box(self):
        """ Click into text input area """
        input_xpath = '//*[@id="inputfield"]'
        self.text_box = self.driver.find_element_by_xpath(input_xpath)
        self.text_box.click()

    def input_words(self):
        """ Get words to be typed """
        for idx in range(1, 346):  # website runs out of words
            word_xpath = f'//*[@id="row1"]/span[{idx}]'
            word_element = self.driver.find_element_by_xpath(word_xpath)
            self.text_box.send_keys(word_element.text + ' ')


if __name__ == '__main__':
    typer = Typer(LINK)
    typer.focus_text_box()
    typer.input_words()
