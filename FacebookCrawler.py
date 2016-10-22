import urllib2
import urllib
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
import FacebookLogin
import unicodedata

image_folder_path = "../profileimages/"
facebook_website_folder_path = "../facebookwebsite/todo/"

# browser should already log in to Facebook, call FacebookLogin.login_withSelenium firsts
def GetPersonnelProfileImg(personnel_url, browser = None):
    personnel_profile_img_link = []
    try:
        personnel_page = urllib2.urlopen(personnel_url).read()
        if "captcha.jpeg" in personnel_page:
            # Facebook got us
            print "Facebook got us!"
            return

        if browser is not None:  # use Chrome driver to get higher resolution profile image
            start = personnel_page.find('a class="profilePicThumb"')
            if start > 0:
                substring_all = personnel_page[start:start + 200].split('"')
                personnel_home_url = ''
                for substring in substring_all:
                    if "www.facebook.com/photo" in substring:
                        personnel_home_url = substring
                        break

                if personnel_home_url != '':
                    browser.get(personnel_home_url)
                    page_src = browser.page_source
                    start = page_src.find('img class="spotlight"')
                    substring_all = page_src[start: start + 300].split('"')

                    for substring in substring_all:
                        if "https" in substring or "http" in substring:
                            print substring
                            personnel_profile_img_link.append(
                                unicodedata.normalize('NFKD', substring.replace('amp;', ''))
                                .encode('ascii', 'ignore'))
                            break


        else:  # no browser engin, get low resolution profile image
            start = personnel_page.find('img class="profilePic img')
            print start
            if start < 0:  # not found
                start = personnel_page.find('img class="4jhq')

            if start > 0:
                substring_all = personnel_page[start:start + 300]
                substrings = substring_all.split('"')
                for substring in substrings:
                    if "https" in substring and "amp;" in substring:
                        personnel_profile_img_link.append(substring.replace('amp;', ''))
                        break

        if len(personnel_profile_img_link) != 0:
            print "user id:" + user_id_str + " img link: " + personnel_profile_img_link[
                len(personnel_profile_img_link) - 1]

    except urllib2.HTTPError:
        print "404 not found, skip"
    except UnicodeEncodeError:
        print "adcii code error, skip"
    except TimeoutException:
        print "Loading took too much time!"
    except BaseException:
        print 'all other errors, skip'


# return a list of all commentors
# for offline facebook_page_link only so far
def GetCommentors(facebook_page_link): # return a list of all commentors
    page = urllib2.urlopen(facebook_page_link)
    soup = BeautifulSoup(page, "lxml")
    id_spans = soup.findAll('a', {"class": True})
    Personnel_Urls = []

    for id_span in id_spans:
        for className in id_span['class']:
            if "UFICommentActorName" in className:
                Personnel_Urls.append(id_span['href'])
    return Personnel_Urls

def GetPersonnelID(personnel_url):
    split_slash = [x.strip() for x in personnel_url.split('/')]
    split_eqsign = [x.strip() for x in split_slash[3].split('=')]
    if 'profile.php' in split_eqsign[0]:
        user_id_str = split_eqsign[1][:-5]
    else:
        user_id_str = split_eqsign[0][:-5]
    return user_id_str



FacebookLogin.login('418557764@qq.com','19891004xyh3984', 'fbcookie')
# CrawlFBProfileImage2('file:///home/xyh3984/Profile%20image%20project/Facebook%20Crawling/facebookwebsite/todo/test1.html')
# CrawlFBProfileImage2('file:///home/xyh3984/Profile%20image%20project/Facebook%20Crawling/facebookwebsite/todo/test2.html')

print GetCommentors('file:///C:/Users/xyh3984/Desktop/FB-Profile-Image-Crawler/test.html')

