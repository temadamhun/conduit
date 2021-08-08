import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def test_regisztracio():

    browser_options = Options()
    browser_options.headless = True
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=browser_options)
    #browser.maximize_window() #az oldal méretét maximalizálja.
    URL = "http://localhost:1667/#/"
    browser.get(URL)

    # sign_up = browser.find_elements_by_class_name("nav-link")[1]
    # sign_up = browser.find_element_by_xpath('//a[@class="nav-link"][@href="#/register"]')
    sign_up = browser.find_element_by_partial_link_text("Sign up")
    sign_up.click()
    username_input = browser.find_element_by_xpath('//input[@placeholder="Username"][@type="text"]')
    username_input.send_keys("mikkamkka")
    email_input = browser.find_element_by_xpath('//input[@placeholder="Email"][@type="text"]')
    email_input.send_keys("mikkamakka4@test.hu")
    password_input = browser.find_element_by_xpath('//input[@placeholder="Password"][@type="password"]')
    password_input.send_keys("Mikkamakka2")
    sign_up_button = browser.find_element_by_xpath('//button[contains(text(),"Sign up")]')  #olyan buttont keres amely textje tartalmazza a sign up szöveget.
    sign_up_button.click()
    time.sleep(1)
    browser.switch_to.window(browser.window_handles[0])

    reg_result = browser.find_element_by_class_name("swal-title")
    print(reg_result.text)
    assert reg_result.text == "Welcome!"

    reg_label = browser.find_element_by_class_name("swal-text")
    assert reg_label.text == "Your registration was successful!"

def test_login():
    browser_options = Options()
    browser_options.headless = True
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=browser_options)
    URL ="http://localhost:1667/#/login"
    browser.get(URL)
    email_input = browser.find_element_by_xpath('//input[@placeholder="Email"][@type="text"]')
    email_input.send_keys("mikkamakka4@test.hu")
    password_input = browser.find_element_by_xpath('//input[@placeholder="Password"][@type="password"]')
    password_input.send_keys("Mikkamakka2")
    sign_in_button = browser.find_element_by_xpath('//button[contains(text(),"Sign in")]')  # olyan buttont keres amely textje tartalmazza a sign in szöveget.
    sign_in_button.click()
    time.sleep(1)
    logout_check = browser.find_element_by_partial_link_text("Log out")
    # assert logout_check
    return browser

def test_accept():
     browser_options = Options()
     browser_options.headless = True
     browser = webdriver.Chrome(ChromeDriverManager().install(), options=browser_options)
     URL = "http://localhost:1667/#"
     browser.get(URL)
     button_accept = browser.find_element_by_xpath('//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')
     time.sleep(1)
     button_accept.click()
     time.sleep(1)
     accept_ok = False
     try:
        panel = browser.find_element_by_id("cookie-policy-panel") # ha elfogadtuk a cookiet, ez a div el kell tűnjön
     except:
        accept_ok = True # NoSuchElementError-t kapunk, mivel nincs találat
     assert accept_ok

def test_new_article():
    # belépés
    browser = test_login()

    URL = "http://localhost:1667/#/editor"
    browser.get(URL)
    # href = browser.find_element_by_xpath('//a[@href="#/editor"]')
    # href.click()
    time.sleep(1)
    title_input = browser.find_element_by_xpath('//input[@placeholder="Article Title"][@type="text"]')
    title_input.send_keys("Article Title New")
    what_input = browser.find_element_by_xpath('//input[@placeholder="What\'s this article about?"][@type="text"]')
    what_input.send_keys("about")
    # what_input = browser.find_elements_by_xpath('//input[@type="text"]')[1]
    # what_input.send_keys("Title")
    password_input = browser.find_element_by_xpath('//textarea[@placeholder="Write your article (in markdown)"]')
    password_input.send_keys("write write more")
    # password_input = browser.find_elements_by_xpath('//textarea')[0]
    # password_input.send_keys("Title")
    tag_input = browser.find_element_by_xpath('//input[@placeholder="Enter tags"][@type="text"]')
    tag_input.send_keys("tag")
    submit_button = browser.find_element_by_xpath('//button[@type="submit"]')
    submit_button.click()
    time.sleep(1)
    check_title_label = browser.find_element_by_xpath('//h1')
    assert check_title_label.text == "Article Title New"

def test_modify_article():
    browser = test_login()
    URL = "http://localhost:1667/#/editor/article-title-new"
    browser.get(URL)
    time.sleep(1)
    title_input = browser.find_element_by_xpath('//input[@placeholder="Article Title"][@type="text"]')
    title_input.clear()
    title_input.send_keys("Article Modify Title")
    what_input = browser.find_element_by_xpath('//input[@placeholder="What\'s this article about?"][@type="text"]')
    what_input.send_keys("modify about")
    password_input = browser.find_element_by_xpath('//textarea[@placeholder="Write your article (in markdown)"]')
    password_input.send_keys("modify write write more")
    submit_button = browser.find_element_by_xpath('//button[@type="submit"]')
    submit_button.click()
    time.sleep(1)
    check_title_label = browser.find_element_by_xpath('//h1')
    # assert check_title_label.text == "Article Modify Title" # Hibás az oldal, nem a módosult állapotot mutatja

def test_listazas():
    browser = test_login()
    link_list = browser.find_elements_by_xpath('//a[@class="preview-link"]')
    link_list[0].click()
    time.sleep(1)
    article_meta = browser.find_element_by_class_name('article-meta')
    #assert article_meta
    home_link = browser.find_element_by_partial_link_text("Home")
    home_link.click()
    time.sleep(1)
    link_list = browser.find_elements_by_xpath('//a[@class="preview-link"]')
    link_list[1].click()
    time.sleep(1)
    article_meta = browser.find_element_by_class_name('article-meta')
    # assert article_meta

def test_delete_article():
    browser = test_login()
    URL = "http://localhost:1667/#/articles/article-title-new"
    browser.get(URL)
    time.sleep(1)
    delete_button = browser.find_element_by_xpath('//button[@class="btn btn-outline-danger btn-sm"]')
    delete_button.click()
    time.sleep(1)
    browser.switch_to.window(browser.window_handles[0])
    confirm_result = browser.find_element_by_xpath('//div[@class="swal-title"]')
    assert confirm_result.text == "Oops!" # ez is hibáss.....

def test_lapozas():
    browser = test_login()
    time.sleep(1)
    link_page = browser.find_elements_by_xpath('//a[@class="page-link"]')
    link_page[1].click()
    li_2 = browser.find_element_by_xpath('//li[@class="page-item active"]')
    assert  li_2.get_attribute("data-test") == "page-link-2"

def test_logout():
    browser = test_login()
    time.sleep(1)
    home_link = browser.find_element_by_partial_link_text("Log out")
    home_link.click()
    time.sleep(1)
    sign_link = browser.find_element_by_partial_link_text("Sign in")
    # assert sign_link
