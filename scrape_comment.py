# download Chromedriver: https://chromedriver.chromium.org/downloads

import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


email = 'your email instagram'
password = 'your password'
url = 'https://www.instagram.com/p/CJ3McKBjuc0/'


class igbot():
    def __init__(self):
        # adjust webdriver path according your path
        self.driver = webdriver.Chrome('chromedriver_win32/chromedriver')
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.driver.get('https://www.instagram.com/accounts/login/')
        self.driver.find_element_by_name('username')
        print('ready')

    def login(self):
        self.email_field = self.driver.find_element_by_name('username')
        self.password_field = self.driver.find_element_by_name('password')
        self.email_field.send_keys(email)
        self.password_field.send_keys(password)
        self.password_field.send_keys(Keys.ENTER)
        self.driver.find_elements_by_class_name('Fifk5')
        print('login')

    def get_comments(self, url):
        self.users = []
        self.texts = []
        self.likes = []

        self.driver.get(url)
        print('get post')
        self.loop = True
        self.no = 1
        self.a = 0
        while self.loop:
            try:
                self.more_btn = self.driver.find_element_by_class_name('dCJp8')
                self.more_btn.click()
                print('click:', self.no)
                self.no += 1

                self.b = len(self.driver.find_elements_by_class_name('Mr508'))
                if self.a == self.b:
                    self.loop = False
                else:
                    self.a = self.b
            except Exception:
                self.loop = False
        self.comments = self.driver.find_elements_by_class_name('Mr508')
        for i in self.comments:
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
        print('comments:', len(self.comments))


bot = igbot()
bot.login()
bot.get_comments(url)

df = pd.DataFrame()
df['user'] = bot.users
df['comment'] = bot.texts
df['like'] = bot.likes
print('export csv')
df.to_csv('scrape_comment.csv', index=False)
