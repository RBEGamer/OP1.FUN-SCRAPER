import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import csv
import time
import re
from selenium import webdriver
import selenium.webdriver.chrome.service as service

os.environ['XDG_DOWNLOAD_DIR'] = str(
    os.path.dirname(os.path.abspath(__file__))) + "/OP1_FUN_DOWNLOADS"

# Configurations
USER_LOGIN = "YOUR_EMAIL"
USER_PASSWORD = "YOUR_PASSWORD"

# Access Denial Prevention Wait Time
EACH_PACK_DOWNLOAD_INTERVAL = 50
PREVENT_ACCESS_DENIAL_WAIT = 500

# Update CSV Database
UPDATE_CSV = True

service = service.Service('./chromedriver')
service.start()
capabilities = {
    'chrome.binary': '/path/to/custom/chrome',
    'prefs': {
        'download': {
            'default_directory': str(os.path.dirname(os.path.abspath(__file__))) + "/OP1_FUN_DOWNLOADS",
            'directory_upgrade':
                True,
            'extensions_to_open':
                ''
        }
    }
}
# ADD USER AGENT
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--user-agent="Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166"')

driver = webdriver.Remote(service.service_url, capabilities, chrome_options=chrome_options)
driver.get('https://op1.fun/users/sign_in')

# FILL IN LOGIN DETAILS
email_field = driver.find_element_by_id("user_email")
email_field.clear()
email_field.send_keys(USER_LOGIN)
pw_field = driver.find_element_by_id("user_password")
pw_field.clear()
pw_field.send_keys(USER_PASSWORD)
pw_field.send_keys(Keys.RETURN)

# go to the packs page
driver.get('https://op1.fun/packs')

# get html code
source = driver.page_source
source = str(source.encode('utf-8'))
# print source

# search for last button get get the pages
matches = re.finditer(r"\?page\=(\d)*\">Last", source, re.MULTILINE)

highest_page_id = -1
for matchNum, match in enumerate(matches, start=1):
    print("Match {matchNum} was found at {start}-{end}: {match}".format(
        matchNum=matchNum,
        start=match.start(),
        end=match.end(),
        match=match.group()))

    print(match.group())
    match_page = re.finditer(r"(\d)+", str(match.group()))
    for matchNum_page, match_page_entry in enumerate(match_page, start=1):
        print(match_page_entry.group())
        if int(match_page_entry.group()) > highest_page_id:
            highest_page_id = int(match_page_entry.group())

if highest_page_id == -1:
    print("no last page id found")
    driver.quit()
    exit(0)

print("found " + str(highest_page_id) + "pages")

links = []
rid = []


# ================Read Existing CSV=============================
def getPreExistedPackNames():
    packs = []
    try:
        with open('pack_List.csv') as f:
            myCsv = csv.reader(f)
            for row in myCsv:
                packs.append(row[0])
        return packs
    except IOError:
        return []


def readCSVLst():
    try:
        with open('pack_List.csv', 'r') as readFile:
            reader = csv.reader(readFile)
            temp = list(reader)
        readFile.close()
        return temp
    except IOError:
        return []


def updateDownloadStatus(line, status):
    CSV = readCSVLst()
    CSV[line] = [name, status, url]
    with open('pack_List.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(CSV)
    writeFile.close()


if UPDATE_CSV:
    scannedPacks = getPreExistedPackNames()
    with open('pack_List.csv', mode='a') as csv_file:
        fieldnames = ['pack_name', 'download_status', 'URL']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        # writer.writeheader()
        for page_id in range(0, highest_page_id + 1):
            print("Scraping Page: " + str(page_id) + "/" + str(highest_page_id))
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
                match_user = re.finditer(r'\/users\/(.)+\"', str(match_pack.group()))
                for matchNum_user, match_user_entry in enumerate(match_user, start=1):
                    st = str(match_user_entry.group())[:-1]
                    if st not in scannedPacks:
                        print("Add: " + st)
                        links.append(st)
                        writer.writerow({'pack_name': st, 'download_status': "N", 'URL': 'https://op1.fun' + st})
                    else:
                        print("Existed: " + st)
            print("========================================")

downloadLst = readCSVLst()
counter = 0
for i in range(0, len(downloadLst)):
    name, stat, url = downloadLst[i]
    if stat != "DL":
        driver.get(url)
        try:
            elem = driver.find_element_by_class_name('download').click()
            counter = counter + 1
            print("DL- " + name)
            updateDownloadStatus(i, "DL")
            time.sleep(EACH_PACK_DOWNLOAD_INTERVAL)

        except Exception as identifier:
            print("ERROR- " + name)
            updateDownloadStatus(i, "ERROR")

        # isAccessDenied = "<Code>AccessDenied</Code>" in driver.get(driver.current_url)
        if driver.current_url in "https://op1fun.s3.amazonaws.com/":
            print("|-------> Access Denied" + name)
            updateDownloadStatus(i, "Access Denied")

        if counter >= 12:
            counter = 0
            time.sleep(PREVENT_ACCESS_DENIAL_WAIT)
    else:
        print("Downloaded skipping: " + name)

driver.quit()
