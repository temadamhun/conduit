import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from conduit_data import *


class TestConduit(object):

    def setup(self):
        browser_options = Options()
        browser_options.headless = True
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=browser_options)
        URL = "http://localhost:1667/#/"
        self.browser.get(URL)

    def teardown(self):
        self.browser.quit()

    def test_regisztracio(self):
        # sign_up = browser.find_elements_by_class_name("nav-link")[1]
        # sign_up = browser.find_element_by_xpath('//a[@class="nav-link"][@href="#/register"]')
        sign_up = self.browser.find_element_by_partial_link_text("Sign up")
        sign_up.click()
        username_input = self.browser.find_element_by_xpath('//input[@placeholder="Username"][@type="text"]')
        username_input.send_keys("mikkamkka")
        email_input = self.browser.find_element_by_xpath('//input[@placeholder="Email"][@type="text"]')
        email_input.send_keys("mikkamakka6@test.hu")
        password_input = self.browser.find_element_by_xpath('//input[@placeholder="Password"][@type="password"]')
        password_input.send_keys("Mikkamakka2")
        sign_up_button = self.browser.find_element_by_xpath('//button[contains(text(),"Sign up")]')  # olyan buttont keres amely textje tartalmazza a sign up szöveget.
        sign_up_button.click()
        time.sleep(3)

        reg_result = self.browser.find_element_by_class_name("swal-title")
        assert reg_result.text == "Welcome!"

        reg_label = self.browser.find_element_by_class_name("swal-text")
        assert reg_label.text == "Your registration was successful!"

    def test_login(self):
        signin_btn = self.browser.find_element_by_xpath('//a[@href="#/login"]')
        signin_btn.click()
        email_input = self.browser.find_element_by_xpath('//input[@placeholder="Email"][@type="text"]')
        email_input.send_keys("mikkamakka6@test.hu")
        password_input = self.browser.find_element_by_xpath('//input[@placeholder="Password"][@type="password"]')
        password_input.send_keys("Mikkamakka2")
        sign_in_button = self.browser.find_element_by_xpath(
            '//button[contains(text(),"Sign in")]')  # olyan buttont keres amely textje tartalmazza a sign in szöveget.
        sign_in_button.click()
        time.sleep(1)
        logout_check = self.browser.find_element_by_partial_link_text("Log out")
        assert logout_check.text.strip() == "Log out"

    def test_accept(self):
        button_accept = self.browser.find_element_by_xpath('//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')
        time.sleep(1)
        button_accept.click()
        time.sleep(1)
        accept_ok = False
        panel = self.browser.find_elements_by_id("cookie-policy-panel")  # ha elfogadtuk a cookiet, ez a div el kell tűnjön
        assert len(panel) == 0

    def test_new_article(self):
        # belépés
        conduit_login(self.browser)
        article_link = self.browser.find_element_by_partial_link_text('New Article')
        article_link.click()
        time.sleep(1)
        title_input = self.browser.find_element_by_xpath('//input[@placeholder="Article Title"][@type="text"]')
        article_title = datetime.now().strftime("%Y%m%d%H%M%S")
        title_input.send_keys(article_title)
        what_input = self.browser.find_element_by_xpath('//input[@placeholder="What\'s this article about?"][@type="text"]')
        what_input.send_keys("about")
        # what_input = self.browser.find_elements_by_xpath('//input[@type="text"]')[1]
        # what_input.send_keys("Title")
        password_input = self.browser.find_element_by_xpath('//textarea[@placeholder="Write your article (in markdown)"]')
        password_input.send_keys("write write more")
        # password_input = self.browser.find_elements_by_xpath('//textarea')[0]
        # password_input.send_keys("Title")
        tag_input = self.browser.find_element_by_xpath('//input[@placeholder="Enter tags"][@type="text"]')
        tag_input.send_keys("tag")
        submit_button = self.browser.find_element_by_xpath('//button[@type="submit"]')
        submit_button.click()
        time.sleep(1)
        check_title_label = self.browser.find_element_by_xpath('//h1')
        assert check_title_label.text == article_title
        return article_title

    def test_modify_article(self):
        conduit_login(self.browser)
        article_title = conduit_new_article(self.browser)
        URL = "http://localhost:1667/#/editor/" + article_title
        self.browser.get(URL)
        time.sleep(1)
        title_input = self.browser.find_element_by_xpath('//input[@placeholder="Article Title"][@type="text"]')
        title_input.clear()
        title_input.send_keys("Article Modify Title")
        what_input = self.browser.find_element_by_xpath('//input[@placeholder="What\'s this article about?"][@type="text"]')
        what_input.send_keys("modify about")
        password_input = self.browser.find_element_by_xpath('//textarea[@placeholder="Write your article (in markdown)"]')
        password_input.send_keys("modify write write more")
        submit_button = self.browser.find_element_by_xpath('//button[@type="submit"]')
        submit_button.click()
        time.sleep(1)
        check_title_label = self.browser.find_element_by_xpath('//h1')
        assert check_title_label.text == "Article Modify Title"

    def test_listazas(self):
        conduit_login(self.browser)
        tag = self.browser.find_elements_by_xpath('//div[@class="tag-list"]/a')[0].text # első tag keresése
        # a megtalált első taggel rendelkező articole-ok
        tag_list = self.browser.find_elements_by_xpath('//a[@class="preview-link"]/div[@class="tag-list"]/a[text()="' + tag + '"]')
        tag_list[0].click() # tagre szűrés
        time.sleep(1)
        link_list = self.browser.find_elements_by_xpath('//a[@class="preview-link"]')  # a szűrt tag oldalon az articole-ok keresése
        assert len(link_list) == len(tag_list)

    def test_delete_article(self):
        conduit_login(self.browser)
        article_title = conduit_new_article(self.browser)
        URL = "http://localhost:1667/#/articles/" + article_title  # az újonnan létrehozott article megnyitása.
        self.browser.get(URL)
        time.sleep(1)
        delete_button = self.browser.find_element_by_xpath('//button[@class="btn btn-outline-danger btn-sm"]')
        delete_button.click()
        time.sleep(1)
        confirm_result = self.browser.find_elements_by_xpath('//h1[text()="' + article_title + '"]') # a kitörölt article title-re keresés.
        assert len(confirm_result) == 0

    def test_lapozas(self):
        conduit_login(self.browser)
        link_pages = self.browser.find_elements_by_xpath('//a[@class="page-link"]')
        for page in link_pages:
            page.click()
            link = self.browser.find_element_by_xpath('//li[@class="page-item active"]/a') # az adott oldal active class-t kap. Az alatta lévő link (aktuális oldal) kiolvasása.
            assert link.text == page.text

    def test_adatok_mentese(self):
        conduit_login(self.browser)
        titles = self.browser.find_elements_by_xpath('//a[@class="preview-link"]/h1') # minden articole title h1 kiolvasása
        list = []
        for title in titles:
            list.append(title.text + '\n') # article title-k enterrel
        with open("article_titles.txt", 'w+') as file: # fájl megnyítása írásra, ha nincs létrehozza
            file.writelines(list)
        with open("article_titles.txt", "r") as mod_file:
            assert mod_file.readlines() == list

    def test_new_article_from_file(self):
        # belépés
        conduit_login(self.browser)
        with open('test_conduit/input_article.txt', 'r') as file:
            list = file.read().splitlines()  # \n miatt soronként vágjuk
            for x in range(len(list)//4):  #  articole létrehozása, a fájlban szereplő első négy sor lesz egy article adatai...
                article_link = self.browser.find_element_by_partial_link_text('New Article')
                article_link.click()
                time.sleep(1)
                title_input = self.browser.find_element_by_xpath('//input[@placeholder="Article Title"][@type="text"]')
                title = list[4 * x]
                title_input.send_keys(title)
                what_input = self.browser.find_element_by_xpath('//input[@placeholder="What\'s this article about?"][@type="text"]')
                about = list[4 * x + 1]
                what_input.send_keys(about)
                password_input = self.browser.find_element_by_xpath('//textarea[@placeholder="Write your article (in markdown)"]')
                more = list[4 * x + 2]
                password_input.send_keys(more)
                tag_input = self.browser.find_element_by_xpath('//input[@placeholder="Enter tags"][@type="text"]')
                tag = list[4 * x + 3]
                tag_input.send_keys(tag)
                submit_button = self.browser.find_element_by_xpath('//button[@type="submit"]')
                submit_button.click()
                time.sleep(1)
                check_title_label = self.browser.find_element_by_xpath('//h1')
                assert check_title_label.text == title

    def test_logout(self):
        conduit_login(self.browser)
        home_link = self.browser.find_element_by_partial_link_text("Log out")
        home_link.click()
        time.sleep(1)
        sign_link = self.browser.find_element_by_partial_link_text("Sign in")
        assert sign_link.text == "Sign in"

