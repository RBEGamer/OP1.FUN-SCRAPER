# OP1FUN_SCRAPER
Scrapes all Packages from the Op1.fun Site.
At the time is wrote this script, there was no API so i used the google chrome headless mode to download the files.

The script scans each page on the packages page for the package links.
In the next step the collected links will be downloaded.

The google chrome headless modes makes it very easy with the login system and the downloading.



# SETUP
* install python
* install [google chrome](https://www.chromium.org/getting-involved/download-chromium)
* install the google chrome [ChromeDriver](http://chromedriver.chromium.org/getting-started)
* install [selenium](https://github.com/SeleniumHQ/selenium) `pip install selenium`

## SET USERNAME/PASSWORD
Create a account at the op1.fun site and change the settings in the script:

* `line 39` change YOUR_EMAIL with your email
* `line 42` change YOUR_PASSWORD with your password


# RUN

The script and the ChromeDriver in the same directory
* run the chrome driver in a other Terminal `./chromedriver`
* run `python ./src/op1fun_package_scraper.py` to start downloading


## NOTES

Op1.Fun hosts its files on AWS, the script waits after each download a bit to not trigger a the spam/ddos system from AWS.
After 12 downloads there is an other delay too. That helps to prevent access errors.
For a complete download of all packages (140 pages 03.06.2019) you will need two daysm with my delay settings.
May you can decrese the wait time in a public network.



## TESTED MacOSX, Op1.fun 03.06.2019
