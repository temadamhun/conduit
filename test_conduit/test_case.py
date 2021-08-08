import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

class TestConduit(object):

    def setup(self):
        browser_options = Options()
        browser_options.headless = True
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=browser_options)

    def teardown(self):
        self.browser.quit()

    def test_regisztracio(self):
        URL = "http://localhost:1667/#/"
        self.browser.get(URL)
        # sign_up = browser.find_elements_by_class_name("nav-link")[1]
        # sign_up = browser.find_element_by_xpath('//a[@class="nav-link"][@href="#/register"]')
        sign_up = self.browser.find_element_by_partial_link_text("Sign up")
        sign_up.click()
        username_input = self.browser.find_element_by_xpath('//input[@placeholder="Username"][@type="text"]')
        username_input.send_keys("mikkamkka")
        email_input = self.browser.find_element_by_xpath('//input[@placeholder="Email"][@type="text"]')
        email_input.send_keys("mikkamakka4@test.hu")
        password_input = self.browser.find_element_by_xpath('//input[@placeholder="Password"][@type="password"]')
        password_input.send_keys("Mikkamakka2")
        sign_up_button = self.browser.find_element_by_xpath('//button[contains(text(),"Sign up")]')  #olyan buttont keres amely textje tartalmazza a sign up szöveget.
        sign_up_button.click()
        time.sleep(3)
        #browser.switch_to.window(browser.window_handles[0])

        reg_result = self.browser.find_element_by_class_name("swal-title")
        assert reg_result.text == "Welcome!"

        reg_label = self.browser.find_element_by_class_name("swal-text")
        assert reg_label.text == "Your registration was successful!"

    def test_login(self):
        URL ="http://localhost:1667/#/login"
        self.browser.get(URL)
        email_input = self.browser.find_element_by_xpath('//input[@placeholder="Email"][@type="text"]')
        email_input.send_keys("mikkamakka4@test.hu")
        password_input = self.browser.find_element_by_xpath('//input[@placeholder="Password"][@type="password"]')
        password_input.send_keys("Mikkamakka2")
        sign_in_button = self.browser.find_element_by_xpath('//button[contains(text(),"Sign in")]')  # olyan buttont keres amely textje tartalmazza a sign in szöveget.
        sign_in_button.click()
        time.sleep(1)
        logout_check = self.browser.find_element_by_partial_link_text("Log out")
        assert logout_check.text == " Log out"

    def test_accept(self):
         URL = "http://localhost:1667/#"
         self.browser.get(URL)
         button_accept = self.browser.find_element_by_xpath('//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')
         time.sleep(1)
         button_accept.click()
         time.sleep(1)
         accept_ok = False
         try:
            panel = self.browser.find_element_by_id("cookie-policy-panel") # ha elfogadtuk a cookiet, ez a div el kell tűnjön
         except:
            accept_ok = True # NoSuchElementError-t kapunk, mivel nincs találat
         assert accept_ok

    def test_new_article(self):
        # belépés
        self.test_login()
        # URL = "http://localhost:1667/#/editor"
        # self.browser.get(URL)
        href = self.browser.find_element_by_partial_link_text('New Article')
        href.click()
        time.sleep(1)
        title_input = self.browser.find_element_by_xpath('//input[@placeholder="Article Title"][@type="text"]')
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        title_input.send_keys(now)
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
        assert check_title_label.text == now
        return now

    def test_modify_article(self):
        now = self.test_new_article()
        URL = "http://localhost:1667/#/editor/"+now
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
        self.test_login()
        link_list = self.browser.find_elements_by_xpath('//a[@class="preview-link"]')
        link_list[0].click()
        time.sleep(1)
        title = self.browser.find_element_by_xpath('//h1')
        assert title.text == "Lorem ipsum dolor sit amet"
        home_link = self.browser.find_element_by_partial_link_text("Home")
        home_link.click()
        time.sleep(1)
        link_list = self.browser.find_elements_by_xpath('//a[@class="preview-link"]')
        link_list[1].click()
        time.sleep(1)
        title = self.browser.find_element_by_xpath('//h1')
        assert title.text == "In nisl nisi scelerisque eu"

    def test_delete_article(self):
        now = self.test_new_article()
        URL = "http://localhost:1667/#/articles/"+now
        self.browser.get(URL)
        time.sleep(1)
        delete_button = self.browser.find_element_by_xpath('//button[@class="btn btn-outline-danger btn-sm"]')
        delete_button.click()
        time.sleep(1)
        deleted = False
        try:
            confirm_result = self.browser.find_element_by_xpath('//h1[text()="'+ now +'"]')
        except:
            deleted = True
        assert deleted

    def test_lapozas(self): # mi itt a feladat???
        self.test_login()
        time.sleep(1)
        link_page = self.browser.find_elements_by_xpath('//a[@class="page-link"]')
        link_page[1].click()
        li_2 = self.browser.find_element_by_xpath('//li[@class="page-item active"]')
        assert  li_2.get_attribute("data-test") == "page-link-2"

    def test_adatok_mentese(self):
        self.test_login()
        time.sleep(1)
        titles = self.browser.find_elements_by_xpath('//h1')
        list = []
        for e in titles:
            list.append(e.text+'\n')
        list.pop(0)
        file = open("article_titles.txt", "w+")
        file.writelines(list)
        file.close()
        file = open("article_titles.txt", "r")
        assert file.readlines() == list

    def test_new_article_from_file(self):
        # belépés
        self.test_login()
        file = open('article_titles.txt', 'r')
        list = file.read().splitlines() # \n miatt soronként vágjuk
        for x in range(5):  # 5 articole létrehozása, az első négy sor lesz egy article adatai...
            href = self.browser.find_element_by_partial_link_text('New Article')
            href.click()
            time.sleep(1)
            title_input = self.browser.find_element_by_xpath('//input[@placeholder="Article Title"][@type="text"]')
            title = list[1+4*x]
            title_input.send_keys(title)
            what_input = self.browser.find_element_by_xpath('//input[@placeholder="What\'s this article about?"][@type="text"]')
            about = list[2+4*x]
            what_input.send_keys(about)
            # what_input = self.browser.find_elements_by_xpath('//input[@type="text"]')[1]
            # what_input.send_keys("Title")
            password_input = self.browser.find_element_by_xpath('//textarea[@placeholder="Write your article (in markdown)"]')
            more = list[3+4*x]
            password_input.send_keys(more)
            # password_input = self.browser.find_elements_by_xpath('//textarea')[0]
            # password_input.send_keys("Title")
            tag_input = self.browser.find_element_by_xpath('//input[@placeholder="Enter tags"][@type="text"]')
            tag = list[4+4*x]
            tag_input.send_keys(tag)
            submit_button = self.browser.find_element_by_xpath('//button[@type="submit"]')
            submit_button.click()
            time.sleep(1)
            check_title_label = self.browser.find_element_by_xpath('//h1')
            assert check_title_label.text == title

    def test_logout(self):
        self.test_login()
        time.sleep(1)
        home_link = self.browser.find_element_by_partial_link_text("Log out")
        home_link.click()
        time.sleep(1)
        sign_link = self.browser.find_element_by_partial_link_text("Sign in")
        assert sign_link.text =="Sign in"
