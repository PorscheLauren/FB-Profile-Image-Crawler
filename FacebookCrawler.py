import urllib2
import urllib
from bs4 import BeautifulSoup
import FacebookLogin

image_folder_path = "../profileimages/"
facebook_website_folder_path = "../facebookwebsite/todo/"

def CrawlFBProfileImage(facebook_page_link):
    page = urllib2.urlopen(facebook_page_link)
    soup = BeautifulSoup(page, "lxml")
    id_spans = soup.findAll('a', {"class": True})

    for id_span in id_spans:
        for className in id_span['class']:
            if "UFICommentActorName" in className:
                personnel_url = id_span['href']

                try:
                    personnel_page = urllib2.urlopen(personnel_url).read()
                    # homefbhtml = urllib2.urlopen(personnel_url).read()
                    # htmlfile = open(str(count) + ".html", "w")
                    # htmlfile.write(homefbhtml)
                    # htmlfile.close()
                    # count += 1

                    personnel_soup = BeautifulSoup(personnel_page, "lxml")
                    personnel_imgs = personnel_soup.findAll('img')
                    print personnel_imgs
                    for personnel_img in personnel_imgs:

                        if 'captcha_challenge_code' in personnel_img['src']:
                            # FB found us
                            f = open("captcha.jpeg", 'wb')  # save in the profileimags folder
                            f.write(urllib.urlopen(personnel_img['src']).read())
                            f.close()
                            print "Facebook Got US!"
                            return

                        for sub_className in personnel_img['class']:
                            if "profilePic" in sub_className or "4jhq" in sub_className:
                                split_slash = [x.strip() for x in personnel_url.split('/')]
                                split_eqsign = [x.strip() for x in split_slash[3].split('=')]
                                if 'profile.php' in split_eqsign[0]:
                                    user_id_str = split_eqsign[1][:-5]
                                else:
                                    user_id_str = split_eqsign[0][:-5]

                                print 'Crawling profile image of ' + user_id_str
                                f = open(image_folder_path + user_id_str, 'wb')  # save in the profileimags folder
                                f.write(urllib.urlopen(personnel_img['src']).read())
                                f.close()

                except urllib2.HTTPError:
                    print "404 not found"
                    continue



def CrawlFBProfileImage2(facebook_page_link):
    page = urllib2.urlopen(facebook_page_link)
    soup = BeautifulSoup(page, "lxml")
    id_spans = soup.findAll('a', {"class": True})

    for id_span in id_spans:
        for className in id_span['class']:
            if "UFICommentActorName" in className:
                personnel_url = id_span['href']

                try:
                    personnel_page = urllib2.urlopen(personnel_url).read()
                    if "captcha.jpeg" in personnel_page:
                        #Facebook got us
                        print "Facebook got us!"
                        return

                    start = personnel_page.find('img class="profilePic img')

                    if start < 0: # not found
                        start = personnel_page.find('img class="4jhq')

                    if start > 0:
                        substring_all = personnel_page[start:start + 300]
                        substrings = substring_all.split('"')
                        personnel_img_src = ''
                        for substring in substrings:
                            if "https" in substring and "amp;" in substring:
                                personnel_img_src = substring.replace('amp;', '')
                        split_slash = [x.strip() for x in personnel_url.split('/')]
                        split_eqsign = [x.strip() for x in split_slash[3].split('=')]
                        if 'profile.php' in split_eqsign[0]:
                            user_id_str = split_eqsign[1][:-5]
                        else:
                            user_id_str = split_eqsign[0][:-5]

                        print 'Crawling profile image ' + personnel_img_src + " for " + user_id_str
                        try:
                            f = open(image_folder_path + user_id_str, 'wb')  # save in the profileimags folder
                            f.write(urllib.urlopen(personnel_img_src).read())
                            f.close()
                        except IOError:
                            print 'Parse error, skip'
                            continue



                except urllib2.HTTPError:
                    print "404 not found"
                    continue

FacebookLogin.login('418557764@qq.com','19891004xyh3984', 'fbcookie')
CrawlFBProfileImage2('file:///home/xyh3984/Profile%20image%20project/Facebook%20Crawling/facebookwebsite/todo/test.html')


## test part
# url = 'https://www.facebook.com/cyndi.uchendu?fref=ufi&rc=p'
#
# print url
# page = urllib2.urlopen(url)
#
# req = urllib2.Request(url, None, {'User-agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'})
# page = urllib2.urlopen(req)
#
# print page
# soup = BeautifulSoup(page, "lxml")
#
# imgs = soup.findAll('img', {"alt": True})
#
# for img in imgs:
#     print img['src'] + "  " + img['alt']