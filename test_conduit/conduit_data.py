import time
from datetime import datetime

def conduit_login(browser):
    signin_btn = browser.find_element_by_xpath('//a[@href="#/login"]')
    signin_btn.click()
    email_input = browser.find_element_by_xpath('//input[@placeholder="Email"][@type="text"]')
    email_input.send_keys("mikkamakka6@test.hu")
    password_input = browser.find_element_by_xpath('//input[@placeholder="Password"][@type="password"]')
    password_input.send_keys("Mikkamakka2")
    sign_in_button = browser.find_element_by_xpath(
        '//button[contains(text(),"Sign in")]')  # olyan buttont keres amely textje tartalmazza a sign in szöveget.
    sign_in_button.click()
    time.sleep(2)


def conduit_new_article(browser):
    href = browser.find_element_by_partial_link_text('New Article')
    href.click()
    time.sleep(1)
    title_input = browser.find_element_by_xpath('//input[@placeholder="Article Title"][@type="text"]')
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    title_input.send_keys(now)
    what_input =browser.find_element_by_xpath('//input[@placeholder="What\'s this article about?"][@type="text"]')
    what_input.send_keys("about")
    # what_input = self.browser.find_elements_by_xpath('//input[@type="text"]')[1]
    # what_input.send_keys("Title")
    password_input = browser.find_element_by_xpath('//textarea[@placeholder="Write your article (in markdown)"]')
    password_input.send_keys("write write more")
    # password_input = self.browser.find_elements_by_xpath('//textarea')[0]
    # password_input.send_keys("Title")
    tag_input = browser.find_element_by_xpath('//input[@placeholder="Enter tags"][@type="text"]')
    tag_input.send_keys("tag")
    submit_button = browser.find_element_by_xpath('//button[@type="submit"]')
    submit_button.click()
    time.sleep(2)
    return now