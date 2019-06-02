import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import random

import time
import re
from selenium import webdriver
import selenium.webdriver.chrome.service as service


os.environ['XDG_DOWNLOAD_DIR'] = str(
    os.path.dirname(os.path.abspath(__file__))) + "/OP1_FUN_DOWNLOADS"


service = service.Service('./chromedriver')
service.start()
capabilities = {
    'chrome.binary': '/path/to/custom/chrome',
    'prefs': {
        'download': {
            'default_directory':str(os.path.dirname(os.path.abspath(__file__))) +"/OP1_FUN_DOWNLOADS",
            'directory_upgrade':
            True,
            'extensions_to_open':
            ''
        }
    }
}
driver = webdriver.Remote(service.service_url, capabilities)
driver.get('https://op1.fun/users/sign_in')



#FILL IN LOGIN DETAILS
email_field = driver.find_element_by_id("user_email")
email_field.clear()
email_field.send_keys("YOUR_EMAIL")

pw_field = driver.find_element_by_id("user_password")
pw_field.clear()
pw_field.send_keys("YOUR_PASSWORD")
pw_field.send_keys(Keys.RETURN)

#go to the packs page
driver.get('https://op1.fun/packs')

#get html code
source =  driver.page_source
source = str(source.encode('utf-8'))
#print source

#search for last button get get the pages
matches = re.finditer(r"\?page\=(\d)*\">Last", source, re.MULTILINE)

highest_page_id = -1
for matchNum, match in enumerate(matches, start=1):
    print("Match {matchNum} was found at {start}-{end}: {match}".format(
        matchNum=matchNum,
        start=match.start(),
        end=match.end(),
        match=match.group()))

    print match.group()
    match_page = re.finditer(r"(\d)+", str(match.group()))
    for matchNum_page, match_page_entry in enumerate(match_page, start=1):
        print match_page_entry.group()
        if(int(match_page_entry.group()) > highest_page_id):
            highest_page_id = int(match_page_entry.group())


if(highest_page_id == -1):
    print("no last page id found")
    driver.quit()
    exit(0)

print("found " + str(highest_page_id) + "pages")


links = []
rid = []
for page_id in range(75, highest_page_id):
    if page_id in rid:
        print("skip pid")
        continue
    rid.append(page_id)

    driver.get('https://op1.fun/packs?page=' + str(page_id))
    source_page = str(driver.page_source.encode('utf-8'))

    pack_matches = re.finditer(
        r"<a class=\"pack-name parent-link\" href=\"(.)*\">(.)*<\/a>",
        source_page, re.MULTILINE)

    for matchNum_pack, match_pack in enumerate(pack_matches, start=1):
        #print match_pack.group()

        match_user = re.finditer(r'\/users\/(.)+"', str(match_pack.group()))
        for matchNum_user, match_user_entry in enumerate(match_user, start=1):
            st = str(match_user_entry.group())[:-1]
            links.append(st)
            print(st)

counter = 0

for link in links:

    driver.get('https://op1.fun' + link)
    try:
        elem = driver.find_element_by_class_name('download').click()
        time.sleep(30)
        counter = counter + 1
        print("DL- "+link)
    except Exception as identifier:
        print("ERROR- "+link)
    #to avoid the spam protection
    if(counter == 12):
        counter = 0
        time.sleep(500)

time.sleep(50)
driver.quit()
