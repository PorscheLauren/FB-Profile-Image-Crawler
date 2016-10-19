import urllib2
import urllib
from bs4 import BeautifulSoup

image_folder_path = "../profileimages/"
twitter_website_folder_path = "../facebookwebsite/todo/"

def CrawlFBProfileImage(facebook_page_link):
    page = urllib2.urlopen(facebook_page_link)
    soup = BeautifulSoup(page, "lxml")
    id_spans = soup.findAll('a', {"class": True})
    for id_span in id_spans:
        for className in id_span['class']:
            if "UFICommentActorName" in className:
                personnel_url = id_span['href']

                try:
                    personnel_page = urllib2.urlopen(personnel_url)
                    personnel_soup = BeautifulSoup(personnel_page, "lxml")
                    personnel_imgs = personnel_soup.findAll('img', {"class": True})
                    for personnel_img in personnel_imgs:
                        for sub_className in personnel_img['class']:
                           if "profilePic" in sub_className:
                                split_slash = [x.strip() for x in personnel_url.split('/')]
                                split_eqsign = [x.strip() for x in split_slash[3].split('=')]
                                user_id_str = ''
                                if 'profile.php' in split_eqsign[0]:
                                   user_id_str = split_eqsign[1][:-5]
                                else:
                                   user_id_str = split_eqsign[0][:-5]

                                print 'Crawling image ' + personnel_img['src']
                                f = open(image_folder_path + user_id_str, 'wb')  # save in the profileimags folder
                                f.write(urllib.urlopen(personnel_img['src']).read())
                                f.close()

                except urllib2.HTTPError:
                    continue

        # if id_span['class'] == "UFICommentActorName":
        #     print id_span['href']

        # for img_tag in id_span.findChildren("img", {"src": True}):
        #     if 'profile_image' in img_tag['src'] and 'default_' not in img_tag:
        #         img_link_str = img_tag['src']
        #         img_link_str = re.sub('_bigger', '', img_link_str)  # remove the "_bigger" substring, to achieve the bigger image
        #
        #         print "crawling the image " + img_link_str
        #
        #         user_id_str = id_span['href'].strip('/')
        #         f = open(image_folder_path + user_id_str, 'wb')  # save in the profileimags folder
        #         f.write(urllib.urlopen(img_link_str).read())
        #         f.close()


# for root, dirs, htmlfiles in os.walk(twitter_website_folder_path):
#     for htmlfile in htmlfiles:
#         abs_path_str = os.path.realpath(os.path.join(root, htmlfile))
#         abs_path_url_str = "file://" + abs_path_str
#         abs_path_url_str = re.sub(' ', '%20', abs_path_url_str) # replace all the spaces with %20
#         CrawlTwitProfileImage(abs_path_url_str)

CrawlFBProfileImage('file:///home/xyh3984/Profile%20image%20project/Facebook%20Crawling/facebookwebsite/test.html')


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