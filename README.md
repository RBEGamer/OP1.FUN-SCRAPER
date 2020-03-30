# OP1.FUN SCRAPER
Scrapes all Packages from the Op1.fun Site.
At the time is wrote this script, there was no API so i used the google chrome headless mode to download the files.

The script scans each page on the packages page for the package links.
In the next step the collected links will be downloaded.

The google chrome headless modes makes it very easy with the login into the system and downloading files.



# SETUP
* install python
* install [google chrome](https://www.chromium.org/getting-involved/download-chromium)
* install the google chrome [ChromeDriver](http://chromedriver.chromium.org/getting-started)
* install [selenium](https://github.com/SeleniumHQ/selenium) `pip install selenium`

## SET USERNAME/PASSWORD
Create a account at the op1.fun site and change the settings in the script:

* `line 15` change YOUR_EMAIL with your email
* `line 16` change YOUR_PASSWORD with your password

## Keeping track
`UPDATE_CSV = True` enables CSV capability.  
It updates and keep tracks of all the packs available on the op1fun website. And keep track of every pack's download status. This prevents you from downloading redundant files.  
It also resumes to undownloaded files if the program ever stops.


# RUN
### Scrapper
The script and the ChromeDriver in the same directory
* run the chrome driver in a other Terminal `./chromedriver`
* run `python ./src/op1fun_package_scraper.py` to start downloading

### Unpacker
Unpacks all the downloaded zip files into more OP1 friendly folder system 
#### setup
Assign folder path that contains all the zip files and also your destination path
* `line 6` ZIP_FILES_PATH = "/Users/path/to/the/zip/folders/...."        
* `line 7` UNPACK_TO = "/Users/paths/to/unpack/folder/...."  
#### run
run `python unpacker.py` to start unpacking
prompt and enter `Y` to confirm and continue  


## NOTES

Op1.Fun hosts its files on AWS, the script waits after each download a bit to not trigger a the spam/ddos system from AWS.
After 12 downloads there is an other delay too. That helps to prevent access errors.
For a complete download of all packages (140 pages 03.06.2019) you will need two days with my delay settings.
May you can decrese the wait time in a public network.


# MODIFY

The following regex statements are used to find the links in the page:

* `\?page\=(\d)*\">Last"` to find the last page index (line 55)
* `<a class=\"pack-name parent-link\" href=\"(.)*\">(.)*<\/a` to get on each packs page, the link to the packs (line 93)

* `elem = driver.find_element_by_class_name('download').click()` find the download button on a pack site


## TESTED MacOSX, Safari 13.0, Op1.fun 03.06.2019
## TESTED Ubuntu18.04, Op1.fun 17.10.2019
