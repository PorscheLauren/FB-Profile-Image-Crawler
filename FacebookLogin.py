import urllib
import urllib2
import cookielib

import time
from selenium import webdriver


def login(username, pwd, cookie_file):
    # POST data per LOGIN
    login_data = {
            'sd': 'AVrkAll-',
            'display':'',
            'enable_profile_selector':'',
            'isprivate':'',
            'email': username,
            'pass': pwd,
            'login':1,
            'persistent': '',
            'default_persistent': 1,
            'timezone': 240,
            'lgndim': 'eyJ3IjoxOTIwLCJoIjoxMDgwLCJhdyI6MTg1NSwiYWgiOjEwNTYsImMiOjI0fQ==',
            'lgnrnd': '150721_mB59',
            'lgnjs': 1476914842,
            'ab_test_data': 'AAAAAAA//AAAA/AAAAAAA/AAAAAAAAAAAAAAAAAA/ZMGAAAAAACGAC',
            'locale': 'en_US',
            'next': 'https://www.facebook.com/'
        }

    cookie_jar2 = cookielib.LWPCookieJar()
    cookie_support2 = urllib2.HTTPCookieProcessor(cookie_jar2)
    opener2 = urllib2.build_opener(cookie_support2, urllib2.HTTPHandler)
    urllib2.install_opener(opener2)
    login_url = 'https://www.facebook.com/login.php?login_attempt=1&lwv=100'


    # Fill POST data
    login_data = urllib.urlencode(login_data)
    http_headers ={
                    # 'authority': 'www.facebook.com',
                    # 'method': 'POST',
                    # 'path': '/ login.php?login_attempt = 1 & lwv = 110',
                    # 'scheme': 'https',
                    # 'accept': 'text / html, application / xhtml + xml, application / xml; q = 0.9, image / webp, * / *;q = 0.8',
                    # 'accept-encoding': 'gzip, deflate, br',
                    # 'accept-language': 'en - US, en;q = 0.8',
                    # 'cache - control': 'max - age = 0',
                    # 'content-length': 352,
                    # 'content-type': 'application / x - www - form - urlencoded',
                    'cookie': 'locale=en_US; sb=GtUGWGiIXhcq87pBCbAr4XkJ; lu=gAMjt_GNuTQq5u8SNiFUb5CQ; reg_fb_gate=https%3A%2F%2Fwww.facebook.com%2F%3Fstype%3Dlo%26jlou%3DAfcN-xj66dy32J-e1yhRx9Fbz7OOsqTszJFJzYDTE5nqT8yPj1STntHTQufUrdewtr_BUuAX_ucH5q-YEmuft7I1VBW_BBpFn6QviqsZk37obA%26smuh%3D64704%26lh%3DAc-OFOiQLty2_Epr; fr=0vIY9Y26BUQhhB8Nx.AWWsRWQY1VkDsz6y3mEmJzFy-Mc.BYBtUN.ii.AAA.0.0.BYB_l3.AWUzdI_4; datr=DdUGWLZcYmKdZvazY4hyc5q8; reg_fb_ref=https%3A%2F%2Fwww.facebook.com%2Flogin.php%3Flogin_attempt%2B%3D%2B1%2B%26%2Blwv%2B%3D%2B110; wd=495x644',
                    # 'origin': 'https: // www.facebook.com',
                    # 'referer': 'https: // www.facebook.com /',
                    # 'upgrade-insecure-requests': 1,
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
                    }
    print 'begin login'
    req_login = urllib2.Request(
        url=login_url,
        data=login_data,
        headers=http_headers
    )
    print 'end login'
    cookie_jar2.save(cookie_file, ignore_discard=True, ignore_expires=True)
    urllib2.urlopen(req_login)


def login_withSelenium(username, password):
    browser = webdriver.Chrome('chromedriver')
    browser.get('https://www.facebook.com')

    input_username = browser.find_element_by_id('email')
    input_username.send_keys(username)

    input_password = browser.find_element_by_id('pass')
    input_password.send_keys(password)

    login_btn = browser.find_element_by_id('u_0_n')
    login_btn.click()

    return browser

