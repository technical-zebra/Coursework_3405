import pytest
from flask import Flask, url_for
from flask_testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Create a test Flask app
app = Flask(__name__)


# Define a test route
@app.route('/')
def index():
    return 'Welcome to Kahoot-like App'


# This is a Python class that tests the homepage and login functionality of a web application using
# Selenium webdriver.
class SystemTest(LiveServerTestCase):

    def create_app(self):
        """
        This function creates and returns a Flask app with testing mode enabled.
        :return: The `app` object with the `TESTING` configuration set to `True`.
        """
        app.config['TESTING'] = True
        return app

    def setUp(self):
        """
        This function sets up a Chrome webdriver instance for use in automated testing.
        """
        self.driver = webdriver.Chrome()

    def tearDown(self):
        """
        The function is used to close the web driver instance after the test is completed.
        """
        self.driver.quit()

    def test_homepage(self):
        """
        This is a test function that checks if the homepage of a website contains the text "Welcome to
        QuizPod".
        """
        self.driver.get(self.get_server_url())
        assert 'Welcome to QuizPod' in self.driver.page_source

    def test_login(self):
        """
        This function tests the login functionality by clicking on the login button on a web page.
        """
        self.driver.get(self.get_server_url() + url_for('index'))
        login_button = self.driver.find_element_by_id('login-button')
        login_button.click()

        username_input = self.driver.find_element_by_id('username-input')
        password_input = self.driver.find_element_by_id('password-input')
        submit_button = self.driver.find_element_by_id('submit-button')

        username_input.send_keys('testuser')
        password_input.send_keys('password')
        submit_button.click()

        assert 'Logged in as testuser' in self.driver.page_source


# Run the tests
if __name__ == '__main__':
    pytest.main()
