# download Chromedriver: https://chromedriver.chromium.org/downloads

import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException

email = 'your telegram email'
password = 'your telegram password'
urls = [
    'https://www.instagram.com/p/CJqdjHnHgGW/',
    'https://www.instagram.com/p/CJ52Z0oJ8A9/',
    'https://www.instagram.com/p/CJ2TAAhgr8G/',
    'https://www.instagram.com/p/CJyICnBp_2e/',
    'https://www.instagram.com/p/CJsRmRhlewV/',
    'https://www.instagram.com/p/CJvxAuMAoiY/',
    'https://www.instagram.com/p/CJsnNYdA1n2/',
    'https://www.instagram.com/p/CJ41pVAJ4BO/',
    'https://www.instagram.com/p/CJxLmSkBZEa/',
    'https://www.instagram.com/p/CJxwGdgDTWB/',
    'https://www.instagram.com/p/CJsVOrAAQye/',
    'https://www.instagram.com/p/CJ5bmVRs4el/',
    'https://www.instagram.com/p/CJm5M-CAyyt/',
    'https://www.instagram.com/p/CJ2Nnd4LFhj/',
    'https://www.instagram.com/p/CJ3ImjsLD6P/',
    'https://www.instagram.com/p/CJ5ZCqmhZNT/',
    'https://www.instagram.com/p/CJoBkDAhd3b/',
    'https://www.instagram.com/p/CJ4beczAOOM/',
    'https://www.instagram.com/p/CJxoBLXg1n1/',
    'https://www.instagram.com/p/CJuz4lgAcWu/',
]


class igbot():
    def __init__(self):
        # adjust webdriver path according your path
        print('Inisiate bot, and go to instagram login page')
        self.driver = webdriver.Chrome('chromedriver_win32/chromedriver')
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.driver.get('https://www.instagram.com/accounts/login/')
        self.wait = WebDriverWait(self.driver, 15)
        print('Ready')

    def login(self):
        print('Try to login')
        self.email_field = self.wait.until(EC.visibility_of_element_located((By.NAME, 'username')))
        self.password_field = self.driver.find_element_by_name('password')
        self.email_field.send_keys(email)
        self.password_field.send_keys(password)
        self.password_field.send_keys(Keys.ENTER)
        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'Fifk5')))
        print('Login succeed')

    def get_comments(self, url, num_comment=None):
        self.users = []
        self.texts = []
        self.likes = []
        self.url = url
        self.num_comment = num_comment

        print('Get post')
        self.driver.get(url)
        self.loop = True
        self.no = 1
        self.a = 0
        while self.loop:
            try:
                self.more_btn = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'dCJp8')))
                self.more_btn.click()
                print('Click load more:', self.no)
                self.no += 1

                self.b = len(self.driver.find_elements_by_class_name('Mr508'))
                try:
                    if self.b > self.num_comment:  # only take num_comment (eg. only take 50 comments)
                        print('Number of comment > {}'.format(self.num_comment))
                        self.loop = False
                except TypeError:
                    pass
                if self.a == self.b:
                    print('No more comment')
                    self.loop = False
                else:
                    self.a = self.b
            except TimeoutException:
                print('No load more comment button')
                self.loop = False
            except StaleElementReferenceException:
                print('Some element is missing, anyway keep going')
                continue

        print('Load comments')
        self.comments = self.driver.find_elements_by_class_name('Mr508')
        for i in self.comments[:self.num_comment]:
            self.user = i.text.split('\n')[0]
            self.text = i.text.split('\n')[1]
            self.like = i.text.split('\n')[2]
            try:
                self.like = re.findall(r'\d+', self.like)[1]
            except Exception:
                self.like = '0'
            self.like = int(self.like)

            self.users.append(self.user)
            self.texts.append(self.text)
            self.likes.append(self.like)
        print('Get {} comments'.format(len(self.comments[:self.num_comment])))


bot = igbot()
bot.login()
for i, url in enumerate(urls):
    print()
    print('#' * 50)
    print('url', i + 1)
    bot.get_comments(url, num_comment=50)  # only take 50 comments per url
                                           # num_comment is optional, if not specified then
                                           # bot will take all comments per url

    df = pd.DataFrame()
    df['user'] = bot.users
    df['comment'] = bot.texts
    df['like'] = bot.likes
    print('export csv')
    df.to_csv('scrape_comment/{}.csv'.format(url[28:-1]), index=False)
